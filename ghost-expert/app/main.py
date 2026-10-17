import json
import os
import re
import subprocess
import sys
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Request, WebSocket
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from app import assist, author, models
from app.live import run_session
from app.vlm import HEADERS, VLLM_URL

PROCEDURES = Path(os.environ.get("PROCEDURES_DIR", "procedures"))
WEB = Path(__file__).resolve().parent.parent / "web"
APP_TOKEN = os.environ.get("APP_TOKEN")  # if set, every write needs it: the app URL is public
MAX_UPLOAD = int(os.environ.get("MAX_UPLOAD_MB", "500")) * 1024 * 1024
MAX_QUESTION = 5 * 1024 * 1024  # a push-to-talk clip is a few hundred KB
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")

TTS = os.environ.get("TTS", "kokoro")  # kokoro: voice on the GPU | browser: the page's own speech
tts_state = {"ready": False, "langs": set(), "errors": {} if TTS == "kokoro" else {"all": "TTS=browser"}}


def warm_tts():
    """Load Kokoro before the first interrupt needs it, one language at a time.

    espeak-ng (Kokoro's phonemizer) exits the whole process on a broken install instead of raising,
    so each language is proven in a child process first. A failure only turns that language over to browser speech.
    """
    for lang, line in (("en", "Ready."), ("it", "Pronto.")):
        child = subprocess.run([sys.executable, "-c", f"from app.models import speak; speak({line!r}, {lang!r})"],
                               capture_output=True, text=True, timeout=900)
        if child.returncode:
            tts_state["errors"][lang] = (child.stderr.strip() or f"exit {child.returncode}")[-300:]
            print(f"Kokoro unavailable for {lang}, browser speech will be used: {tts_state['errors'][lang]}")
            continue
        models.speak(line, lang)
        tts_state["langs"].add(lang)
    tts_state["ready"] = True


@asynccontextmanager
async def lifespan(_):
    if TTS == "kokoro":
        threading.Thread(target=warm_tts, daemon=True).start()
    yield


PROCEDURES.mkdir(exist_ok=True)
app = FastAPI(title="Ghost Expert", lifespan=lifespan)
app.mount("/files", StaticFiles(directory=PROCEDURES), name="files")


def writer(x_app_token: str | None = Header(default=None)):
    if APP_TOKEN and x_app_token != APP_TOKEN:
        raise HTTPException(401, "missing or wrong X-App-Token")


def proc_dir(pid):
    if not ID_RE.match(pid):  # the id becomes a folder name: no slashes, no dots
        raise HTTPException(400, "procedure id: lowercase letters, digits and dashes, max 40")
    return PROCEDURES / pid


@app.get("/")
def author_page():
    return FileResponse(WEB / "author.html")


@app.get("/coach")
def coach_page():
    return FileResponse(WEB / "coach.html")


@app.websocket("/ws/coach/{pid}")
async def coach_ws(ws: WebSocket, pid: str, token: str | None = None):
    # Browsers can't set headers on a WebSocket, so the token comes as ?token=. Every session uses the GPU.
    d = PROCEDURES / pid
    if (APP_TOKEN and token != APP_TOKEN) or not ID_RE.match(pid) or not (d / "procedure.json").exists():
        await ws.close(code=4403 if APP_TOKEN and token != APP_TOKEN else 4404)
        return
    await ws.accept()
    await run_session(ws, d)


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{VLLM_URL}/v1/models", headers=HEADERS)
            r.raise_for_status()
    except httpx.HTTPError as e:
        return JSONResponse({"app": "ok", "vllm": f"down: {e}"}, status_code=503)
    return {"app": "ok", "vllm": "ok", "models": [m["id"] for m in r.json()["data"]]}


@app.get("/api/procedures")
def list_procedures():
    return sorted(p.name for p in PROCEDURES.iterdir() if p.is_dir() and ID_RE.match(p.name))


@app.put("/api/procedures/{pid}/video", dependencies=[Depends(writer)])
async def upload_video(pid: str, request: Request):
    d = proc_dir(pid)
    d.mkdir(exist_ok=True)
    part, size = d / "expert.mp4.part", 0
    with part.open("wb") as f:
        async for chunk in request.stream():
            size += len(chunk)
            if size > MAX_UPLOAD:
                f.close()
                part.unlink()
                raise HTTPException(413, f"video over {MAX_UPLOAD // 2**20} MB")
            f.write(chunk)
    part.replace(d / "expert.mp4")
    return {"bytes": size}


@app.post("/api/procedures/{pid}/draft", dependencies=[Depends(writer)])
async def make_draft(pid: str):
    d = proc_dir(pid)
    if not (d / "expert.mp4").exists():
        raise HTTPException(404, "upload the expert video first")
    try:
        return await run_in_threadpool(author.draft, d)
    except ValueError as e:
        raise HTTPException(422, str(e))


@app.get("/api/procedures/{pid}/draft")
def get_draft(pid: str):
    f = proc_dir(pid) / "draft.json"
    if not f.exists():
        raise HTTPException(404, "no draft yet")
    return json.loads(f.read_text())


@app.put("/api/procedures/{pid}/draft", dependencies=[Depends(writer)])
def save_draft(pid: str, body: dict):
    f = proc_dir(pid) / "draft.json"
    if not f.exists():
        raise HTTPException(404, "no draft yet")
    d = json.loads(f.read_text())
    steps = body.get("steps", d["steps"])
    if not isinstance(steps, list) or not all(isinstance(s, dict) for s in steps):
        raise HTTPException(422, "steps must be a list of objects")
    # Only the editable parts come from the browser; everything else stays as the pipeline wrote it.
    d.update(title=str(body.get("title", d["title"])), steps=steps,
             edits=int(body.get("edits", d["edits"])), approved=False)
    f.write_text(json.dumps(d, indent=2, ensure_ascii=False))
    return d


@app.post("/api/procedures/{pid}/approve", dependencies=[Depends(writer)])
async def approve(pid: str):
    try:
        return await run_in_threadpool(author.approve, proc_dir(pid))
    except ValueError as e:
        raise HTTPException(422, str(e))


def approved(pid):
    d = proc_dir(pid)
    if not (d / "procedure.json").exists():
        raise HTTPException(404, "no approved procedure")
    return d


def language(lang):
    if lang not in assist.LANGUAGES:
        raise HTTPException(422, f"language must be one of {sorted(assist.LANGUAGES)}")
    return lang


@app.post("/api/procedures/{pid}/translate", dependencies=[Depends(writer)])
async def translate(pid: str, lang: str):
    return await run_in_threadpool(assist.translate, approved(pid), language(lang))


@app.post("/api/coach/{pid}/ask", dependencies=[Depends(writer)])
async def ask(pid: str, request: Request, step: int = 0, lang: str = "en"):
    """Body: a push-to-talk recording (audio/*), or JSON {"text": "..."} for the typed fallback."""
    d, lang = approved(pid), language(lang)
    body = await request.body()
    if len(body) > MAX_QUESTION:
        raise HTTPException(413, "question too long")
    if request.headers.get("content-type", "").startswith("application/json"):
        question = str(json.loads(body or b"{}").get("text", "")).strip()[:500]
    else:
        question = await run_in_threadpool(assist.hear, body)
    if not question:
        raise HTTPException(422, "didn't catch a question")
    return {"question": question, **await run_in_threadpool(assist.answer, d, step, question, lang)}


@app.post("/api/tts", dependencies=[Depends(writer)])
async def tts(body: dict):
    """{"text", "lang"} -> WAV from Kokoro on the GPU. 503 tells the page to use its own speech instead."""
    text, lang = str(body.get("text", "")).strip()[:400], language(str(body.get("lang", "en")))
    if "all" in tts_state["errors"]:
        raise HTTPException(503, f"Kokoro off: {tts_state['errors']['all']}")
    if not tts_state["ready"] and lang not in tts_state["langs"]:
        raise HTTPException(503, "Kokoro warming up")
    if lang not in tts_state["langs"]:
        raise HTTPException(503, f"Kokoro off for {lang}: {tts_state['errors'].get(lang, 'unknown')}")
    if not text:
        raise HTTPException(422, "no text")
    t0 = time.perf_counter()
    try:
        wav = await run_in_threadpool(models.speak, text, lang)
    except Exception as e:
        raise HTTPException(503, f"Kokoro failed: {type(e).__name__}: {e}")
    return Response(wav, media_type="audio/wav", headers={"X-TTS-Ms": f"{(time.perf_counter() - t0) * 1000:.0f}"})

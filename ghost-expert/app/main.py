import json
import os
import re
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Request, WebSocket
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app import author
from app.live import run_session
from app.vlm import HEADERS, VLLM_URL

PROCEDURES = Path(os.environ.get("PROCEDURES_DIR", "procedures"))
WEB = Path(__file__).resolve().parent.parent / "web"
APP_TOKEN = os.environ.get("APP_TOKEN")  # if set, every write needs it: the app URL is public
MAX_UPLOAD = int(os.environ.get("MAX_UPLOAD_MB", "500")) * 1024 * 1024
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,39}$")

PROCEDURES.mkdir(exist_ok=True)
app = FastAPI(title="Ghost Expert")
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

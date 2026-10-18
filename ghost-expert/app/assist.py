"""Coaching extras on top of an approved procedure: "show me how" answers and translations for bilingual coaching."""
import json
import time
from pathlib import Path

from app.models import transcribe
from app.prompts import (ANSWER_SCHEMA, ANSWER_SYSTEM, TRANSLATE_SCHEMA, TRANSLATE_SYSTEM, procedure_full_text)
from app.video import audio
from app.vlm import chat_json

# ponytail: languages the coach page has spoken phrases for; Gemma itself could do many more.
LANGUAGES = {"en": "English", "it": "Italian"}


def load(proc_dir):
    return json.loads((Path(proc_dir) / "procedure.json").read_text())


def hear(recording):
    """Push-to-talk audio (webm/ogg/wav, any format ffmpeg reads) -> text. Whisper detects the language."""
    samples = audio(recording)
    return " ".join(s["text"] for s in transcribe(samples)).strip() if len(samples) else ""


def answer(proc_dir, step_id, question, lang="en"):
    """-> {"answer", "show_step", "secs"}. show_step is checked against the procedure, never trusted blindly."""
    procedure = load(proc_dir)
    draft = Path(proc_dir) / "draft.json"
    narration = " ".join(s["text"] for s in json.loads(draft.read_text()).get("transcript", [])) if draft.exists() else ""
    step = next((s for s in procedure["steps"] if s["id"] == step_id), None)
    where = f"The trainee is on step {step['id']}: {step['title']}." if step else "The trainee has finished."
    messages = [
        {"role": "system", "content": ANSWER_SYSTEM.format(procedure=procedure_full_text(procedure),
                                                          narration=narration[:4000] or "(no narration)",
                                                          language=LANGUAGES[lang])},
        {"role": "user", "content": f"{where}\nQuestion: {question}"},
    ]
    t0 = time.perf_counter()
    out, _ = chat_json(messages, ANSWER_SCHEMA, max_tokens=200)
    ids = {s["id"] for s in procedure["steps"]}
    return {"answer": out["answer"].strip(), "show_step": out["show_step"] if out["show_step"] in ids else 0,
            "secs": round(time.perf_counter() - t0, 2)}


def translate(proc_dir, lang):
    """Step texts in `lang`, cached next to procedure.json until the procedure is approved again."""
    proc_dir = Path(proc_dir)
    src, cache = proc_dir / "procedure.json", proc_dir / f"procedure.{lang}.json"
    if lang == "en":
        return {s["id"]: {k: s[k] for k in ("title", "instruction", "visual_check")} for s in load(proc_dir)["steps"]}
    if cache.exists() and cache.stat().st_mtime >= src.stat().st_mtime:
        return {int(k): v for k, v in json.loads(cache.read_text()).items()}
    procedure = load(proc_dir)
    source = [{k: s.get(k, "") for k in ("id", "title", "instruction", "visual_check")} for s in procedure["steps"]]
    messages = [{"role": "system", "content": TRANSLATE_SYSTEM.format(language=LANGUAGES[lang])},
                {"role": "user", "content": json.dumps(source, ensure_ascii=False)}]
    out, _ = chat_json(messages, TRANSLATE_SCHEMA, max_tokens=3000)
    by_id = {s["id"]: s for s in out["steps"]}
    # Any step Gemma dropped keeps its English text rather than disappearing from the coach.
    result = {s["id"]: {k: (by_id.get(s["id"]) or s)[k] for k in ("title", "instruction", "visual_check")} for s in source}
    cache.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result

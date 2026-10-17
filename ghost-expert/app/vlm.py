"""Gemma 3 on our AMD vLLM server: image encoding, strict-JSON chat, and the step verify call."""
import base64
import io
import json
import os
import time

import httpx
from PIL import Image

from app.prompts import VERIFY_SCHEMA, verify_messages

VLLM_URL = os.environ.get("VLLM_URL", "http://localhost:8000")
MODEL = os.environ.get("MODEL", "google/gemma-3-12b-it")
VLLM_API_KEY = os.environ.get("VLLM_API_KEY")
HEADERS = {"Authorization": f"Bearer {VLLM_API_KEY}"} if VLLM_API_KEY else {}
VERIFY_TIMEOUT_S = float(os.environ.get("VERIFY_TIMEOUT_S", 5))  # a later answer is useless to the live coach


def data_url(image, max_side=512):
    """JPEG bytes or a file path -> downscaled JPEG data URL."""
    img = Image.open(io.BytesIO(image) if isinstance(image, bytes) else image).convert("RGB")
    img.thumbnail((max_side, max_side))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def chat_json(messages, schema, max_tokens=150, timeout=60):
    """One chat call constrained to a JSON schema. Returns (parsed JSON, seconds)."""
    body = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_schema", "json_schema": {"name": "out", "schema": schema}},
    }
    t0 = time.perf_counter()
    r = httpx.post(f"{VLLM_URL}/v1/chat/completions", json=body, headers=HEADERS, timeout=timeout)
    r.raise_for_status()
    return json.loads(r.json()["choices"][0]["message"]["content"]), time.perf_counter() - t0


def verify(procedure, step_id, frames, keyframe=None):
    """Is the trainee doing / done with this step? frames: JPEG bytes, oldest first. Returns (verdict, seconds)."""
    step = next(s for s in procedure["steps"] if s["id"] == step_id)
    messages = verify_messages(procedure, step, [data_url(f) for f in frames], keyframe and data_url(keyframe))
    verdict, secs = chat_json(messages, VERIFY_SCHEMA, timeout=VERIFY_TIMEOUT_S)
    verdict["confidence"] = min(1.0, max(0.0, float(verdict["confidence"])))
    return verdict, secs

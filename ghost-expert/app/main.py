import os

import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

VLLM_URL = os.environ.get("VLLM_URL", "http://localhost:8000")
VLLM_API_KEY = os.environ.get("VLLM_API_KEY")

app = FastAPI(title="Ghost Expert")


@app.get("/health")
async def health():
    headers = {"Authorization": f"Bearer {VLLM_API_KEY}"} if VLLM_API_KEY else {}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{VLLM_URL}/v1/models", headers=headers)
            r.raise_for_status()
    except httpx.HTTPError as e:
        return JSONResponse({"app": "ok", "vllm": f"down: {e}"}, status_code=503)
    return {"app": "ok", "vllm": "ok", "models": [m["id"] for m in r.json()["data"]]}

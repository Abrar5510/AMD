import httpx
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.vlm import HEADERS, VLLM_URL

app = FastAPI(title="Ghost Expert")


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(f"{VLLM_URL}/v1/models", headers=HEADERS)
            r.raise_for_status()
    except httpx.HTTPError as e:
        return JSONResponse({"app": "ok", "vllm": f"down: {e}"}, status_code=503)
    return {"app": "ok", "vllm": "ok", "models": [m["id"] for m in r.json()["data"]]}

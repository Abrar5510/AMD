"""Models that run inside the app on the AMD GPU (Gemma runs in the vLLM container): SigLIP and Whisper."""
import io
import os
from functools import lru_cache

import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, SiglipVisionModel, pipeline

SIGLIP_MODEL = os.environ.get("SIGLIP_MODEL", "google/siglip-so400m-patch14-384")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "openai/whisper-large-v3-turbo")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # ROCm builds of PyTorch use the "cuda" name
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


@lru_cache(maxsize=1)
def _siglip():
    model = SiglipVisionModel.from_pretrained(SIGLIP_MODEL, dtype=DTYPE).to(DEVICE).eval()
    return model, AutoImageProcessor.from_pretrained(SIGLIP_MODEL)


@torch.inference_mode()
def embed(jpegs, batch=32):
    """JPEG bytes -> L2-normalized SigLIP image embeddings, shape [n, d]."""
    model, proc = _siglip()
    out = []
    for i in range(0, len(jpegs), batch):
        images = [Image.open(io.BytesIO(j)).convert("RGB") for j in jpegs[i:i + batch]]
        pixels = proc(images=images, return_tensors="pt")["pixel_values"].to(DEVICE, DTYPE)
        feats = model(pixel_values=pixels).pooler_output.float()
        out.append(torch.nn.functional.normalize(feats, dim=-1).cpu().numpy().astype(np.float32))
    return np.concatenate(out)


@lru_cache(maxsize=1)
def _whisper():
    return pipeline("automatic-speech-recognition", model=WHISPER_MODEL, dtype=DTYPE, device=DEVICE)


def transcribe(samples, sr=16000, pause_s=0.6):
    """Mono float32 audio -> sentence segments [{"start", "end", "text"}] (Whisper detects the language).

    Built from word timestamps: Whisper's own segment timestamps can lump half a minute of speech together,
    which makes them useless for lining narration up with steps.
    """
    out = _whisper()({"raw": samples, "sampling_rate": sr}, return_timestamps="word", chunk_length_s=30, batch_size=8)
    segments = []
    for w in out["chunks"]:
        start, end = w["timestamp"][0], w["timestamp"][1] or w["timestamp"][0]
        prev = segments[-1] if segments else None
        if prev and not prev["text"].endswith((".", "?", "!")) and start - prev["end"] < pause_s:
            prev["text"] += w["text"]
            prev["end"] = end
        else:
            segments.append({"start": start, "end": end, "text": w["text"].strip()})
    return [s for s in segments if s["text"]]

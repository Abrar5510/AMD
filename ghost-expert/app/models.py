"""Models that run inside the app on the AMD GPU (Gemma runs in the vLLM container). Phase 2: SigLIP."""
import io
import os
from functools import lru_cache

import numpy as np
import torch
from PIL import Image
from transformers import AutoImageProcessor, SiglipVisionModel

SIGLIP_MODEL = os.environ.get("SIGLIP_MODEL", "google/siglip-so400m-patch14-384")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"  # ROCm builds of PyTorch use the "cuda" name
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32


@lru_cache(maxsize=1)
def _siglip():
    model = SiglipVisionModel.from_pretrained(SIGLIP_MODEL, torch_dtype=DTYPE).to(DEVICE).eval()
    return model, AutoImageProcessor.from_pretrained(SIGLIP_MODEL)


@torch.inference_mode()
def embed(jpegs):
    """JPEG bytes -> L2-normalized SigLIP image embeddings, shape [n, d]."""
    model, proc = _siglip()
    images = [Image.open(io.BytesIO(j)).convert("RGB") for j in jpegs]
    pixels = proc(images=images, return_tensors="pt")["pixel_values"].to(DEVICE, DTYPE)
    feats = model(pixel_values=pixels).pooler_output.float()
    return torch.nn.functional.normalize(feats, dim=-1).cpu().numpy().astype(np.float32)

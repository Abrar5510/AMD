# ROCm PyTorch base: SigLIP, Whisper and Kokoro run in this container on the AMD GPU.
# ponytail: "latest" until the first build works on the box; then pin that tag.
ARG BASE=rocm/pytorch:latest
FROM ${BASE}
WORKDIR /srv
# espeak-ng: Kokoro's phonemizer for non-English voices (Italian)
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg espeak-ng && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Kokoro's English G2P needs this spaCy model; bake it in rather than download on the first sentence.
RUN python -m spacy download en_core_web_sm
COPY app app
COPY scripts scripts
COPY web web
COPY tests tests
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

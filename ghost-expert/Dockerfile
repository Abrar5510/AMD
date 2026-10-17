# ROCm PyTorch base: SigLIP (and later Whisper/Kokoro) run in this container on the AMD GPU.
# ponytail: "latest" until the first build works on the box; then pin that tag.
ARG BASE=rocm/pytorch:latest
FROM ${BASE}
WORKDIR /srv
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY scripts scripts
COPY web web
COPY tests tests
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

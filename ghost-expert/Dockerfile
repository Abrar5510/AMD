# ponytail: slim CPU image is enough while the app only talks to vLLM.
# Switch to a rocm/pytorch base in Phase 2, when SigLIP/Whisper/Kokoro run in this container.
FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY scripts scripts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

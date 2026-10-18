#!/usr/bin/env bash
# Temporary public demo from a Mac, no AMD GPU: Gemma 3 4B on Ollama, small CPU models, Cloudflare quick tunnel.
# ponytail: quick tunnel URL changes on every restart; a named tunnel on your own domain if it must stay put.
# Needs: brew install ollama cloudflared && ollama pull gemma3:4b, and the .venv (see README).
set -euo pipefail
cd "$(dirname "$0")/.."

[ -f .env.local ] || echo "APP_TOKEN=$(openssl rand -hex 16)" > .env.local
set -a; source .env.local; set +a
export VLLM_URL=${VLLM_URL:-http://localhost:11434} MODEL=${MODEL:-gemma3:4b}
export SIGLIP_MODEL=${SIGLIP_MODEL:-google/siglip-base-patch16-224} WHISPER_MODEL=${WHISPER_MODEL:-openai/whisper-base}
export VERIFY_TIMEOUT_S=${VERIFY_TIMEOUT_S:-20} MAX_UPLOAD_MB=${MAX_UPLOAD_MB:-200}
export HF_HUB_DOWNLOAD_TIMEOUT=30  # a stalled model download otherwise hangs the request forever

PORT=${PORT:-8090}
.venv/bin/uvicorn app.main:app --port "$PORT" &
trap 'kill $!' EXIT
rm -f .public-url
# trycloudflare's API is flaky (slow or blackholed IPs on some networks): retry until a tunnel comes up.
while :; do
  cloudflared tunnel --no-autoupdate --url "http://localhost:$PORT" 2>&1 | while read -r line; do
    echo "$line" | grep -E "ERR|failed" || true
    url=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' <<<"$line" | grep -v '//api\.' || true)
    if [ -n "$url" ]; then
      echo "PUBLIC: $url/?token=$APP_TOKEN" | tee .public-url
      # ghost-expert.pages.dev/app follows the current tunnel. The token is in it on purpose: anyone with the link can author.
      echo "/app $url/?token=$APP_TOKEN 302" > ../submission/_redirects
      npx -y wrangler@3 pages deploy ../submission --project-name ghost-expert --branch main --commit-dirty=true >/dev/null 2>&1 &
    fi
  done || true
  echo "tunnel exited, retrying in 5 s"; sleep 5
done

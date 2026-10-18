#!/usr/bin/env bash
# Install Ollama + serve_mac.sh as LaunchDaemons so the demo runs with nobody logged in.
# Run: sudo ./scripts/install_daemons.sh   Logs: ~/Library/Logs/ghost-expert*.log
# Undo: sudo launchctl bootout system/com.ghostexpert.serve system/com.ghostexpert.ollama
set -euo pipefail
cd "$(dirname "$0")"
[ "$(id -u)" = 0 ] || { echo "run with sudo"; exit 1; }

# The brew LaunchAgent and any hand-started copy would fight the daemons for ports 11434/8090.
sudo -u "$SUDO_USER" /opt/homebrew/bin/brew services stop ollama || true
pkill -f serve_mac.sh || true; pkill -f "uvicorn app.main:app" || true; pkill -f "cloudflared tunnel --no-autoupdate --url" || true
sleep 2

for name in com.ghostexpert.ollama com.ghostexpert.serve; do
  launchctl bootout "system/$name" 2>/dev/null || true
  install -o root -g wheel -m 644 "$name.plist" /Library/LaunchDaemons/
  launchctl bootstrap system "/Library/LaunchDaemons/$name.plist"
done
echo "installed; public URL lands in ghost-expert/.public-url within ~30 s"

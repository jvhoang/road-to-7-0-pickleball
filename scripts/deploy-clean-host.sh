#!/usr/bin/env bash
# Deploy to a neutral Vercel URL (no jvhoang / github in the domain).
# One-time: run `vercel login` in the browser when prompted.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Prefer modern Node if present
if [[ -x /tmp/node-v22.14.0-darwin-arm64/bin/node ]]; then
  export PATH="/tmp/node-v22.14.0-darwin-arm64/bin:$PATH"
fi

echo "Deploying static site to Vercel as project: road-to-7-0-pickleball"
echo "If asked to log in, complete the browser step once."
npx --yes vercel@latest deploy --prod --yes --name road-to-7-0-pickleball

echo ""
echo "After deploy, send THIS URL (not github.io):"
echo "  https://road-to-7-0-pickleball.vercel.app/"
echo ""
echo "Optional: set a custom domain in the Vercel dashboard for something like"
echo "  https://lookinside.roadto7pickleball.com"

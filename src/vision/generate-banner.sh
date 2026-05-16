#!/usr/bin/env bash
# generate-banner.sh — Generate the Resolver Royale banner via OpenAI DALL-E 3
# Requires: OPENAI_API_KEY environment variable, curl, jq

set -euo pipefail

# ─── Configuration ────────────────────────────────────────────────────────────
OUTPUT_FILE="${1:-banner.png}"

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "ERROR: OPENAI_API_KEY environment variable is not set." >&2
  echo "Export it before running: export OPENAI_API_KEY='sk-...'" >&2
  exit 1
fi

for cmd in curl jq; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: Required command '${cmd}' not found." >&2
    exit 1
  fi
done

# TODO:
# ─── Prompt ───────────────────────────────────────────────────────────────────
read -r -d '' PROMPT << 'EOF' || true
Write your prompt here.
EOF

# ─── API Call ─────────────────────────────────────────────────────────────────
echo "Generating banner image via DALL-E 3..."

response=$(curl --silent --show-error \
  "https://api.openai.com/v1/images/generations" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg prompt "$PROMPT" \
    '{
      model: "gpt-image-2-2026-04-21",
      prompt: $prompt,
      size: "1792x1024",
      quality: "high",
      n: 1
    }'
  )")

# Check for API error in response
api_error=$(echo "$response" | jq -r '.error.message // empty')
if [[ -n "$api_error" ]]; then
  echo "ERROR: OpenAI API returned: ${api_error}" >&2
  exit 1
fi

# ─── Extract URL and Download ─────────────────────────────────────────────────
image_url=$(echo "$response" | jq -r '.data[0].url // empty')

if [[ -z "$image_url" ]]; then
  echo "ERROR: No image URL in API response." >&2
  echo "Response: ${response}" >&2
  exit 1
fi

curl --silent --fail --show-error --output "$OUTPUT_FILE" "$image_url"

echo "Banner saved to: ${OUTPUT_FILE}"
echo "Dimensions: 1792x1024 (crop to 1920x600 for a tighter banner if needed)"
echo "<img src=\"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...\" />"

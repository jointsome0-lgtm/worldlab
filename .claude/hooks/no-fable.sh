#!/usr/bin/env bash
set -uo pipefail

input=$(cat)

script=$(printf '%s' "$input" | jq -r '.tool_input.script // ""')
name=$(printf '%s' "$input" | jq -r '.tool_input.name // ""')
path=$(printf '%s' "$input" | jq -r '.tool_input.scriptPath // ""')

text="${script}
${name}"

if [ -n "$path" ] && [ -f "$path" ]; then
  text="${text}
$(cat "$path")"
fi

if printf '%s' "$text" | grep -qi 'fable'; then
  echo "Blocked by project policy: workflow scripts must not route work to the fable model (model: 'fable' / 'claude-fable-5'). Omit the model option or pick another model." >&2
  exit 2
fi

exit 0

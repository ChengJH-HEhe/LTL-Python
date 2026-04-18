#!/usr/bin/env bash
# Download antlr-4.13.2-complete.jar with resume (curl -C -).
# Usage: bash tools/fetch_antlr_jar.sh
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JAR="$ROOT/tools/antlr-4.13.2-complete.jar"
# Maven Central (primary) and antlr.org mirror
URLS=(
  "https://repo1.maven.org/maven2/org/antlr/antlr4/4.13.2/antlr4-4.13.2-complete.jar"
  "https://www.antlr.org/download/antlr-4.13.2-complete.jar"
)
# Published size on Maven for this artifact (bytes)
EXPECTED_MIN=2000000

fetch_one() {
  local url="$1"
  local n=0
  while [ "$n" -lt 30 ]; do
    n=$((n + 1))
    if curl -fL --connect-timeout 30 --max-time 600 --retry 2 --retry-delay 3 \
      -C - -o "$JAR" "$url" 2>/dev/null; then
      local sz
      sz=$(wc -c <"$JAR" | tr -d ' ')
      if [ "$sz" -ge "$EXPECTED_MIN" ] && unzip -t "$JAR" >/dev/null 2>&1; then
        echo "OK: $JAR ($sz bytes)"
        return 0
      fi
    fi
    echo "retry $n (partial or corrupt), resuming..." >&2
    sleep 2
  done
  return 1
}

mkdir -p "$ROOT/tools"
for u in "${URLS[@]}"; do
  echo "Trying: $u" >&2
  if fetch_one "$u"; then
    java -jar "$JAR" 2>&1 | head -1 >&2 || true
    exit 0
  fi
  rm -f "$JAR"
done
echo "error: could not download a valid ANTLR jar; try manually in browser:" >&2
echo "  ${URLS[0]}" >&2
exit 1

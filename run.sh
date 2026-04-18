#!/usr/bin/env bash
# Run model checker from repo root (README: TS.txt + benchmark.txt → A+B 行 0/1)。
#   ./run.sh
#   ./run.sh path/TS.txt path/benchmark.txt
#
# ANTLR 4：jar 默认 tools/antlr4-4.13.2-complete.jar；由本脚本导出 ANTLR_JAR供生成脚本使用。
# 从 grammars/LTL.g4 生成 Python解析器：
#   ./run.sh --gen-antlr
#   ANTLR_JAR=/path/to/antlr-4.13.2-complete.jar ./run.sh --gen-antlr
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

DEFAULT_ANTLR_JAR="$ROOT/tools/antlr4-4.13.2-complete.jar"
export ANTLR_JAR="${ANTLR_JAR:-$DEFAULT_ANTLR_JAR}"

if [[ "${1:-}" == "--gen-antlr" ]]; then
  shift
  exec bash "$ROOT/tools/generate_antlr_parser.sh" "$@"
fi

if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
elif [[ -n "${PYTHON:-}" ]]; then
  PY="$PYTHON"
else
  PY="python3"
fi

exec "$PY" "$ROOT/src/main.py" "$@"

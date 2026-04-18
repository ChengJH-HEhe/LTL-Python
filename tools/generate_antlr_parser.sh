#!/usr/bin/env bash
# Generate Python 3 lexer, parser, and visitor from grammars/LTL.g4 (ANTLR 4.13.x).
#
# Run with Bash (not `sh`):  bash tools/generate_antlr_parser.sh
#
# Prerequisites:
#   - Java 8+ on PATH
#   - antlr4-4.13.2-complete.jar (default: tools/antlr4-4.13.2-complete.jar)
#   - pip: antlr4-python3-runtime matching the jar major.minor (e.g. 4.13.x)
#
# Usage:
#   bash tools/generate_antlr_parser.sh
#   ANTLR_JAR=/path/to/antlr-4.13.2-complete.jar bash tools/generate_antlr_parser.sh  # official name ok too
#
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEFAULT_JAR="$ROOT/tools/antlr4-4.13.2-complete.jar"
JAR="${ANTLR_JAR:-$DEFAULT_JAR}"
GRAMMAR="$ROOT/grammars/LTL.g4"
OUT="$ROOT/ltl_formula/generated"

die() {
  echo "error: $*" >&2
  exit 1
}

command -v java >/dev/null 2>&1 || die "java not found (install JRE 8+)"
[ -f "$GRAMMAR" ] || die "grammar not found: $GRAMMAR"
[ -f "$JAR" ] || die "ANTLR jar not found: $JAR (set ANTLR_JAR or download from https://www.antlr.org/download.html )"
[ -s "$JAR" ] || die "ANTLR jar is empty: $JAR"

mkdir -p "$OUT"

echo "== ANTLR LTL -> Python =="
echo "   grammar: $GRAMMAR"
echo "   jar:     $JAR"
echo "   out:     $OUT"
echo

java -jar "$JAR" \
  -Dlanguage=Python3 \
  -visitor \
  -no-listener \
  -o "$OUT" \
  "$GRAMMAR"

echo
echo "Generated:"
ls -1 "$OUT"/*.py 2>/dev/null | sed 's/^/   /' || true
echo
echo "Next: pip install -r requirements.txt"
echo "Then: from ltl_formula.antlr_parse import parse_ltl_antlr"
echo "  or:  from ltl_formula import parse_ltl"

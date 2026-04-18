#!/usr/bin/env bash
# Backwards-compatible wrapper; must be run with Bash.
set -eu
exec "$(cd "$(dirname "$0")" && pwd)/generate_antlr_parser.sh"

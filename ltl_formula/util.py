from __future__ import annotations

import re

_PREFIX = re.compile(r"^\s*\d+\s+")


def strip_state_prefix(line: str) -> str:
    """Remove leading 'k ' from per-state LTL lines in benchmarks (e.g. '3 cU(!a)' -> 'cU(!a)')."""
    return _PREFIX.sub("", line, count=1).strip()

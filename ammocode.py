#!/usr/bin/env python3
"""AmmoCode — single secured executable entry (replacement-only updates)."""
from __future__ import annotations

import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(ROOT, "server")
if SERVER not in sys.path:
    sys.path.insert(0, SERVER)

_spec = importlib.util.spec_from_file_location(
    "ammocode_serve", os.path.join(SERVER, "ammocode-serve.py"),
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_mod)

if __name__ == "__main__":
    raise SystemExit(_mod.main())
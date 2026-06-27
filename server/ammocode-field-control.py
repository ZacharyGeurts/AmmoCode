#!/usr/bin/env python3
"""SG / Grok16 field control — detect fielded posture and defield safely."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SG = ROOT.parent
GROK16 = Path(os.environ.get("GROK16_ROOT", SG / "Grok16"))
NEWLATEST = Path(os.environ.get("NEXUS_INSTALL_ROOT", SG / "NewLatest"))
STATE = Path(os.environ.get("NEXUS_STATE_DIR", NEWLATEST / ".nexus-state"))

DEFIELD_MARKER = STATE / "ammocode-defield.marker"
DEFIELD_JSON = STATE / "ammocode-defield.json"
FIELD_RUNTIME = STATE / "field-combinatorics-runtime.json"
ZNET_MARKER = STATE / "znetwork-running.marker"
ZNET_SOCK = STATE / "znetwork-field.sock"
FIELD_DRIVE = NEWLATEST / ".nexus-field-drive"


def _load_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default if default is not None else {}


def _save_json(path: Path, doc: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def _grok16_posture() -> dict[str, Any]:
    instill = GROK16 / "lib" / "g16-ammocode-field-instill.py"
    if not instill.is_file():
        return {"posture": "unknown", "field": False}
    try:
        proc = subprocess.run(
            [sys.executable, str(instill), "posture", "plain"],
            capture_output=True, text=True, timeout=8,
        )
        if proc.returncode == 0 and proc.stdout.strip():
            return json.loads(proc.stdout)
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return {"posture": "unknown", "field": False}


def sg_field_status() -> dict[str, Any]:
    """Detect whether SG / Grok16 / NEXUS field stack is actively fielded."""
    signals: list[dict[str, Any]] = []
    fielded = False

    if ZNET_MARKER.is_file():
        fielded = True
        signals.append({"id": "znetwork_running_marker", "active": True})
    if ZNET_SOCK.exists():
        fielded = True
        signals.append({"id": "znetwork_field_sock", "active": True})

    attach = _load_json(STATE / "ammocode-znetwork-attach.json", {})
    if attach.get("znetwork_running"):
        fielded = True
        signals.append({"id": "ammocode_znetwork_running", "active": True})
    if attach.get("detail") == "startup_with_us" and attach.get("interfered"):
        signals.append({"id": "ammocode_field_startup_attempt", "active": True, "fielded_hint": True})

    rt = _load_json(FIELD_RUNTIME, {})
    if rt.get("updated"):
        signals.append({"id": "field_combinatorics_runtime", "active": True, "updated": rt.get("updated")})
        fielded = True

    if FIELD_DRIVE.is_dir() and any(FIELD_DRIVE.rglob("nexus-field")):
        signals.append({"id": "nexus_field_drive_mirror", "active": True})
        fielded = True

    posture = _grok16_posture()
    if posture.get("field") and posture.get("posture") == "field":
        signals.append({"id": "grok16_ammocode_posture_field", "active": True})

    defield_active = DEFIELD_MARKER.is_file()
    doc = _load_json(DEFIELD_JSON, {})

    return {
        "ok": True,
        "fielded": fielded and not defield_active,
        "defield_active": defield_active,
        "signals": signals,
        "grok16_posture": posture,
        "defield": doc,
        "motto": "Resting on field → defield. No subfields.",
    }


def defield_sg(*, reason: str = "operator_request", force: bool = False) -> dict[str, Any]:
    """Defield SG/Grok16 — stop field-on-field, block re-field until cleared."""
    before = sg_field_status()
    if not force and not before.get("fielded") and before.get("defield_active"):
        return {"ok": True, "already_defielded": True, "status": before}

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    doc = {
        "schema": "ammocode-defield/v1",
        "defielded": True,
        "field": False,
        "posture": "defield",
        "no_subfields": True,
        "resting_on_field": True,
        "reason": reason,
        "ts": ts,
        "signals_before": before.get("signals") or [],
    }
    try:
        STATE.mkdir(parents=True, exist_ok=True)
        DEFIELD_MARKER.write_text(f"ammocode-defield {ts}\n", encoding="utf-8")
        _save_json(DEFIELD_JSON, doc)
    except OSError as exc:
        return {"ok": False, "error": str(exc)}

    cleared: list[str] = []
    for path in (ZNET_MARKER, STATE / "ammocode-shield-active.marker"):
        try:
            if path.is_file():
                path.unlink()
                cleared.append(path.name)
        except OSError:
            pass

    env_hint = STATE / "ammocode-defield.env"
    try:
        env_hint.write_text("G16_AMMOCODE_RESTING_ON_FIELD=1\nAMMOCODE_NO_ZNETWORK=1\n", encoding="utf-8")
    except OSError:
        pass

    after = sg_field_status()
    return {
        "ok": True,
        "defielded": True,
        "cleared_markers": cleared,
        "before": before,
        "after": after,
        "receipt": doc,
    }


def is_defielded() -> bool:
    return DEFIELD_MARKER.is_file()


def clear_defield() -> dict[str, Any]:
    removed = []
    for path in (DEFIELD_MARKER, DEFIELD_JSON, STATE / "ammocode-defield.env"):
        try:
            if path.is_file():
                path.unlink()
                removed.append(path.name)
        except OSError:
            pass
    return {"ok": True, "cleared": removed, "status": sg_field_status()}


def auto_defield_if_fielded() -> dict[str, Any]:
    st = sg_field_status()
    if st.get("fielded"):
        return defield_sg(reason="auto_on_ammocode_boot", force=True)
    return {"ok": True, "action": "none", "fielded": False, "status": st}
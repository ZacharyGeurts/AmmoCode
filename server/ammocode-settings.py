#!/usr/bin/env python3
"""AmmoCode secured settings — signed file, schema migration on every run."""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any

from ammocode_runtime import bundle_root, executable_dir, is_frozen, settings_dir

SCHEMA_PATH = bundle_root() / "data" / "ammocode-settings-schema.json"
SETTINGS_FILE = os.environ.get("AMMOCODE_SETTINGS_FILE", "").strip()
KEY_FILE = "ammocode-settings.key"


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _load_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default if default is not None else {}


def _save_json_atomic(path: Path, doc: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def settings_path() -> Path:
    if SETTINGS_FILE:
        return Path(SETTINGS_FILE).expanduser()
    name = _load_json(bundle_root() / "data" / "ammocode-distribution-doctrine.json", {}).get(
        "settings", {},
    ).get("filename", "ammocode-settings.secure.json")
    return settings_dir() / name


def key_path() -> Path:
    return settings_dir() / KEY_FILE


def _signing_key() -> bytes:
    kp = key_path()
    if kp.is_file():
        return kp.read_bytes()[:64]
    key = secrets.token_bytes(32)
    settings_dir().mkdir(parents=True, exist_ok=True)
    kp.write_bytes(key)
    try:
        os.chmod(kp, 0o600)
    except OSError:
        pass
    return key


def load_schema() -> dict[str, Any]:
    return _load_json(SCHEMA_PATH, {"schema_version": 1, "options": {}})


def _canonical_values(values: dict[str, Any]) -> bytes:
    return json.dumps(values, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _signature(schema_version: int, values: dict[str, Any], settings_version: str) -> str:
    payload = f"{schema_version}:{settings_version}:".encode("utf-8") + _canonical_values(values)
    return hmac.new(_signing_key(), payload, hashlib.sha256).hexdigest()


def _verify(doc: dict[str, Any]) -> bool:
    sig = str(doc.get("signature") or "")
    if not sig:
        return False
    expected = _signature(
        int(doc.get("schema_version") or 0),
        doc.get("values") or {},
        str(doc.get("settings_version") or ""),
    )
    return hmac.compare_digest(sig, expected)


def _coerce_option(spec: dict[str, Any], value: Any) -> Any:
    typ = spec.get("type", "string")
    if typ == "boolean":
        return bool(value)
    if typ == "integer":
        try:
            v = int(value)
        except (TypeError, ValueError):
            v = int(spec.get("default", 0))
        return max(int(spec.get("min", v)), min(int(spec.get("max", v)), v))
    if typ == "number":
        try:
            v = float(value)
        except (TypeError, ValueError):
            v = float(spec.get("default", 0))
        return max(float(spec.get("min", v)), min(float(spec.get("max", v)), v))
    if typ == "object":
        return value if isinstance(value, dict) else dict(spec.get("default") or {})
    s = str(value if value is not None else spec.get("default", ""))
    mx = int(spec.get("maxLength", 512))
    return s[:mx]


def migrate_values(
    incoming: dict[str, Any] | None,
    *,
    from_schema_version: int = 0,
) -> dict[str, Any]:
    """Intelligent migration — add new defaults, drop removed keys, coerce types."""
    schema = load_schema()
    target_sv = int(schema.get("schema_version") or 1)
    options: dict[str, Any] = schema.get("options") or {}
    deprecated: dict[str, Any] = schema.get("deprecated") or {}
    src = dict(incoming or {})
    out: dict[str, Any] = {}
    added: list[str] = []
    removed: list[str] = []

    for key, spec in options.items():
        if key in src:
            out[key] = _coerce_option(spec, src[key])
        else:
            out[key] = _coerce_option(spec, spec.get("default"))
            if from_schema_version < target_sv:
                added.append(key)

    for key in list(src.keys()):
        if key in options:
            continue
        if key in deprecated:
            repl = deprecated[key].get("replace_with")
            if repl and repl in options and repl not in out:
                out[repl] = _coerce_option(options[repl], src[key])
            removed.append(key)
        else:
            removed.append(key)

    return {
        "values": out,
        "schema_version": target_sv,
        "settings_version": str(schema.get("settings_version") or "4.9.0"),
        "added_keys": added,
        "removed_keys": removed,
        "migrated": from_schema_version < target_sv or bool(added) or bool(removed),
    }


def build_document(values: dict[str, Any], *, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    schema = load_schema()
    sv = int(schema.get("schema_version") or 1)
    settings_version = str(schema.get("settings_version") or "4.9.0")
    doc: dict[str, Any] = {
        "schema": "ammocode-settings-secure/v1",
        "schema_version": sv,
        "settings_version": settings_version,
        "updated": _now(),
        "values": values,
        "signature": "",
    }
    if meta:
        doc.update({k: v for k, v in meta.items() if k not in doc})
    doc["signature"] = _signature(sv, values, settings_version)
    return doc


def load_settings(*, import_local: dict[str, Any] | None = None) -> dict[str, Any]:
    """Load secured settings; migrate and rewrite when schema/options change."""
    path = settings_path()
    schema = load_schema()
    target_sv = int(schema.get("schema_version") or 1)
    existing: dict[str, Any] | None = None
    from_sv = 0
    tampered = False

    if path.is_file():
        raw = _load_json(path, {})
        if raw.get("schema") == "ammocode-settings-secure/v1":
            if _verify(raw):
                existing = raw.get("values") or {}
                from_sv = int(raw.get("schema_version") or 0)
            else:
                tampered = True
                existing = None

    if existing is None and import_local:
        existing = import_local

    mig = migrate_values(existing, from_schema_version=from_sv)
    values = mig["values"]
    changed = mig["migrated"] or tampered or not path.is_file()

    doc = build_document(values, meta={
        "migration": {
            "added_keys": mig.get("added_keys") or [],
            "removed_keys": mig.get("removed_keys") or [],
            "from_schema_version": from_sv,
            "to_schema_version": target_sv,
            "tampered_recovery": tampered,
        },
    })
    if changed:
        _save_json_atomic(path, doc)

    return {
        "ok": True,
        "settings": values,
        "path": str(path),
        "schema_version": target_sv,
        "settings_version": doc["settings_version"],
        "migrated": changed,
        "migration": doc.get("migration"),
        "signed": True,
        "tampered_recovery": tampered,
    }


def save_settings(patch: dict[str, Any]) -> dict[str, Any]:
    current = load_settings()
    values = dict(current.get("settings") or {})
    schema = load_schema()
    options = schema.get("options") or {}
    for key, val in (patch or {}).items():
        if key not in options:
            continue
        values[key] = _coerce_option(options[key], val)
    doc = build_document(values)
    _save_json_atomic(settings_path(), doc)
    return {
        "ok": True,
        "settings": values,
        "path": str(settings_path()),
        "updated": doc["updated"],
        "signed": True,
    }


def settings_status() -> dict[str, Any]:
    schema = load_schema()
    path = settings_path()
    doc = _load_json(path, {}) if path.is_file() else {}
    return {
        "ok": True,
        "frozen": is_frozen(),
        "executable": str(executable_dir()),
        "bundle_root": str(bundle_root()),
        "settings_path": str(path),
        "settings_exists": path.is_file(),
        "signature_valid": _verify(doc) if doc else False,
        "schema_version": int(schema.get("schema_version") or 1),
        "settings_version": str(schema.get("settings_version") or "4.9.0"),
        "distribution": _load_json(bundle_root() / "data" / "ammocode-distribution-doctrine.json", {}),
        "replacement_only": True,
    }


def editor_settings() -> dict[str, Any]:
    s = load_settings().get("settings") or {}
    return {
        "fontSize": s.get("fontSize"),
        "tabSize": s.get("tabSize"),
        "wordWrap": s.get("wordWrap"),
        "autodetect": s.get("autodetect"),
        "profile": s.get("profile"),
        "theme": s.get("theme"),
        "tabAging": s.get("tabAging"),
    }


def collab_settings() -> dict[str, Any]:
    s = load_settings().get("settings") or {}
    return {
        "name": s.get("collabName"),
        "cursorId": s.get("collabCursorId"),
        "invite": s.get("collabInvite"),
        "muted": s.get("collabMuted"),
        "volume": s.get("collabVolume"),
    }
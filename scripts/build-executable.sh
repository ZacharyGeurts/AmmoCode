#!/usr/bin/env bash
# Build single secured AmmoCode executable — replace file to upgrade; settings stay external.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OUT="${AMMOCODE_BUILD_DIR:-$ROOT/dist}"
NAME="${AMMOCODE_EXE_NAME:-ammocode}"

if ! python3 -c "import PyInstaller" 2>/dev/null; then
  echo "Installing PyInstaller…" >&2
  python3 -m pip install --user pyinstaller
fi

export AMMOCODE_FROZEN=1
python3 -m PyInstaller \
  --onefile \
  --name "$NAME" \
  --add-data "index.html:." \
  --add-data "tab.html:." \
  --add-data "assets:assets" \
  --add-data "lib:lib" \
  --add-data "data:data" \
  --add-data "embed:embed" \
  --hidden-import "ammocode_runtime" \
  --hidden-import "ammocode_settings" \
  --hidden-import "ammocode_field_control" \
  --hidden-import "ammocode_security_manage" \
  --hidden-import "ammocode_network" \
  --hidden-import "ammocode_znetwork" \
  --hidden-import "ammocode_collab" \
  --hidden-import "ddos_guard" \
  --collect-all "websockets" \
  --distpath "$OUT" \
  --workpath "$OUT/build" \
  --specpath "$OUT" \
  ammocode.py

echo "Built: $OUT/$NAME"
echo "Upgrade: replace $OUT/$NAME only — settings in ~/.config/ammocode/"
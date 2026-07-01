#!/usr/bin/env bash
# Publish AmmoCode/docs → GitHub Pages (gh-pages). Programmerland manual home.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCS="${ROOT}/docs"
REPO_DIR="${PAGES_REPO:-${ROOT}/.pages-ammocode-publish}"
REMOTE="${PAGES_REMOTE:-https://github.com/ZacharyGeurts/AmmoCode.git}"
BRANCH="${PAGES_BRANCH:-gh-pages}"
VER="${AMMOCODE_VERSION:-$(python3 -c "import json;print(json.load(open('${ROOT}/data/ammocode-version.json'))['distro_version'])" 2>/dev/null || echo 6.1.0)}"

[[ -d "$DOCS" ]] || { echo "Missing ${DOCS}" >&2; exit 1; }

if [[ ! -d "${REPO_DIR}/.git" ]]; then
  rm -rf "$REPO_DIR"
  if git ls-remote --heads "$REMOTE" "$BRANCH" 2>/dev/null | grep -q "$BRANCH"; then
    git clone --branch "$BRANCH" --single-branch "$REMOTE" "$REPO_DIR"
  else
    mkdir -p "$REPO_DIR"
    git -C "$REPO_DIR" init -b "$BRANCH"
    git -C "$REPO_DIR" remote add origin "$REMOTE"
  fi
fi

rsync -a --delete --exclude='.git' "${DOCS}/" "${REPO_DIR}/"
cd "$REPO_DIR"
git add -A
if git diff --cached --quiet; then
  echo "AmmoCode Pages up to date"
  exit 0
fi
git -c user.email="gzac5314@users.noreply.github.com" -c user.name="ZacharyGeurts" \
  commit -m "pages: AmmoCode Programmerland v${VER}"
git push origin "$BRANCH" 2>/dev/null || git push -u origin "$BRANCH"
echo "Pages: https://zacharygeurts.github.io/AmmoCode/"
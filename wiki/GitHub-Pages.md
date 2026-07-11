# GitHub Pages

AmmoCode on github.io is a **static editor** — pure HTML/CSS/JS.

## Features online

- Syntax highlight (client-side)
- 268-extension language map from `data/field-programming-filetypes.json`
- Themes + toolbar
- File open via browser picker
- **Export** download (never writes the repo or your disk from Pages)

## Not available on Pages

- Loopback g16 compile/run API
- Local secure settings vault (uses `localStorage` instead)
- Collab / znetwork server modules

Force static mode on any host: `?pages=1`

## Publish

From AmmoOS stack:

```bash
# scripts/publish-ammocode-pages.sh  (AmmoOS)
# or rsync static tree to gh-pages / main (this repo serves Pages from main)
```

Required root files: `index.html`, `.nojekyll`, `lib/`, `assets/`, `data/`.

## Docs on Pages

- `/docs.html` — hub linking into this wiki
- `/releases.html` — version + best-version policy

# Troubleshooting

## Pages editor blank / no highlight

- Hard refresh (CSP + cached assets)
- Confirm `lib/pages-static.js` loads first
- Open DevTools → network: `data/field-programming-filetypes.json` must be 200

## g16 offline pill

Expected on github.io. Clone AmmoCode, put Grok16 on `PATH`, run `python3 ammocode.py`.

## Python obsolete on Field hosts

Field AmmoLang intercepts `python3` toward native C++ tools. For AmmoCode loopback server use a real CPython outside Field `bin/` or serve static files only:

```bash
# static preview
python3 -m http.server 9555
# open http://127.0.0.1:9555/?pages=1
```

## Wrong “best” tree

If an old `package.json` says 4.9.0 but `data/ammocode-version.json` says 6.1.0 — **trust ammocode-version.json** and this wiki. UI pills show **v6.1.0**.

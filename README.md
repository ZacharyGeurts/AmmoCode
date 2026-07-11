# AmmoCode 6.1 — NEXUS C2 Stack Editor

**Live editor (GitHub Pages):** https://zacharygeurts.github.io/AmmoCode/  
**Wiki:** https://github.com/ZacharyGeurts/AmmoCode/wiki  
**Releases / SHA:** https://zacharygeurts.github.io/AmmoCode/releases.html  
**Issues:** https://github.com/ZacharyGeurts/AmmoCode/issues

Lean sovereign code editor — opens **any text-era file**, 268 extensions, **g16 discern**, zero telemetry, non-destructive export.

Paired with **Grok16** (compiler plane in Field / AmmoOS stack).

| Surface | Best source |
|---------|-------------|
| Editor UI + Pages | **this repo** · AmmoCode **6.1.0** |
| Compiler / g16 / g++16 | **Grok16** · `16.1.0-hard`+ (Field stack) |
| Full OS install | [AmmoOS](https://github.com/ZacharyGeurts/AmmoOS) |

## Quick start

### Browser (no install)

Open the live Pages editor:

https://zacharygeurts.github.io/AmmoCode/

- Open a file from disk (browser picker)
- Syntax highlight · themes · export download
- **Non-destructive** — never writes your disk; export only

### Local loopback (g16 run/compile)

```bash
git clone https://github.com/ZacharyGeurts/AmmoCode.git
cd AmmoCode
# optional: pair Grok16 from Field / AmmoOS stack so g16 is on PATH
python3 ammocode.py
# → http://127.0.0.1:9555/
./scripts/ammocode-open.sh /path/to/file.txt
```

For a full stack install (AmmoOS + Grok16 + Hostess7):

```bash
git clone https://github.com/ZacharyGeurts/AmmoOS.git
cd AmmoOS && git checkout v2.0.0-beta6   # or latest release
./scripts/wire-stack.sh
```

## Text-era open

Canonical **268-extension** DB (`data/field-programming-filetypes.json`):

| Era | Examples | Encoding |
|-----|----------|----------|
| Modern | `.ts`, `.py`, `.rs`, `.md`, `.cpp` | UTF-8 |
| DOS / BBS | `CONFIG.SYS`, `.nfo`, `.ans` | CP437 / Latin-1 |
| Legacy | `.bas`, `.f90`, `.cob`, `.pas` | Latin-1 ladder |
| Plain | `.txt`, `.log`, `.lst` | Auto-detect |

Binary guard rejects `.exe`, images, archives — unless the extension is in the programming DB.

## Non-destructive

| Rule | Behavior |
|------|----------|
| Disk API | Read-only in Pages mode |
| Save | **Export** (browser download) |
| Run/compile | Loopback + g16 when local server is up |
| Settings | `localStorage` on Pages · secure store when loopback |

Doctrine: `data/ammocode-nondestructive-doctrine.json`

## GitHub Pages

Static editor — no server required:

| URL | Role |
|-----|------|
| [/](https://zacharygeurts.github.io/AmmoCode/) | Live editor |
| [/releases.html](https://zacharygeurts.github.io/AmmoCode/releases.html) | Version · checksums |
| [/docs.html](https://zacharygeurts.github.io/AmmoCode/docs.html) | Docs hub → wiki |

Query `?pages=1` forces static mode on any host.

## Version

See `data/ammocode-version.json`:

- **AmmoCode** `6.1.0` · codename NEXUS C2  
- **Grok16** pairing `16.2.0` / Field hard plane `16.1.0-hard`  
- Tag: `v6.1.0`

## License

© 2025–2026 Zachary Robert Geurts · see stack license / Hostess7 license tree.
GPL-3.0-or-later for package metadata; operational Field surfaces may carry additional doctrine.

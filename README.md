# AmmoCode 6.2 — Full Compiler Suite + Editor

**Live:** https://zacharygeurts.github.io/AmmoCode/  
**Grok16 hard plane:** https://github.com/ZacharyGeurts/Grok16 · `v16.1.0-hard`  
**Wiki:** https://github.com/ZacharyGeurts/AmmoCode/wiki

AmmoCode is the **full compiler suite and code editor** for 2026+ — wired bidirectionally with **Grok16**.

## Language suite

- Dropdown: **Python, JS/TS, C/C++, Rust, Go, Java…** plus **BASIC, QBasic, QuickBASIC, FreeBASIC, VBA, Pascal, Fortran, COBOL…**
- **★ Popular** — most-used languages first  
- **A–Z** — alphabetize  
- `?lang=qbasic` deep-link works on Pages

## Grok16 wire

| Mode | Behavior |
|------|----------|
| Pages | Full suite UI · highlight · export · no local compile |
| Loopback | `g16` check / build / run · profiles per language |

```bash
git clone https://github.com/ZacharyGeurts/AmmoCode.git
cd AmmoCode
# put Grok16 hard on PATH (NewLatest/Grok16/bin or this stack)
python3 ammocode.py   # http://127.0.0.1:9555/
```

Pair: `data/ammocode-g16-pair.json` · suite: `data/ammocode-language-suite.json`

## Run tab (Pages = local)

**Editor | Run** switcher. **F7** sends the buffer into a **sandboxed** iframe (`allow-scripts` only · no parent DOM · no network).

| Language on github.io | Behavior |
|----------------------|----------|
| JavaScript / TypeScript | Sandbox run |
| HTML | Sandbox document |
| BASIC / QBasic / FreeBASIC / VBA | Built-in interpreter |
| C / C++ / Rust / Go / Python | Needs Grok16 hard (clone + loopback) |

Same UI and run path on https://zacharygeurts.github.io/AmmoCode/ and local loopback.

## Features

- Non-destructive export · 268 text-era extensions  
- Language suite · ★ Popular + A–Z  
- g16 discern · NEXUS C2 themes · F5/F6/F7  
- Field / AmmoLang / Hostess secure profiles  

**Version:** 6.2.0 · tag `v6.2.0`

# Install

## Browser only (GitHub Pages)

No clone required:

1. Open https://zacharygeurts.github.io/AmmoCode/
2. Use **Open** to pick a file
3. **Export** to download edits (non-destructive)

## Clone this repo

```bash
git clone https://github.com/ZacharyGeurts/AmmoCode.git
cd AmmoCode
python3 ammocode.py
# http://127.0.0.1:9555/
```

Optional open helper:

```bash
./scripts/ammocode-open.sh /path/to/file.cpp
```

## Full Field / AmmoOS stack

For Grok16 + Hostess7 + mesh:

```bash
git clone https://github.com/ZacharyGeurts/AmmoOS.git
cd AmmoOS
git checkout v2.0.0-beta6   # or latest
./scripts/wire-stack.sh
sudo ./install-all.sh
```

AmmoCode lives under `AmmoOS/AmmoCode` in the stack; this standalone repo is the **public best editor** for Pages + wiki.

## Requirements

| Mode | Needs |
|------|--------|
| Pages static | Modern browser only |
| Local loopback | Python 3 for `ammocode.py` server (optional) |
| g16 compile | Grok16 on `PATH` (`g16`, `g++16`) |

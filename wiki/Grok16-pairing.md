# Grok16 pairing

## Roles

| Component | Role |
|-----------|------|
| **AmmoCode 6.1** | Editor UI · Pages · filetypes · non-destructive export |
| **Grok16** | Field compiler plane · `g16` / `g++16` · hard flags · exploit-free policy |

## Best version rule

1. Prefer **AmmoCode 6.1.0** for anything the operator *sees and types in*.
2. Prefer **Grok16 hard** (`16.1.0-hard`+) for anything that *compiles or links*.
3. Never treat Grok16 README samples that still mention Python forge as the editor product — AmmoCode is the editor; Grok16 is the toolplane.

## Local compile flow

```text
AmmoCode (loopback) → g16 discern → g16 / g++16 build → output pane
```

On Pages, the pill shows **pages editor** — clone + Grok16 for full compile.

## Field stack locations (SG)

- Editor: `NewLatest/AmmoOS/AmmoCode`
- Compiler: `NewLatest/Grok16` → `bin/g16`, `bin/g++16`, `field-ammolang`

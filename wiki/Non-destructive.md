# Non-destructive

Doctrine: `data/ammocode-nondestructive-doctrine.json`

| Rule | Behavior |
|------|----------|
| Pages disk | **No** server-side write |
| Save | **Export** browser download |
| Run jail | Blocks writing AmmoCode tree / system paths (local) |
| Settings | Pages → `localStorage`; loopback → secure settings store |

AmmoCode never “save in place” on github.io. Operators always choose the export destination.

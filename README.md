# AmmoCode

**THE compiler GUI for 2027** — Grok16 **5.0.0** stack, GitHub **v4.9.0** upload track.

Hardened editor with invite-only collab, network mesh, ZNetwork shield, and g16 belt_2_0 integration. Zero telemetry. Loopback only.

```bash
npm start          # dev tree
npm run build      # single secured executable → dist/ammocode
./dist/ammocode    # replacement-only upgrade; settings stay external
```

- GUI: http://127.0.0.1:9555/
- Browser tab: http://127.0.0.1:9555/tab.html
- Settings: `~/.config/ammocode/ammocode-settings.secure.json` (signed, auto-migrates on run)

**No alterations to the executable** — replace the file to upgrade. Options added or removed in new versions migrate into the secured settings file automatically.

See [RELEASE-4.9.md](RELEASE-4.9.md) and [REVIEW_PREP.md](REVIEW_PREP.md).
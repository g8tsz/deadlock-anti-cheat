# Roadmap

**Deadlock AC (UrnIt Anticheat)** – current state, known issues, and next steps. For setup and usage see the [main README](https://github.com/lorddummy/deadlock-anti-cheat/blob/main/README.md).

---

## Current state

| Feature | Status | Notes |
|--------|--------|--------|
| **Screenshots** | ✅ | Game window or full desktop PNG every 5 s (WIC); partial window title match (e.g. "Deadlock - …"). |
| **Task list** | ✅ | Process name, PID, SessionID to TASK.TXT every 3 s. |
| **PC/Hardware** | ✅ | OS user, Windows build from registry, CPU (brand, cores, vendor, cache, microarch), GPU (DXGI). |
| **Keylogger** | ✅ | KeyDown/KeyUp to KEY_LOG.TXT (only when Deadlock window focused); timestamps in ms. |
| **Discord upload** | ✅ | Webhook upload of REPORT, KEY_LOG, TASK, screenshots at session end. Upload status written to report. |
| **Session end** | ✅ | Auto when Deadlock process exits; F12 still ends manually. Config: `AUTO_UPLOAD_ON_GAME_EXIT`. |
| **Cheat list** | ✅ | Load from `cheat_list.txt` next to exe (or built-in list). Use `scripts/scrape_deadlock_cheats.py` to generate from elitepvpers. |

---

## Known issues

**Fixed:** Task loop variable, duplicate flagged programs, null process name, invalid log handles, OS version from registry, log handles closed after upload.

**Still known (low priority):** CPU block is x64-only (`#ifdef CPU_FEATURES_ARCH_X86_64`); on 32-bit/ARM no CPU details. `ConvertWideToString` can throw on invalid UTF-16 in process names (rare).

---

## Next steps

- **Config** – Intervals and options load from `config.txt` next to exe; no recompile needed.
- **Macro hint** – Report includes "Possible macro/bot" when key interval variance is very low (configurable threshold).
- **Session cleanup** – Optional: delete session folder after successful upload (`CLEANUP_AFTER_UPLOAD=1` in config.txt).

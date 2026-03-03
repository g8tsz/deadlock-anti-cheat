# Suggestions to Make UrnIt Anticheat Better

## Implemented (first pass)
- **CPU load first sample** – Avoid divide-by-zero / garbage on first tick (prev_total/prev_idle init + skip when delta 0).
- **Discord rate limit** – Sleep between webhook batches so we stay under 5 req/2 sec.
- **WinHTTP timeouts** – Set send/receive timeouts so upload doesn’t hang forever on bad network.
- **Client version in report** – One line in REPORT.TXT so you know which build produced the log.

## Implemented (second pass)
- **Named constants** – All intervals and limits in `Config::` (TASK_SCAN_INTERVAL_SEC, SCREENSHOT_INTERVAL_SEC, KEYLOG_INTERVAL_SEC, LOOP_SLEEP_MS, WEBHOOK_BATCH_SIZE, UPLOAD_TIMEOUT_MS, etc.) so you can tune in one place.
- **Session summary in report** – At end of REPORT.TXT: “SESSION SUMMARY” with Multiple Deadlock instances (Yes/No), Flagged (cheat list), Flagged (performance list). Reviewers see flags at a glance.
- **Optional player ID** – If `player_id.txt` (one line) exists next to the exe, Discord message is “Player: &lt;id&gt; – UrnIt Anticheat session (part N)”. Copy `player_id.txt.example` to `player_id.txt` and set tournament tag or Discord ID.
- **Upload retry** – If a webhook batch fails, wait 1 s and retry once.
- **Screenshot upload cap** – BMPs over 8 MB are not attached to Discord (still saved on disk) to avoid huge uploads and rate limits.

## Implemented (third pass – “make it better”)
- **OS version from registry** – Replaced `GetVersionEx` with registry read (`CurrentBuild`, `DisplayVersion`) so the report shows the real Windows build and release (e.g. "build 19045 (22H2)").
- **Game-window-only screenshots** – When the Deadlock window exists, screenshots capture only that window (smaller files, in-game evidence). Report line says "Screen Shot (game window) at …". Falls back to full screen if the window isn’t found.
- **Player ID in report** – If `player_id.txt` is set, the report header includes "Player ID: &lt;id&gt;" so the uploaded REPORT.TXT identifies the player.
- **Upload status in Discord** – After all batches, the client sends a final webhook message: "UrnIt upload: completed" or "UrnIt upload: one or more batches failed" (with optional "Player: …" prefix). Staff can see at a glance whether the session uploaded fully.
- **Log file handles closed** – ReportConclusion now closes the three log file handles after upload instead of relying on process exit.

---

## Reliability & robustness

- **OS version** – `GetVersionEx` is deprecated and often wrong on Win 10/11. Prefer:
  - `RtlGetVersion` (ntdll), or
  - Registry `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion` (CurrentBuild, DisplayVersion, etc.).
- **Upload failure** – On WinHTTP or non-2xx response, optionally retry once and/or append a line to REPORT.TXT (“Upload failed: …”) so you know it didn’t reach Discord.
- **Oversized screenshots** – Multi‑monitor BMPs can be huge. Cap per-file size (e.g. skip or truncate BMPs > 8 MB) or reduce capture resolution so uploads stay manageable.

---

## Anticheat effectiveness

- **Cheat process list** – `all_programs_list` is still placeholder. Add real process names (e.g. known FPS cheat executables, overlay injectors). Research what’s common for your scene and update the list; flag when any match is running.
- **Game-window-only screenshots** – Use `FindWindow` + `GetWindowRect` for the Deadlock window and capture only that region (smaller files, more relevant evidence). Already noted in ROADMAP.
- **Screenshot format** – Consider PNG (e.g. via WIC) instead of BMP to cut size and upload time while keeping quality good enough for review.
- **Optional suspicion hint** – From keylog timestamps, compute simple stats (e.g. variance of inter-key intervals). Very low variance could be noted in the report as “possible macro” for human review.

---

## Performance & UX

- **Upload in background** – Run `UploadSessionToDiscord` on a separate thread so the app doesn’t block at F12. e.g. “Uploading…” then exit after a short delay, or wait for thread finish with a max wait (e.g. 30 s).
- **Screenshot interval** – 5 s is good; for long matches you could make it configurable (e.g. 30 s) to reduce disk and upload size if you don’t need high frequency.

---

## Operational & identity

- **Player/session ID** – Optional `player_id.txt` (or `session_id.txt`) in the exe folder: one line = identifier (Discord ID, tournament tag, etc.). Include it in the webhook message (e.g. “Player: XYZ – UrnIt session part 1”) so you know whose report is whose without opening files.
- **Webhook per channel** – Use one webhook per tournament or tier so reports land in the right Discord channel.

---

## Security & privacy

- **Webhook URL** – Keep `webhook.txt` out of repo and builds (already in .gitignore). For distribution, document “staff places webhook.txt next to exe” so players never see the URL.
- **Report contents** – Document what’s collected (username, OS, CPU, processes, key timings, screenshots) and that it’s only used for anticheat review.

---

## Code quality (optional)

- **Magic numbers** – Replace with named constants (e.g. `TASK_SCAN_INTERVAL_SEC`, `SCREENSHOT_INTERVAL_SEC`, `MAX_UPLOAD_FILE_MB`, `WEBHOOK_BATCH_SIZE`).
- **Flow** – Consider refactoring the main loop and `ReportConclusion` into a `run_session()` style function instead of labels/gotos for readability.
- **GPU / monitor** – Fill the empty GPU and monitor info blocks (e.g. DXGI or WMI) so hardware context in the report is complete.

---

## Quick wins already done
- CPU first-sample fix.
- Discord rate-limit sleep between batches.
- WinHTTP timeouts.
- Version line in report.

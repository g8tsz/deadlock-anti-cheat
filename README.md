# Deadlock AC (UrnIt Anticheat)

Anticheat client for **Deadlock**: logs tasks, screenshots (game window), key input (only when Deadlock is focused), and hardware info, then **uploads the session to your Discord** when the player presses **F12** to end the session.

## How it works

- **Run** the .exe next to the game (or on the same PC). It creates a timestamped folder and writes:
  - `REPORT.TXT` – OS, CPU, session summary, cheat/performance flags
  - `TASK.TXT` – process list (name, PID, session)
  - `KEY_LOG.TXT` – key down/up with timestamps (only while the "Deadlock" window is focused)
  - `*.bmp` – screenshots (game window when found, else full screen) every 5 seconds
- **End session**: player presses **F12**. The client uploads all of the above to your Discord channel via webhook, then exits.

No manual file upload: everything is sent automatically to **your** Discord.

## Setup (so uploads go “here” — your Discord)

1. **Build** the project (Visual Studio; open `UrnItAnticheat-main\UrnItAnticheat\UrnItAnticheat.sln`).
2. **Discord webhook** (required for upload):
   - In Discord: Channel → Integrations → Webhooks → New Webhook. Copy the webhook URL.
   - Next to the built `.exe`, create `webhook.txt` with **one line**: that URL.
   - See `UrnItAnticheat-main\UrnItAnticheat\webhook.txt.example`.
3. **Player ID** (optional): create `player_id.txt` next to the .exe with one line (e.g. tournament tag or Discord ID). This is included in report and Discord messages so you know whose session it is.
4. **Cheat/performance lists**: edit `all_programs_list` in `UrnItAnticheat.cpp`: after `"cheats"` add process names to flag (e.g. `"cheat.exe"`), after `"performance"` add tools (e.g. `"msi afterburner.exe"`). Names are case-insensitive.

## Config (in code)

In `UrnItAnticheat.cpp`, `Config::`:

- `TASK_SCAN_INTERVAL_SEC` – process list interval (default 3 s)
- `SCREENSHOT_INTERVAL_SEC` – screenshot interval (default 5 s)
- `KEYLOG_INTERVAL_SEC` – key sampling interval (default 0.05 s)
- `WEBHOOK_BATCH_SIZE`, `WEBHOOK_RATE_LIMIT_MS`, `UPLOAD_TIMEOUT_MS` – Discord upload behavior

## “Upload it all to here”

- **Anticheat → Discord**: With `webhook.txt` set, F12 uploads the session (REPORT, TASK, KEY_LOG, screenshots) to the Discord channel that owns the webhook. That’s “upload to here” for the logs.
- **This repo**: To publish the code “here” (e.g. GitHub), clone or push this folder to your repo. Do **not** commit `webhook.txt` (keep it only on the machine where you build/distribute the exe).

## Summary

- Intervals use **seconds** (task scan 3 s, screenshots 5 s, keylog 50 ms).
- Keylog and game-window screenshots only when the **Deadlock** window is focused.
- Session ends with **F12**; upload to Discord is automatic; optional player ID and cheat/performance lists as above.

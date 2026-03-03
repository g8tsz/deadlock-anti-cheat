# Deadlock AC (UrnIt Anticheat)

Anticheat client for **Deadlock**: logs tasks, PNG screenshots (game window), key input (only when Deadlock is focused), and hardware info (OS, CPU, GPU), then **uploads the session to your Discord** when the player ends the session (automatically on game exit or manually with **F12**). Supports a **config file** and **cheat list from file** (including a script to scrape current cheats from the Deadlock trading forum), **macro/bot hint** in the report, and optional **session folder cleanup** after upload.

## Requirements

- **Windows** 10/11 (x64)
- **Visual Studio 2022** (or 2019) with C++ desktop workload and **Windows 10/11 SDK**
- Build for **x64** (Debug or Release); the project is configured for x64

## How it works

- **Run** the .exe next to the game (or on the same PC). It creates a timestamped folder and writes:
  - `REPORT.TXT` – OS, CPU, **GPU**, session summary, cheat/performance flags, optional **"Possible macro/bot"** line (when key interval variance is very low), and Discord upload status
  - `TASK.TXT` – process list (name, PID, session)
  - `KEY_LOG.TXT` – key down/up with timestamps (only while the "Deadlock" window is focused)
  - `*.png` – screenshots (game window when found, else full screen) every 5 seconds (PNG for smaller size and faster upload)
- **End session** (automatic or manual):
  - **Automatic**: When the Deadlock process exits (player closes the game), the client writes the session summary, uploads to Discord in the **background** (console shows "Uploading…"), and exits. No F12 needed.
  - **Manual**: Player can still press **F12** anytime to end the session early and upload.
- **Optional**: If `config.txt` has `CLEANUP_AFTER_UPLOAD=1`, the session folder is deleted after a successful upload so no local copy remains.

No manual file upload: everything is sent automatically to **your** Discord.

## Setup

1. **Clone** the repo and open `UrnItAnticheat-main\UrnItAnticheat\UrnItAnticheat.sln` in Visual Studio. Select **x64** (Debug or Release) and build. The `.exe` is in `UrnItAnticheat-main\UrnItAnticheat\x64\Debug\` or `...\x64\Release\`.

2. **Place these files next to the built `.exe`** (same folder as the exe):

   | File | Required? | Description |
   |------|-----------|-------------|
   | `webhook.txt` | **Yes** (for upload) | One line: your Discord webhook URL. See `webhook.txt.example`. |
   | `player_id.txt` | No | One line: tournament tag or Discord ID; included in report and Discord messages. |
   | `config.txt` | No | Overrides intervals and options (see **Config** below). Copy from `config.txt.example`. |
   | `cheat_list.txt` | No | List of process names to flag as cheat/performance. If missing, built-in list in code is used. See **Cheat list** below. |

3. **Discord webhook**: In Discord: Channel → Integrations → Webhooks → New Webhook. Copy the URL into `webhook.txt`.

4. **Cheat list** (optional): Format of `cheat_list.txt`: first line `cheats`, then one process name per line (e.g. `syntheticskill.exe`), then line `performance`, then tool names. Lines starting with `#` are ignored. To **generate a list from current Deadlock cheats**, run:
   ```bash
   python UrnItAnticheat-main/scripts/scrape_deadlock_cheats.py
   ```
   This scrapes the [elitepvpers Deadlock trading](https://www.elitepvpers.com/forum/deadlock-trading/) forum and writes `UrnItAnticheat-main/UrnItAnticheat/cheat_list.txt`. Copy that file next to the exe (or use `--output` to write directly to the exe folder). If `cheat_list.txt` is missing, the built-in list in code is used.

## Config (config.txt)

If `config.txt` is present next to the exe, these keys are loaded (one per line, `KEY=value`); otherwise defaults apply. Copy `config.txt.example` and edit.

| Key | Default | Description |
|-----|---------|-------------|
| `TASK_SCAN_INTERVAL_SEC` | 3 | Seconds between process list scans. |
| `SCREENSHOT_INTERVAL_SEC` | 5 | Seconds between PNG screenshots. |
| `KEYLOG_INTERVAL_SEC` | 0.05 | Key sampling interval (seconds). |
| `LOOP_SLEEP_MS` | 20 | Main loop sleep (ms). |
| `AUTO_UPLOAD_ON_GAME_EXIT` | 1 | If 1/true/yes, session ends and uploads when Deadlock process exits; else F12 only. |
| `UPLOAD_WAIT_TIMEOUT_SEC` | 30 | Max seconds to wait for Discord upload (upload runs in background; console shows "Uploading…"). |
| `CLEANUP_AFTER_UPLOAD` | 0 | If 1/true/yes, delete the session folder after a successful upload. |
| `MACRO_VARIANCE_THRESHOLD_MS2` | 500 | If key interval variance (ms²) is below this, report adds "Possible macro/bot" for human review. |

The report includes **GPU** (via DXGI) and, when key timings show very low variance, a **macro/bot hint** line.

## Upload to Discord

With `webhook.txt` set, ending the session (game exit or F12) uploads REPORT, TASK, KEY_LOG, and PNG screenshots to the Discord channel. Upload runs in the background (max wait from config). The report gets a final line: Discord upload completed, failed, or timed out. Do **not** commit `webhook.txt`, `config.txt`, or `cheat_list.txt`.

## Releases

No pre-built releases yet. Build from source (see **Setup**). When releases are published, they will appear at [Releases](https://github.com/lorddummy/deadlock-anti-cheat/releases). To create a release: **Releases → Create a new release**, choose a tag (e.g. `v1.0`), add notes, attach the built `UrnItAnticheat.exe` from `x64\Release\` or `x64\Debug\`. Do not include `webhook.txt`.

## Privacy / data collected

The client collects and sends to your Discord: Windows username, OS version, CPU and **GPU** info, process list, key timings (only while the Deadlock window is focused), and PNG screenshots (game window or full screen). The report may include a **"Possible macro/bot"** line when key interval variance is very low. Use only for anticheat review; inform players what is collected.

## Tips for staff

- Use a **private** Discord channel for the webhook so only staff see reports.
- Use one webhook per tournament or tier so reports are easy to sort.
- Some antivirus may flag the .exe (keyboard/screenshot behavior); players may need to allow or whitelist it.

## Summary

- **Config** and **cheat list** load from `config.txt` and `cheat_list.txt` next to the exe (optional); use the Python scraper to build the cheat list from the Deadlock trading forum.
- Intervals use **seconds** (tunable via config: task scan, screenshots, keylog).
- Keylog and game-window screenshots only when the **Deadlock** window is focused.
- **PNG** screenshots; **GPU** in report; **macro/bot hint** when key variance is very low.
- Session ends when the **game exits** (auto-upload) or when the player presses **F12**; upload runs in the **background**; optional **session folder cleanup** after successful upload.

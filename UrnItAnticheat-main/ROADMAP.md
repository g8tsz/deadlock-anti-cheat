# UrnIt Anticheat – Roadmap & Hurdles

## Current state (from `UrnItAnticheat.cpp`)

| Feature | Status | Notes |
|--------|--------|--------|
| **Screenshots** | ✅ Working | Full desktop BMP every 5s to timestamped folder |
| **Task list** | ✅ Working | `WTSEnumerateProcesses` → process name, PID, SessionID to TASK.TXT |
| **PC/Hardware** | ✅ Mostly done | OS user/version, CPU (brand, cores, vendor, cache, microarch). GPU/Monitor blocks empty |
| **Keylogger** | ❌ Stub only | KEY_LOG.TXT created, F12 only used to exit – no keys logged |
| **Discord/Steam** | ❌ Stubs | Placeholder `report_str += "\n";` only |
| **Cheat list** | ⚠️ Empty | `all_programs_list` only has `"cheats"` and `"performance"` – no actual exe names to match |
| **Output** | Local only | All output to local timestamped folder – no upload |

---

## 1. Legible, non‑intrusive keylogger

**Goal:** Log key events so reviewers can see input patterns (e.g. human vs macro/script), without hurting FPS or feeling invasive.

**Options:**

- **Polling with `GetAsyncKeyState`**  
  - In the main loop, sample only “interesting” keys (e.g. alphanumeric, space, common game keys).  
  - Write to `KEY_LOG.TXT` in a readable form, e.g. `[A][B][Space][Enter]` or `[KeyDown:0x41][KeyUp:0x41]` with optional timestamps.  
  - Pros: simple, no extra threads. Cons: can miss very fast keypresses; need to avoid double-counting (track previous state and only log transitions).

- **Low-level hook (`SetWindowsHookEx(WH_KEYBOARD_LL)`)**  
  - Log on key down/up with virtual key code (and optionally character).  
  - Pros: captures every key. Cons: more code, must run message loop or use a dedicated thread; some antivirus may flag it.

**Recommendation:** Start with **GetAsyncKeyState polling** in the existing loop:  
- Only log key **down** transitions (not every frame).  
- Limit to a small set (e.g. A–Z, 0–9, Space, Enter, mouse buttons if needed).  
- Format: one line per key event with optional timestamp, e.g. `[12:34:56] Key: A` so logs stay legible and small.

**Non‑intrusive:**  
- Sample keys at a fixed interval (e.g. every 50–100 ms) instead of every frame.  
- Write to file in small batches (e.g. buffer 64–256 chars and flush) to avoid I/O spikes.

---

## 2. Usable over the internet → Discord bot (no manual file turn‑in)

**Goal:** Send screenshots, keylog, task list, and report data to a Discord bot so staff don’t rely on players uploading files.

**Options:**

- **Discord webhooks (simplest)**  
  - One webhook URL per “report” or per tournament.  
  - Client does HTTP POST (e.g. `WinHTTP` or `libcurl`):  
    - Report text (and optionally keylog/task summary) in message content or embeds.  
    - Screenshots as file attachments (Discord allows multipart/form-data).  
  - Pros: no bot process; easy to add from C++. Cons: webhook URL is a secret; rate limits; no slash commands.

- **Discord bot with HTTP API**  
  - Your server (or a small service) runs a bot.  
  - Client sends HTTP POST to your server with report + files; server forwards to Discord (e.g. channel or DM).  
  - Pros: one place to validate, rate-limit, and store; can add auth (e.g. token per player). Cons: you need a backend.

**Implementation outline (client side):**

- Add a “upload” step (e.g. at `ReportConclusion` or on a timer):  
  - Pack: REPORT.TXT, KEY_LOG.TXT, TASK.TXT + screenshot BMPs (or PNGs) from the session.  
- Use **WinHTTP** (Windows API) or **libcurl** to POST multipart/form-data to:  
  - A Discord webhook URL, or  
  - Your own backend that then talks to Discord.  
- Optional: compress (e.g. ZIP) before upload to reduce size and number of requests.

**Security:**  
- Don’t hardcode webhook/API URL in the binary; use config file or env var that only your build/deploy has.  
- Prefer HTTPS and, if you have a backend, a short-lived token per session.

---

## 3. MOSS equivalent

**MOSS (Multiple Output Screenshot System)** in esports = periodic screenshots (e.g. during a match) for anti-cheat review. You already have the core: **scheduled screenshots every 5 seconds**.

To make it “MOSS-like” in behavior and legibility:

- **Keep periodic capture** (e.g. every 30–60 s for MOSS-style, or keep 5 s for stricter leagues).  
- **Option: game window only**  
  - Use `FindWindow` / `GetWindowRect` for Deadlock’s window and capture that region instead of full desktop (smaller files, less noise).  
- **Format:**  
  - Consider **PNG** (e.g. via WIC or a small library) to reduce size vs BMP for upload and storage.  
- **Naming/metadata:**  
  - Filename or report line: timestamp + “Screenshot N” so reviewers and your Discord bot can order them.  
- **Tie to session:**  
  - Same timestamped folder and report block (“BEGINNING GAME LOGGING” … “ENDING GAME LOGGING”) so one “run” = one set of screenshots + logs.

So: your current screenshot loop **is** the MOSS equivalent; the main improvements are optional game-window capture, PNG, and clear naming + upload (see hurdle 2).

---

## Suggested order of work

1. **Keylogger (legible, low impact)**  
   - Implement GetAsyncKeyState-based logging to KEY_LOG.TXT (transition-based, limited key set, batched writes).  
   - Then you have something meaningful to send to Discord.

2. **Discord (or your backend) upload**  
   - Add WinHTTP (or curl) upload at end of session: report + keylog + task + screenshots to webhook or your API.  
   - Keeps “no file turn-in” and makes the MOSS-style screens useful remotely.

3. **MOSS refinements**  
   - Optional: game-window-only capture, PNG, and interval/naming tweaks.

4. **Cheat list**  
   - Fill `all_programs_list` with known cheat/overlay process names (e.g. from community or your own list) so task scanning actually flags them.

If you tell me which hurdle you want to tackle first (keylogger, Discord upload, or MOSS tweaks), I can outline or write the exact code changes in `UrnItAnticheat.cpp` and any new files (e.g. `upload.cpp` / `keylog.cpp`) next.

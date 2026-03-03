# Known issues and limitations

## Fixed in this pass
- **Task manager loop** – Loop variable was `static`, so after the first run the loop never ran again (or skipped). Changed to normal `DWORD i`.
- **Flagged programs duplicated** – Same process was pushed every 3 s, so summary showed "cheat.exe cheat.exe …". Now we only add if not already in the list.
- **Null process name** – `pProcessName` could be NULL; we now skip that process instead of undefined behavior.
- **Invalid log file handles** – If CreateDirectory or CreateFile failed, we could flush/write to invalid handles. Handles are now initialized and ReportConclusion checks before use.
- **Redundant static in task scan** – Cleaned up so `wpi_ptr`/`dwProcCount` are not static and shadowing.

## Fixed (third pass)
- **OS version** – Now read from registry (`CurrentBuild`, `DisplayVersion`) so Win10/11 report accurate build and release (e.g. "build 19045 (22H2)").

## Still known (low priority)
- **Non-x64** – CPU block is `#ifdef CPU_FEATURES_ARCH_X86_64`; on 32-bit or ARM the report gets no CPU details.
- **Wide-char process names** – `ConvertWideToString` can throw on invalid UTF-16 in process names; rare.
- **File handles** – Log file handles are never explicitly closed; they close on process exit. Fine for this app.

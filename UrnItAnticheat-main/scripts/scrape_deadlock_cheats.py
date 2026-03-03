#!/usr/bin/env python3
"""
Scrape Deadlock cheat names from elitepvpers forum and write cheat_list.txt
for use with the anticheat. Run from repo root or pass --output path.
Usage: python scrape_deadlock_cheats.py [--output path/to/cheat_list.txt]
"""
import re
import sys
import argparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# Target: https://www.elitepvpers.com/forum/deadlock-trading/
URL = "https://www.elitepvpers.com/forum/deadlock-trading/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Map known product names from thread titles to plausible process names (.exe).
# Thread titles look like "[Selling][Synthetic Skill - Deadlock |External|...]"
# We extract the first part and convert to exe name, or use this map for known ones.
KNOWN_MAPPING = {
    "synthetic skill": "syntheticskill.exe",
    "foxyz": "foxyz.exe",
    "eshub": "eshub.exe",
    "coconut": "coconut.exe",
    "medusa": "medusa.exe",
    "predator": "predator.exe",
    "umbrella": "umbrella.exe",
    "deadlockml": "deadlockml.exe",
    "phoenix": "phoenix.exe",
    "storm": "storm.exe",
    "obstruct": "obstruct.exe",
    "pussycat": "pussycat.exe",
    "mason": "mason.exe",
    "byster": "byster.exe",
    "belltower": "belltower.exe",
    "spyderrz": "spyderrz.exe",
    "unlockcheat": "unlockcheat.exe",
    "dmaperk": "dmaperk.exe",
    "cocon": "cocon.exe",
    "medus": "medus.exe",
    "yyhacks": "yyhacks.exe",
    "dexaim": "dexaimdma.exe",
}


def slug_to_exe(slug: str) -> str:
    """Turn a product slug into a plausible .exe name."""
    s = re.sub(r"[^a-z0-9]", "", slug.lower())
    if not s:
        return ""
    return s + ".exe"


def extract_cheat_names(html: str) -> set:
    """Parse forum listing HTML for thread titles and extract cheat/product names."""
    names = set()
    # Thread titles: [Selling][Product Name - Deadlock |...] or [Selling][Product Name ...]
    for m in re.finditer(r"\[Selling\]\s*\[([^\]]+?)(?:\s*[-|]\s*|\])", html, re.IGNORECASE):
        title_part = m.group(1).strip()
        # Strip trailing "Deadlock" and common suffixes
        title_part = re.sub(r"\s*-\s*Deadlock.*$", "", title_part, flags=re.IGNORECASE)
        # First meaningful token(s): "Synthetic Skill" -> syntheticskill, "FOXYZ.NET" -> foxyz
        parts = re.split(r"[\s\-–—|]+", title_part)
        first = parts[0] if parts else ""
        first = re.sub(r"\.(net|com|xyz|org)$", "", first, flags=re.IGNORECASE)
        slug = first.lower().replace(" ", "").replace(".", "")
        if len(slug) >= 2 and slug not in ("deadlock", "selling", "buy", "cheat", "hack"):
            names.add(slug)
    for name in re.findall(r"(?i)(synthetic\s*skill|foxyz|coconut|medusa|predator|umbrella|deadlock\s*ml|phoenix|storm|obstruct|pussycat|mason|belltower|spyderrz|dma\s*perk|eshub|dmaperk)", html):
        names.add(name.lower().replace(" ", ""))
    return names


def main():
    ap = argparse.ArgumentParser(description="Scrape Deadlock cheats from elitepvpers and write cheat_list.txt")
    ap.add_argument("--output", "-o", default=None, help="Output path for cheat_list.txt")
    args = ap.parse_args()

    out_path = args.output
    if not out_path:
        # Default: next to script's repo, UrnItAnticheat/cheat_list.txt
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.dirname(script_dir)
        out_path = os.path.join(repo_root, "UrnItAnticheat", "cheat_list.txt")

    print("Fetching", URL, "...")
    req = Request(URL, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError, OSError) as e:
        print("Error fetching page:", e, file=sys.stderr)
        sys.exit(1)

    names = extract_cheat_names(html)
    exes = set()
    for n in names:
        if n in KNOWN_MAPPING:
            exes.add(KNOWN_MAPPING[n])
        else:
            exe = slug_to_exe(n)
            if exe:
                exes.add(exe)

    lines = ["cheats"] + sorted(exes) + ["performance", "# msi afterburner.exe"]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Wrote", len(exes), "entries to", out_path)


if __name__ == "__main__":
    main()

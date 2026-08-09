"""
collect_activity_files.py
─────────────────────────
Searches all sub-folders of the folder this script sits in and copies
three types of files into a new folder called all_activities_files:

  generate_graphs_*.py
  practice_set_*_2.html
  practice_set_*_3.html

INSTRUCTIONS
─────────────
  1. Set DRY_RUN = True to preview, False to actually copy.
  2. Click Run.
"""

import shutil
from pathlib import Path

# ── SETTINGS ──────────────────────────────────────────────────────────────────

DRY_RUN = False   # ← Change to False when you're ready to copy

# ──────────────────────────────────────────────────────────────────────────────

ROOT   = Path(__file__).parent
DEST   = ROOT / "all_activities_files"

PATTERNS = [
    "generate_graphs_*.py",
    "practice_set_*_2.html",
    "practice_set_*_3.html",
]

def collect(root: Path, dest: Path, dry_run: bool) -> None:
    # Gather all matching files
    matches = []
    for pattern in PATTERNS:
        matches.extend(root.rglob(pattern))

    # Skip anything already inside the destination folder
    matches = sorted(f for f in matches if dest not in f.parents)

    if not matches:
        print("No matching files found.")
        return

    mode_label = "[DRY RUN]" if dry_run else "[COPIED ]"
    ok = skipped = 0

    if not dry_run:
        dest.mkdir(exist_ok=True)

    for src in matches:
        dst = dest / src.name

        if dst.exists():
            print(f"[SKIP   ] {src.name}  ← already exists in destination")
            skipped += 1
            continue

        print(f"{mode_label} {src.name}  ←  {src.parent.name}/")

        if not dry_run:
            shutil.copy2(src, dst)

        ok += 1

    print()
    print(f"{'Would copy' if dry_run else 'Copied'}: {ok}   Skipped: {skipped}")
    if dry_run:
        print(f"\nLooks good? Set DRY_RUN = False and click Run again.")
    else:
        print(f"\nFiles saved to: {dest}")


# ── run ───────────────────────────────────────────────────────────────────────

print("=" * 60)
print(f"  Root : {ROOT}")
print(f"  Dest : {DEST}")
print(f"  Mode : {'DRY RUN (preview)' if DRY_RUN else 'LIVE — copying files'}")
print("=" * 60)
print()

collect(ROOT, DEST, DRY_RUN)

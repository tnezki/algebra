"""
rename_generate_graphs.py
─────────────────────────
Renames every generate_graphs.py found in sub-folders by appending
the unit/section suffix extracted from the folder name.

  practice_sets_4_3/generate_graphs.py  →  practice_sets_4_3/generate_graphs_4_3.py
  notes_1_2/generate_graphs.py          →  notes_1_2/generate_graphs_1_2.py
  warmups_0A_1/generate_graphs.py       →  warmups_0A_1/generate_graphs_0A_1.py

Usage
─────
  python rename_generate_graphs.py                   # dry-run from current folder
  python rename_generate_graphs.py path/to/root      # dry-run from a specific root
  python rename_generate_graphs.py --run             # actually rename (current folder)
  python rename_generate_graphs.py path/to/root --run  # actually rename (specific root)

The suffix is the LAST TWO underscore-separated tokens of the parent folder name.
"""

import os
import sys
from pathlib import Path


# ── helpers ──────────────────────────────────────────────────────────────────

def extract_suffix(folder_name: str) -> str | None:
    """
    Pull the unit_section suffix out of a folder name.

    'practice_sets_4_3'  →  '4_3'
    'notes_0A_1'         →  '0A_1'
    'warmups_4_3'        →  '4_3'

    Returns None if the folder name has fewer than two underscore-separated parts.
    """
    parts = folder_name.split("_")
    if len(parts) < 2:
        return None
    return "_".join(parts[-2:])


def find_and_rename(root: Path, dry_run: bool) -> None:
    """Walk root recursively, find every generate_graphs.py, and rename it."""

    targets = sorted(root.rglob("generate_graphs.py"))

    if not targets:
        print("No generate_graphs.py files found under:", root.resolve())
        return

    mode_label = "[DRY RUN]" if dry_run else "[RENAME ]"
    ok = skipped = 0

    for src in targets:
        folder_name = src.parent.name
        suffix = extract_suffix(folder_name)

        if suffix is None:
            print(f"[SKIP   ] {src}  ← can't parse suffix from folder '{folder_name}'")
            skipped += 1
            continue

        new_name = f"generate_graphs_{suffix}.py"
        dst = src.parent / new_name

        if dst.exists():
            print(f"[SKIP   ] {src}  ← destination already exists: {dst.name}")
            skipped += 1
            continue

        print(f"{mode_label} {src}  →  {dst.name}")

        if not dry_run:
            src.rename(dst)

        ok += 1

    # ── summary ──
    print()
    print(f"{'Would rename' if dry_run else 'Renamed'}: {ok}   Skipped: {skipped}")
    if dry_run:
        print("Run with --run to apply changes.")


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    dry_run = "--run" not in args
    positional = [a for a in args if not a.startswith("--")]

    root = Path(positional[0]) if positional else Path(".")

    if not root.is_dir():
        print(f"ERROR: '{root}' is not a directory.")
        sys.exit(1)

    print("=" * 60)
    print(f"  Root   : {root.resolve()}")
    print(f"  Mode   : {'DRY RUN (preview)' if dry_run else 'LIVE — files will be renamed'}")
    print("=" * 60)
    print()

    find_and_rename(root, dry_run)

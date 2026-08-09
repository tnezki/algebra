"""
rename_generate_graphs.py
─────────────────────────
Renames every generate_graphs.py found in sub-folders by appending
the unit/section suffix extracted from the folder name.

  practice_sets_4_3/generate_graphs.py  →  generate_graphs_4_3.py
  notes_1_2/generate_graphs.py          →  generate_graphs_1_2.py
  warmups_0A_1/generate_graphs.py       →  generate_graphs_0A_1.py

INSTRUCTIONS
─────────────
  1. Set ROOT to the folder that contains all your sub-folders.
  2. Set DRY_RUN = True to preview, False to actually rename.
  3. Click Run.
"""

from pathlib import Path

# ── SETTINGS ──────────────────────────────────────────────────────────────────

ROOT    = Path(__file__).parent   # folder to search inside
DRY_RUN = False   # ← Change to False when you're ready to rename

# ──────────────────────────────────────────────────────────────────────────────


def extract_suffix(folder_name: str) -> str | None:
    parts = folder_name.split("_")
    if len(parts) < 2:
        return None
    return "_".join(parts[-2:])


def find_and_rename(root: Path, dry_run: bool) -> None:
    targets = sorted(root.rglob("generate_graphs.py"))

    if not targets:
        print("No generate_graphs.py files found under:", root.resolve())
        return

    mode_label = "[DRY RUN]" if dry_run else "[RENAMED]"
    ok = skipped = 0

    for src in targets:
        folder_name = src.parent.name
        suffix = extract_suffix(folder_name)

        if suffix is None:
            print(f"[SKIP   ] {src}  ← can't parse suffix from '{folder_name}'")
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

    print()
    print(f"{'Would rename' if dry_run else 'Renamed'}: {ok}   Skipped: {skipped}")
    if dry_run:
        print("\nLooks good? Set DRY_RUN = False and click Run again.")


# ── run ───────────────────────────────────────────────────────────────────────

root = Path(ROOT)

if not root.is_dir():
    print(f"ERROR: '{ROOT}' is not a directory. Check the ROOT path above.")
else:
    print("=" * 60)
    print(f"  Root : {root.resolve()}")
    print(f"  Mode : {'DRY RUN (preview)' if DRY_RUN else 'LIVE — renaming files'}")
    print("=" * 60)
    print()
    find_and_rename(root, DRY_RUN)

# database_updater/main.py
# run this module with "python -m database_updater.main"
from __future__ import annotations

import argparse
import sys
from importlib import import_module
from typing import Iterable, Tuple, Set

from tqdm import tqdm

# ---------------------------------------------------------------------------
# Pipeline configuration
# ---------------------------------------------------------------------------

STEP_MODULES: Tuple[Tuple[str, str, str], ...] = (
    ("Step 1: TSV → Parquet", "database_updater.step1_tsv_to_parquet", "run_step1"),
    ("Step 2: Merge Financial Statements", "database_updater.step2_merge_fs", "run_step2"),
    ("Step 3: Update Ticker Info", "database_updater.step3_update_ticker_info", "run_step3"),
    ("Step 4: Split FS by SIC & CIK", "database_updater.step4_split_and_classify_fs", "run_step4"),
    ("Step 5: Build Ticker Mapper", "database_updater.step5_update_mapper", "run_step5"),
    ("Step 6: Extract Tags & Segments", "database_updater.step6_update_tag_segments", "run_step6"),
)

DEFAULT_MAX_WORKERS: int = 8  # 💡 Apple M‑프로 칩 기준 권장값


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _iter_requested_steps(indices: Set[int] | None) -> Iterable[Tuple[int, str, callable]]:
    """Yield (ordinal, description, function) for the selected steps."""
    for idx, (desc, mod_path, fn_name) in enumerate(STEP_MODULES, start=1):
        if indices and idx not in indices:
            continue
        mod = import_module(mod_path)
        func = getattr(mod, fn_name)
        yield idx, desc, func


def _run_steps(max_workers: int, selected: Set[int] | None) -> None:
    print("\n📦  Starting database‑update pipeline…")
    steps = list(_iter_requested_steps(selected))
    for idx, desc, func in tqdm(
        steps, desc="📊  Pipeline Progress", unit="step", ncols=110, colour=None
    ):
        print(f"\n▶ ({idx}/{len(STEP_MODULES)}) {desc}")
        try:
            if "max_workers" in func.__code__.co_varnames:
                func(max_workers=max_workers)
            else:
                func()
            print(f"✅  Finished {desc}")
        except Exception as exc:
            print(f"❌  Error in {desc}: {exc}")

    print("\n🎉  Pipeline complete!\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str]) -> Tuple[int, Set[int]]:
    parser = argparse.ArgumentParser(
        prog="database_updater",
        description="Run the SEC financial‑statement ETL pipeline end‑to‑end.",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=DEFAULT_MAX_WORKERS,
        help=f"Parallel workers for supported steps (default: {DEFAULT_MAX_WORKERS})",
    )
    parser.add_argument(
        "-s",
        "--steps",
        type=str,
        metavar="LIST",
        help="Comma‑separated list or range of steps to run (e.g. '1,3-5'). If omitted, all steps run.",
    )
    ns = parser.parse_args(argv)

    # Parse the step selection string ➜ set[int]
    selected: Set[int] = set()
    if ns.steps:
        for part in ns.steps.split(","):
            if "-" in part:
                a, b = map(int, part.split("-", 1))
                selected.update(range(a, b + 1))
            else:
                selected.add(int(part))
    return ns.workers, selected


def main(argv: list[str] | None = None) -> None:
    workers, selected_steps = _parse_args(argv or sys.argv[1:])
    _run_steps(max_workers=workers, selected=selected_steps)


if __name__ == "__main__":
    main()

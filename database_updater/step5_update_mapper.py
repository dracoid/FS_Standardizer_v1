# database_updater/step5_update_mapper.py
"""
Step 5 ― Build/update **ticker_mapper.parquet**
==============================================
Maps every available ticker → CIK → SIC/office/industry title → 재무제표
폴더 경로.

• 직접 실행:  `python -m database_updater.step5_update_mapper`
• 파이프라인: `database_updater.main` 내에서 `run_step5()` 호출
"""

from __future__ import annotations

import json
import os
from glob import glob
from typing import List, Optional

import pandas as pd

# ---------------------------------------------------------------------------
# Constants (project‑specific paths)
# ---------------------------------------------------------------------------

SIC_PATH = (
    "/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/sic_table.xlsx"
)
JSON_PATH = (
    "/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/"
    "company_tickers_exchange.json"
)
FS_DIRS = [
    "/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/month",
    "/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/quarter",
]
OUTPUT_PATH = (
    "/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/"
    "ticker_mapper.parquet"
)
PATH_COL = "FS_Path"  # downstream scripts use this column name

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _collect_cik_to_sic(fs_dirs: List[str]) -> dict[int, int]:
    """Scan merged‑FS parquet files and build {cik: sic} mapping."""

    cik_to_sic: dict[int, int] = {}
    parquet_files = [fp for d in fs_dirs for fp in glob(os.path.join(d, "*.parquet"))]

    for fp in parquet_files:
        try:
            tmp = pd.read_parquet(fp, columns=["cik", "sic"]).dropna()
            for cik, sic in tmp[["cik", "sic"]].drop_duplicates().values:
                cik_to_sic[int(cik)] = int(sic)  # last‑write wins
        except Exception as exc:  # pragma: no cover  – I/O diagnostics only
            print(f"⚠️ {fp}: {exc}")

    return cik_to_sic


def _build_records(
    ticker_df: pd.DataFrame,
    sic_df: pd.DataFrame,
    cik_to_sic: dict[int, int],
) -> list[dict]:
    """Return list of mapping dicts – one per *ticker* (not per CIK)."""

    records: list[dict] = []

    for _, row in ticker_df.iterrows():
        ticker = row["ticker"].upper().strip()
        cik = int(row["cik"])
        name = row.get("name")
        exchange = row.get("exchange")

        sic = cik_to_sic.get(cik)
        if sic is None:
            continue  # no merged FS yet

        # Office & industry title lookup
        match = sic_df.loc[sic_df["sic"] == sic]
        if match.empty:
            office, ind_title = "[Unknown]", "[Unknown]"
        else:
            office = match.iloc[0]["Office"]
            ind_title = match.iloc[0]["Industry Title"]

        fs_path = (
            "/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/SIC_CIK/"
            f"{office}/{sic}_{ind_title}/{cik}"
        )

        records.append(
            {
                "ticker": ticker,
                "name": name,
                "cik": cik,
                "office": office,
                "Industry Title": ind_title,
                "exchange": exchange,
                PATH_COL: fs_path,
                "sic": sic,
            }
        )

    return records

# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_step5(
    *,
    sic_path: str = SIC_PATH,
    json_path: str = JSON_PATH,
    fs_paths: Optional[List[str]] = None,
    output_path: str = OUTPUT_PATH,
) -> None:
    """Generate *ticker_mapper.parquet*.

    Called from the main pipeline or executed directly. All arguments have
    sensible project‑specific defaults but can be overridden for testing.
    """

    # 1) Load supporting tables ------------------------------------------------
    sic_df = pd.read_excel(sic_path)
    with open(json_path, "r") as fh:
        json_data = json.load(fh)
    ticker_df = pd.DataFrame(json_data["data"], columns=json_data["fields"])
    ticker_df["ticker"] = ticker_df["ticker"].str.upper().str.strip()

    # 2) Map CIK → SIC from merged parquet files ------------------------------
    cik_to_sic = _collect_cik_to_sic(fs_paths or FS_DIRS)

    # 3) Build per‑ticker records --------------------------------------------
    records = _build_records(ticker_df, sic_df, cik_to_sic)

    # 4) Persist --------------------------------------------------------------
    pd.DataFrame(records).to_parquet(output_path, index=False)
    print(f"✅ Mapping saved → {output_path}  (총 {len(records)}건)")


# ---------------------------------------------------------------------------
# CLI shim
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_step5()

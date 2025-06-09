# FS_standardizer_CF/standardizer.py
"""
Cash-Flow Statement standardizer
────────────────────────────────
• stmt == "CF" 행만 추출
• classify_cashflow_entry → 4-tuple 매핑
• 매핑 실패 시에도 identifier 생성 + “99. Unclassified” 코드 입력
"""
from __future__ import annotations
import pandas as pd

from FS_standardizer_CF.tag_mapper import classify_cashflow_entry
from FS_standardizer_CF.utils.helper import clean_text


# ──────────────────────────────────────────────────────────────────────────
def _safe_classify(row: pd.Series, sic: int | None):
    """Wrapper that guarantees non-null identifier & default category."""
    cat, sub, ident, ilabel = classify_cashflow_entry(
        row.tag, row.segments, row.plabel, sic=sic
    )

    # ── identifier / label ― 항상 채우기
    seg = row.segments or "[Total]"
    pl  = row.plabel   or "[Unlabeled]"
    base_ident = f"[{seg}] | {pl}"
    ident  = ident  or base_ident
    ilabel = ilabel or f"{base_ident} | {clean_text(row.tag)}"

    # ── 매핑 실패 시 기본 코드
    if cat is None:
        cat = "99. Unclassified"
        sub = "000. Unclassified"

    return cat, sub, ident, ilabel


# ──────────────────────────────────────────────────────────────────────────
def standardize_cashflow(df: pd.DataFrame, *, sic: int | None = None) -> pd.DataFrame:
    """Return CF-only DataFrame with mapping columns attached."""
    cf = df[df["stmt"].str.upper() == "CF"].copy()
    if cf.empty:
        return cf

    cf[["category", "subcategory", "identifier", "identifier_label"]] = cf.apply(
        _safe_classify, axis=1, result_type="expand", sic=sic
    )
    cf["stmt"] = "CF"
    return cf


__all__ = ["standardize_cashflow"]
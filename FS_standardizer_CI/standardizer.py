"""
DataFrame → (category, subcategory, identifier, identifier_label) 컬럼 생성

사용법
>>> ci_df = standardize_comp_income(raw_df, default_sic=6020)
"""
from __future__ import annotations

import pandas as pd

from FS_standardizer_CI.tag_mapper import classify_ci_entry


def standardize_comp_income(df: pd.DataFrame, *, default_sic: int | None = None) -> pd.DataFrame:
    """df (전처리 완료) 에서 stmt ∈ {CI, COMPREH, OCI} 행만 정규화."""
    mask = df["stmt"].str.upper().isin({"CI", "COMPREH", "OCI"})
    ci_df = df[mask].copy()
    if ci_df.empty:
        return ci_df  # nothing to do

    ci_df[["category", "subcategory", "identifier", "identifier_label"]] = ci_df.apply(
        lambda r: classify_ci_entry(r["tag"], r["segments"], r.get("plabel"), sic=default_sic),
        axis=1,
        result_type="expand",
    )
    ci_df["stmt"] = "CI"
    return ci_df


__all__ = ["standardize_comp_income"]
"""DataFrame → EQ 표준화"""

import pandas as pd
from FS_standardizer_EQ.tag_mapper import classify_equity_entry

def standardize_equity(df: pd.DataFrame, *, default_sic: int | None = None) -> pd.DataFrame:
    """Input:  *raw merged FS df*   Output:  EQ 전용 표준화 DataFrame"""
    # SEC는 'EQ' 또는 'SE' 로 표기 → 모두 허용
    eq_mask = df["stmt"].str.upper().isin({"EQ", "SE"})
    eq_df   = df[eq_mask].copy()
    if eq_df.empty:
        return eq_df  # 그대로 빈 DF 반환

    eq_df[["category", "subcategory", "identifier", "identifier_label"]] = eq_df.apply(
        lambda r: classify_equity_entry(r["tag"], r["segments"], r["plabel"], sic=default_sic),
        axis=1,
        result_type="expand",
    )
    eq_df["stmt"] = "EQ"
    return eq_df
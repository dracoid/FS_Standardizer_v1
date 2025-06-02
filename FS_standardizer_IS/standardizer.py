# FS_standardizer_IS/standardizer.py

import pandas as pd
from FS_standardizer_IS.tag_mapper import classify_income_statement_entry

def standardize_income_statement(df: pd.DataFrame, default_sic=None) -> pd.DataFrame:
    """
    손익계산서(IS) 항목 분류 및 중복 제거까지 포함한 전처리 함수.

    Parameters:
    - df: 전처리된 재무제표 DataFrame (필수 컬럼: tag, segments, plabel, stmt, ddate_label_month 등)
    - default_sic: SIC 코드 누락 시 사용할 기본값

    Returns:
    - IS 항목만 필터링하여, 분류 결과를 포함한 정제된 DataFrame 반환
    """

    # ✅ IS 항목만 필터링
    df_is = df[df['stmt'].str.upper() == 'IS'].copy()

    # ✅ segments 공란은 "[Total]" 처리
    df_is["segments"] = df_is["segments"].fillna("[Total]")

    # ✅ IS 항목 분류
    df_is[["category", "subcategory", "identifier", "identifier_label"]] = df_is.apply(
        lambda row: pd.Series(
            classify_income_statement_entry(
                tag=row["tag"],
                segments=row["segments"],
                plabel=row.get("plabel"),
                stmt=row.get("stmt"),
                sic=row.get("sic") if pd.notnull(row.get("sic")) else default_sic
            )
        ),
        axis=1
    )

    # ✅ 분석에 필요한 컬럼만 선택
    columns_to_keep = [
        "adsh", "tag", "segments", "plabel", "stmt",
        "qtrs", "uom", "iprx", "value", "cik", "name", "sic", "form",
        "datatype", "iord", "crdr", "tlabel", "doc",
        "adsh_rank", "ddate_label_month",
        "category", "subcategory", "identifier", "identifier_label"
    ]
    df_is = df_is[[col for col in columns_to_keep if col in df_is.columns]]

    # ✅ 중복 제거 기준
    dedup_cols = [
        "stmt", "qtrs", "uom", "value", "cik", "name", "sic",
        "datatype", "iord", "crdr", "ddate_label_month",
        "category", "subcategory", "identifier_label"
    ]

    before = len(df_is)
    df_is = df_is.drop_duplicates(subset=dedup_cols, keep="first").reset_index(drop=True)
    after = len(df_is)
    print(f"🧹 IS Deduplication complete: {before - after} rows removed (from {before} to {after})")

    return df_is

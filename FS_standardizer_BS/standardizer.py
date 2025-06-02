# FS_standardizer_BS/standardizer.py
import pandas as pd
from .tag_mapper import classify_balance_sheet_entry
from .utils.helper import clean_plabel


def standardize_balance_sheet(df: pd.DataFrame, default_sic: str) -> pd.DataFrame:
    """
    대차대조표(BS) 항목 분류 및 중복 제거 포함 전처리 함수

    Parameters:
        df (pd.DataFrame): 전체 재무제표 데이터프레임 (필수 컬럼: tag, segments, plabel, stmt, sic 등)
        default_sic (str): SIC 코드 누락 시 사용할 기본값

    Returns:
        pd.DataFrame: BS 항목만 필터링 및 표준화 후 정제된 데이터프레임
    """
    # ✅ BS 항목만 필터링
    df_bs = df[df["stmt"].str.upper() == "BS"].copy()
    if df_bs.empty:
        print("⚠ No BS data found.")
        return pd.DataFrame(columns=df.columns.tolist() + ["category", "subcategory", "identifier", "identifier_label"])

    # ✅ segments 공란은 "[Total]" 처리
    df_bs["segments"] = df_bs["segments"].fillna("[Total]")

    # ✅ plabel 정제 → temp 컬럼 사용
    df_bs["temp_cleaned_plabel"] = df_bs["plabel"].apply(clean_plabel)

    # ✅ 항목 분류 (temp_cleaned_plabel 사용)
    df_bs[["category", "subcategory", "identifier", "identifier_label"]] = df_bs.apply(
        lambda row: pd.Series(
            classify_balance_sheet_entry(
                tag=row["tag"],
                segments=row["segments"],
                plabel=row["temp_cleaned_plabel"],
                stmt=row["stmt"],
                sic=row["sic"] if pd.notnull(row.get("sic")) else default_sic
            )
        ),
        axis=1
    )

    # ✅ 임시 컬럼 제거
    df_bs.drop(columns=["temp_cleaned_plabel"], inplace=True)

    # ✅ 분석에 필요한 컬럼만 선택
    columns_to_keep = [
        "adsh", "tag", "segments", "plabel", "stmt",
        "qtrs", "uom", "iprx", "value", "cik", "name", "sic", "form",
        "datatype", "iord", "crdr", "tlabel", "doc",
        "adsh_rank", "ddate_label_month",
        "category", "subcategory", "identifier", "identifier_label"
    ]
    df_bs = df_bs[[col for col in columns_to_keep if col in df_bs.columns]]

    # ✅ 중복 제거 기준
    dedup_cols = [
        "stmt", "qtrs", "uom", "value", "cik", "name", "sic",
        "datatype", "iord", "crdr", "ddate_label_month",
        "category", "subcategory", "identifier_label"
    ]
    before = len(df_bs)
    df_bs = df_bs.drop_duplicates(subset=dedup_cols, keep="first").reset_index(drop=True)
    after = len(df_bs)
    print(f"🧹 BS Deduplication complete: {before - after} rows removed (from {before} to {after})")

    return df_bs

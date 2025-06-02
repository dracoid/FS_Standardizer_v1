# FS_Deduplicator/preprocessor.py
import pandas as pd
from FS_Deduplicator.utils import _compute_adsh_rank, _normalize_tag, _normalize_segment
from FS_Deduplicator.deduplicator import remove_duplicates

def preprocess_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    재무제표 데이터 전처리 통합 함수.
    - value 컬럼 정제 및 0 제거
    - ddate, period 컬럼을 datetime 형식으로 변환
    - 중복 제거
    - ddate_label_month 파생 컬럼 생성
    """
    # ✅ value 전처리: 결측치 및 0 제거, 정수형 변환
    if 'value' in df.columns:
        df = df[df['value'].notna() & (df['value'] != 0)].copy()
        try:
            df['value'] = df['value'].astype(int)
        except Exception as e:
            print(f"⚠️ Error converting 'value' to int: {e}")

    # ✅ 날짜 컬럼 전처리: ddate, period
    for col in ['ddate', 'period']:
        if col in df.columns:
            df = df[df[col].notna()].copy()
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = pd.to_datetime(df[col].astype(float).astype(int).astype(str), format='%Y%m%d', errors='coerce')
                else:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                n_invalid = df[col].isna().sum()
                if n_invalid > 0:
                    print(f"⚠️ {col}: {n_invalid} rows could not be converted to datetime.")
            except Exception as e:
                print(f"⚠️ Error converting '{col}' to datetime: {e}")

    # ✅ 중복 제거
    df = remove_duplicates(df)

    # ✅ ddate_label_month 생성
    if 'ddate' in df.columns and pd.api.types.is_datetime64_any_dtype(df['ddate']):
        try:
            df['ddate_label_month'] = df['ddate'].dt.strftime('%yY%mM')
        except Exception as e:
            print(f"⚠️ Failed to generate 'ddate_label_month': {e}")

    return df
# FS_Deduplicator/utils.py

import pandas as pd

def _compute_adsh_rank(df: pd.DataFrame) -> pd.DataFrame:
    """
    adsh에서 연도 뒤의 일련번호를 추출해 adsh_rank 컬럼 생성
    예: '0001193125-14-303175' → 14303175 (14는 연도, 303175는 순번)
    """
    if 'adsh' in df.columns:
        try:
            df = df.copy()
            df['adsh_rank'] = df['adsh'].str[11:13] + df['adsh'].str[14:]
            df['adsh_rank'] = pd.to_numeric(df['adsh_rank'], errors='coerce')
        except Exception as e:
            print(f"❌ Error computing adsh_rank: {e}")
    return df

def _normalize_tag(s: str) -> str:
    """
    tag 정규화: 대문자 변환 + 공백 제거
    """
    return str(s).strip().upper().replace(" ", "")

def _normalize_segment(s: str) -> str:
    """
    segments 정규화: 소문자 변환 + 세미콜론/공백 제거
    """
    return str(s).strip().lower().replace(";", "").replace(" ", "")

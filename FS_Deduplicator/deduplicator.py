# FS_Deduplicator/deduplicator.py
import pandas as pd
from FS_Deduplicator.utils import _compute_adsh_rank, _normalize_tag, _normalize_segment

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    동일한 ddate, tag, segments, qtrs 조합에서
    adsh_rank가 가장 높은(가장 최신 보고서) 데이터만 남긴다.
    원본 tag/segments 값은 보존하며, 중복 제거는 정규화된 임시 컬럼을 기준으로 수행.
    """
    required_cols = {'ddate', 'tag', 'segments', 'qtrs'}
    if not required_cols.issubset(df.columns):
        print("⚠️ Required columns not found for deduplication.")
        return df

    df = _compute_adsh_rank(df).copy()

    df['tag_tmp'] = df['tag'].astype(str).apply(_normalize_tag)
    df['segments_tmp'] = df['segments'].astype(str).apply(_normalize_segment)
    df['qtrs'] = pd.to_numeric(df['qtrs'], errors='coerce').fillna(0).astype(int)

    try:
        df['ddate'] = pd.to_datetime(df['ddate'], errors='coerce')
    except Exception as e:
        print(f"❌ Failed to parse ddate: {e}")

    df = df.sort_values("adsh_rank", ascending=False)
    df = df.drop_duplicates(
        subset=['ddate', 'tag_tmp', 'segments_tmp', 'qtrs'],
        keep='first'
    )

    df.drop(columns=['tag_tmp', 'segments_tmp'], inplace=True)
    return df
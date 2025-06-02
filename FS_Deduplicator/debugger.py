# FS_Deduplicator/debugger.py
import pandas as pd
from FS_Deduplicator.utils import _compute_adsh_rank, _normalize_tag, _normalize_segment

def print_duplicate_groups_with_differences(df: pd.DataFrame) -> None:
    """
    중복 조건에 해당하지만 제거되지 않은 항목들을 출력하고,
    어떤 컬럼이 다르기 때문에 drop_duplicates에서 걸러지지 않는지를 비교.
    """
    required_cols = {'ddate', 'tag', 'segments', 'qtrs'}
    if not required_cols.issubset(df.columns):
        print("⚠️ Required columns not found for duplicate debugging.")
        return

    df = _compute_adsh_rank(df)

    df['tag_tmp'] = df['tag'].astype(str).apply(_normalize_tag)
    df['segments_tmp'] = df['segments'].astype(str).apply(_normalize_segment)
    df['qtrs'] = pd.to_numeric(df['qtrs'], errors='coerce').fillna(0).astype(int)

    try:
        df['ddate'] = pd.to_datetime(df['ddate'], errors='coerce')
    except Exception as e:
        print(f"❌ Failed to parse ddate: {e}")

    grouped = df.groupby(['ddate', 'tag_tmp', 'segments_tmp', 'qtrs'])

    for key, group in grouped:
        if len(group) > 1:
            diffs = group.drop(columns=['adsh_rank', 'tag_tmp', 'segments_tmp']).nunique()
            diff_cols = diffs[diffs > 1].index.tolist()
            if diff_cols:
                print(f"\n🟠 Duplicate group with differences in {diff_cols}:")
                print(group[['adsh', 'value'] + diff_cols])
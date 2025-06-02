# database_updater/step6_update_tag_segments.py

import os
import shutil
import pandas as pd
from glob import glob
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_fs_file(file, required_cols, temp_path):
    try:
        df = pd.read_parquet(file)

        for col in required_cols:
            if col not in df.columns:
                df[col] = pd.NA
        df = df[required_cols]
        df = df[df["tag"].notna()].drop_duplicates()

        file_id = os.path.basename(file).replace(".parquet", "")
        output_file = os.path.join(temp_path, f"{file_id}.parquet")
        df.to_parquet(output_file, index=False)
        return True
    except Exception as e:
        print(f"❗ Error processing {file}: {e}")
        return False

def run_step6(
    fs_month_path="/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/month",
    fs_quarter_path="/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/quarter",
    output_base_path="/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker",
    max_workers=6  # ✅ M3 Pro 기준 권장 값
):
    output_path = os.path.join(output_base_path, "all_tags_segments.parquet")
    temp_path = os.path.join(output_base_path, "temp_tags_segments")
    os.makedirs(temp_path, exist_ok=True)

    fs_files = glob(os.path.join(fs_month_path, "FS_*.parquet")) + \
               glob(os.path.join(fs_quarter_path, "FS_*.parquet"))

    required_cols = ["tag", "segments", "plabel", "tlabel", "doc", "sic"]

    print(f"🧵 Processing {len(fs_files)} FS files using {max_workers} threads...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_fs_file, file, required_cols, temp_path) for file in fs_files]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="🔄 Converting FS files"):
            pass

    temp_files = glob(os.path.join(temp_path, "*.parquet"))
    dfs = [pd.read_parquet(file) for file in tqdm(temp_files, desc="📦 병합 중")]
    if dfs:
        merged = pd.concat(dfs, ignore_index=True).drop_duplicates()
        merged.to_parquet(output_path, index=False)
        print(f"✅ 병합 및 저장 완료: {output_path}")
    else:
        print("⚠️ 병합할 데이터가 없습니다.")

    shutil.rmtree(temp_path, ignore_errors=True)
    print(f"🧹 임시 폴더 삭제 완료: {temp_path}")

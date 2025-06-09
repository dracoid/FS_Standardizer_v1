# database_updater/step2_merge_fs.py
import os
import pandas as pd
from datetime import datetime

def run_step2(parquet_base_dir="/Volumes/SSD1TB/30.Financial_data_python/SEC_FS_parquet/month",
              output_dir="/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/month"):
    current_year = datetime.now().year
    current_month = datetime.now().month

    os.makedirs(output_dir, exist_ok=True)
    skipped_folders = []

    for year in range(2023, current_year + 1):
        start_month = 7 if year == 2023 else 1
        end_month = current_month if year == current_year else 12

        for month in range(start_month, end_month + 1):
            month_str = f"{month:02d}"
            base_dir = os.path.join(parquet_base_dir, f"{year}_{month_str}_notes")

            if not os.path.exists(base_dir):
                print(f"Directory not found: {base_dir}, skipping...")
                skipped_folders.append(base_dir)
                continue

            dim_file = os.path.join(base_dir, "dim.parquet")
            num_file = os.path.join(base_dir, "num.parquet")
            pre_file = os.path.join(base_dir, "pre.parquet")
            sub_file = os.path.join(base_dir, "sub.parquet")
            tag_file = os.path.join(base_dir, "tag.parquet")

            if not all(map(os.path.exists, [dim_file, num_file, pre_file, sub_file, tag_file])):
                print(f"Missing files in: {base_dir}, skipping...")
                skipped_folders.append(base_dir)
                continue

            output_file = os.path.join(output_dir, f"FS_{year}{month_str}.parquet")
            if os.path.exists(output_file):
                print(f"Output exists: {output_file}, skipping...")
                continue

            try:
                dim = pd.read_parquet(dim_file)
                num = pd.read_parquet(num_file)
                pre = pd.read_parquet(pre_file)
                sub = pd.read_parquet(sub_file)
                tag = pd.read_parquet(tag_file)

                sub_reduced = sub[['adsh', 'cik', 'name', 'sic', 'wksi', 'form', 'period', 'fy', 'fp']]
                num_reduced = num[['adsh', 'tag', 'version', 'ddate', 'qtrs', 'uom', 'dimh', 'iprx', 'value','version']]
                pre_reduced = pre[['adsh', 'stmt', 'tag', 'version', 'plabel']]
                dim.rename(columns={'dimhash': 'dimh'}, inplace=True)

                merged = pd.merge(num_reduced, sub_reduced, on='adsh', how='outer')
                merged = pd.merge(merged, tag, on=['tag', 'version'], how='outer')
                merged = pd.merge(merged, dim, on='dimh', how='outer')
                merged = pd.merge(merged, pre_reduced, on=['adsh', 'tag', 'version'])

                merged = merged[merged['iprx'] == 0]
                merged = merged.dropna(subset=['stmt'])

                merged.to_parquet(output_file, index=False)
                print(f"🟢 File saved: {output_file}")
            except Exception as e:
                print(f"❌ Error processing {base_dir}: {e}")
                skipped_folders.append(base_dir)

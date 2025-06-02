# database_updater/step1_tsv_to_parquet.py
import os
import pandas as pd

def run_step1(tsv_base_dir="/Volumes/SSD1TB/30.Financial_data_python/SEC_FS_TSV/month",
              parquet_base_dir="/Volumes/SSD1TB/30.Financial_data_python/SEC_FS_parquet/month"):
    for subdir, _, files in os.walk(tsv_base_dir):
        for file in files:
            if not file.endswith(".tsv"):
                continue

            tsv_file_path = os.path.join(subdir, file)
            relative_subdir = os.path.relpath(subdir, tsv_base_dir)
            parquet_subdir = os.path.join(parquet_base_dir, relative_subdir)
            os.makedirs(parquet_subdir, exist_ok=True)

            parquet_file_path = os.path.join(parquet_subdir, file.replace(".tsv", ".parquet"))

            if os.path.exists(parquet_file_path):
                print(f"✅ Already exists, skipping: {parquet_file_path}")
                continue

            try:
                df = pd.read_csv(tsv_file_path, sep="\t", low_memory=False, on_bad_lines='skip')
                df.to_parquet(parquet_file_path, index=False)
                print(f"🟢 Converted: {tsv_file_path} → {parquet_file_path}")
            except Exception as e:
                print(f"❌ Failed to convert {tsv_file_path}: {e}")
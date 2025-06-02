# database_updater/step4_split_and_classify_fs.py
import os
import pandas as pd
from glob import glob

def run_step4(
    sic_excel_path="/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/sic_table.xlsx",
    fs_month_path="/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/month",
    fs_quarter_path="/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/quarter",
    output_base_path="/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/SIC_CIK"
):
    print("📥 Loading SIC classification table...")
    sic_df = pd.read_excel(sic_excel_path)
    sic_df['folder_name'] = sic_df.apply(
        lambda row: os.path.join(output_base_path, row['Office'], f"{row['sic']}_{row['Industry Title']}"), axis=1
    )

    for path in sic_df['folder_name']:
        os.makedirs(path, exist_ok=True)

    fs_files = glob(os.path.join(fs_month_path, "FS_*.parquet")) + \
               glob(os.path.join(fs_quarter_path, "FS_*.parquet"))

    for i, fs_path in enumerate(fs_files, start=1):
        try:
            print(f"[{i}/{len(fs_files)}] Processing: {os.path.basename(fs_path)}")
            df = pd.read_parquet(fs_path)

            if not {'sic', 'cik'}.issubset(df.columns):
                print("  ⚠️ Skipped: Required columns missing.")
                continue

            df = df[df['sic'].notna() & df['cik'].notna()]
            df['sic'] = df['sic'].astype(int)
            df['cik'] = df['cik'].astype(int)

            for sic_value, sic_group in df.groupby('sic'):
                match = sic_df[sic_df['sic'] == sic_value]
                if match.empty:
                    print(f"  ⚠️ Unknown SIC code: {sic_value}")
                    continue

                sic_folder = match.iloc[0]['folder_name']

                for cik_value, cik_group in sic_group.groupby('cik'):
                    cik_folder = os.path.join(sic_folder, str(cik_value))
                    os.makedirs(cik_folder, exist_ok=True)
                    output_file = os.path.join(cik_folder, os.path.basename(fs_path))
                    cik_group.to_parquet(output_file, index=False)
                    print(f"    ✅ Saved to {output_file} ({len(cik_group)} rows)")

        except Exception as e:
            print(f"  ❌ Error processing {fs_path}: {e}")
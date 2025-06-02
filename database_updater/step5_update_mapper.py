# database_updater/step5_update_mapper.py
import os
import json
import pandas as pd
from glob import glob

def run_step5(
    sic_path="/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/sic_table.xlsx",
    json_path="/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/company_tickers_exchange.json",
    fs_paths=None,
    output_path="/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/ticker_mapper.parquet"
):
    if fs_paths is None:
        fs_paths = [
            "/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/month",
            "/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/mergedFS/quarter"
        ]

    sic_df = pd.read_excel(sic_path)

    with open(json_path, 'r') as f:
        json_data = json.load(f)
    ticker_df = pd.DataFrame(json_data['data'], columns=json_data['fields'])

    ticker_to_exchange = {
        row['ticker']: {
            "cik": int(row['cik']),
            "exchange": row.get('exchange'),
            "name": row.get('name')
        }
        for _, row in ticker_df.iterrows() if row['ticker']
    }

    parquet_files = []
    for path in fs_paths:
        parquet_files.extend(glob(os.path.join(path, "*.parquet")))

    cik_to_filepaths = {}
    for file_path in parquet_files:
        try:
            df = pd.read_parquet(file_path, columns=["cik", "sic"])
            df = df.dropna(subset=["cik", "sic"])
            for cik, sic in df[["cik", "sic"]].drop_duplicates().values:
                cik = int(cik)
                sic = int(sic)
                if cik not in cik_to_filepaths:
                    cik_to_filepaths[cik] = {"sic": sic, "files": []}
                cik_to_filepaths[cik]["files"].append(file_path)
        except Exception as e:
            print(f"⚠️ Error reading {file_path}: {e}")

    cik_to_ticker = {v["cik"]: k for k, v in ticker_to_exchange.items()}
    records = []
    for cik, info in cik_to_filepaths.items():
        ticker = cik_to_ticker.get(cik)
        if not ticker:
            continue
        meta = ticker_to_exchange[ticker]
        sic_row = sic_df[sic_df["sic"] == info["sic"]]
        if not sic_row.empty:
            office = sic_row.iloc[0]["Office"]
            industry = sic_row.iloc[0]["Industry Title"]
            fs_path = f"/Volumes/SSD1TB/30.Financial_data_python/Refinded_data/SIC_CIK/{office}/{info['sic']}_{industry}/{cik}"
            records.append({
                "ticker": ticker,
                "name": meta["name"],
                "cik": cik,
                "office": office,
                "Industry Title": industry,
                "exchange": meta["exchange"],
                "FS_Path": fs_path,
                "sic": info["sic"]  # ✅ 추가
            })

    output_df = pd.DataFrame(records)
    output_df.to_parquet(output_path, index=False)
    print(f"✅ Mapping saved to: {output_path}")
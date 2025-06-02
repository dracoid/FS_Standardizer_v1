# main_specific_company.py
import pandas as pd
import os
from glob import glob
from datetime import datetime

from FS_Deduplicator import preprocess_financial_data
from FS_standardizer_IS.standardizer import standardize_income_statement
from FS_standardizer_BS.standardizer import standardize_balance_sheet


def run_fs_standardization():
    # Step 1: 사용자 입력
    ticker = input("Enter the ticker symbol: ").upper().strip()

    # Step 2: 매핑 정보 불러오기
    mapper_path = "/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/ticker_mapper.parquet"
    mapper_df = pd.read_parquet(mapper_path)

    if ticker not in mapper_df['ticker'].values:
        raise ValueError(f"❌ {ticker} not found in ticker_mapper.parquet")

    target_path = mapper_df.loc[mapper_df['ticker'] == ticker, 'FS_Path'].values[0]
    cik = mapper_df.loc[mapper_df['ticker'] == ticker, 'cik'].values[0]
    sic = mapper_df.loc[mapper_df['ticker'] == ticker, 'sic'].values[0]

    if not os.path.exists(target_path):
        raise FileNotFoundError(f"❌ Target path does not exist: {target_path}")
    print(f"✔ Ticker {ticker} is mapped to path: {target_path}")

    # Step 3: 파일 병합
    parquet_files = sorted(glob(os.path.join(target_path, "*.parquet")))
    if not parquet_files:
        raise FileNotFoundError("❌ No parquet files found in the target directory.")

    dfs = [pd.read_parquet(pf) for pf in parquet_files]
    merged_df = pd.concat(dfs, ignore_index=True)
    print(f"✔ Merged {len(parquet_files)} files with total {len(merged_df)} rows")

    # Step 4: 공통 전처리
    cleaned_df = preprocess_financial_data(merged_df)
    cleaned_df["segments"] = cleaned_df["segments"].fillna("[Total]")

    # Step 5: IS / BS 표준화
    is_df = standardize_income_statement(cleaned_df, default_sic=sic)
    bs_df = standardize_balance_sheet(cleaned_df, default_sic=sic)

    # Step 6: 나머지 stmt 구분
    known_stmts = ["IS", "BS"]
    other_df = cleaned_df[~cleaned_df["stmt"].str.upper().isin(known_stmts)].copy()

    # Step 7: 전체 병합 및 정렬
    final_df = pd.concat([is_df, bs_df, other_df], ignore_index=True)
    final_df.sort_values("ddate_label_month", inplace=True)

    # Step 8: 저장 경로 설정
    output_dir = "/Volumes/SSD1TB/30.Financial_data_python/CompanyAnalysis"
    os.makedirs(output_dir, exist_ok=True)
    today_str = datetime.today().strftime("%y-%m-%d")
    base_name = f"{ticker}_{today_str}"

    # Step 9: 전체 파일 저장
    final_parquet = os.path.join(output_dir, f"{base_name}.parquet")
    final_excel = os.path.join(output_dir, f"{base_name}.xlsx")
    final_df.to_parquet(final_parquet, index=False)
    final_df.to_excel(final_excel, index=False)
    print(f"\n📁 Full FS saved to:\n  - {final_parquet}\n  - {final_excel}")

    # Step 10: stmt별 분리 저장
    for stmt_type in final_df['stmt'].dropna().unique():
        stmt_df = final_df[final_df['stmt'].str.upper() == stmt_type.upper()].copy()
        if stmt_df.empty:
            continue

        stmt_excel = os.path.join(output_dir, f"{base_name}_{stmt_type.upper()}.xlsx")
        stmt_df.to_excel(stmt_excel, index=False)

        print(f"📄 Saved {stmt_type.upper()} to:\n  - {stmt_excel}\n ")


if __name__ == "__main__":
    run_fs_standardization()

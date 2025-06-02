# database_updater/step3_update_ticker_info.py
import os, json, requests, pandas as pd

def run_step3(
    json_url: str = "https://www.sec.gov/files/company_tickers_exchange.json",

    # ⬇️ Step 5가 기대하는 위치와 동일하게 맞춤
    local_json_path: str = (
        "/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/"
        "company_tickers_exchange.json"
    ),
    output_path: str = (
        "/Volumes/SSD1TB/30.Financial_data_python/SEC_data_SIC_ticker/"
        "company_tickers_exchange_refined.parquet"
    ),

    user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "database_updater/1.0 (+mailto:your_email@example.com)"
    ),
) -> None:
    """Download latest SEC ticker–CIK–exchange JSON and save as Parquet + cache JSON."""

    # ── helper ───────────────────────────────────────────────────────────────
    def _download_json(url: str) -> dict:
        hdrs = {"User-Agent": user_agent, "Accept": "application/json"}
        resp = requests.get(url, headers=hdrs, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # 1️⃣ JSON 확보 ───────────────────────────────────────────────────────────
    if os.path.exists(local_json_path):
        print(f"📂 Using cached JSON: {local_json_path}")
        with open(local_json_path, "r") as f:
            json_data = json.load(f)
    else:
        print(f"🌐 Downloading latest JSON from SEC …")
        json_data = _download_json(json_url)

        # 캐시 디렉터리 생성 후 저장
        os.makedirs(os.path.dirname(local_json_path), exist_ok=True)
        with open(local_json_path, "w") as f:
            json.dump(json_data, f)
        print(f"📝 Cached JSON → {local_json_path}")

    # 2️⃣ Parquet 변환 & 저장 ────────────────────────────────────────────────
    try:
        df = pd.DataFrame(json_data["data"], columns=json_data["fields"])
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_parquet(output_path, index=False)
        print(f"🟢 Parquet saved → {output_path}  (rows={len(df)})")
    except Exception as e:
        print(f"❌ Failed to save Parquet: {e}")
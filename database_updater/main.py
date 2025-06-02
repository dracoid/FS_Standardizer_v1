# database_updater/main_specific_company.py
# run this module with "python -m database_updater.main"
from .step1_tsv_to_parquet import run_step1
from .step2_merge_fs import run_step2
from .step3_update_ticker_info import run_step3
from .step4_split_and_classify_fs import run_step4
from .step5_update_mapper import run_step5
from .step6_update_tag_segments import run_step6
from tqdm import tqdm
import time

# 💡 M4 Pro 기준 안정적인 병렬 수 설정 (8~10 스레드 안정권)
DEFAULT_MAX_WORKERS = 8

def run_all(max_workers=6):  # ✅ M3 Pro 권장값
    steps = [
        ("Step 1: TSV → Parquet", run_step1),
        ("Step 2: Merge Financial Statements", run_step2),
        ("Step 3: Update Ticker Info", run_step3),
        ("Step 4: Split FS by SIC & CIK", run_step4),
        ("Step 5: Build Ticker Mapper", run_step5),
        ("Step 6: Extract Tags & Segments", run_step6),  # 병렬 지원
    ]

    print("\n📦 Starting database update process...")
    for i, (desc, func) in enumerate(tqdm(steps, desc="📊 Database Update Progress", unit="step", ncols=100)):
        print(f"\n✅ {desc}")
        try:
            if "max_workers" in func.__code__.co_varnames:
                func(max_workers=max_workers)
            else:
                func()
        except Exception as e:
            print(f"❌ Error in {desc}: {e}")
            continue

    print("\n🎉 All steps completed successfully!")

if __name__ == "__main__":
    run_all()

# FS_standardizer_BS/utils/helper.py
import re

def clean_text(text: str) -> str:
    # CamelCase → 띄어쓰기
    text = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
    # 앞뒤 공백 제거
    return text.strip().title()


def clean_plabel(plabel: str) -> str:
    """
    plabel에서 금액 정보(예: "$250 and $335")를 제거하여 identifier 중복을 줄이기 위함.

    예:
    "Accounts receivable, net of allowance for doubtful accounts of $250 and $335"
    → "Accounts receivable, net of allowance for doubtful accounts of"
    """
    return re.sub(r"\$[0-9,]+( and \$[0-9,]+)?", "", plabel or "[Unlabeled]").strip()

# FS_standardizer_IS/sector/bank_mapper.py
from FS_standardizer_IS.general_mapper import classify_general
from FS_standardizer_IS.utils.helper import clean_text


def classify_bank(tag: str, segments: str, plabel: str):
    """
    은행(및 금융업) 손익계산서 항목을 카테고리·서브카테고리·식별자로 매핑한다.
    매핑되지 않는 항목은 general_mapper 로 위임.
    """
    tag_lower = (tag or "").lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"

    # ────────────────────────────────
    # 1) 기본값 (fallback 대비)
    # ────────────────────────────────
    category = None
    subcategory = None

    # ────────────────────────────────
    # 2) 은행 업종 전용 매핑 로직
    # ────────────────────────────────
    if "interestincome" in tag_lower:
        category = "01. Revenue"
        subcategory = "Interest Income"

    elif "noninterestincome" in tag_lower or "feeincome" in tag_lower:
        category = "01. Revenue"
        subcategory = "Non-Interest Income"

    elif "interestexpense" in tag_lower:
        category = "02. Cost of Revenue"
        subcategory = "Interest Expense"

    elif (
        "provisionforloanlosses" in tag_lower
        or "loanloss" in tag_lower
        or "creditloss" in tag_lower
    ):
        category = "04. Operating Expenses"
        subcategory = "Provision for Credit Losses"

    elif "noninterestexpense" in tag_lower or "generalandadministrative" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Non-Interest Expense"

    elif "operatingincome" in tag_lower:
        category = "05. Operating Income"
        subcategory = "Operating Income"

    elif (
        "investment" in tag_lower
        or "othernonoperating" in tag_lower
        or "otherincomeexpense" in tag_lower
    ):
        category = "06. Non-operating Items"
        subcategory = "Other Gains/Losses"

    elif "beforeincometax" in tag_lower or "incomebeforetax" in tag_lower:
        category = "07. Income Before Tax"
        subcategory = "Income Before Tax"

    elif "incometax" in tag_lower and "netof" not in tag_lower:
        category = "08. Income Tax Expense"
        subcategory = "Income Tax Expense"

    elif "netincomeloss" in tag_lower or "profitloss" in tag_lower:
        category = "09. Net Income"
        subcategory = "Net Income"

    elif "earningspershare" in tag_lower or "weightedaverage" in tag_lower:
        category = "10. Earnings per Share"
        if "diluted" in tag_lower:
            subcategory = "Diluted EPS"
        elif "basic" in tag_lower:
            subcategory = "Basic EPS"
        else:
            subcategory = "EPS"

    elif "split" in tag_lower:
        category = "99. Unclassified"
        subcategory = "Stock Split"

    else:
        # 은행 전용 규칙에 안 걸리면 general_mapper 에 위임
        return classify_general(tag, segments, plabel)

    # ────────────────────────────────
    # 3) 식별자·레이블 생성 후 반환
    # ────────────────────────────────
    identifier = f"[{segments_str}] | {plabel_str}"
    identifier_label = f"{identifier} | {clean_text(tag)}"

    return category, subcategory, identifier, identifier_label

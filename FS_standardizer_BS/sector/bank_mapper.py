# FS_standardizer_BS/sector/bank_mapper.py
"""
Bank-sector Balance Sheet mapper
--------------------------------
• 자산(Assets), 부채(Liabilities), 자본(Equity)의 세부 항목을 업종 특화 규칙으로 분류
• 매핑 실패 시 (None, None, None, None) 반환 → 상위 로직에서 'Unclassified' 처리
"""

from FS_standardizer_BS.utils.helper import clean_text


def classify_bank_bs(tag: str, segments: str, plabel: str) -> tuple:
    """
    Parameters
    ----------
    tag : str
        XBRL tag (e.g., 'CashAndDueFromBanks')
    segments : str
        Segment 정보 (없으면 None)
    plabel : str
        Presentation label (없으면 None)

    Returns
    -------
    tuple
        (category, subcategory, identifier, identifier_label)
        모든 요소가 None이면 미분류(Unclassified)
    """
    tag_lower = tag.lower()
    seg_lower = (segments or "[Total]").lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"

    # ---------- 기본값 ----------
    category = subcategory = identifier = identifier_label = None

    # ---------- 자산(Assets) ----------
    if tag_lower in {"cash", "cashequivalents", "cashandduefrombanks"}:
        category, subcategory = "01. Assets", "Cash and Reserves"

    elif any(kw in tag_lower for kw in ("availableforsale", "heldtomaturity", "securities")):
        category, subcategory = "01. Assets", "Investments and Securities"

    elif any(kw in tag_lower for kw in ("loan", "leasefinancing", "loansreceivable")):
        category, subcategory = "01. Assets", "Loans and Leases"

    elif "premises" in tag_lower or "equipment" in tag_lower:
        category, subcategory = "01. Assets", "Premises and Equipment"

    elif "goodwill" in tag_lower or "intangible" in tag_lower:
        category, subcategory = "01. Assets", "Goodwill and Intangibles"

    elif "deferred" in tag_lower or "otherasset" in tag_lower:
        category, subcategory = "01. Assets", "Other Assets"

    # ---------- 부채(Liabilities) ----------
    elif "deposit" in tag_lower or "interestbearing" in tag_lower:
        category, subcategory = "02. Liabilities", "Deposits"

    elif any(kw in tag_lower for kw in ("borrowings", "shorttermdebt", "longtermdebt")):
        category, subcategory = "02. Liabilities", "Borrowings and Debt"

    elif "deferred" in tag_lower or "tax" in tag_lower or "otherliabilities" in tag_lower:
        category, subcategory = "02. Liabilities", "Other Liabilities"

    # ---------- 자본(Equity) ----------
    elif any(kw in tag_lower for kw in ("equity", "commonstock", "retained", "accumulated")):
        category, subcategory = "03. Equity", "Stockholders’ Equity"

    # ---------- 매핑 실패 ----------
    if category is None:
        return None, None, None, None

    # ---------- identifier / identifier_label ----------
    identifier = f"[{segments_str}] | {plabel_str}"
    identifier_label = f"{identifier} | {clean_text(tag)}"

    return category, subcategory, identifier, identifier_label

from FS_standardizer_BS.utils.helper import clean_text


def classify_bank_bs(tag: str, segments: str, plabel: str) -> tuple:
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"
    seg_lower = segments_str.lower()

    category = None
    subcategory = None

    # ✅ Step 1: 금융업 전용 태그 분류
    if tag_lower in ["cash", "cashequivalents", "cashandduefrombanks"]:
        category = "01. Assets"
        subcategory = "Cash and Reserves"
    elif any(kw in tag_lower for kw in ["availableforsale", "heldtomaturity", "securities"]):
        category = "01. Assets"
        subcategory = "Investments and Securities"
    elif "loan" in tag_lower or "leasefinancing" in tag_lower or "loansreceivable" in tag_lower:
        category = "01. Assets"
        subcategory = "Loans and Leases"
    elif "premises" in tag_lower or "equipment" in tag_lower:
        category = "01. Assets"
        subcategory = "Premises and Equipment"
    elif "goodwill" in tag_lower or "intangible" in tag_lower:
        category = "01. Assets"
        subcategory = "Goodwill and Intangibles"
    elif "deferred" in tag_lower or "otherasset" in tag_lower:
        category = "01. Assets"
        subcategory = "Other Assets"

    elif "deposit" in tag_lower or "interestbearing" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Deposits"
    elif "borrowings" in tag_lower or "shorttermdebt" in tag_lower or "longtermdebt" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Borrowings and Debt"
    elif "deferred" in tag_lower or "tax" in tag_lower or "otherliabilities" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Other Liabilities"

    elif any(kw in tag_lower for kw in ["equity", "commonstock", "retained", "accumulated"]):
        category = "03. Equity"
        subcategory = "Stockholders’ Equity"

    # ✅ Step 2: Unknown → None 반환
    if category is None:
        return None, None, None, None

    # ✅ Step 3: identifier 및 label
    identifier = f"[{segments_str}] | {plabel_str}"
    identifier_label = f"{identifier} | {clean_text(tag)}"

    return category, subcategory, identifier, identifier_label

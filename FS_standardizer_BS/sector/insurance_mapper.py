from FS_standardizer_BS.utils.helper import clean_text


def classify_insurance_bs(tag: str, segments: str, plabel: str) -> tuple:
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"
    seg_lower = segments_str.lower()

    category = None
    subcategory = None

    # ✅ Step 1: 보험사 전용 항목 분류
    if "cash" in tag_lower or "reserves" in tag_lower:
        category = "01. Assets"
        subcategory = "Cash and Reserves"
    elif "investments" in tag_lower or "securities" in tag_lower:
        category = "01. Assets"
        subcategory = "Investments and Securities"
    elif "reinsurance" in tag_lower and "recoverable" in tag_lower:
        category = "01. Assets"
        subcategory = "Reinsurance Recoverables"
    elif "deferredpolicyacquisitioncosts" in tag_lower or "dac" in tag_lower:
        category = "01. Assets"
        subcategory = "Deferred Acquisition Costs"
    elif "goodwill" in tag_lower or "intangible" in tag_lower:
        category = "01. Assets"
        subcategory = "Goodwill and Intangibles"
    elif "other" in tag_lower or "deferred" in tag_lower:
        category = "01. Assets"
        subcategory = "Other Assets"

    elif "unpaidclaims" in tag_lower or "claimliabilities" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Unpaid Claims"
    elif "unearnedpremium" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Unearned Premiums"
    elif "futurepolicybenefits" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Future Policy Benefits"
    elif "reinsurance" in tag_lower and ("payable" in tag_lower or "ceded" in tag_lower):
        category = "02. Liabilities"
        subcategory = "Reinsurance Payables"
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

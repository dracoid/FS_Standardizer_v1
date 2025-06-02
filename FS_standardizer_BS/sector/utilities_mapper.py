from FS_standardizer_BS.utils.helper import clean_text


def classify_utilities_bs(tag: str, segments: str, plabel: str) -> tuple:
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"
    seg_lower = segments_str.lower()

    category = None
    subcategory = None

    # ✅ Step 1: 유틸리티 업종 전용 분류
    if "regulatoryasset" in tag_lower:
        category = "01. Assets"
        subcategory = "Regulatory Assets"
    elif "fuelinventory" in tag_lower or "emissionallowance" in tag_lower:
        category = "01. Assets"
        subcategory = "Fuel and Environmental Assets"
    elif "property" in tag_lower or "plant" in tag_lower or "equipment" in tag_lower:
        category = "01. Assets"
        subcategory = "Property, Plant and Equipment"
    elif "cash" in tag_lower or "reserves" in tag_lower:
        category = "01. Assets"
        subcategory = "Cash and Reserves"
    elif "intangible" in tag_lower or "goodwill" in tag_lower:
        category = "01. Assets"
        subcategory = "Goodwill and Intangibles"
    elif "other" in tag_lower or "deferred" in tag_lower:
        category = "01. Assets"
        subcategory = "Other Assets"

    elif "regulatoryliability" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Regulatory Liabilities"
    elif "assetretirementobligation" in tag_lower or "environment" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Asset Retirement Obligations"
    elif "shorttermdebt" in tag_lower or "longtermdebt" in tag_lower or "borrowings" in tag_lower:
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

from FS_standardizer_BS.utils.helper import clean_text


def classify_reit_bs(tag: str, segments: str, plabel: str) -> tuple:
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"
    seg_lower = segments_str.lower()

    category = None
    subcategory = None

    # ✅ Step 1: 리츠 업종 전용 분류
    if "realestateheldforsale" in tag_lower:
        category = "01. Assets"
        subcategory = "Real Estate Held for Sale"
    elif "investmentproperty" in tag_lower or "operatingrealestate" in tag_lower:
        category = "01. Assets"
        subcategory = "Investment Property"
    elif "rentreceivable" in tag_lower or "straightline" in tag_lower:
        category = "01. Assets"
        subcategory = "Rent and Lease Receivables"
    elif "cash" in tag_lower or "reserves" in tag_lower:
        category = "01. Assets"
        subcategory = "Cash and Reserves"
    elif "intangible" in tag_lower or "goodwill" in tag_lower:
        category = "01. Assets"
        subcategory = "Goodwill and Intangibles"
    elif "other" in tag_lower or "deferred" in tag_lower:
        category = "01. Assets"
        subcategory = "Other Assets"

    elif "mortgagedebt" in tag_lower or "secureddebt" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Mortgage and Secured Debt"
    elif "tenantdeposit" in tag_lower or "securitydeposit" in tag_lower:
        category = "02. Liabilities"
        subcategory = "Tenant Deposits"
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

# FS_standardizer_BS/general_mapper.py
from FS_standardizer_BS.utils.helper import clean_text


def classify_general_bs(tag: str, segments: str, plabel: str) -> tuple:
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"
    seg_lower = segments_str.lower()

    category = None
    subcategory = None
    identifier = None
    identifier_label = None

    # ✅ Step 1: 명확한 태그 분류 (자산/부채/자본 및 유동성)
    if tag_lower in ["accountsreceivablenetcurrent", "allowancefordoubtfulaccountsreceivablecurrent"]:
        category = "01. Assets"
        subcategory = "Current Assets"
        identifier = "Accounts Receivable"
    elif tag_lower in ["availableforsalesecuritiescurrent", "cashandcashequivalentsatcarryingvalue",
                       "cashcashequivalentsandshortterminvestments", "inventorynet", "shortterminvestments"]:
        category = "01. Assets"
        subcategory = "Current Assets"
        identifier = "Current Investments"
    elif tag_lower == "commercialpaper":
        category = "02. Liabilities"
        subcategory = "Current Liabilities"
        identifier = "Commercial Paper"
    elif tag_lower == "securitiesloaned":
        category = "02. Liabilities"
        subcategory = "Securities Lending"
        identifier = "Securities Lending"
    elif tag_lower == "securitiesownedandloaned":
        category = "01. Assets"
        subcategory = "Trading Securities"
        identifier = "Trading Securities"
    elif tag_lower == "securitiesreceivedascollateralclassified":
        category = "01. Assets"
        subcategory = "Other Assets"
        identifier = "Collateralized Securities"
    elif tag_lower in ["longterminvestments"]:
        category = "01. Assets"
        subcategory = "Non-current Assets"
        identifier = "Long-term Investments"
    elif tag_lower in ["propertyplantandequipmentnet"]:
        category = "01. Assets"
        subcategory = "Non-current Assets"
        identifier = "PPE"
    elif tag_lower == "goodwill":
        category = "01. Assets"
        subcategory = "Non-current Assets"
        identifier = "Goodwill"
    elif tag_lower in ["deferredrevenuecurrent", "depositsreceivedforsecuritiesloanedatcarryingvalue", "shorttermborrowings"]:
        category = "02. Liabilities"
        subcategory = "Current Liabilities"
        identifier = clean_text(tag)
    elif tag_lower == "deferredrevenuenoncurrent":
        category = "02. Liabilities"
        subcategory = "Non-current Liabilities"
        identifier = clean_text(tag)
    elif any(kw in tag_lower for kw in ["equity", "stock", "retained", "accumulated"]):
        category = "03. Equity"
        subcategory = "Stockholders’ Equity"
        identifier = "Equity"

    # ✅ Step 2: fallback 분류
    elif "asset" in tag_lower:
        category = "01. Assets"
        subcategory = "Current Assets" if any(kw in tag_lower for kw in ["current", "cash", "receivable", "inventory", "prepaid"]) else "Non-current Assets"
        identifier = clean_text(tag)
    elif any(kw in tag_lower for kw in ["liabilit", "payable", "debt", "lease", "accrued"]):
        category = "02. Liabilities"
        subcategory = "Current Liabilities" if any(kw in tag_lower for kw in ["current", "shortterm", "accrued"]) else "Non-current Liabilities"
        identifier = clean_text(tag)

    # ✅ Step 3: 분류 실패 시 None 반환
    if category is None:
        return None, None, None, None

    # ✅ Step 4: identifier_label 생성
    identifier_label = f"[{segments_str}] | {identifier}"

    return category, subcategory, identifier, identifier_label

# FS_standardizer_IS/general_mapper.py
from .utils.helper import clean_text

def classify_general(tag, segments, plabel):
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"
    seg_lower = segments_str.lower()

    # Step 1: Category (순서 중요)
    if "regulatory" in tag_lower:
        category = "01. Revenue"
        subcategory = "Regulatory Credit"
    elif "costofgoodsandservicessold" in tag_lower or "costofservicesandother" in tag_lower:
        category = "02. Cost of Goods Sold"
    elif "costofgoodssold" in tag_lower:
        category = "02. Cost of Goods Sold"
        subcategory = "Product"
    elif "costofrevenue" in tag_lower or "costofsales" in tag_lower or ("cost" in tag_lower and "revenue" in tag_lower):
        category = "02. Cost of Goods Sold"
    elif ("lease" in tag_lower and "cost" in tag_lower) or "rented" in tag_lower:
        category = "02. Cost of Goods Sold"
        subcategory = "Leasing"
    elif "revenue" in tag_lower or "sales" in tag_lower:
        category = "01. Revenue"
    elif "leasing" in tag_lower:
        category = "01. Revenue"
        subcategory = "Leasing"
    elif "grossprofit" in tag_lower or "grossprofitloss" in tag_lower:
        category = "03. Gross Profit"
    elif "sellinggeneralandadministrative" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "SG&A"
    elif "generalandadministrativeexpense" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "General & Administrative"
    elif "researchanddevelopment" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "R&D"
    elif "depreciation" in tag_lower or "amortization" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Depreciation & Amortization"
    elif "operatingexpense" in tag_lower or "costsandexpenses" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Total Operating Expenses"
    elif "restructuring" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Restructuring"
    elif "impairment" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Impairment"
    elif "severance" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Severance"
    elif "marketing" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Marketing"
    elif "integration" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Restructuring"
    elif "operatingincome" in tag_lower:
        category = "05. Operating Income"
    elif "interest" in tag_lower:
        category = "06. Non-operating Items"
        subcategory = "Interest Income/Expense"
    elif "investment" in tag_lower or "othernonoperating" in tag_lower or "otherincomeexpense" in tag_lower:
        category = "06. Non-operating Items"
        subcategory = "Other Gains/Losses"
    elif "beforeincometax" in tag_lower or "incomebeforetax" in tag_lower or "continuingoperationsbeforetax" in tag_lower:
        category = "07. Income Before Tax"
    elif "incometax" in tag_lower:
        category = "08. Income Tax Expense"
    elif "netincomeloss" in tag_lower or "profitloss" in tag_lower or "continuingoperations" in tag_lower:
        category = "09. Net Income"
    elif "earningspershare" in tag_lower or "weightedaverage" in tag_lower:
        category = "10. Earnings per Share"
        if "diluted" in tag_lower:
            subcategory = "Diluted EPS"
        elif "basic" in tag_lower:
            subcategory = "Basic EPS"
        else:
            subcategory = "EPS"
    elif "dividend" in tag_lower:
        category = "99. Unclassified"
        subcategory = "Dividend"
    elif "split" in tag_lower:
        category = "99. Unclassified"
        subcategory = "Stock Split"
    else:
        return None, None, None, None

    # Step 2: Subcategory fallback based on segments
    if 'subcategory' not in locals() or subcategory is None:
        if "automotive" in seg_lower:
            subcategory = "Automotive"
        elif "energygenerationandstorage" in seg_lower:
            subcategory = "Energy Generation and Storage"
        elif "servicesandother" in seg_lower or "service" in seg_lower:
            subcategory = "Services and Other"
        elif "regulatory" in seg_lower:
            subcategory = "Regulatory Credit"
        else:
            subcategory = "Other"

    # Step 3: Identifier
    identifier = f"[{segments_str}] | {plabel_str}"

    # Step 4: Identifier Label
    tag_label = clean_text(tag)
    identifier_label = f"{identifier} | {tag_label}"

    return category, subcategory, identifier, identifier_label

# FS_standardizer_IS/sector/telecom_mapper.py
from FS_standardizer_IS.general_mapper import classify_general
from FS_standardizer_IS.utils.helper import clean_text

def classify_telecom(tag, segments, plabel):
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"

    # Step 1: Telecom-specific mapping
    if "subscriptionrevenue" in tag_lower:
        category = "01. Revenue"
        subcategory = "Subscription Revenue"
    elif "devicerevenue" in tag_lower:
        category = "01. Revenue"
        subcategory = "Device Revenue"
    elif "interconnection" in tag_lower:
        category = "02. Cost of Goods Sold"
        subcategory = "Interconnection Costs"
    elif "networkdepreciation" in tag_lower or ("depreciation" in tag_lower and "network" in tag_lower):
        category = "04. Operating Expenses"
        subcategory = "Network Depreciation"
    elif "spectrum" in tag_lower and ("amortization" in tag_lower or "expense" in tag_lower):
        category = "04. Operating Expenses"
        subcategory = "Spectrum Amortization"
    elif "sellinggeneralandadministrative" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "SG&A"
    elif "researchanddevelopment" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "R&D"
    elif "depreciation" in tag_lower or "amortization" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Depreciation & Amortization"
    elif "operatingexpense" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Total Operating Expenses"
    elif "restructuring" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Restructuring"
    elif "operatingincome" in tag_lower:
        category = "05. Operating Income"
    elif "interest" in tag_lower:
        category = "06. Non-operating Items"
        subcategory = "Interest Income/Expense"
    elif "othernonoperating" in tag_lower or "otherincomeexpense" in tag_lower:
        category = "06. Non-operating Items"
        subcategory = "Other Gains/Losses"
    elif "incomebeforetax" in tag_lower or "beforeincometax" in tag_lower:
        category = "07. Income Before Tax"
    elif "incometax" in tag_lower:
        category = "08. Income Tax Expense"
    elif "netincomeloss" in tag_lower or "profitloss" in tag_lower:
        category = "09. Net Income"
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
        return classify_general(tag, segments, plabel)

    # Step 2: Identifier
    identifier = f"[{segments_str}] | {plabel_str}"
    identifier_label = f"{identifier} | {clean_text(tag)}"

    return category, subcategory, identifier, identifier_label

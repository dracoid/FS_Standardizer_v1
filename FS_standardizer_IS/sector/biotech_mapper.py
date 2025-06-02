# FS_standardizer_IS/sector/biotech_mapper.py
from FS_standardizer_IS.general_mapper import classify_general
from FS_standardizer_IS.utils.helper import clean_text

def classify_biotech(tag, segments, plabel):
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"

    # Step 1: Biotech-specific category
    if "collaborationrevenue" in tag_lower:
        category = "01. Revenue"
        subcategory = "Collaboration Revenue"
    elif "milestonerevenue" in tag_lower:
        category = "01. Revenue"
        subcategory = "Milestone Revenue"
    elif "grantrevenue" in tag_lower or "researchgrant" in tag_lower:
        category = "01. Revenue"
        subcategory = "Grant Revenue"
    elif "contractrevenue" in tag_lower:
        category = "01. Revenue"
        subcategory = "Contract Revenue"
    elif "upfront" in tag_lower and "revenue" in tag_lower:
        category = "01. Revenue"
        subcategory = "Upfront Revenue"
    elif "costofrevenue" in tag_lower or "costofsales" in tag_lower:
        category = "02. Cost of Revenue"
    elif "researchanddevelopment" in tag_lower or "rnd" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "R&D"
    elif "sellinggeneralandadministrative" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "SG&A"
    elif "restructuring" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Restructuring"
    elif "depreciation" in tag_lower or "amortization" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Depreciation & Amortization"
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

    # Step 2: Identifier and Label
    identifier = f"[{segments_str}] | {plabel_str}"
    identifier_label = f"{identifier} | {clean_text(tag)}"

    return category, subcategory, identifier, identifier_label

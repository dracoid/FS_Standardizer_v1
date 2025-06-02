# FS_standardizer_IS/sector/bank_mapper.py
from FS_standardizer_IS.general_mapper import classify_general
from FS_standardizer_IS.utils.helper import clean_text

def classify_bank(tag, segments, plabel):
    tag_lower = tag.lower()
    segments_str = segments or "[Total]"
    plabel_str = plabel or "[Unlabeled]"

    # Step 1: Bank-specific category
    if "interestincome" in tag_lower:
        category = "01. Revenue"
        subcategory = "Interest Income"
    elif "noninterestincome" in tag_lower or "feeincome" in tag_lower:
        category = "01. Revenue"
        subcategory = "Non-Interest Income"
    elif "interestexpense" in tag_lower:
        category = "02. Cost of Revenue"
        subcategory = "Interest Expense"
    elif "provisionforloanlosses" in tag_lower or "loanloss" in tag_lower or "creditloss" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Provision for Credit Losses"
    elif "noninterestexpense" in tag_lower or "generalandadministrative" in tag_lower:
        category = "04. Operating Expenses"
        subcategory = "Non-Interest Expense"
    elif "operatingincome" in tag_lower:
        category = "05. Operating Income"
    elif "investment" in tag_lower or "othernonoperating" in tag_lower or "otherincomeexpense" in tag_lower:
        category = "06. Non-operating Items"
        subcategory = "Other Gains/Losses"
    elif "beforeincometax" in tag_lower or "incomebeforetax" in tag_lower:
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

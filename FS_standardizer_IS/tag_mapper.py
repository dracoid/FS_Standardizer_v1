# FS_standardizer_IS/tag_mapper.py
from .general_mapper import classify_general
from .sector.auto_mapper import classify_auto
from .sector.bank_mapper import classify_bank
from .sector.biotech_mapper import classify_biotech
from .sector.telecom_mapper import classify_telecom


def classify_income_statement_entry(tag, segments, plabel, stmt, sic=None):
    """
    Classifies income statement items into 4 levels:
    category, subcategory, identifier, and identifier_label.

    Parameters:
        tag (str): XBRL tag
        segments (str): XBRL segment information
        plabel (str): Plain label (human-readable)
        stmt (str): Statement type (only processes "IS")
        sic (int or str, optional): SIC code for industry classification

    Returns:
        category (str): Main category (e.g., "1. Revenue")
        subcategory (str): Subcategory within the main category
        identifier (str): Combined identifier using segments and plabel
        identifier_label (str): Unique label combining identifier and tag
    """
    if stmt != "IS":
        return None, None, None, None

    # Industry-specific mapper (based on SIC code)
    if sic:
        sic_str = str(sic)

        if sic_str.startswith("37"):  # Auto/machinery
            return classify_auto(tag, segments, plabel)
        elif sic_str.startswith(("60", "61", "62")):  # Banking/Finance
            return classify_bank(tag, segments, plabel)
        elif sic_str.startswith("28"):  # Biotech/Pharma
            return classify_biotech(tag, segments, plabel)
        elif sic_str.startswith("48"):  # Telecom
            return classify_telecom(tag, segments, plabel)

    # Default general mapper
    return classify_general(tag, segments, plabel)

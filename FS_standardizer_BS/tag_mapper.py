from .general_mapper import classify_general_bs
from .sector.bank_mapper import classify_bank_bs
from .sector.insurance_mapper import classify_insurance_bs
from .sector.securities_mapper import classify_securities_bs
from .sector.reit_mapper import classify_reit_bs
from .sector.utilities_mapper import classify_utilities_bs


def classify_balance_sheet_entry(tag: str, segments: str, plabel: str, stmt: str, sic: str = None):
    """
    Classifies balance sheet items into category, subcategory, identifier, and label.

    Parameters:
        tag (str): XBRL tag
        segments (str): Segment string (e.g., "[Total]")
        plabel (str): Human-readable label
        stmt (str): Statement type (only processes "BS")
        sic (str or int, optional): SIC code for industry classification

    Returns:
        (category, subcategory, identifier, identifier_label) as tuple,
        or (None, None, None, None) if stmt != "BS"
    """
    if stmt.upper() != "BS":
        return None, None, None, None

    # ✅ 업종별 분기
    if sic:
        sic_str = str(sic)
        if sic_str.startswith("60"):
            return classify_bank_bs(tag, segments, plabel)
        elif sic_str.startswith("63"):
            return classify_insurance_bs(tag, segments, plabel)
        elif sic_str.startswith("62"):
            return classify_securities_bs(tag, segments, plabel)
        elif sic_str.startswith("65"):
            return classify_reit_bs(tag, segments, plabel)
        elif sic_str.startswith("49"):
            return classify_utilities_bs(tag, segments, plabel)

    # ✅ 기본 분류 로직
    return classify_general_bs(tag, segments, plabel)

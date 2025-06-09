"""
general_mapper – 산업 공통 주식·지분변동표(EQ) 매퍼
결과: (category, subcategory, identifier, identifier_label)
카테고리 체계
    01. Opening Balance
    02. Issuances & Exercises
    03. Repurchases & Reductions
    04. Dividends / Distributions
    05. OCI / AOCI & FX
    06. Other Adjustments
    99. Unclassified   (모두 None 반환 시 upstream 에서 부여)
"""

from __future__ import annotations
from FS_standardizer_EQ.utils.helper import clean_text

# ────────────────────────────────────────────────────────────────
# 키워드 묶음 (전부 소문자 substrings) – 필요시 자유롭게 확장
# ────────────────────────────────────────────────────────────────
_OPENING     = ("balancebeginning", "beginningofperiod", "openingbalance")
_ENDING      = ("balanceend", "endofperiod", "endingbalance")

_ISSUANCE    = ("sharesissued", "stockissued", "issuanceofcommon", "exercisesofoptions")
_STOCK_COMP  = ("stockbasedcompensation", "sharebasedcompensation")

_REPURCHASE  = ("repurchaseofcommon", "treasurystock", "sharesrepurchased")
_STOCK_SPLIT = ("stocksplit", "stockdividend")

_DIVIDEND    = ("dividend", "distribution", "returnofcapital")

_OCI         = ("othercomprehensiveincome", "accumulatedother", "foreigncurrencytranslation")
_AOCI_RECLS  = ("reclassification", "aocireclassification")

_OTHER       = ("noncontrollinginterest", "entitytransactionswithowners", "equitycomponentadjustment")

# ────────────────────────────────────────────────────────────────
def _build(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"


def classify_general_eq(tag: str, segments: str | None, plabel: str | None):  # noqa: C901
    t = tag.lower()

    # 01. Opening / Ending (먼저 체크 – 표준 라인)
    if any(k in t for k in _OPENING): return _build("01. Opening Balance", "010. Opening Balance", segments, plabel, tag)
    if any(k in t for k in _ENDING):  return _build("06. Other Adjustments", "601. Ending Balance", segments, plabel, tag)

    # 02. Issuance
    if any(k in t for k in _ISSUANCE):   return _build("02. Issuances & Exercises", "120. Shares / Options Issued", segments, plabel, tag)
    if any(k in t for k in _STOCK_COMP): return _build("02. Issuances & Exercises", "121. Stock-based Compensation", segments, plabel, tag)

    # 03. Repurchase
    if any(k in t for k in _REPURCHASE): return _build("03. Repurchases & Reductions", "310. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _STOCK_SPLIT):return _build("03. Repurchases & Reductions", "320. Stock Split / Dividend", segments, plabel, tag)

    # 04. Dividends
    if any(k in t for k in _DIVIDEND):   return _build("04. Dividends / Distributions", "410. Cash / Stock Dividends", segments, plabel, tag)

    # 05. OCI
    if any(k in t for k in _OCI):        return _build("05. OCI & FX", "510. OCI Movements", segments, plabel, tag)
    if any(k in t for k in _AOCI_RECLS): return _build("05. OCI & FX", "520. AOCI Reclassifications", segments, plabel, tag)

    # 06. Other
    if any(k in t for k in _OTHER):      return _build("06. Other Adjustments", "600. Other Equity Adjustments", segments, plabel, tag)

    # None ⇒ Unclassified
    return None, None, None, None


# 외부 export 이름
classify_general = classify_general_eq
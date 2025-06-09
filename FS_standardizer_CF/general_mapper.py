# FS_standardizer_CF/general_mapper.py
"""
Industry-agnostic CF mapper – 3-digit sub-code 체계
"""
from __future__ import annotations
from FS_standardizer_CF.utils.helper import clean_text

# ── 키워드 bucket (보강 포함) ─────────────────────────────────────────────
_OP_INT_PAID   = ("cashpaidforinterest", "interestpaid")
_OP_TAX_PAID   = ("cashpaidforincome", "incometaxespaid")
_OP_STOCK_COMP = ("stockbasedcompensation", "sharebasedcompensation", "stockbasedcompensationnet")
_OP_NET_CASH   = (
    "netcashprovidedbyusedinoperatingactivities",
    "netcashprovidedbyusedinoperatingactivitiescontinuingoperations",
    "netcashprovidedbyusedinoperatingactivitiesdiscontinuedoperations",
    "cashgeneratedfromoperations",
)

_INV_CAPEX     = (
    "capitalexpenditure", "capitalexpenditures",
    "paymentstoacquirepropertyplantandequipment",
)
_INV_PURCHASE  = (
    "purchasesofinvestments", "purchaseofsecurities", "purchaseofmarketablesecurities",
)
_INV_PROCEEDS  = (
    "proceedsfromsaleofassets", "proceedsfrommaturity",
    "proceedsfromsaleandmaturityofmarketablesecurities",
)
_INV_NET_CASH  = (
    "netcashprovidedbyusedininvestingactivities",
    "netcashprovidedbyusedininvestingactivitiescontinuingoperations",
)

_FIN_DIVIDEND  = ("dividendspaid", "cashdividends")
_FIN_REPURCHASE= ("repurchaseofcommonstock", "treasurystock")
_FIN_DEBT_PROC = ("proceedsfromissuanceofdebt", "proceedsfromdebt")
_FIN_NET_CASH  = (
    "netcashprovidedbyusedinfinancingactivities",
    "netcashprovidedbyusedinfinancingactivitiescontinuingoperations",
)

_SUPPL_EFFECT  = (
    "effectofexchangeratechangesoncash",
    "effectofexchangerateoncashandequivalents",
)
_SUPPL_NONCASH = (
    "noncashinvestingandfinancingactivities",
    "supplementalscheduleofnoncashinvestingandfinancingactivities",
)

# ── helper ───────────────────────────────────────────────────────────────
def _build(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"

# ── public mapper ────────────────────────────────────────────────────────
def classify_general_cf(tag: str, segments: str | None, plabel: str | None):  # noqa
    t = tag.lower()

    # Operating
    if any(k in t for k in _OP_INT_PAID):
        return _build("01. Operating Activities", "191. Interest Paid", segments, plabel, tag)
    if any(k in t for k in _OP_TAX_PAID):
        return _build("01. Operating Activities", "193. Income Taxes Paid", segments, plabel, tag)
    if any(k in t for k in _OP_STOCK_COMP):
        return _build("01. Operating Activities", "150. Stock-based Compensation", segments, plabel, tag)
    if any(k in t for k in _OP_NET_CASH):
        return _build("01. Operating Activities", "199. Net Cash from Operating", segments, plabel, tag)

    # Investing
    if any(k in t for k in _INV_CAPEX):
        return _build("02. Investing Activities", "210. Capital Expenditures", segments, plabel, tag)
    if any(k in t for k in _INV_PURCHASE):
        return _build("02. Investing Activities", "240. Securities Purchased", segments, plabel, tag)
    if any(k in t for k in _INV_PROCEEDS):
        return _build("02. Investing Activities", "241. Securities Proceeds", segments, plabel, tag)
    if any(k in t for k in _INV_NET_CASH):
        return _build("02. Investing Activities", "299. Net Cash from Investing", segments, plabel, tag)

    # Financing
    if any(k in t for k in _FIN_DIVIDEND):
        return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)
    if any(k in t for k in _FIN_REPURCHASE):
        return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DEBT_PROC):
        return _build("03. Financing Activities", "340. Proceeds from Debt", segments, plabel, tag)
    if any(k in t for k in _FIN_NET_CASH):
        return _build("03. Financing Activities", "399. Net Cash from Financing", segments, plabel, tag)

    # Supplemental
    if any(k in t for k in _SUPPL_EFFECT):
        return _build("04. Supplemental", "410. FX Effect on Cash", segments, plabel, tag)
    if any(k in t for k in _SUPPL_NONCASH):
        return _build("04. Supplemental", "420. Non-cash Invest & Finance", segments, plabel, tag)

    # Unclassified
    return None, None, None, None

# alias
classify_general = classify_general_cf
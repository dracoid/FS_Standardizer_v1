# FS_standardizer_CF/sector/tech_mapper.py
"""
Tech-sector CF mapper – Software / Internet / Hardware
"""
from __future__ import annotations
from FS_standardizer_CF.general_mapper import classify_general
from FS_standardizer_CF.utils.helper import clean_text

# Keyword buckets
_OP_CAP_SOFT_DEV = (
    "capitalizedsoftwaredevelopmentcosts", "capitalizedsoftwaredevelopment",
    "capitalizedsoftwaresize",
)
_OP_STOCK_COMP = (
    "stockbasedcompensation", "sharebasedcompensation", "stockbasedcompensationnet",
)

_INV_MKT_SEC_PUR = (
    "purchaseofmarketablesecurities", "purchasesofavailableforsale",
    "purchaseoftradingsecurities",
)
_INV_MKT_SEC_PRO = (
    "proceedsfromsaleofmarketablesecurities", "proceedsfrommaturityofmarketablesecurities",
    "proceedsfromsaleandmaturityofmarketablesecurities",
)
_INV_INTANGIBLE = ("purchaseofintangibleassets", "intangibleassetsacquired")
_INV_BUS_COMB   = (
    "paymentforbusinesscombination", "acquisitionofbusiness",
    "paymentstoacquirebusinesses",
)

_FIN_SHARE_REPUR = ("repurchasecommonstock", "treasurystock")
_FIN_DIVIDENDS   = ("dividendspaid", "cashdividends")

_SUPPLEMENTAL = (
    "effectofexchangerateoncashandequivalents", "exchangerate", "fxeffect", "noncash",
)

# Helper
def _build(cat, sub, seg, pl, tag):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"

# Public mapper
def classify_tech_cf(tag, segments, plabel):  # noqa
    t = tag.lower()

    # Operating
    if any(k in t for k in _OP_CAP_SOFT_DEV):
        return _build("01. Operating Activities", "118. Capitalised Software Dev Costs", segments, plabel, tag)
    if any(k in t for k in _OP_STOCK_COMP):
        return _build("01. Operating Activities", "150. Stock-based Compensation", segments, plabel, tag)

    # Investing
    if any(k in t for k in _INV_INTANGIBLE):
        return _build("02. Investing Activities", "220. Purchase of Intangible Assets", segments, plabel, tag)
    if any(k in t for k in _INV_BUS_COMB):
        return _build("02. Investing Activities", "230. Business Combinations", segments, plabel, tag)
    if any(k in t for k in _INV_MKT_SEC_PUR):
        return _build("02. Investing Activities", "240. Securities Purchased", segments, plabel, tag)
    if any(k in t for k in _INV_MKT_SEC_PRO):
        return _build("02. Investing Activities", "241. Securities Proceeds", segments, plabel, tag)

    # Financing
    if any(k in t for k in _FIN_SHARE_REPUR):
        return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DIVIDENDS):
        return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)

    # Supplemental
    if any(k in t for k in _SUPPLEMENTAL):
        return _build("04. Supplemental", "420. Other / FX / Non-cash", segments, plabel, tag)

    # Fallback
    return classify_general(tag, segments, plabel)

__all__ = ["classify_tech_cf"]
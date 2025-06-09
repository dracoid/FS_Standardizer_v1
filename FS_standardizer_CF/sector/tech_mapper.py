"""tech_mapper.py – CF mapper for **Technology / Software / Internet** companies

특징
────
* CAPEX 비중 < **무형자산(소프트웨어·IP) 투자** 비중 → Intangible, Capitalized Dev.
* 대형 Tech는 **증권투자**(Marketable securities) 매입·매도 빈번.
* 잦은 M&A → Business Combination 항목 자주 등장.
"""
from __future__ import annotations

from FS_standardizer_CF.general_mapper import classify_general  # fallback
from FS_standardizer_CF.utils.helper import clean_text

# ---------------------------------------------------------------------------
# Keyword buckets
# ---------------------------------------------------------------------------

_OP_CAP_SOFT_DEV  = ("capitalizedsoftwaresize", "capitalizedsoftwaredevelopmentcosts")
_OP_STOCK_COMP    = ("stockbasedcompensation", "sharebasedcompensation")

_INV_MKT_SEC_PUR  = ("purchaseofmarketablesecurities", "purchasesofavailableforsale")
_INV_MKT_SEC_PRO  = ("proceedsfromsaleofmarketablesecurities", "proceedsfrommaturityofmarketablesecurities")
_INV_INTANGIBLE   = ("purchaseofintangibleassets", "intangibleassetsacquired")
_INV_BUS_COMB     = ("paymentforbusinesscombination", "acquisitionofbusiness")

_FIN_SHARE_REPUR  = ("repurchasecommonstock", "treasurystock")
_FIN_DIVIDENDS    = ("dividendspaid", "cashdividends")

_SUPPLEMENTAL     = ("exchangerate", "noncash", "fxeffect")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _build(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    identifier = f"[{seg}] | {pl}"
    return cat, sub, identifier, f"{identifier} | {clean_text(tag)}"


# ---------------------------------------------------------------------------
# Public mapper
# ---------------------------------------------------------------------------

def classify_tech_cf(tag: str, segments: str | None, plabel: str | None):  # noqa: C901
    t = tag.lower()

    # ── Operating ───────────────────────────────────────────────────────────
    if any(k in t for k in _OP_CAP_SOFT_DEV):
        return _build("01. Operating Activities", "118. Capitalised Software Dev Costs", segments, plabel, tag)
    if any(k in t for k in _OP_STOCK_COMP):
        return _build("01. Operating Activities", "150. Stock-based Compensation", segments, plabel, tag)

    # ── Investing ───────────────────────────────────────────────────────────
    if any(k in t for k in _INV_INTANGIBLE):
        return _build("02. Investing Activities", "220. Purchase of Intangible Assets", segments, plabel, tag)
    if any(k in t for k in _INV_BUS_COMB):
        return _build("02. Investing Activities", "230. Business Combinations", segments, plabel, tag)
    if any(k in t for k in _INV_MKT_SEC_PUR):
        return _build("02. Investing Activities", "240. Securities Purchased", segments, plabel, tag)
    if any(k in t for k in _INV_MKT_SEC_PRO):
        return _build("02. Investing Activities", "241. Securities Proceeds", segments, plabel, tag)

    # ── Financing ───────────────────────────────────────────────────────────
    if any(k in t for k in _FIN_SHARE_REPUR):
        return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DIVIDENDS):
        return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)

    # ── Supplemental ────────────────────────────────────────────────────────
    if any(k in t for k in _SUPPLEMENTAL):
        return _build("04. Supplemental", "420. Other / FX / Non-cash", segments, plabel, tag)

    # ── Fallback ────────────────────────────────────────────────────────────
    return classify_general(tag, segments, plabel)


__all__ = ["classify_tech_cf"]
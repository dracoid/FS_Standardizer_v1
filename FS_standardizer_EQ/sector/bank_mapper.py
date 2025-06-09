# FS_standardizer_EQ/sector/bank_mapper.py

"""
bank_mapper.py – EQ mapper for **Banks / Depository Institutions**
(보강 버전)
"""
from __future__ import annotations

from FS_standardizer_EQ.general_mapper import classify_general
from FS_standardizer_EQ.utils.helper import clean_text

# ─────────────────────────────────────────────────────────────
# keyword buckets (lower-case)
# ─────────────────────────────────────────────────────────────
_BANK_PREFERRED     = ("preferredstock", "series", "noncumulative")
_ISSUANCE_COMMON    = ("commonstockissued", "commonsharesissued")
_TDR_ISSUANCE       = ("tdr", "troubleddebtrestructuring")
_STOCK_SPLIT        = ("stocksplit", "stockdividend")
_REPURCHASE_CANCEL  = ("treasurystockcancel", "retired", "repurchaseofcommon")
_CECL               = ("cecladjustment", "allowanceforcredit")

_OCI_AFS            = ("availableforsale", "afsgainloss")
_OCI_PENSION        = ("pension", "postretirement")
_REG_CAP            = ("restrictedcorecapital", "atrisk")

# ─────────────────────────────────────────────────────────────
def _b(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    i   = f"[{seg}] | {pl}"
    return cat, sub, i, f"{i} | {clean_text(tag)}"

# ─────────────────────────────────────────────────────────────
def classify_bank_eq(tag: str, segments: str | None, plabel: str | None):
    lo = tag.lower()

    # 02 Issuances & Exercises
    if any(k in lo for k in _BANK_PREFERRED):
        return _b("02. Issuances & Exercises", "122. Preferred Stock Issued", segments, plabel, tag)
    if any(k in lo for k in _ISSUANCE_COMMON):
        return _b("02. Issuances & Exercises", "120. Common Shares Issued", segments, plabel, tag)
    if any(k in lo for k in _TDR_ISSUANCE):
        return _b("02. Issuances & Exercises", "124. TDR-related Issuance", segments, plabel, tag)
    if any(k in lo for k in _STOCK_SPLIT):
        return _b("03. Repurchases & Reductions", "320. Stock Split / Dividend", segments, plabel, tag)

    # 03 Repurchases
    if any(k in lo for k in _REPURCHASE_CANCEL):
        return _b("03. Repurchases & Reductions", "310. Share Repurchase / Cancel", segments, plabel, tag)

    # 05 OCI
    if any(k in lo for k in _OCI_AFS):
        return _b("05. OCI & FX", "511. Unrealised AFS Gains/Losses", segments, plabel, tag)
    if any(k in lo for k in _OCI_PENSION):
        return _b("05. OCI & FX", "514. Pension OCI Adjustments", segments, plabel, tag)

    # 06 Other Adjustments
    if any(k in lo for k in _CECL):
        return _b("06. Other Adjustments", "630. CECL Day-1 Adjustment", segments, plabel, tag)
    if any(k in lo for k in _REG_CAP):
        return _b("06. Other Adjustments", "640. Regulatory Capital Adj.", segments, plabel, tag)

    # fallback
    return classify_general(tag, segments, plabel)


__all__ = ["classify_bank_eq"]
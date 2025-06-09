"""
energy_mapper.py – EQ mapper for **Energy / Oil & Gas / Mining** (SIC 10xx·13xx·29xx)
──────────────────────────────────────────────────────────────────────────────────────
특화 포인트
  • **Asset-Retirement-Obligation (ARO)** 및 **Decommissioning** 조정
  • **Share-based Royalty / Production-Related** 주식발행
  • 외화환산(Upstream 해외사업) OCI 비중이 큼
"""
from __future__ import annotations

from FS_standardizer_EQ.general_mapper import classify_general
from FS_standardizer_EQ.utils.helper import clean_text

# ────────────────────────────────────────────────────────────
# keyword buckets
# ────────────────────────────────────────────────────────────
_OPENING = ("openingbalance", "balancebeginning")

# Issuances
_ISSUANCE_SCRIP      = ("sharesissued", "stockissued")
_ISSUANCE_ROYALTY    = ("royaltyinterest", "override", "productionpayment")
_STOCK_COMP          = ("stockbasedcompensation", "sharebasedcompensation")

# Repurchase / Split
_REPURCHASE          = ("repurchaseofcommon", "treasurystock")
_SPLIT               = ("stocksplit",)

# Dividends
_DIVIDEND            = ("dividend", "distribution")

# OCI
_OCI_FX              = ("foreigncurrencytranslation", "cumulativetranslation")
_OCI_CASHFLOW_HEDGE  = ("cashflowhedge", "derivative")

# ARO & Decommissioning Adj.
_ARO_ACC             = ("assetretirementobligation", "dismantling", "abandonment", "decommissioning")

# Non-controlling Interest – often with JVs
_NCI                 = ("noncontrollinginterest", "minorityinterest")

# ────────────────────────────────────────────────────────────
def _b(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    i   = f"[{seg}] | {pl}"
    return cat, sub, i, f"{i} | {clean_text(tag)}"

# ────────────────────────────────────────────────────────────
def classify_energy_eq(tag: str, segments: str | None, plabel: str | None):
    lo = tag.lower()

    # Opening
    if any(k in lo for k in _OPENING):
        return _b("01. Opening Balance", "010. Opening Balance", segments, plabel, tag)

    # Issuances
    if any(k in lo for k in _ISSUANCE_ROYALTY):
        return _b("02. Issuances & Exercises", "124. Royalty / Production Shares", segments, plabel, tag)
    if any(k in lo for k in _ISSUANCE_SCRIP):
        return _b("02. Issuances & Exercises", "120. Shares / Scrip Issued", segments, plabel, tag)
    if any(k in lo for k in _STOCK_COMP):
        return _b("02. Issuances & Exercises", "121. Stock-based Compensation", segments, plabel, tag)

    # Repurchase
    if any(k in lo for k in _REPURCHASE):
        return _b("03. Repurchases & Reductions", "310. Share Repurchase", segments, plabel, tag)
    if any(k in lo for k in _SPLIT):
        return _b("03. Repurchases & Reductions", "320. Stock Split", segments, plabel, tag)

    # Dividends
    if any(k in lo for k in _DIVIDEND):
        return _b("04. Dividends / Distributions", "410. Cash / Scrip Dividends", segments, plabel, tag)

    # OCI
    if any(k in lo for k in _OCI_FX):
        return _b("05. OCI & FX", "513. FX Translation OCI", segments, plabel, tag)
    if any(k in lo for k in _OCI_CASHFLOW_HEDGE):
        return _b("05. OCI & FX", "512. Derivative / Hedge OCI", segments, plabel, tag)

    # ARO / Decommissioning
    if any(k in lo for k in _ARO_ACC):
        return _b("06. Other Adjustments", "640. ARO / Decommissioning Adj.", segments, plabel, tag)

    # NCI
    if any(k in lo for k in _NCI):
        return _b("06. Other Adjustments", "650. Non-controlling Interest", segments, plabel, tag)

    # fallback
    return classify_general(tag, segments, plabel)


__all__ = ["classify_energy_eq"]
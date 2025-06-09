"""
insurance_mapper.py – EQ mapper for **Insurance (SIC 63xx)**
─────────────────────────────────────────────────────────────
보험사는 일반기업과 달리
    • **AOCI** 변동(‘Unrealized Investment Gains/Losses’) 규모가 매우 큽니다.
    • **Policyholder Dividend / Rebate** 가 Equity 표에 직접 기재됩니다.
    • **Non-Controlling Interest** = Separate Account 관련 조정치가 자주 등장합니다.
본 모듈은 그러한 태그를 우선적으로 분류하고, 매칭 실패 시
`FS_standardizer_EQ.general_mapper.classify_general` 로 위임합니다.
"""
from __future__ import annotations

from FS_standardizer_EQ.general_mapper import classify_general
from FS_standardizer_EQ.utils.helper import clean_text

# ────────────────────────────────────────────────────────────
# 1) Keyword buckets (모두 lower-case substrings)
# ────────────────────────────────────────────────────────────
_OPENING = ("balancebeginning", "openingbalance")

# Issuances / Exercises
_ISSUANCE_PREFERRED  = ("preferredstockissued", "surplusnotesissued")
_STOCK_COMP          = ("stockbasedcompensation", "sharebasedcompensation")

# Repurchase / Reduction
_REDEMPTION          = ("redemptionofpreferred", "repurchaseofcommon", "treasurystock")
_STOCK_SPLIT         = ("stocksplit", "stockdividend")

# Dividends / Policyholder Dividend
_DIVIDEND            = ("dividend", "policyholderdividend", "policyholderrebate")

# OCI (Unrealised Inv. gains/losses, FX, Cash-flow hedge 등)
_OCI_INV_GAIN        = ("unrealizedinvestmentgainloss", "unrealisedinvestmentgainloss")
_OCI_DERIV_HEDGE     = ("cashflowhedge", "derivativegainloss")
_OCI_FX              = ("foreigncurrencytranslation",)

# AOCI reclassification
_AOCI_RECLASS        = ("reclassificationoutofaoci", "reclassificationoutofaccumulatedother")

# Other Adjustments
_NCI_SEPA            = ("separateaccount", "noncontrollinginterest")
_ACTUARIAL           = ("pensionadjustments", "postretirementbenefit")

# ────────────────────────────────────────────────────────────
def _b(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl  or "[Unlabeled]"
    i   = f"[{seg}] | {pl}"
    return cat, sub, i, f"{i} | {clean_text(tag)}"

# ────────────────────────────────────────────────────────────
def classify_insurance_eq(tag: str, segments: str | None, plabel: str | None):
    t = tag.lower()

    # Opening Balance
    if any(k in t for k in _OPENING):
        return _b("01. Opening Balance", "010. Opening Balance", segments, plabel, tag)

    # 02 Issuances
    if any(k in t for k in _ISSUANCE_PREFERRED):
        return _b("02. Issuances & Exercises", "123. Preferred / Surplus Issued", segments, plabel, tag)
    if any(k in t for k in _STOCK_COMP):
        return _b("02. Issuances & Exercises", "121. Stock-based Compensation", segments, plabel, tag)

    # 03 Repurchase / Redemption
    if any(k in t for k in _REDEMPTION):
        return _b("03. Repurchases & Reductions", "311. Share / Note Redemption", segments, plabel, tag)
    if any(k in t for k in _STOCK_SPLIT):
        return _b("03. Repurchases & Reductions", "320. Stock Split / Dividend", segments, plabel, tag)

    # 04 Dividends
    if any(k in t for k in _DIVIDEND):
        return _b("04. Dividends / Distributions", "420. Cash / Policyholder Dividends", segments, plabel, tag)

    # 05 OCI & FX
    if any(k in t for k in _OCI_INV_GAIN):
        return _b("05. OCI & FX", "511. Unrealised Inv. Gains/Losses", segments, plabel, tag)
    if any(k in t for k in _OCI_DERIV_HEDGE):
        return _b("05. OCI & FX", "512. Derivative / Hedge OCI", segments, plabel, tag)
    if any(k in t for k in _OCI_FX):
        return _b("05. OCI & FX", "513. FX Translation OCI", segments, plabel, tag)
    if any(k in t for k in _AOCI_RECLASS):
        return _b("05. OCI & FX", "520. AOCI Reclassifications", segments, plabel, tag)

    # 06 Other
    if any(k in t for k in _NCI_SEPA):
        return _b("06. Other Adjustments", "610. Separate Account / NCI", segments, plabel, tag)
    if any(k in t for k in _ACTUARIAL):
        return _b("06. Other Adjustments", "620. Actuarial & Pension Adj.", segments, plabel, tag)

    # fallback
    return classify_general(tag, segments, plabel)


__all__ = ["classify_insurance_eq"]
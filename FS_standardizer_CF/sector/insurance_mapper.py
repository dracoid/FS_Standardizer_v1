# FS_standardizer_CF/sector/insurance_mapper.py

"""insurance_mapper.py – CF mapper for **Insurance Companies**

보험업은 현금흐름이 ① 보험료 유입 ② 클레임/급부 유출 ③ 리인슈어런스 거래 ④ 투자
포트폴리오 활동 등으로 구성된다. 3-자리 코드 체계를 적용해 subcategory 를 반환.
"""
from __future__ import annotations

from FS_standardizer_CF.general_mapper import classify_general  # fallback
from FS_standardizer_CF.utils.helper import clean_text

# ---------------------------------------------------------------------------
# Keyword buckets
# ---------------------------------------------------------------------------

_OP_PREMIUM_IN      = ("premiumswritten", "premiumsreceived", "policyfees")
_OP_CLAIM_OUT       = ("claimspaid", "benefitspaid", "lossespayments")
_OP_REINSURANCE_IN  = ("cededreinsurance", "recoveries")
_OP_REINSURANCE_OUT = ("cededpremiumspaid", "reinsurancepremium")
_OP_ACQ_COST        = ("policyacquisitioncost", "commissionspaid")
_OP_RESERVE_CHG     = ("changepolicyreserves", "reservesinc", "reservechange")

_INV_SECURITIES_PUR = ("purchaseofinvestments", "purchaseofsecurities")
_INV_SECURITIES_PRO = ("proceedsfromsaleofinvestments", "proceedsfrommaturity")
_INV_MORTGAGE_LOAN  = ("mortgageloansoriginated", "mortgageloanscollect")
_INV_OTHER          = ("realestateinvest", "partnershipinvest", "derivative")

_FIN_DEBT_IN        = ("proceedsfromdebt", "issuancedebt")
_FIN_DEBT_OUT       = ("repaymentofdebt", "debtmaturitypayment")
_FIN_DIVIDENDS      = ("dividendspaid", "cashdividends")
_FIN_SHARE_REPUR    = ("repurchasecommonstock", "treasurystock")

_SUPPLEMENTAL       = ("exchangerate", "noncash", "fxeffect")


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

def classify_insurance_cf(tag: str, segments: str | None, plabel: str | None):  # noqa: C901
    t = tag.lower()

    # ── Operating ───────────────────────────────────────────────────────────
    if any(k in t for k in _OP_PREMIUM_IN):
        return _build("01. Operating Activities", "112. Premiums Received", segments, plabel, tag)
    if any(k in t for k in _OP_CLAIM_OUT):
        return _build("01. Operating Activities", "113. Claims & Benefits Paid", segments, plabel, tag)
    if any(k in t for k in _OP_REINSURANCE_IN):
        return _build("01. Operating Activities", "114. Reinsurance Recoveries", segments, plabel, tag)
    if any(k in t for k in _OP_REINSURANCE_OUT):
        return _build("01. Operating Activities", "115. Reinsurance Premiums Paid", segments, plabel, tag)
    if any(k in t for k in _OP_ACQ_COST):
        return _build("01. Operating Activities", "116. Policy Acquisition Costs", segments, plabel, tag)
    if any(k in t for k in _OP_RESERVE_CHG):
        return _build("01. Operating Activities", "117. Change in Policy Reserves", segments, plabel, tag)

    # ── Investing ───────────────────────────────────────────────────────────
    if any(k in t for k in _INV_SECURITIES_PUR):
        return _build("02. Investing Activities", "240. Securities Purchased", segments, plabel, tag)
    if any(k in t for k in _INV_SECURITIES_PRO):
        return _build("02. Investing Activities", "241. Securities Proceeds", segments, plabel, tag)
    if any(k in t for k in _INV_MORTGAGE_LOAN):
        return _build("02. Investing Activities", "242. Mortgage Loans", segments, plabel, tag)
    if any(k in t for k in _INV_OTHER):
        return _build("02. Investing Activities", "249. Other Investments", segments, plabel, tag)

    # ── Financing ───────────────────────────────────────────────────────────
    if any(k in t for k in _FIN_DEBT_IN):
        return _build("03. Financing Activities", "340. Proceeds from Debt", segments, plabel, tag)
    if any(k in t for k in _FIN_DEBT_OUT):
        return _build("03. Financing Activities", "341. Repayment of Debt", segments, plabel, tag)
    if any(k in t for k in _FIN_SHARE_REPUR):
        return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DIVIDENDS):
        return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)

    # ── Supplemental ────────────────────────────────────────────────────────
    if any(k in t for k in _SUPPLEMENTAL):
        return _build("04. Supplemental", "420. Other / FX / Non-cash", segments, plabel, tag)

    # ── Fallback ────────────────────────────────────────────────────────────
    return classify_general(tag, segments, plabel)


__all__ = ["classify_insurance_cf"]
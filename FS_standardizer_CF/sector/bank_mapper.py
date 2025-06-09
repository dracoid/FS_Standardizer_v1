"""bank_mapper.py – CF mapper for **Banks & Depository Institutions**

은행업 CF는 예금·대출 흐름 때문에 일반 기업과 달리
Financing(Deposits/Borrowings) ‧ Operating(Interest/Loans) 항목이 혼합된다.
본 매퍼는 **3-자리 코드 + 라벨** 체계를 사용해 subcategory를 반환한다.
"""
from __future__ import annotations

from FS_standardizer_CF.general_mapper import classify_general  # fallback
from FS_standardizer_CF.utils.helper import clean_text

# ---------------------------------------------------------------------------
# Keyword buckets – 최소 키워드 우선, 추후 확장 가능
# ---------------------------------------------------------------------------

# Operating
_OP_INTEREST_IN    = ("interestreceived", "interestincome")
_OP_INTEREST_OUT   = ("interestpaid", "interestexpense")
_OP_LOAN_ORIG      = ("loansoriginated", "loanfunding", "loanadvances")
_OP_LOAN_PRINC_INC = ("loanprincipalcollected", "repaymentofloans")
_OP_CREDIT_LOSS    = ("provisionforloanloss", "creditloss", "allowanceforcredit")

# Investing
_INV_SECURITIES_PUR = ("purchase", "acquisition")
_INV_SECURITIES_PRO = ("sale", "proceeds", "maturity")
_INV_CAPEX          = ("premises", "equipment", "capitalexpenditure")

# Financing
_FIN_DEPOSITS_INC = ("increaseindeposits", "depositreceived")
_FIN_DEPOSITS_DEC = ("decreaseindeposits", "depositwithdrawal")
_FIN_DEBT_INC     = ("proceedsfromborrowings", "issuancedebt", "fhlbadvances")
_FIN_DEBT_DEC     = ("repaymentofborrowings", "repaymentofdebt")
_FIN_DIVIDENDS    = ("dividendspaid", "cashdividends")
_FIN_SHARE_REPUR  = ("repurchasecommonstock", "treasurystock")

_SUPPLEMENTAL     = ("exchangerate", "noncash", "fxeffect")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _build(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl = pl or "[Unlabeled]"
    identifier = f"[{seg}] | {pl}"
    return cat, sub, identifier, f"{identifier} | {clean_text(tag)}"


# ---------------------------------------------------------------------------
# Public mapper
# ---------------------------------------------------------------------------

def classify_bank_cf(tag: str, segments: str | None, plabel: str | None):  # noqa: C901
    t = tag.lower()

    # ── Operating ───────────────────────────────────────────────────────────
    if any(k in t for k in _OP_INTEREST_IN):
        return _build("01. Operating Activities", "192. Interest Received", segments, plabel, tag)
    if any(k in t for k in _OP_INTEREST_OUT):
        return _build("01. Operating Activities", "191. Interest Paid", segments, plabel, tag)
    if any(k in t for k in _OP_LOAN_ORIG):
        return _build("01. Operating Activities", "180. Loans Originated", segments, plabel, tag)
    if any(k in t for k in _OP_LOAN_PRINC_INC):
        return _build("01. Operating Activities", "181. Loan Principal Collected", segments, plabel, tag)
    if any(k in t for k in _OP_CREDIT_LOSS):
        return _build("01. Operating Activities", "155. Provision for Credit Losses", segments, plabel, tag)

    # ── Investing ───────────────────────────────────────────────────────────
    if any(k in t for k in _INV_CAPEX):
        return _build("02. Investing Activities", "210. Premises & Equipment", segments, plabel, tag)
    if any(k in t for k in _INV_SECURITIES_PUR):
        return _build("02. Investing Activities", "240. Securities Purchased", segments, plabel, tag)
    if any(k in t for k in _INV_SECURITIES_PRO):
        return _build("02. Investing Activities", "241. Securities Proceeds", segments, plabel, tag)

    # ── Financing ───────────────────────────────────────────────────────────
    if any(k in t for k in _FIN_DEPOSITS_INC):
        return _build("03. Financing Activities", "360. Increase in Deposits", segments, plabel, tag)
    if any(k in t for k in _FIN_DEPOSITS_DEC):
        return _build("03. Financing Activities", "361. Decrease in Deposits", segments, plabel, tag)
    if any(k in t for k in _FIN_DEBT_INC):
        return _build("03. Financing Activities", "340. Borrowings Proceeds", segments, plabel, tag)
    if any(k in t for k in _FIN_DEBT_DEC):
        return _build("03. Financing Activities", "341. Borrowings Repayment", segments, plabel, tag)
    if any(k in t for k in _FIN_SHARE_REPUR):
        return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DIVIDENDS):
        return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)

    # ── Supplemental ────────────────────────────────────────────────────────
    if any(k in t for k in _SUPPLEMENTAL):
        return _build("04. Supplemental", "420. Other / FX / Non-cash", segments, plabel, tag)

    # ── Fallback ────────────────────────────────────────────────────────────
    return classify_general(tag, segments, plabel)


__all__ = ["classify_bank_cf"]
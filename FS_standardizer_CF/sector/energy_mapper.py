# FS_standardizer_CF/sector/energy_mapper.py

"""energy_mapper.py – CF mapper for **Energy / Oil & Gas / Mining**

• Exploration / Development CAPEX 는 Investing 이 기본, 일부 Operating 예외 처리
• Asset Retirement Obligation(ARO) / Abandonment 정산은 Financing 에 배치
• 3-자리 코드 체계 사용 (210, 352 …) → IS/BS 와 통일
"""
from __future__ import annotations

from FS_standardizer_CF.general_mapper import classify_general  # fallback
from FS_standardizer_CF.utils.helper import clean_text

# ---------------------------------------------------------------------------
# Keyword buckets
# ---------------------------------------------------------------------------

_OP_PROD_TAX   = ("productiontax", "severancetax", "royaltypayment")
_OP_EXPLR_EXP  = ("explorationexpense", "geological", "seismic")

_INV_CAPEX     = ("capitalexpenditure", "exploration", "development", "wellcompletion")
_INV_ACQUIRE   = ("acquisitionofproperties", "purchaseofinterests")
_INV_DISPOSE   = ("proceedsfromsaleofproperties", "assetdisposition")

_FIN_ABAND     = ("assetretirementobligationsettlement", "pluggingandabandonment", "dismantlingcosts")
_FIN_DIVIDEND  = ("dividendspaid", "cashdividends")
_FIN_REPUR     = ("repurchasecommonstock", "treasurystock")

_SUPPLEMENTAL  = ("exchangerate", "noncash", "aroaccretion", "fxeffect")


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

def classify_energy_cf(tag: str, segments: str | None, plabel: str | None):  # noqa: C901
    t = tag.lower()

    # ── Operating (rare) ────────────────────────────────────────────────────
    if any(k in t for k in _OP_PROD_TAX):
        return _build("01. Operating Activities", "175. Production & Severance Taxes", segments, plabel, tag)
    if any(k in t for k in _OP_EXPLR_EXP):
        return _build("01. Operating Activities", "176. Exploration Expense", segments, plabel, tag)

    # ── Investing ───────────────────────────────────────────────────────────
    if any(k in t for k in _INV_CAPEX):
        return _build("02. Investing Activities", "212. Exploration & Development CAPEX", segments, plabel, tag)
    if any(k in t for k in _INV_ACQUIRE):
        return _build("02. Investing Activities", "230. Acquisition of Mineral Rights", segments, plabel, tag)
    if any(k in t for k in _INV_DISPOSE):
        return _build("02. Investing Activities", "241. Proceeds from Asset Disposal", segments, plabel, tag)

    # ── Financing ───────────────────────────────────────────────────────────
    if any(k in t for k in _FIN_ABAND):
        return _build("03. Financing Activities", "352. ARO / Abandonment Settlement", segments, plabel, tag)
    if any(k in t for k in _FIN_REPUR):
        return _build("03. Financing Activities", "320. Share Repurchase", segments, plabel, tag)
    if any(k in t for k in _FIN_DIVIDEND):
        return _build("03. Financing Activities", "330. Dividends Paid", segments, plabel, tag)

    # ── Supplemental ────────────────────────────────────────────────────────
    if any(k in t for k in _SUPPLEMENTAL):
        return _build("04. Supplemental", "420. Other / FX / Non-cash", segments, plabel, tag)

    # ── Fallback ────────────────────────────────────────────────────────────
    return classify_general(tag, segments, plabel)


__all__ = ["classify_energy_cf"]

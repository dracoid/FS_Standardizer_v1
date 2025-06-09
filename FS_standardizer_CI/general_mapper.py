"""
Industry-agnostic mapper for **Statement of Comprehensive Income** (CI)

반환값: (category, subcategory, identifier, identifier_label)
* category  : 01. Net Income / 02. OCI / 03. Total Comprehensive / 04. Reclass Adj
* subcategory: 3-digit 세부 코드 + 라벨 (예: "120. OCI – AFS/FVOCI")
"""
from __future__ import annotations

from FS_standardizer_CI.utils.helper import clean_text


# ──────────────────────────────────────────────────────────────────────────────
# 키워드 버킷 (lower-case substring)
# ──────────────────────────────────────────────────────────────────────────────
_NET_INC           = ("netincomeloss", "netincome", "netincomelossavailable")
_TOTAL_COMP        = ("comprehensiveincomenetof", "totalcomprehensiveincome")
_OCI_AFS           = ("unrealizedgainlossonavailableforsalesecurities",
                      "othercomprehensiveincomefairvalue",
                      "unrealizedinvestmentgainloss")
_OCI_FX            = ("foreigncurrencytranslation", "cumulativeforeign", "fxtranslation")
_OCI_PENSION       = ("definedbenefit", "pension", "retirementbenefit")
_OCI_CASHFLOW_HDG  = ("cashflowhedge",)
_RECLASS_ADJ       = ("reclassification", "reclass", "amountreclassified")

# ──────────────────────────────────────────────────────────────────────────────
def _build(cat: str, sub: str, seg: str | None, pl: str | None, tag: str):
    seg = seg or "[Total]"
    pl  = pl or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"


def classify_general_ci(tag: str, segments: str | None, plabel: str | None):
    """fallback mapper (4-tuple)"""
    t = tag.lower()

    # 01 Net Income & Total Comprehensive (맨 위/맨 아래 줄)
    if any(k in t for k in _NET_INC):
        return _build("01. Net Income", "101. Net Income", segments, plabel, tag)
    if any(k in t for k in _TOTAL_COMP):
        return _build("03. Total Comprehensive", "301. Total Comprehensive", segments, plabel, tag)

    # 02 OCI 세부 분류
    if any(k in t for k in _OCI_AFS):
        return _build("02. Other Comprehensive Income", "120. OCI – AFS / FVOCI", segments, plabel, tag)
    if any(k in t for k in _OCI_FX):
        return _build("02. Other Comprehensive Income", "130. OCI – FX Translation", segments, plabel, tag)
    if any(k in t for k in _OCI_PENSION):
        return _build("02. Other Comprehensive Income", "140. OCI – Pension / DB Plans", segments, plabel, tag)
    if any(k in t for k in _OCI_CASHFLOW_HDG):
        return _build("02. Other Comprehensive Income", "150. OCI – Cash-Flow Hedge", segments, plabel, tag)

    # 04 Reclassification Adjustments
    if any(k in t for k in _RECLASS_ADJ):
        return _build("04. Reclass Adjustment", "410. Reclass Adjustment (OCI→NI)", segments, plabel, tag)

    # 미매핑
    return None, None, None, None


# 외부 노출명
classify_general = classify_general_ci
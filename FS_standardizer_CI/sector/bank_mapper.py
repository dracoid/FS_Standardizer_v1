"""
은행업 CI mapper – OCI 구성이 증권·현금흐름 헤지 비중이 높음
"""
from __future__ import annotations

from FS_standardizer_CI.general_mapper import classify_general  # fallback
from FS_standardizer_CI.utils.helper import clean_text


_OCI_AFS_DEBT      = ("debtsecurities", "afssecurities", "fvocisecurities")
_OCI_CREDIT        = ("allowanceforcreditloss",)
_OCI_CASHFLOW_HDG  = ("cashflowhedge",)
_OCI_FX            = ("foreigncurrencytranslation",)
_TOTAL_COMP        = ("totalcomprehensiveincome",)


def _build(cat, sub, seg, pl, tag):
    seg = seg or "[Total]"; pl = pl or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"


def classify_bank_ci(tag: str, segments: str | None, plabel: str | None):
    t = tag.lower()

    if any(k in t for k in _OCI_AFS_DEBT):
        return _build("02. Other Comprehensive Income", "122. OCI – AFS Debt Sec.", segments, plabel, tag)
    if any(k in t for k in _OCI_CREDIT):
        return _build("02. Other Comprehensive Income", "125. OCI – Credit Reserve", segments, plabel, tag)
    if any(k in t for k in _OCI_CASHFLOW_HDG):
        return _build("02. Other Comprehensive Income", "150. OCI – Cash-Flow Hedge", segments, plabel, tag)
    if any(k in t for k in _OCI_FX):
        return _build("02. Other Comprehensive Income", "130. OCI – FX Translation", segments, plabel, tag)
    if any(k in t for k in _TOTAL_COMP):
        return _build("03. Total Comprehensive", "301. Total Comprehensive", segments, plabel, tag)

    return classify_general(tag, segments, plabel)


__all__ = ["classify_bank_ci"]
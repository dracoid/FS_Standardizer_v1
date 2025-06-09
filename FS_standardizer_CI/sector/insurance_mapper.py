"""
보험업 CI mapper – 채권평가손익·보험부채 재측정(Discount Rate) 강조
"""
from __future__ import annotations

from FS_standardizer_CI.general_mapper import classify_general  # fallback
from FS_standardizer_CI.utils.helper import clean_text


_OCI_AFS_DEBT    = ("unrealizedgainlossonavailableforsalesecurities", "fvocibonds")
_OCI_FV_CHANGE   = ("changeinfairvalue", "fairvaluechange")
_OCI_PENSION     = ("pension", "retirementbenefit")
_OCI_FX          = ("foreigncurrencytranslation",)
_TOTAL_COMP      = ("totalcomprehensiveincome",)


def _build(cat, sub, seg, pl, tag):
    seg = seg or "[Total]"; pl = pl or "[Unlabeled]"
    ident = f"[{seg}] | {pl}"
    return cat, sub, ident, f"{ident} | {clean_text(tag)}"


def classify_insurance_ci(tag: str, segments: str | None, plabel: str | None):
    t = tag.lower()

    if any(k in t for k in _OCI_AFS_DEBT):
        return _build("02. Other Comprehensive Income", "121. OCI – AFS Bonds", segments, plabel, tag)
    if any(k in t for k in _OCI_FV_CHANGE):
        return _build("02. Other Comprehensive Income", "124. OCI – Fair-value Change", segments, plabel, tag)
    if any(k in t for k in _OCI_PENSION):
        return _build("02. Other Comprehensive Income", "140. OCI – Pension / DB Plans", segments, plabel, tag)
    if any(k in t for k in _OCI_FX):
        return _build("02. Other Comprehensive Income", "130. OCI – FX Translation", segments, plabel, tag)
    if any(k in t for k in _TOTAL_COMP):
        return _build("03. Total Comprehensive", "301. Total Comprehensive", segments, plabel, tag)

    return classify_general(tag, segments, plabel)


__all__ = ["classify_insurance_ci"]
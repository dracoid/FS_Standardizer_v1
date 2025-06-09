# FS_standardizer_CF/tag_mapper.py
"""
SIC → CF mapper dispatcher
"""
from __future__ import annotations
from typing import Callable, Optional, Tuple, TypeAlias

from FS_standardizer_CF.general_mapper import classify_general
from FS_standardizer_CF.utils.helper import clean_text  # re-export

CashTuple: TypeAlias = Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]

# lazy import helpers
def _lazy_bank():     from FS_standardizer_CF.sector.bank_mapper import classify_bank_cf;     return classify_bank_cf
def _lazy_insur():    from FS_standardizer_CF.sector.insurance_mapper import classify_insurance_cf; return classify_insurance_cf
def _lazy_energy():   from FS_standardizer_CF.sector.energy_mapper import classify_energy_cf;   return classify_energy_cf
def _lazy_tech():     from FS_standardizer_CF.sector.tech_mapper import classify_tech_cf;       return classify_tech_cf

# SIC tables
_BANK_SIC       = range(6000, 6100)
_INSURANCE_SIC  = range(6300, 6400)
_ENERGY_SIC: set[int] = set(range(1000, 1300)) | set(range(1300, 1400)) | set(range(2900, 3000))
_TECH_SIC:   set[int] = set(range(3570, 3580)) | set(range(7370, 7380))

def _select_mapper(sic: int | None) -> Callable[[str, str | None, str | None], CashTuple]:
    if sic is None:           return classify_general
    if sic in _BANK_SIC:      return _lazy_bank()
    if sic in _INSURANCE_SIC: return _lazy_insur()
    if sic in _ENERGY_SIC:    return _lazy_energy()
    if sic in _TECH_SIC:      return _lazy_tech()
    return classify_general

# public
def classify_cashflow_entry(tag: str, segments: str | None, plabel: str | None, *, sic: int | None = None) -> CashTuple:
    return _select_mapper(sic)(tag, segments, plabel)

__all__ = ["classify_cashflow_entry", "clean_text"]
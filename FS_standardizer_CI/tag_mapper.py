"""
Dispatcher – SIC 코드로 sector mapper 선택 → 기본은 general_mapper
"""
from __future__ import annotations

from typing import Callable, Optional, Tuple, TypeAlias

from FS_standardizer_CI.general_mapper import classify_general
from FS_standardizer_CI.utils.helper import clean_text  # re-export

CashTuple: TypeAlias = Tuple[
    Optional[str], Optional[str], Optional[str], Optional[str]
]


def _lazy_bank():      # 지연 import
    from FS_standardizer_CI.sector.bank_mapper import classify_bank_ci
    return classify_bank_ci


def _lazy_insurance():
    from FS_standardizer_CI.sector.insurance_mapper import classify_insurance_ci
    return classify_insurance_ci


# SIC 범위
_BANK_SIC       = range(6000, 6100)
_INSURANCE_SIC  = range(6300, 6400)


def _select_mapper(sic: int | None) -> Callable[[str, str | None, str | None], CashTuple]:
    if sic is None:
        return classify_general
    if sic in _BANK_SIC:
        return _lazy_bank()
    if sic in _INSURANCE_SIC:
        return _lazy_insurance()
    return classify_general


def classify_ci_entry(tag: str, segments: str | None, plabel: str | None, *, sic: int | None = None) -> CashTuple:
    mapper = _select_mapper(sic)
    return mapper(tag, segments, plabel)


__all__ = ["classify_ci_entry", "clean_text"]
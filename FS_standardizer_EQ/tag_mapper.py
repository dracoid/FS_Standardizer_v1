"""tag_mapper – SIC 코드에 따라 EQ 매퍼 선택"""
from __future__ import annotations
from typing import Callable, Tuple, Optional, TypeAlias

from FS_standardizer_EQ.general_mapper import classify_general
# lazy import 함수
def _lazy_bank():
    from FS_standardizer_EQ.sector.bank_mapper import classify_bank_eq
    return classify_bank_eq

CashTuple: TypeAlias = Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]

# SIC 범위
_BANK = range(6000, 6100)

def _select(sic: int | None) -> Callable[[str, str | None, str | None], CashTuple]:
    if sic is not None and sic in _BANK:
        return _lazy_bank()
    return classify_general


def classify_equity_entry(tag: str, segments: str | None, plabel: str | None, *, sic: int | None = None) -> CashTuple:
    return _select(sic)(tag, segments, plabel)


__all__ = ["classify_equity_entry", "classify_general"]
"""공통 유틸 – 단순 텍스트 정리 & 캐시"""
import re
from functools import lru_cache

_WS_RE = re.compile(r"\s+")


@lru_cache(maxsize=16_384)
def clean_text(txt: str | None) -> str:
    """CamelCase → spaced lower + collapse WS → title-case."""
    if txt is None:
        return ""
    # CamelCase split
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", txt)
    s = _WS_RE.sub(" ", s).strip()
    return s.title()
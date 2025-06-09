"""공통 헬퍼 – 태그/레이블 문자열 정리"""
import re

_BAD = re.compile(r"[^A-Za-z0-9]+")

def clean_text(text: str | None) -> str:
    if text is None:
        return ""
    # CamelCase → space 삽입, 특수문자 제거
    spaced  = re.sub(r"(?<!^)(?=[A-Z])", " ", text)
    cleaned = _BAD.sub(" ", spaced).strip()
    return re.sub(r"\s{2,}", " ", cleaned)
# FS_standardizer_CF/utils/helper.py

"""helper.py – Utility helpers for CF standardizer"""

from __future__ import annotations

import re
from unicodedata import normalize as _uni_normalize

_CAMEL_RE = re.compile(r"(?<!^)(?=[A-Z])")
_SPECIAL_RE = re.compile(r"[^A-Za-z0-9\s]+")
_MULTISPACE_RE = re.compile(r"\s{2,}")


def clean_text(text: str | None) -> str:
    """Human-friendly version of an XBRL tag or label.

    Steps:
    1. Unicode NFC normalization ➜ ASCII fallback
    2. CamelCase ➜ "Camel Case"
    3. Remove non-alphanumeric (keep spaces)
    4. Collapse multi-spaces; strip()
    """
    if not text:
        return ""

    # 1) Unicode normalize → ASCII fallback
    txt = _uni_normalize("NFKD", text).encode("ascii", "ignore").decode()

    # 2) CamelCase splitter (e.g., NetCashProvidedBy → Net Cash Provided By)
    txt = _CAMEL_RE.sub(" ", txt)

    # 3) Remove special characters (underscores, dashes, etc.)
    txt = _SPECIAL_RE.sub(" ", txt)

    # 4) Collapse whitespace & trim
    txt = _MULTISPACE_RE.sub(" ", txt).strip()

    return txt.title()


__all__ = ["clean_text"]

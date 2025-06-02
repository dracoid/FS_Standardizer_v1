# FS_standardizer_IS/utils/helper.py

def clean_text(text):
    """특수문자 제거용 간단한 유틸 함수"""
    if not isinstance(text, str):
        return ""
    return text.replace(" ", "").replace("\n", "").strip()

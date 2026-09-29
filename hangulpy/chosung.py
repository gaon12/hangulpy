# chosung.py


import warnings

from hangulpy._jamo_extract import collect_chosung
from hangulpy.utils import CHOSUNG_BASE, CHOSUNG_LIST, HANGUL_BEGIN_UNICODE, is_complete_hangul_char


def get_chosung_string(
    text: str,
    keep_spaces: bool = False,
    *,
    keep_non_hangul: bool | None = None,
) -> str:
    """
    문자열의 초성을 추출합니다.

    keep_non_hangul을 지정하면 독립 초성 자모도 보존하며 공백과 비한글
    문자를 각각 제어합니다. 생략하면 기존 keep_spaces 동작을 유지합니다.
    """
    from hangulpy.hangul_normalize import normalize_hangul

    if keep_non_hangul is not None:
        return collect_chosung(text, keep_spaces=keep_spaces, keep_non_hangul=keep_non_hangul)

    normalized = normalize_hangul(text, "NFC")
    if keep_spaces:
        return "".join(_get_chosung_char(char) for char in normalized)
    return "".join(_get_chosung_char(char) for char in normalized if is_complete_hangul_char(char))


def _get_chosung_char(c: str) -> str:
    if is_complete_hangul_char(c):
        code = ord(c) - HANGUL_BEGIN_UNICODE
        cho_idx = code // CHOSUNG_BASE
        return CHOSUNG_LIST[cho_idx]
    else:
        return c


def extract_chosung(c: str) -> str:
    """Deprecated single-character helper retained until v1.6."""
    warnings.warn(
        "hangulpy.chosung.extract_chosung is deprecated and will be removed in v1.6; "
        "use hangulpy.get_chosung for a syllable, or get_chosung_string for text.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _get_chosung_char(c)


def chosung_includes(word: str, pattern: str) -> bool:
    """
    Python 스타일 초성 검색 API입니다.
    """
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(word, "NFC")
    word_chosung = "".join(
        _get_chosung_char(char) for char in normalized if is_complete_hangul_char(char)
    )
    return pattern in word_chosung

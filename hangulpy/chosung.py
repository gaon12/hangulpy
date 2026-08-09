# chosung.py

import warnings

from hangulpy._deprecated import HangulpyDeprecationWarning
from hangulpy.utils import CHOSUNG_BASE, CHOSUNG_LIST, HANGUL_BEGIN_UNICODE, is_complete_hangul_char


def get_chosung_string(text: str, keep_spaces: bool = False) -> str:
    """
    문자열의 초성을 추출합니다.
    """
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(text, "NFC")
    if keep_spaces:
        return "".join(extract_chosung(char) for char in normalized)
    return "".join(extract_chosung(char) for char in normalized if is_complete_hangul_char(char))


def extract_chosung(c: str) -> str:
    if is_complete_hangul_char(c):
        code = ord(c) - HANGUL_BEGIN_UNICODE
        cho_idx = code // CHOSUNG_BASE
        return CHOSUNG_LIST[cho_idx]
    else:
        return c


def chosungIncludes(word: str, pattern: str) -> bool:
    """
    초성으로 검색합니다.

    :param word: 검색 대상 문자열
    :param pattern: 초성 패턴
    :return: 포함 여부
    """
    warnings.warn(
        "'chosungIncludes' is deprecated and will be removed in the next release; "
        "use 'chosung_includes' instead",
        HangulpyDeprecationWarning,
        stacklevel=2,
    )
    return chosung_includes(word, pattern)


def chosung_includes(word: str, pattern: str) -> bool:
    """
    Python 스타일 초성 검색 API입니다.
    """
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(word, "NFC")
    word_chosung = "".join(
        extract_chosung(char) for char in normalized if is_complete_hangul_char(char)
    )
    return pattern in word_chosung

# chosung.py

import warnings

from hangulpy.utils import CHOSUNG_BASE, CHOSUNG_LIST, HANGUL_BEGIN_UNICODE, is_hangul


def get_chosung_string(text: str, keep_spaces: bool = False) -> str:
    """
    문자열의 초성을 추출합니다.
    """
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(text, "NFC")
    return (
        "".join(extract_chosung(c) if is_hangul(c) else c for c in normalized)
        if keep_spaces
        else "".join(
            extract_chosung(c) if is_hangul(c) and not c.isspace() else "" for c in normalized
        )
    )


def extract_chosung(c: str) -> str:
    if is_hangul(c):
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
        DeprecationWarning,
        stacklevel=2,
    )
    return chosung_includes(word, pattern)


def chosung_includes(word: str, pattern: str) -> bool:
    """
    Python 스타일 초성 검색 API입니다.
    """
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(word, "NFC")
    word_chosung = "".join(extract_chosung(c) for c in normalized if is_hangul(c))
    return pattern in word_chosung

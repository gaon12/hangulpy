# hangul_properties.py
# Advanced character property checking functions

import unicodedata
from typing import List, Optional, Tuple

from hangulpy.utils import (
    CHOSUNG_INDEX,
    CHOSUNG_LIST,
    JONGSUNG_INDEX,
    JONGSUNG_LIST,
    JUNGSUNG_INDEX,
    JUNGSUNG_LIST,
    decompose_syllable,
    is_complete_hangul_char,
)


def _one_composed_syllable(text: str) -> Optional[str]:
    if is_complete_hangul_char(text):
        return text

    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(text, "NFC")
    if len(normalized) != 1:
        return None
    if is_complete_hangul_char(normalized):
        return normalized
    return None


def is_complete_hangul(char: str) -> bool:
    """
    주어진 문자가 완성형 한글 음절인지 확인합니다.

    :param char: 검사할 문자
    :return: 완성형 한글이면 True, 아니면 False
    """
    return _one_composed_syllable(char) is not None


def is_chosung(char: str) -> bool:
    """
    주어진 문자가 초성(자음)인지 확인합니다.

    :param char: 검사할 문자
    :return: 초성이면 True, 아니면 False
    """
    if len(char) != 1:
        return False
    return char in CHOSUNG_INDEX


def is_jungsung(char: str) -> bool:
    """
    주어진 문자가 중성(모음)인지 확인합니다.

    :param char: 검사할 문자
    :return: 중성이면 True, 아니면 False
    """
    if len(char) != 1:
        return False
    return char in JUNGSUNG_INDEX


def is_jongsung(char: str) -> bool:
    """
    주어진 문자가 종성(받침)인지 확인합니다.
    빈 문자열은 받침 없음을 나타내므로 False를 반환합니다.

    :param char: 검사할 문자
    :return: 종성이면 True, 아니면 False
    """
    if len(char) != 1:
        return False
    return char in JONGSUNG_INDEX and char != ""


def has_jongsung(char: str) -> bool:
    """
    주어진 한글 음절에 받침(종성)이 있는지 확인합니다.

    :param char: 검사할 한글 음절 문자
    :return: 받침이 있으면 True, 없으면 False
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return False
    components = decompose_syllable(composed)
    return components is not None and bool(components[2])


def get_chosung(char: str) -> Optional[str]:
    """
    완성형 한글 음절에서 초성을 추출합니다.

    :param char: 한글 음절 문자
    :return: 초성 문자, 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    components = decompose_syllable(composed)
    return components[0] if components is not None else None


def get_jungsung(char: str) -> Optional[str]:
    """
    완성형 한글 음절에서 중성을 추출합니다.

    :param char: 한글 음절 문자
    :return: 중성 문자, 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    components = decompose_syllable(composed)
    return components[1] if components is not None else None


def get_jongsung(char: str) -> Optional[str]:
    """
    완성형 한글 음절에서 종성을 추출합니다.

    :param char: 한글 음절 문자
    :return: 종성 문자 (받침 없으면 빈 문자열), 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    components = decompose_syllable(composed)
    return components[2] if components is not None else None


def get_hangul_components(char: str) -> Optional[Tuple[str, str, str]]:
    """
    완성형 한글 음절을 초성, 중성, 종성으로 분해합니다.

    :param char: 한글 음절 문자
    :return: (초성, 중성, 종성) 튜플, 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    return decompose_syllable(composed)


def _keep_extraction_separator(char: str, keep_non_hangul: bool) -> bool:
    if char.isspace():
        return True
    code = ord(char)
    is_modern_jamo = (
        0x1100 <= code <= 0x1112
        or 0x1161 <= code <= 0x1175
        or 0x11A8 <= code <= 0x11C2
        or char in CHOSUNG_INDEX
        or char in JUNGSUNG_INDEX
        or char in JONGSUNG_INDEX
    )
    return keep_non_hangul and not is_modern_jamo


def extract_chosung(text: str, *, keep_non_hangul: bool = False) -> str:
    """Extract initial consonants from every Hangul syllable in *text*.

    Whitespace and standalone compatibility choseong are retained. Other text
    is retained only when ``keep_non_hangul`` is true.
    """
    result: List[str] = []
    for char in unicodedata.normalize("NFD", text):
        code = ord(char)
        if 0x1100 <= code <= 0x1112:
            result.append(CHOSUNG_LIST[code - 0x1100])
        elif char in CHOSUNG_INDEX:
            result.append(char)
        elif _keep_extraction_separator(char, keep_non_hangul):
            result.append(char)
    return "".join(result)


def extract_jungsung(text: str, *, keep_non_hangul: bool = False) -> str:
    """Extract medial vowels from every Hangul syllable in *text*."""
    result: List[str] = []
    for char in unicodedata.normalize("NFD", text):
        code = ord(char)
        if 0x1161 <= code <= 0x1175:
            result.append(JUNGSUNG_LIST[code - 0x1161])
        elif char in JUNGSUNG_INDEX:
            result.append(char)
        elif _keep_extraction_separator(char, keep_non_hangul):
            result.append(char)
    return "".join(result)


def extract_jongsung(text: str, *, keep_non_hangul: bool = False) -> str:
    """Extract final consonants from every Hangul syllable in *text*."""
    result: List[str] = []
    for char in unicodedata.normalize("NFD", text):
        code = ord(char)
        if 0x11A8 <= code <= 0x11C2:
            result.append(JONGSUNG_LIST[code - 0x11A7])
        elif _keep_extraction_separator(char, keep_non_hangul):
            result.append(char)
    return "".join(result)

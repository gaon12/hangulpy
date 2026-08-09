# hangul_properties.py
# Advanced character property checking functions

from typing import Optional, Tuple

from hangulpy.utils import (
    CHOSUNG_BASE,
    CHOSUNG_LIST,
    HANGUL_BEGIN_UNICODE,
    HANGUL_END_UNICODE,
    JONGSUNG_COUNT,
    JONGSUNG_LIST,
    JUNGSUNG_BASE,
    JUNGSUNG_LIST,
)


def _one_composed_syllable(text: str) -> Optional[str]:
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(text, "NFC")
    if len(normalized) != 1:
        return None
    code = ord(normalized)
    if HANGUL_BEGIN_UNICODE <= code <= HANGUL_END_UNICODE:
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
    return char in CHOSUNG_LIST


def is_jungsung(char: str) -> bool:
    """
    주어진 문자가 중성(모음)인지 확인합니다.

    :param char: 검사할 문자
    :return: 중성이면 True, 아니면 False
    """
    if len(char) != 1:
        return False
    return char in JUNGSUNG_LIST


def is_jongsung(char: str) -> bool:
    """
    주어진 문자가 종성(받침)인지 확인합니다.
    빈 문자열은 받침 없음을 나타내므로 False를 반환합니다.

    :param char: 검사할 문자
    :return: 종성이면 True, 아니면 False
    """
    if len(char) != 1:
        return False
    # First element of JONGSUNG_LIST is empty string (no jongsung)
    return char in JONGSUNG_LIST and char != ""


def has_jongsung(char: str) -> bool:
    """
    주어진 한글 음절에 받침(종성)이 있는지 확인합니다.

    :param char: 검사할 한글 음절 문자
    :return: 받침이 있으면 True, 없으면 False
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return False
    char_index = ord(composed) - HANGUL_BEGIN_UNICODE
    return (char_index % JONGSUNG_COUNT) != 0


def get_chosung(char: str) -> Optional[str]:
    """
    완성형 한글 음절에서 초성을 추출합니다.

    :param char: 한글 음절 문자
    :return: 초성 문자, 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    char_index = ord(composed) - HANGUL_BEGIN_UNICODE
    chosung_index = char_index // CHOSUNG_BASE
    return CHOSUNG_LIST[chosung_index]


def get_jungsung(char: str) -> Optional[str]:
    """
    완성형 한글 음절에서 중성을 추출합니다.

    :param char: 한글 음절 문자
    :return: 중성 문자, 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    char_index = ord(composed) - HANGUL_BEGIN_UNICODE
    jungsung_index = (char_index % CHOSUNG_BASE) // JUNGSUNG_BASE
    return JUNGSUNG_LIST[jungsung_index]


def get_jongsung(char: str) -> Optional[str]:
    """
    완성형 한글 음절에서 종성을 추출합니다.

    :param char: 한글 음절 문자
    :return: 종성 문자 (받침 없으면 빈 문자열), 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    char_index = ord(composed) - HANGUL_BEGIN_UNICODE
    jongsung_index = char_index % JUNGSUNG_BASE
    return JONGSUNG_LIST[jongsung_index]


def get_hangul_components(char: str) -> Optional[Tuple[str, str, str]]:
    """
    완성형 한글 음절을 초성, 중성, 종성으로 분해합니다.

    :param char: 한글 음절 문자
    :return: (초성, 중성, 종성) 튜플, 한글이 아니면 None
    """
    composed = _one_composed_syllable(char)
    if composed is None:
        return None
    char_index = ord(composed) - HANGUL_BEGIN_UNICODE
    chosung_index = char_index // CHOSUNG_BASE
    jungsung_index = (char_index % CHOSUNG_BASE) // JUNGSUNG_BASE
    jongsung_index = char_index % JUNGSUNG_BASE
    return (
        CHOSUNG_LIST[chosung_index],
        JUNGSUNG_LIST[jungsung_index],
        JONGSUNG_LIST[jongsung_index],
    )

# hangul_role.py

from hangulpy.hangul_normalize import to_compat_jamo
from hangulpy.utils import (
    CHOSUNG_INDEX,
    COMPOUND_FINAL_MAP,
    JONGSUNG_INDEX,
    JUNGSUNG_INDEX,
    VOWEL_COMBO,
)


def can_be_chosung(char: str) -> bool:
    """
    주어진 문자가 한글 초성으로 쓰일 수 있는지 확인합니다.

    :param char: 확인할 문자
    :return: 초성으로 쓰일 수 있으면 True, 아니면 False
    """
    return char in CHOSUNG_INDEX


def can_be_jungsung(char: str) -> bool:
    """Return whether one or two Jamo can form a modern medial vowel.

    Both a composed compatibility vowel such as ``ㅘ`` and its keyboard-style
    representation ``ㅗㅏ`` are accepted.
    """
    if not char:
        return False
    compatibility = char if char in JUNGSUNG_INDEX else to_compat_jamo(char)
    return compatibility in JUNGSUNG_INDEX or tuple(compatibility) in VOWEL_COMBO


def can_be_jongsung(char: str) -> bool:
    """
    주어진 문자가 한글 종성으로 쓰일 수 있는지 확인합니다.

    :param char: 확인할 문자
    :return: 종성으로 쓰일 수 있으면 True, 아니면 False
    """
    if not char:
        return False
    compatibility = char if char in JONGSUNG_INDEX else to_compat_jamo(char)
    return compatibility in JONGSUNG_INDEX or tuple(compatibility) in COMPOUND_FINAL_MAP

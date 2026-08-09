"""Predictable sorting for composed Hangul, Jamo, and mixed text."""

from typing import List, Tuple

from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.utils import (
    CHOSUNG_BASE,
    CHOSUNG_INDEX,
    CHOSUNG_LIST,
    HANGUL_BEGIN_UNICODE,
    JONGSUNG_INDEX,
    JONGSUNG_LIST,
    JUNGSUNG_BASE,
    JUNGSUNG_INDEX,
    JUNGSUNG_LIST,
)

CharacterKey = Tuple[int, int, int, int]
WordKey = Tuple[CharacterKey, ...]


def _character_key(char: str) -> CharacterKey:
    code = ord(char)
    if HANGUL_BEGIN_UNICODE <= code <= 0xD7A3:
        offset = code - HANGUL_BEGIN_UNICODE
        return (
            0,
            offset // CHOSUNG_BASE,
            (offset % CHOSUNG_BASE) // JUNGSUNG_BASE,
            offset % JUNGSUNG_BASE,
        )
    if char in CHOSUNG_LIST:
        return (0, CHOSUNG_INDEX[char], -1, -1)
    if char in JUNGSUNG_LIST:
        return (1, JUNGSUNG_INDEX[char], -1, -1)
    if char in JONGSUNG_LIST[1:]:
        return (1, len(JUNGSUNG_LIST) + JONGSUNG_INDEX[char], -1, -1)
    return (2, code, 0, 0)


def sort_hangul(words: List[str], reverse: bool = False) -> List[str]:
    """한글의 Unicode 초성·중성·종성 순서로 문자열을 안정 정렬합니다."""

    def hangul_key(word: str) -> WordKey:
        return tuple(_character_key(char) for char in normalize_hangul(word, "NFC"))

    return sorted(words, key=hangul_key, reverse=reverse)

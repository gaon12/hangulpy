"""Unicode normalization helpers for modern Hangul text."""

import unicodedata
from typing import Literal

from hangulpy.utils import CHOSUNG_LIST, JONGSUNG_LIST, JUNGSUNG_LIST

NormalizationForm = Literal["NFC", "NFD", "HCJ"]

CANONICAL_CHOSUNG = tuple(chr(code) for code in range(0x1100, 0x1113))
CANONICAL_JUNGSUNG = tuple(chr(code) for code in range(0x1161, 0x1176))
CANONICAL_JONGSUNG = tuple(chr(code) for code in range(0x11A8, 0x11C3))

CANONICAL_TO_COMPAT = {
    **dict(zip(CANONICAL_CHOSUNG, CHOSUNG_LIST)),
    **dict(zip(CANONICAL_JUNGSUNG, JUNGSUNG_LIST)),
    **dict(zip(CANONICAL_JONGSUNG, JONGSUNG_LIST[1:])),
}
COMPAT_JAMO = frozenset(CHOSUNG_LIST + JUNGSUNG_LIST + JONGSUNG_LIST[1:])


def to_compat_jamo(text: str) -> str:
    """완성형 및 canonical Jamo를 호환 자모(HCJ)로 변환합니다."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    decomposed = unicodedata.normalize("NFD", text)
    return "".join(CANONICAL_TO_COMPAT.get(char, char) for char in decomposed)


def normalize_hangul(text: str, form: NormalizationForm = "NFC") -> str:
    """현대 한글을 NFC, NFD 또는 호환 자모 형태로 정규화합니다.

    Unicode canonical Jamo는 표준 정규화를 그대로 따릅니다. 호환 자모가
    포함된 입력은 음절 조합기를 거쳐 문맥상 조합 가능한 부분만 조합합니다.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if form not in ("NFC", "NFD", "HCJ"):
        raise ValueError("form must be one of 'NFC', 'NFD', or 'HCJ'")
    if form == "HCJ":
        return to_compat_jamo(text)

    normalized = text
    if any(char in COMPAT_JAMO for char in text):
        # Import lazily to avoid a module cycle with join_jamos.
        from hangulpy.hangul_assemble import join_jamos

        canonical_as_compat = "".join(CANONICAL_TO_COMPAT.get(char, char) for char in text)
        normalized = join_jamos(canonical_as_compat)

    return unicodedata.normalize(form, normalized)


def to_jamo(text: str, compatibility: bool = False) -> str:
    """문자열을 canonical Jamo(NFD) 또는 호환 자모로 분해합니다."""
    if compatibility:
        return to_compat_jamo(text)
    return normalize_hangul(text, "NFD")

"""Keyboard-level Jamo decomposition with a bounded, lazy translation table."""

from typing import Dict, List

from hangulpy.utils import JONGSUNG_DECOMPOSE, JUNGSUNG_DECOMPOSE, decompose_syllable

# Only modern syllables and the fixed compound-Jamo repertoire are retained.
# Unknown Unicode characters pass through and cannot grow this table.
_TRANSLATIONS: Dict[int, str] = {
    ord(char): "".join(parts)
    for char, parts in {**JUNGSUNG_DECOMPOSE, **JONGSUNG_DECOMPOSE}.items()
}


def decompose_text(text: str) -> str:
    """Return flat Jamo text, preserving other characters after NFC normalization."""
    from hangulpy.hangul_normalize import normalize_hangul

    normalized = normalize_hangul(text, "NFC")
    for char in set(normalized):
        code = ord(char)
        if 0xAC00 <= code <= 0xD7A3 and code not in _TRANSLATIONS:
            parts = decompose_syllable(char)
            if parts is not None:
                cho, jung, jong = parts
                medial = JUNGSUNG_DECOMPOSE.get(jung, (jung,))
                final = JONGSUNG_DECOMPOSE.get(jong, (jong,) if jong else ())
                _TRANSLATIONS[code] = cho + "".join(medial) + "".join(final)
    return normalized.translate(_TRANSLATIONS)


def split_hangul_string(s: str) -> List[str]:
    """Split syllables, compound vowels and compound finals into keyboard Jamo."""
    return list(decompose_text(s))

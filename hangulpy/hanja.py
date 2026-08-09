"""Unicode-aware helpers for identifying and splitting Hanja text."""

from dataclasses import dataclass
from typing import List, Tuple

# Unified ideographs, their major extensions, and compatibility ideographs.
# Keeping explicit inclusive ranges avoids broad Unicode-name heuristics that
# accidentally classify radicals, strokes, or punctuation as Hanja.
_CJK_IDEOGRAPH_RANGES: Tuple[Tuple[int, int], ...] = (
    (0x3400, 0x4DBF),  # Extension A
    (0x4E00, 0x9FFF),  # Unified Ideographs
    (0xF900, 0xFAFF),  # Compatibility Ideographs
    (0x20000, 0x2A6DF),  # Extension B
    (0x2A700, 0x2B73F),  # Extension C
    (0x2B740, 0x2B81F),  # Extension D
    (0x2B820, 0x2CEAF),  # Extension E
    (0x2CEB0, 0x2EBEF),  # Extension F
    (0x2EBF0, 0x2EE5F),  # Extension I
    (0x2F800, 0x2FA1F),  # Compatibility Supplement
    (0x30000, 0x3134F),  # Extension G
    (0x31350, 0x323AF),  # Extension H
)


@dataclass(frozen=True)
class HanjaRun:
    """A consecutive run sharing the same Hanja classification."""

    text: str
    is_hanja: bool


def is_hanja(char: str) -> bool:
    """Return whether ``char`` is one Unicode CJK ideograph."""
    if not isinstance(char, str):
        raise TypeError("char must be a string")
    if len(char) != 1:
        return False

    codepoint = ord(char)
    return any(start <= codepoint <= end for start, end in _CJK_IDEOGRAPH_RANGES)


def split_hanja(text: str) -> List[HanjaRun]:
    """Split text into consecutive Hanja and non-Hanja runs."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not text:
        return []

    runs: List[HanjaRun] = []
    current_is_hanja = is_hanja(text[0])
    current_chars = [text[0]]

    for char in text[1:]:
        char_is_hanja = is_hanja(char)
        if char_is_hanja == current_is_hanja:
            current_chars.append(char)
            continue
        runs.append(HanjaRun("".join(current_chars), current_is_hanja))
        current_chars = [char]
        current_is_hanja = char_is_hanja

    runs.append(HanjaRun("".join(current_chars), current_is_hanja))
    return runs

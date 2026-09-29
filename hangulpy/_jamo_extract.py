"""Internal helpers shared by the component extraction APIs."""

import unicodedata

from hangulpy.utils import CHOSUNG_INDEX, CHOSUNG_LIST, JONGSUNG_INDEX, JUNGSUNG_INDEX


def keep_extraction_separator(char: str, keep_non_hangul: bool, keep_spaces: bool) -> bool:
    if char.isspace():
        return keep_spaces
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


def collect_chosung(text: str, *, keep_spaces: bool, keep_non_hangul: bool) -> str:
    result: list[str] = []
    for char in unicodedata.normalize("NFD", text):
        code = ord(char)
        if 0x1100 <= code <= 0x1112:
            result.append(CHOSUNG_LIST[code - 0x1100])
        elif char in CHOSUNG_INDEX:
            result.append(char)
        elif keep_extraction_separator(char, keep_non_hangul, keep_spaces):
            result.append(char)
    return "".join(result)

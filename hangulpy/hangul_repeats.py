"""Reduce standalone Jamo repeats and a bounded set of chat emoticon forms."""

import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass

from hangulpy._validation import require_bool, require_positive_int, require_str
from hangulpy.hangul_normalize import (
    CANONICAL_TO_COMPAT,
    COMPAT_JAMO,
    normalize_halfwidth_hangul,
)
from hangulpy.utils import compose_syllable, decompose_syllable

_LAUGH_CONSONANTS = frozenset("ㅋㅎ")
_CRY_VOWELS = frozenset("ㅜㅠ")


@dataclass(frozen=True)
class _TextUnit:
    source: str
    jamo: str | None = None
    components: tuple[str, str, str] | None = None


def _iter_units(text: str) -> Iterator[_TextUnit]:
    """Keep complete NFC/NFD syllables atomic and preserve their source form."""
    index = 0
    while index < len(text):
        start = index
        char = text[index]
        components = decompose_syllable(char)
        index += 1
        if (
            components is None
            and 0x1100 <= ord(char) <= 0x1112
            and index < len(text)
            and 0x1161 <= ord(text[index]) <= 0x1175
        ):
            index += 1
            if index < len(text) and 0x11A8 <= ord(text[index]) <= 0x11C2:
                index += 1
            components = decompose_syllable(unicodedata.normalize("NFC", text[start:index]))
        if components is not None:
            yield _TextUnit(text[start:index], components=components)
        else:
            jamo = CANONICAL_TO_COMPAT.get(char, char)
            yield _TextUnit(char, jamo=jamo if jamo in COMPAT_JAMO else None)


def _has_repeat(units: list[_TextUnit], index: int, direction: int, jamo: str) -> bool:
    first, second = index + direction, index + 2 * direction
    return (
        0 <= first < len(units)
        and 0 <= second < len(units)
        and units[first].jamo == units[second].jamo == jamo
    )


def _normalize_emoticon_units(units: list[_TextUnit]) -> Iterator[_TextUnit]:
    for index, unit in enumerate(units):
        if unit.components is not None:
            cho, jung, jong = unit.components
            if jong in _LAUGH_CONSONANTS and _has_repeat(units, index, 1, jong):
                # 앜ㅋㅋ -> 아 + ㅋㅋㅋ. Keep an NFD base in its original form.
                base = compose_syllable(cho, jung) if len(unit.source) == 1 else unit.source[:-1]
                yield _TextUnit(base)
                yield _TextUnit(jong, jamo=jong)
                continue
            if not jong and jung in _CRY_VOWELS and _has_repeat(units, index, 1, jung):
                if cho in _LAUGH_CONSONANTS and _has_repeat(units, index, -1, cho):
                    # ㅋㅋ쿠ㅜㅜ -> ㅋㅋㅋ + ㅜㅜㅜ, before reducing each run.
                    yield _TextUnit(cho, jamo=cho)
                    yield _TextUnit(jung, jamo=jung)
                    continue
                if cho == "ㅇ" and _has_repeat(units, index, -1, jung):
                    # ㅠㅠ유ㅠㅠ -> one contiguous run of ㅠ.
                    yield _TextUnit(jung, jamo=jung)
                    continue
        yield unit


def reduce_jamo_repeats(
    text: str,
    max_repeats: int = 2,
    *,
    normalize_emoticons: bool = True,
) -> str:
    """Limit consecutive standalone modern Jamo without reducing words or digits.

    Halfwidth Hangul is converted to compatibility Jamo. Complete NFC/NFD
    syllables remain atomic and retain their source spelling. Optional emoticon
    normalization handles ㅋ/ㅎ finals before a run of at least two matching
    consonants and 쿠/휴/유-like bridges between matching laugh/cry Jamo runs.
    Other characters and whitespace are preserved. Processing is linear in the
    input length, and ``max_repeats`` must be a positive integer, excluding bool.
    """
    text = require_str(text)
    max_repeats = require_positive_int(max_repeats, "max_repeats")
    normalize_emoticons = require_bool(normalize_emoticons, "normalize_emoticons")
    units = list(_iter_units(normalize_halfwidth_hangul(text)))
    output = _normalize_emoticon_units(units) if normalize_emoticons else iter(units)

    result: list[str] = []
    previous_jamo: str | None = None
    run_length = 0
    for unit in output:
        if unit.jamo is None:
            previous_jamo = None
            run_length = 0
            result.append(unit.source)
        else:
            run_length = run_length + 1 if unit.jamo == previous_jamo else 1
            previous_jamo = unit.jamo
            if run_length <= max_repeats:
                result.append(unit.source)
    return "".join(result)

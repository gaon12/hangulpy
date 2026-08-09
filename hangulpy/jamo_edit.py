"""Jamo-aware length, slicing, and typing helpers."""

import unicodedata
from dataclasses import dataclass
from typing import Iterator, List, Optional, Tuple

from hangulpy.hangul_assemble import join_jamos, split_syllables
from hangulpy.hangul_normalize import normalize_hangul

_ZWJ = "\u200d"


@dataclass(frozen=True)
class _EditGroup:
    parts: Tuple[str, ...]


def _is_regional_indicator(char: str) -> bool:
    return 0x1F1E6 <= ord(char) <= 0x1F1FF


def _is_grapheme_extend(char: str) -> bool:
    codepoint = ord(char)
    return (
        unicodedata.category(char).startswith("M")
        or 0xFE00 <= codepoint <= 0xFE0F
        or 0xE0100 <= codepoint <= 0xE01EF
        or 0x1F3FB <= codepoint <= 0x1F3FF
        or 0xE0020 <= codepoint <= 0xE007F
    )


def _iter_graphemes(text: str) -> Iterator[str]:
    cluster = ""
    regional_count = 0

    for char in text:
        if not cluster:
            cluster = char
            regional_count = 1 if _is_regional_indicator(char) else 0
            continue

        joins_cluster = (
            _is_grapheme_extend(char)
            or char == _ZWJ
            or cluster.endswith(_ZWJ)
            or (cluster == "\r" and char == "\n")
            or (_is_regional_indicator(char) and regional_count > 0 and regional_count % 2 == 1)
        )
        if joins_cluster:
            cluster += char
            if _is_regional_indicator(char):
                regional_count += 1
            continue

        yield cluster
        cluster = char
        regional_count = 1 if _is_regional_indicator(char) else 0

    if cluster:
        yield cluster


def _edit_groups(text: str) -> List[_EditGroup]:
    normalized = normalize_hangul(text, "NFC")
    groups: List[_EditGroup] = []
    for grapheme in _iter_graphemes(normalized):
        parts = tuple(split_syllables(grapheme)) if len(grapheme) == 1 else (grapheme,)
        groups.append(_EditGroup(parts))
    return groups


def _render_parts(parts: Tuple[str, ...]) -> str:
    return join_jamos(list(parts))


def jamo_len(text: str) -> int:
    """Count keyboard-level Jamo while treating non-Hangul graphemes atomically."""
    return sum(len(group.parts) for group in _edit_groups(text))


def jamo_slice(
    text: str,
    start: Optional[int] = None,
    stop: Optional[int] = None,
) -> str:
    """Slice by Jamo offset without recomposing across original syllable boundaries.

    ``start`` and ``stop`` follow normal Python slice rules, including negative
    indices. A partial syllable is reassembled only from parts belonging to
    that original syllable. Non-Hangul grapheme clusters count as one part.
    """
    groups = _edit_groups(text)
    total = sum(len(group.parts) for group in groups)
    slice_start, slice_stop, _ = slice(start, stop).indices(total)
    if slice_start >= slice_stop:
        return ""

    result: List[str] = []
    offset = 0
    for group in groups:
        group_end = offset + len(group.parts)
        overlap_start = max(slice_start, offset)
        overlap_end = min(slice_stop, group_end)
        if overlap_start < overlap_end:
            local_start = overlap_start - offset
            local_end = overlap_end - offset
            result.append(_render_parts(group.parts[local_start:local_end]))
        offset = group_end
        if offset >= slice_stop:
            break
    return "".join(result)


def typing_steps(text: str) -> List[str]:
    """Return the visible text after each Jamo/grapheme typing step."""
    steps: List[str] = []
    completed = ""
    for group in _edit_groups(text):
        for end in range(1, len(group.parts) + 1):
            steps.append(completed + _render_parts(group.parts[:end]))
        completed += _render_parts(group.parts)
    return steps

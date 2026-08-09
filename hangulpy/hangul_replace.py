"""Source-preserving replacement and splitting for Hangul-aware patterns."""

from typing import Callable, List, Tuple, Union

from hangulpy.hangul_contains import HangulMatch, find_hangul_spans

HangulReplacement = Union[str, Callable[[HangulMatch], str]]


def _validate_pattern(pattern: str) -> None:
    if not pattern:
        raise ValueError("pattern must not be empty")


def _validate_limit(value: int, name: str) -> None:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < -1:
        raise ValueError(f"{name} must be -1 or a non-negative integer")


def hangul_replace(
    text: str,
    pattern: str,
    replacement: HangulReplacement,
    count: int = -1,
) -> str:
    """Replace non-overlapping Hangul-aware matches in original source coordinates."""
    _validate_pattern(pattern)
    _validate_limit(count, "count")
    if not isinstance(replacement, str) and not callable(replacement):
        raise TypeError("replacement must be a string or callable")
    if count == 0:
        return text

    matches = find_hangul_spans(text, pattern)
    if count >= 0:
        matches = matches[:count]
    if not matches:
        return text

    result: List[str] = []
    source_end = 0
    for match in matches:
        result.append(text[source_end : match.start])
        value = replacement(match) if callable(replacement) else replacement
        if not isinstance(value, str):
            raise TypeError("replacement callable must return a string")
        result.append(value)
        source_end = match.end
    result.append(text[source_end:])
    return "".join(result)


def hangul_split(text: str, pattern: str, maxsplit: int = -1) -> List[str]:
    """Split text at non-overlapping Hangul-aware matches."""
    _validate_pattern(pattern)
    _validate_limit(maxsplit, "maxsplit")
    if maxsplit == 0:
        return [text]

    matches = find_hangul_spans(text, pattern)
    if maxsplit >= 0:
        matches = matches[:maxsplit]

    parts: List[str] = []
    source_end = 0
    for match in matches:
        parts.append(text[source_end : match.start])
        source_end = match.end
    parts.append(text[source_end:])
    return parts


def hangul_partition(text: str, pattern: str) -> Tuple[str, str, str]:
    """Partition text around the first Hangul-aware match."""
    _validate_pattern(pattern)
    matches = find_hangul_spans(text, pattern)
    if not matches:
        return text, "", ""
    match = matches[0]
    return text[: match.start], match.text, text[match.end :]


def hangul_rpartition(text: str, pattern: str) -> Tuple[str, str, str]:
    """Partition text around the last Hangul-aware match."""
    _validate_pattern(pattern)
    matches = find_hangul_spans(text, pattern)
    if not matches:
        return "", "", text
    match = matches[-1]
    return text[: match.start], match.text, text[match.end :]

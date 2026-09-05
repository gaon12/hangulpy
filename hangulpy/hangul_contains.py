# hangul_contains.py

import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Iterator, List, Optional, Tuple, TypeVar

from hangulpy._deprecated import resolve_legacy_bool
from hangulpy.hangul_normalize import (
    CANONICAL_CHOSUNG,
    CANONICAL_TO_COMPAT,
    COMPAT_JAMO,
    normalize_hangul,
)
from hangulpy.hangul_split import split_hangul_string
from hangulpy.utils import CHOSUNG_LIST, is_hangul

_SearchData = Tuple[str, Tuple[int, ...], Tuple[int, ...]]


_T = TypeVar("_T")


def _cache_short_text(function: Callable[[str], _T]) -> Callable[[str], _T]:
    """Bound both the number and length of retained global-cache keys."""
    cached = lru_cache(maxsize=256)(function)

    def lookup(text: str) -> _T:
        return cached(text) if len(text) <= 256 else function(text)

    return lookup


@dataclass(frozen=True)
class HangulMatch:
    """원문 문자열에서 찾은 한글 검색 결과입니다."""

    start: int
    end: int
    text: str

    def span(self) -> Tuple[int, int]:
        """원문 기준의 ``(start, end)`` 구간을 반환합니다."""
        return self.start, self.end


def _normalize_with_source_spans(text: str) -> Tuple[str, Tuple[Tuple[int, int], ...]]:
    """Normalize once while tracking assembly and canonical combining clusters.

    A combining cluster is indivisible in source coordinates: a match for a
    composed character also covers marks reordered across it during NFC.
    """
    from hangulpy.hangul_assemble import assemble_fragments

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    fragments: Iterator[Tuple[str, int, int]]
    if any(char in COMPAT_JAMO for char in text):
        fragments = assemble_fragments([CANONICAL_TO_COMPAT.get(c, c) for c in text])
    else:
        fragments = ((char, i, i + 1) for i, char in enumerate(text))

    parts: List[str] = []
    spans: List[Tuple[int, int]] = []
    cluster: List[str] = []
    cluster_start = 0
    cluster_end = 0
    starter = ""

    def flush() -> None:
        if cluster:
            normalized = unicodedata.normalize("NFC", "".join(cluster))
            parts.append(normalized)
            spans.extend([(cluster_start, cluster_end)] * len(normalized))
            cluster.clear()

    for fragment, start, end in fragments:
        for char in unicodedata.normalize("NFD", fragment):
            if unicodedata.combining(char):
                if not cluster:
                    cluster_start = start
                cluster.append(char)
                cluster_end = end
                starter = ""  # Nonstarters block Hangul L/V/T composition.
                continue
            combined = unicodedata.normalize("NFC", starter + char) if starter else ""
            if cluster and len(combined) == 1:
                cluster.append(char)
                cluster_end = end
                starter = combined
            else:
                flush()
                cluster_start, cluster_end = start, end
                cluster.append(char)
                starter = char
    flush()
    return "".join(parts), tuple(spans)


@_cache_short_text
def _decompose_cached(text: str) -> str:
    """
    Cached version of string decomposition for performance.

    :param text: String to decompose
    :return: Decomposed string
    """
    normalized = normalize_hangul(text, "NFC")
    normalized = "".join(CANONICAL_TO_COMPAT.get(char, char) for char in normalized)
    return "".join("".join(split_hangul_string(char)) for char in normalized)


@dataclass(frozen=True)
class PreparedSearchText:
    """Internal immutable search representations owned by a collection index."""

    normalized: str
    jamo: _SearchData
    chosung: _SearchData

    def find_index(self, searcher: "HangulSearcher") -> int:
        if not searcher.pattern:
            return 0
        basis, pattern, starts, _ = _select_search_basis(self, searcher)
        index = basis.find(pattern)
        return starts[index] if index >= 0 else -1


def prepare_search_text(text: str) -> PreparedSearchText:
    normalized, spans = _normalize_with_source_spans(text)
    parts: List[str] = []
    starts: List[int] = []
    ends: List[int] = []
    initials: List[str] = []
    initial_starts: List[int] = []
    initial_ends: List[int] = []
    for char, (start, end) in zip(normalized, spans):
        split = split_hangul_string(CANONICAL_TO_COMPAT.get(char, char))
        parts.extend(split)
        starts.extend([start] * len(split))
        ends.extend([end] * len(split))
        if is_hangul(char) or char in CHOSUNG_LIST or char in CANONICAL_CHOSUNG:
            initials.append(split[0])
            initial_starts.append(start)
            initial_ends.append(end)
    return PreparedSearchText(
        normalized,
        ("".join(parts), tuple(starts), tuple(ends)),
        ("".join(initials), tuple(initial_starts), tuple(initial_ends)),
    )


_get_prepared_text = _cache_short_text(prepare_search_text)


@_cache_short_text
def _plain_search_text(text: str) -> Tuple[str, str]:
    normalized = normalize_hangul(text, "NFC")
    initials = "".join(
        split_hangul_string(char)[0] if is_hangul(char) else CANONICAL_TO_COMPAT.get(char, char)
        for char in normalized
        if is_hangul(char) or char in CHOSUNG_LIST or char in CANONICAL_CHOSUNG
    )
    return _decompose_cached(text), initials


def _is_chosung_pattern(pattern: str) -> bool:
    normalized = normalize_hangul(pattern, "NFC")
    return bool(normalized) and all(
        char in CHOSUNG_LIST or char in CANONICAL_CHOSUNG for char in normalized
    )


@_cache_short_text
def _normalize_chosung_pattern(pattern: str) -> str:
    normalized = normalize_hangul(pattern, "NFC")
    return "".join(CANONICAL_TO_COMPAT.get(char, char) for char in normalized)


def _select_search_basis(
    prepared: PreparedSearchText, searcher: "HangulSearcher"
) -> Tuple[str, str, Tuple[int, ...], Tuple[int, ...]]:
    if searcher.is_chosung_pattern:
        word, starts, ends = prepared.chosung
        if searcher.pattern_split in word or len(searcher.pattern_split) != 1:
            return word, searcher.pattern_split, starts, ends
    word, starts, ends = prepared.jamo
    return word, searcher.fallback_pattern_split, starts, ends


def _get_search_basis(word: str, pattern: str) -> Tuple[str, str, Tuple[int, ...], Tuple[int, ...]]:
    return _select_search_basis(_get_prepared_text(word), HangulSearcher(pattern))


def _iter_matches(
    text: str,
    word_basis: str,
    pattern_basis: str,
    starts: Tuple[int, ...],
    ends: Tuple[int, ...],
    overlap: bool,
) -> Iterator[HangulMatch]:
    if not pattern_basis:
        return

    search_start = 0
    previous_source_end = 0
    while True:
        index = word_basis.find(pattern_basis, search_start)
        if index == -1:
            break

        source_start = starts[index]
        source_end = ends[index + len(pattern_basis) - 1]
        if overlap or source_start >= previous_source_end:
            yield HangulMatch(source_start, source_end, text[source_start:source_end])
            previous_source_end = source_end
        search_start = index + 1


def find_hangul_spans(text: str, pattern: str, overlap: bool = False) -> List[HangulMatch]:
    """한글 패턴의 원문 기준 구간을 찾습니다.

    빈 패턴은 매치하지 않습니다. 기본값은 겹치지 않는 매치이며,
    ``overlap=True``이면 검색 기반에서 한 칸씩 이동해 겹치는 결과도 반환합니다.
    단일 초성 패턴은 기존 초성 검색을 우선하고, 초성 매치가 전혀 없을 때
    중성·종성을 포함한 전체 자모 검색으로 대체합니다.
    """
    if not pattern:
        return []

    word_basis, pattern_basis, starts, ends = _get_search_basis(text, pattern)
    return list(_iter_matches(text, word_basis, pattern_basis, starts, ends, overlap))


def hangul_contains(
    word: str,
    pattern: str,
    not_allow_empty: Optional[bool] = None,
    **legacy_options: object,
) -> bool:
    """
    주어진 한글 문자열이 다른 한글 문자열을 포함하는지 검사합니다.

    :param word: 검사할 한글 문자열
    :param pattern: 포함 여부를 검사할 한글 문자열 패턴
    :param not_allow_empty: 패턴이 빈 문자열일 때 false를 반환하는 옵션
    :return: 포함되면 True, 아니면 False
    """
    not_allow_empty = resolve_legacy_bool(
        not_allow_empty, legacy_options, "notallowempty", "not_allow_empty"
    )
    if not pattern:
        return not not_allow_empty

    return HangulSearcher(pattern).search(word)


def hangul_search(
    word: str,
    pattern: str,
    not_allow_empty: Optional[bool] = None,
    **legacy_options: object,
) -> int:
    """
    한글 문자열에서 패턴을 검색하고 첫 번째 매칭 위치의 인덱스를 반환합니다.

    :param word: 검사할 한글 문자열
    :param pattern: 검색할 한글 문자열 패턴
    :param not_allow_empty: 패턴이 빈 문자열일 때 -1을 반환하는 옵션
    :return: 매칭 시작 인덱스, 없으면 -1
    """
    not_allow_empty = resolve_legacy_bool(
        not_allow_empty, legacy_options, "notallowempty", "not_allow_empty"
    )
    if not pattern:
        return -1 if not_allow_empty else 0

    word_split, pattern_split, positions, _ = _get_search_basis(word, pattern)
    index = word_split.find(pattern_split)

    if index == -1:
        return -1

    return positions[index]


def hangul_search_all(
    word: str,
    pattern: str,
    not_allow_empty: Optional[bool] = None,
    **legacy_options: object,
) -> List[int]:
    """
    한글 문자열에서 패턴이 나타나는 모든 위치의 인덱스를 반환합니다.

    :param word: 검사할 한글 문자열
    :param pattern: 검색할 한글 문자열 패턴
    :param not_allow_empty: 패턴이 빈 문자열일 때 빈 리스트를 반환하는 옵션
    :return: 매칭 위치 인덱스 리스트
    """
    not_allow_empty = resolve_legacy_bool(
        not_allow_empty, legacy_options, "notallowempty", "not_allow_empty"
    )
    if not pattern:
        return [] if not_allow_empty else [0]

    word_split, pattern_split, positions, _ = _get_search_basis(word, pattern)

    indices: List[int] = []
    start = 0
    while True:
        index = word_split.find(pattern_split, start)
        if index == -1:
            break
        indices.append(positions[index])
        start = index + 1

    return indices


class HangulSearcher:
    """
    한글 문자열 검색을 최적화하는 클래스.
    동일한 패턴으로 여러 문자열을 검색할 때 성능이 향상됩니다.
    """

    def __init__(self, pattern: str) -> None:
        """
        HangulSearcher 인스턴스를 생성합니다.

        :param pattern: 검색할 패턴
        """
        self.pattern = pattern
        self.is_chosung_pattern = _is_chosung_pattern(pattern)
        self.pattern_split = (
            _normalize_chosung_pattern(pattern)
            if self.is_chosung_pattern
            else _decompose_cached(pattern) if pattern else ""
        )
        self.fallback_pattern_split = _decompose_cached(pattern) if pattern else ""

    def _get_word_basis(self, word: str) -> Tuple[str, str, Tuple[int, ...], Tuple[int, ...]]:
        return _select_search_basis(_get_prepared_text(word), self)

    def search(
        self,
        word: str,
        not_allow_empty: Optional[bool] = None,
        **legacy_options: object,
    ) -> bool:
        """
        문자열에서 패턴을 검색하고 포함 여부를 반환합니다.

        :param word: 검사할 문자열
        :param not_allow_empty: 패턴이 빈 문자열일 때 false를 반환하는 옵션
        :return: 포함되면 True, 아니면 False
        """
        not_allow_empty = resolve_legacy_bool(
            not_allow_empty, legacy_options, "notallowempty", "not_allow_empty"
        )
        if not self.pattern:
            return not not_allow_empty

        jamo, initials = _plain_search_text(word)
        if self.is_chosung_pattern:
            if self.pattern_split in initials:
                return True
            if len(self.pattern_split) != 1:
                return False
        return self.fallback_pattern_split in jamo

    def find_index(
        self,
        word: str,
        not_allow_empty: Optional[bool] = None,
        **legacy_options: object,
    ) -> int:
        """
        문자열에서 패턴의 첫 번째 매칭 위치를 반환합니다.

        :param word: 검사할 문자열
        :param not_allow_empty: 패턴이 빈 문자열일 때 -1을 반환하는 옵션
        :return: 매칭 시작 인덱스, 없으면 -1
        """
        not_allow_empty = resolve_legacy_bool(
            not_allow_empty, legacy_options, "notallowempty", "not_allow_empty"
        )
        if not self.pattern:
            return -1 if not_allow_empty else 0

        word_split, pattern_split, positions, _ = self._get_word_basis(word)
        index = word_split.find(pattern_split)

        if index == -1:
            return -1

        return positions[index]

    def find_all(
        self,
        word: str,
        not_allow_empty: Optional[bool] = None,
        **legacy_options: object,
    ) -> List[int]:
        """
        문자열에서 패턴이 나타나는 모든 위치를 반환합니다.

        :param word: 검사할 문자열
        :param not_allow_empty: 패턴이 빈 문자열일 때 빈 리스트를 반환하는 옵션
        :return: 매칭 위치 인덱스 리스트
        """
        not_allow_empty = resolve_legacy_bool(
            not_allow_empty, legacy_options, "notallowempty", "not_allow_empty"
        )
        if not self.pattern:
            return [] if not_allow_empty else [0]

        word_split, pattern_split, positions, _ = self._get_word_basis(word)
        indices: List[int] = []
        start = 0
        while True:
            index = word_split.find(pattern_split, start)
            if index == -1:
                break
            indices.append(positions[index] if positions else index)
            start = index + 1

        return indices

    def finditer(self, text: str, overlap: bool = False) -> Iterator[HangulMatch]:
        """패턴과 일치하는 원문 구간을 순서대로 반환합니다."""
        if not self.pattern:
            return iter(())

        word_basis, pattern_basis, starts, ends = self._get_word_basis(text)
        return _iter_matches(text, word_basis, pattern_basis, starts, ends, overlap)

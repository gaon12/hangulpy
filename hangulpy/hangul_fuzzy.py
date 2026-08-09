"""Hangul-aware edit distance and reusable fuzzy search index."""

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

from hangulpy.hangul_contains import hangul_search
from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.hangul_split import split_hangul_string


def _search_units(text: str) -> Tuple[str, ...]:
    normalized = normalize_hangul(text, "NFC")
    return tuple(split_hangul_string(normalized))


def _unit_distance(left: Sequence[str], right: Sequence[str]) -> float:
    if len(left) > len(right):
        left, right = right, left
    previous = [float(index) for index in range(len(left) + 1)]

    for right_index, right_unit in enumerate(right, start=1):
        current = [float(right_index)]
        for left_index, left_unit in enumerate(left, start=1):
            substitution = previous[left_index - 1] + (left_unit != right_unit)
            insertion = current[left_index - 1] + 1.0
            deletion = previous[left_index] + 1.0
            current.append(min(substitution, insertion, deletion))
        previous = current

    return previous[-1]


def hangul_distance(left: str, right: str) -> float:
    """자모 단위 Levenshtein 거리를 반환합니다.

    NFC와 NFD 입력은 같은 문자열로 취급하고, 복합 모음과 겹받침은 기본
    자모로 풀어서 비교합니다.
    """
    return _unit_distance(_search_units(left), _search_units(right))


def hangul_similarity(left: str, right: str) -> float:
    """두 문자열의 자모 유사도를 0.0에서 1.0 사이로 반환합니다."""
    left_units = _search_units(left)
    right_units = _search_units(right)
    length = max(len(left_units), len(right_units))
    if length == 0:
        return 1.0
    return 1.0 - (_unit_distance(left_units, right_units) / length)


def _best_substring_similarity(query: Sequence[str], candidate: Sequence[str]) -> float:
    if not query:
        return 1.0
    if not candidate:
        return 0.0

    # Sellers' approximate substring algorithm. The zero in each row makes
    # candidate prefixes free, so the last cell is the distance to a substring
    # ending at the current unit. This is O(len(query) * len(candidate)) and
    # avoids rebuilding a full Levenshtein matrix for every possible window.
    previous = [float(index) for index in range(len(query) + 1)]
    best_distance = previous[-1]
    for candidate_unit in candidate:
        current = [0.0]
        for query_index, query_unit in enumerate(query, start=1):
            substitution = previous[query_index - 1] + (query_unit != candidate_unit)
            insertion = current[query_index - 1] + 1.0
            deletion = previous[query_index] + 1.0
            current.append(min(substitution, insertion, deletion))
        best_distance = min(best_distance, current[-1])
        previous = current

    return 1.0 - (best_distance / len(query))


@dataclass(frozen=True)
class HangulSearchResult:
    """퍼지 검색 결과와 원본 컬렉션 위치입니다."""

    text: str
    score: float
    index: int
    match_index: int

    @property
    def matched(self) -> bool:
        """초성·부분 음절 검색으로 직접 일치했는지 반환합니다."""
        return self.match_index >= 0


class HangulIndex:
    """같은 문자열 컬렉션을 반복 검색하는 메모리 인덱스입니다."""

    def __init__(self, items: Iterable[str]) -> None:
        if isinstance(items, str):
            raise TypeError("items must be an iterable of strings, not a single string")
        self.items = tuple(items)
        if any(not isinstance(item, str) for item in self.items):
            raise TypeError("items must contain only strings")
        self._units = tuple(_search_units(item) for item in self.items)

    def search(
        self,
        query: str,
        *,
        limit: int = 10,
        min_score: float = 0.0,
    ) -> List[HangulSearchResult]:
        """직접 일치와 자모 유사도를 함께 사용해 결과를 정렬합니다."""
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise TypeError("limit must be an integer")
        if limit < 0:
            raise ValueError("limit must be non-negative")
        if not isinstance(min_score, (int, float)) or isinstance(min_score, bool):
            raise TypeError("min_score must be a number")
        if not 0.0 <= min_score <= 1.0:
            raise ValueError("min_score must be between 0.0 and 1.0")
        if limit == 0:
            return []

        query_units = _search_units(query)
        results: List[HangulSearchResult] = []
        for index, (item, candidate_units) in enumerate(zip(self.items, self._units)):
            match_index = hangul_search(item, query)
            score = (
                1.0
                if match_index >= 0
                else _best_substring_similarity(query_units, candidate_units)
            )
            if score >= min_score:
                results.append(HangulSearchResult(item, score, index, match_index))

        normalized_query = normalize_hangul(query, "NFC")
        results.sort(
            key=lambda result: (
                -result.score,
                (
                    0
                    if normalize_hangul(result.text, "NFC") == normalized_query
                    else 1 if result.matched else 2
                ),
                result.index,
            )
        )
        return results[:limit]

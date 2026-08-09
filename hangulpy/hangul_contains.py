# hangul_contains.py

from functools import lru_cache
from typing import List, Optional, Tuple

from hangulpy._deprecated import resolve_legacy_bool
from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.hangul_split import split_hangul_string
from hangulpy.utils import CHOSUNG_LIST, is_hangul


@lru_cache(maxsize=1024)
def _decompose_cached(text: str) -> str:
    """
    Cached version of string decomposition for performance.

    :param text: String to decompose
    :return: Decomposed string
    """
    normalized = normalize_hangul(text, "NFC")
    return "".join("".join(split_hangul_string(char)) for char in normalized)


@lru_cache(maxsize=1024)
def _decompose_search_data(text: str) -> Tuple[str, Tuple[int, ...]]:
    parts: List[str] = []
    positions: List[int] = []

    normalized = normalize_hangul(text, "NFC")
    for char_index, char in enumerate(normalized):
        split = [part for part in split_hangul_string(char) if part]
        parts.extend(split)
        positions.extend([char_index] * len(split))

    return "".join(parts), tuple(positions)


def _is_chosung_pattern(pattern: str) -> bool:
    return bool(pattern) and all(char in CHOSUNG_LIST for char in pattern)


@lru_cache(maxsize=1024)
def _chosung_search_data(text: str) -> Tuple[str, Tuple[int, ...]]:
    chosung_parts: List[str] = []
    positions: List[int] = []

    normalized = normalize_hangul(text, "NFC")
    for char_index, char in enumerate(normalized):
        split = split_hangul_string(char)
        if is_hangul(char):
            chosung_parts.append(split[0])
            positions.append(char_index)
        elif char in CHOSUNG_LIST:
            chosung_parts.append(char)
            positions.append(char_index)

    return "".join(chosung_parts), tuple(positions)


def _get_search_basis(word: str, pattern: str) -> Tuple[str, str, Tuple[int, ...]]:
    if _is_chosung_pattern(pattern):
        chosung_word, positions = _chosung_search_data(word)
        return chosung_word, pattern, positions

    word_split, positions = _decompose_search_data(word)
    return word_split, _decompose_cached(pattern), positions


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

    word_split, pattern_split, _ = _get_search_basis(word, pattern)

    return pattern_split in word_split


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

    word_split, pattern_split, positions = _get_search_basis(word, pattern)
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

    word_split, pattern_split, positions = _get_search_basis(word, pattern)

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
            pattern if self.is_chosung_pattern else _decompose_cached(pattern) if pattern else ""
        )

    def _get_word_basis(self, word: str) -> Tuple[str, Tuple[int, ...]]:
        if self.is_chosung_pattern:
            return _chosung_search_data(word)

        return _decompose_search_data(word)

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

        word_split, _ = self._get_word_basis(word)
        return self.pattern_split in word_split

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

        word_split, positions = self._get_word_basis(word)
        index = word_split.find(self.pattern_split)

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

        word_split, positions = self._get_word_basis(word)
        indices: List[int] = []
        start = 0
        while True:
            index = word_split.find(self.pattern_split, start)
            if index == -1:
                break
            indices.append(positions[index] if positions else index)
            start = index + 1

        return indices

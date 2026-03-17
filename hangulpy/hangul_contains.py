# hangul_contains.py

from functools import lru_cache
from typing import List, Tuple

from hangulpy.utils import CHOSUNG_LIST, is_hangul
from hangulpy.hangul_split import split_hangul_string


@lru_cache(maxsize=1024)
def _decompose_cached(text: str) -> str:
    """
    Cached version of string decomposition for performance.

    :param text: String to decompose
    :return: Decomposed string
    """
    return "".join("".join(split_hangul_string(char)) for char in text)


def _is_chosung_pattern(pattern: str) -> bool:
    return bool(pattern) and all(char in CHOSUNG_LIST for char in pattern)


@lru_cache(maxsize=1024)
def _chosung_search_data(text: str) -> Tuple[str, Tuple[int, ...]]:
    chosung_parts: List[str] = []
    positions: List[int] = []
    decomposed_index = 0

    for char in text:
        split = split_hangul_string(char)
        if is_hangul(char):
            chosung_parts.append(split[0])
            positions.append(decomposed_index)
        elif char in CHOSUNG_LIST:
            chosung_parts.append(char)
            positions.append(decomposed_index)

        decomposed_index += len(split)

    return "".join(chosung_parts), tuple(positions)


def _get_search_basis(word: str, pattern: str) -> Tuple[str, str, Tuple[int, ...]]:
    if _is_chosung_pattern(pattern):
        chosung_word, positions = _chosung_search_data(word)
        return chosung_word, pattern, positions

    return _decompose_cached(word), _decompose_cached(pattern), ()


def hangul_contains(word: str, pattern: str, notallowempty: bool = False) -> bool:
    """
    주어진 한글 문자열이 다른 한글 문자열을 포함하는지 검사합니다.

    :param word: 검사할 한글 문자열
    :param pattern: 포함 여부를 검사할 한글 문자열 패턴
    :param notallowempty: 패턴이 빈 문자열일 때 false를 반환하는 옵션
    :return: 포함되면 True, 아니면 False
    """
    if not pattern:
        return not notallowempty

    word_split, pattern_split, _ = _get_search_basis(word, pattern)

    return pattern_split in word_split


def hangul_search(word: str, pattern: str, notallowempty: bool = False) -> int:
    """
    한글 문자열에서 패턴을 검색하고 첫 번째 매칭 위치의 인덱스를 반환합니다.

    :param word: 검사할 한글 문자열
    :param pattern: 검색할 한글 문자열 패턴
    :param notallowempty: 패턴이 빈 문자열일 때 -1을 반환하는 옵션
    :return: 매칭 시작 인덱스, 없으면 -1
    """
    if not pattern:
        return -1 if notallowempty else 0

    word_split, pattern_split, positions = _get_search_basis(word, pattern)
    index = word_split.find(pattern_split)

    if index == -1:
        return -1

    if positions:
        return positions[index]

    return index


def hangul_search_all(word: str, pattern: str, notallowempty: bool = False) -> List[int]:
    """
    한글 문자열에서 패턴이 나타나는 모든 위치의 인덱스를 반환합니다.

    :param word: 검사할 한글 문자열
    :param pattern: 검색할 한글 문자열 패턴
    :param notallowempty: 패턴이 빈 문자열일 때 빈 리스트를 반환하는 옵션
    :return: 매칭 위치 인덱스 리스트
    """
    if not pattern:
        return [] if notallowempty else [0]

    word_split, pattern_split, positions = _get_search_basis(word, pattern)

    indices: List[int] = []
    start = 0
    while True:
        index = word_split.find(pattern_split, start)
        if index == -1:
            break
        indices.append(positions[index] if positions else index)
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

        return _decompose_cached(word), ()

    def search(self, word: str, notallowempty: bool = False) -> bool:
        """
        문자열에서 패턴을 검색하고 포함 여부를 반환합니다.

        :param word: 검사할 문자열
        :param notallowempty: 패턴이 빈 문자열일 때 false를 반환하는 옵션
        :return: 포함되면 True, 아니면 False
        """
        if not self.pattern:
            return not notallowempty

        word_split, _ = self._get_word_basis(word)
        return self.pattern_split in word_split

    def find_index(self, word: str, notallowempty: bool = False) -> int:
        """
        문자열에서 패턴의 첫 번째 매칭 위치를 반환합니다.

        :param word: 검사할 문자열
        :param notallowempty: 패턴이 빈 문자열일 때 -1을 반환하는 옵션
        :return: 매칭 시작 인덱스, 없으면 -1
        """
        if not self.pattern:
            return -1 if notallowempty else 0

        word_split, positions = self._get_word_basis(word)
        index = word_split.find(self.pattern_split)

        if index == -1:
            return -1

        if positions:
            return positions[index]

        return index

    def find_all(self, word: str, notallowempty: bool = False) -> List[int]:
        """
        문자열에서 패턴이 나타나는 모든 위치를 반환합니다.

        :param word: 검사할 문자열
        :param notallowempty: 패턴이 빈 문자열일 때 빈 리스트를 반환하는 옵션
        :return: 매칭 위치 인덱스 리스트
        """
        if not self.pattern:
            return [] if notallowempty else [0]

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

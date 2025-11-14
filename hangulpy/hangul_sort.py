# sort_hangul.py

from typing import List, Tuple, Union
from hangulpy.hangul_decompose import decompose_hangul_string

def sort_hangul(words: List[str], reverse: bool = False) -> List[str]:
    """
    한글 문자열을 초성, 중성, 종성을 기준으로 정렬합니다.

    :param words: 한글 문자열 리스트
    :param reverse: 역순 정렬 여부 (기본값: False)
    :return: 정렬된 한글 문자열 리스트
    """
    def hangul_key(word: str) -> Tuple[Tuple[str, Union[str, Tuple[str, ...]], Union[str, Tuple[str, ...]]], ...]:
        # 초성, 중성, 종성을 튜플로 변환하여 정렬 키로 사용
        return tuple(decompose_hangul_string(word))

    return sorted(words, key=hangul_key, reverse=reverse)

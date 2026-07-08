import re
from typing import List

from hangulpy.hangul_decompose import decompose_hangul_string


def _compile_pattern(pattern: str, wildcard: bool, regex: bool) -> re.Pattern[str]:
    if regex:
        return re.compile(pattern)

    escaped = re.escape(pattern)
    if wildcard:
        escaped = escaped.replace(r"\*", ".*")
    return re.compile(escaped)


def match_hangul_pattern(
    words: List[str],
    pattern: str,
    wildcard: bool = True,
    regex: bool = False,
) -> List[str]:
    """
    주어진 단어 리스트에서 특정 초성, 중성, 종성 패턴에 매칭되는 단어를 찾습니다.

    :param words: 단어 리스트
    :param pattern: 초성, 중성, 종성 패턴 (예: '*ㅜ')
    :return: 패턴에 매칭되는 단어 리스트
    """
    # 패턴을 정규식으로 변환
    regex_pattern = _compile_pattern(pattern, wildcard=wildcard, regex=regex)

    matched_words: List[str] = []
    for word in words:
        decomposed = decompose_hangul_string(word)  # 한글 분해
        decomposed_flat = "".join(
            chosung + "".join(jungsung) + "".join(jongsung)
            for chosung, jungsung, jongsung in decomposed
        )  # 초성, 중성, 종성을 문자열로 결합

        if regex_pattern.fullmatch(decomposed_flat):
            matched_words.append(word)

    return matched_words

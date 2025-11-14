# chosung.py

from hangulpy.utils import is_hangul, CHOSUNG_LIST, HANGUL_BEGIN_UNICODE, CHOSUNG_BASE

def get_chosung_string(text: str, keep_spaces: bool = False) -> str:
    """
    문자열의 초성을 추출합니다.
    """
    return ''.join(extract_chosung(c) if is_hangul(c) else c for c in text) if keep_spaces else ''.join(extract_chosung(c) if is_hangul(c) and not c.isspace() else '' for c in text)


def extract_chosung(c: str) -> str:
    if is_hangul(c):
        code = ord(c) - HANGUL_BEGIN_UNICODE
        cho_idx = code // CHOSUNG_BASE
        return CHOSUNG_LIST[cho_idx]
    else:
        return c

def chosungIncludes(word: str, pattern: str) -> bool:
    """
    초성으로 검색합니다.

    :param word: 검색 대상 문자열
    :param pattern: 초성 패턴
    :return: 포함 여부
    """
    word_chosung = ''.join(extract_chosung(c) for c in word if is_hangul(c))
    return pattern in word_chosung

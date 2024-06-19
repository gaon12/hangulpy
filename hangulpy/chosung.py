# chosung.py

from hangulpy.utils import CHOSUNG_LIST, CHOSUNG_BASE, is_hangul_char, HANGUL_BEGIN_UNICODE

def get_chosung(c):
    """
    주어진 한글 음절의 초성을 반환합니다.
    
    :param c: 한글 음절 문자
    :return: 초성 문자 (한글이 아니면 그대로 반환)
    """
    if is_hangul_char(c):
        char_index = ord(c) - HANGUL_BEGIN_UNICODE
        chosung_index = char_index // CHOSUNG_BASE
        return CHOSUNG_LIST[chosung_index]
    return c

def get_chosung_string(text, keep_spaces=False):
    """
    주어진 문자열의 각 문자의 초성을 반환합니다.
    
    :param text: 한글 문자열
    :param keep_spaces: 공백을 유지할지 여부 (기본값: False)
    :return: 초성 문자열
    """
    if keep_spaces:
        return ''.join(get_chosung(c) if is_hangul_char(c) else c for c in text)
    else:
        return ''.join(get_chosung(c) for c in text if is_hangul_char(c) or not c.isspace())

def chosungIncludes(word, pattern):
    """
    주어진 단어에 패턴의 초성이 포함되어 있는지 확인합니다.
    
    :param word: 검색할 단어
    :param pattern: 검색할 초성 패턴
    :return: 패턴이 단어의 초성에 포함되어 있으면 True, 아니면 False
    """
    # 단어의 각 문자를 초성으로 변환하여 문자열을 생성합니다.
    word_chosung = ''.join(get_chosung(c) for c in word)
    # 패턴이 초성 문자열에 포함되어 있는지 확인합니다.
    return pattern in word_chosung
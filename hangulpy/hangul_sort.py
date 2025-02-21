# sort_hangul.py

from hangulpy.hangul_decompose import decompose_hangul_string

def sort_hangul(words, reverse=False):
    """
    한글 문자열을 초성, 중성, 종성을 기준으로 정렬합니다.
    
    :param words: 한글 문자열 리스트
    :param reverse: 역순 정렬 여부 (기본값: False)
    :return: 정렬된 한글 문자열 리스트
    """
    if not isinstance(words, list) or not all(isinstance(word, str) for word in words):
        raise TypeError("입력 값은 문자열 리스트여야 합니다. (Input must be a list of strings)")

    def hangul_key(word):
        # 초성, 중성, 종성을 튜플로 변환하여 정렬 키로 사용
        return tuple(decompose_hangul_string(word))

    return sorted(words, key=hangul_key, reverse=reverse)

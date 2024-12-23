# sort_hangul.py

from hangulpy.hangul_decompose import decompose_hangul_string

def sort_hangul(words):
    """
    한글 문자열을 초성, 중성, 종성을 기준으로 정렬합니다.

    :param words: 한글 문자열 리스트
    :return: 정렬된 한글 문자열 리스트
    """
    if not isinstance(words, list):
        raise ValueError("입력 값은 리스트여야 합니다. (Input must be a list of strings)")

    def hangul_key(word):
        # 각 글자를 초성, 중성, 종성으로 분해하여 정렬 키로 사용
        decomposed = decompose_hangul_string(word)
        # 분해된 결과를 튜플로 묶어서 반환
        return [(chosung, ''.join(jungsung), ''.join(jongsung)) for chosung, jungsung, jongsung in decomposed]

    return sorted(words, key=hangul_key)

# hangul_decompose.py

import warnings
from hangulpy.utils import (
    CHOSUNG_LIST, CHOSUNG_BASE, is_hangul, HANGUL_BEGIN_UNICODE,
    JUNGSUNG_LIST, JUNGSUNG_DECOMPOSE, JONGSUNG_LIST, JONGSUNG_DECOMPOSE, JUNGSUNG_BASE
)

def decompose_hangul_string(s):
    """
    주어진 문자열의 각 한글 음절을 초성, 중성, 종성으로 분해하여 배열 형태로 반환합니다.

    :param s: 문자열
    :return: 각 한글 음절을 초성, 중성, 종성으로 분해한 결과를 포함하는 배열
    """
    result = []
    for char in s:
        if is_hangul(char):
            # 한글 음절의 유니코드 값을 기준으로 각 성분의 인덱스를 계산합니다.
            char_index = ord(char) - HANGUL_BEGIN_UNICODE
            chosung_index = char_index // CHOSUNG_BASE
            jungsung_index = (char_index % CHOSUNG_BASE) // JUNGSUNG_BASE
            jongsung_index = char_index % JUNGSUNG_BASE

            # 중성 및 종성 분해
            jungsung = JUNGSUNG_LIST[jungsung_index]
            jongsung = JONGSUNG_LIST[jongsung_index]

            jungsung_decomposed = JUNGSUNG_DECOMPOSE.get(jungsung, (jungsung,))
            jongsung_decomposed = JONGSUNG_DECOMPOSE.get(jongsung, (jongsung,))

            result.append((CHOSUNG_LIST[chosung_index], jungsung_decomposed, jongsung_decomposed))
        else:
            result.append((char, '', ''))  # 한글이 아니면 그대로 추가

    return result

# hangul_split.py

from typing import List

from hangulpy.utils import (
    JONGSUNG_DECOMPOSE,
    JUNGSUNG_DECOMPOSE,
    decompose_syllable,
)


def split_hangul_string(s: str) -> List[str]:
    """
    주어진 문자열의 각 한글 음절을 초성, 중성, 종성으로 분해하여 배열 형태로 반환합니다.

    :param s: 문자열
    :return: 각 한글 음절을 초성, 중성, 종성으로 분해한 결과를 포함하는 배열
    """
    from hangulpy.hangul_normalize import normalize_hangul

    result: List[str] = []
    for char in normalize_hangul(s, "NFC"):
        components = decompose_syllable(char)
        if components is not None:
            chosung, jungsung, jongsung = components

            jungsung_decomposed = JUNGSUNG_DECOMPOSE.get(jungsung, (jungsung,))
            jongsung_decomposed = JONGSUNG_DECOMPOSE.get(jongsung, (jongsung,) if jongsung else ())

            result.append(chosung)
            result.extend(jungsung_decomposed)
            result.extend(jongsung_decomposed)
        elif char in JUNGSUNG_DECOMPOSE:
            result.extend(JUNGSUNG_DECOMPOSE[char])
        elif char in JONGSUNG_DECOMPOSE:
            result.extend(JONGSUNG_DECOMPOSE[char])
        else:
            result.append(char)  # 한글이 아니면 그대로 추가

    return result

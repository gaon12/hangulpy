# hangul_decompose.py


from hangulpy.utils import (
    JONGSUNG_DECOMPOSE,
    JUNGSUNG_DECOMPOSE,
    decompose_syllable,
)


def decompose_hangul_string(
    s: str,
) -> list[tuple[str, str | tuple[str, ...], str | tuple[str, ...]]]:
    """
    주어진 문자열의 각 한글 음절을 초성, 중성, 종성으로 분해하여 배열 형태로 반환합니다.

    :param s: 문자열
    :return: 각 한글 음절을 초성, 중성, 종성으로 분해한 결과를 포함하는 배열
    """
    result: list[tuple[str, str | tuple[str, ...], str | tuple[str, ...]]] = []
    for char in s:
        components = decompose_syllable(char)
        if components is not None:
            chosung, jungsung, jongsung = components

            jungsung_decomposed = JUNGSUNG_DECOMPOSE.get(jungsung, (jungsung,))
            jongsung_decomposed = JONGSUNG_DECOMPOSE.get(jongsung, (jongsung,))

            result.append((chosung, jungsung_decomposed, jongsung_decomposed))
        else:
            result.append((char, "", ""))  # 한글이 아니면 그대로 추가

    return result

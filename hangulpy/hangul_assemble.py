# hangul_assemble.py
# High-level API for syllable splitting and joining

from typing import List, Union
from hangulpy.hangul_split import split_hangul_string
from hangulpy.utils import (
    CHOSUNG_LIST,
    JUNGSUNG_LIST,
    JONGSUNG_LIST,
    compose_syllable,
)


def split_syllables(text: str, output_format: str = 'list') -> Union[List[str], str]:
    """
    한글 문자열을 자모 단위로 분해합니다.
    hangul-utils의 split_syllables와 유사한 고수준 API입니다.

    :param text: 분해할 문자열
    :param output_format: 출력 형식 ('list', 'string')
    :return: 분해된 자모 (리스트 또는 문자열)
    """
    result: List[str] = []
    for char in text:
        decomposed = split_hangul_string(char)
        result.extend(decomposed)

    if output_format == 'string':
        return ''.join(result)
    return result


def join_jamos(jamos: Union[List[str], str]) -> str:
    """
    자모 리스트나 문자열을 완성형 한글로 조합합니다.
    hangul-utils의 join_jamos와 유사한 고수준 API입니다.

    :param jamos: 자모 리스트 또는 문자열
    :return: 조합된 한글 문자열
    """
    if isinstance(jamos, str):
        jamos = list(jamos)

    result: List[str] = []
    i = 0
    while i < len(jamos):
        char = jamos[i]

        # 초성인 경우
        if char in CHOSUNG_LIST:
            cho = char
            jung = ''
            jong = ''

            # 다음 문자가 중성인지 확인
            if i + 1 < len(jamos) and jamos[i + 1] in JUNGSUNG_LIST:
                jung = jamos[i + 1]
                i += 1

                # 다음 문자가 종성인지 확인
                if i + 1 < len(jamos) and jamos[i + 1] in JONGSUNG_LIST:
                    jong = jamos[i + 1]
                    i += 1

                # 음절 조합
                try:
                    syllable = compose_syllable(cho, jung, jong)
                    result.append(syllable)
                except:
                    # 조합 실패 시 원본 자모 그대로 추가
                    result.append(cho)
                    result.append(jung)
                    if jong:
                        result.append(jong)
            else:
                # 중성이 없으면 초성만 추가
                result.append(char)
        else:
            # 초성이 아닌 경우 그대로 추가
            result.append(char)

        i += 1

    return ''.join(result)


def disassemble(text: str, output_format: str = 'list') -> Union[List[str], str]:
    """
    한글 문자열을 자모로 분해합니다 (split_syllables의 별칭).

    :param text: 분해할 문자열
    :param output_format: 출력 형식 ('list', 'string')
    :return: 분해된 자모
    """
    return split_syllables(text, output_format)


def assemble(jamos: Union[List[str], str]) -> str:
    """
    자모를 한글로 조합합니다 (join_jamos의 별칭).

    :param jamos: 자모 리스트 또는 문자열
    :return: 조합된 한글 문자열
    """
    return join_jamos(jamos)

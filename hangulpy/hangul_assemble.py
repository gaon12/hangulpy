# hangul_assemble.py
# High-level API for syllable splitting and joining

from typing import Dict, List, Optional, Union

from hangulpy.hangul_split import split_hangul_string
from hangulpy.utils import (
    CHOSUNG_LIST,
    COMPOUND_FINAL_MAP,
    JONGSUNG_LIST,
    JUNGSUNG_LIST,
    VOWEL_COMBO,
    compose_syllable,
)


def split_syllables(text: str, output_format: str = "list") -> Union[List[str], str]:
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

    if output_format == "string":
        return "".join(result)
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

        if char not in CHOSUNG_LIST or i + 1 >= len(jamos) or jamos[i + 1] not in JUNGSUNG_LIST:
            result.append(char)
            i += 1
            continue

        cho = char
        jung = jamos[i + 1]
        consumed = 2

        if i + consumed < len(jamos) and (jung, jamos[i + consumed]) in VOWEL_COMBO:
            jung = VOWEL_COMBO[(jung, jamos[i + consumed])]
            consumed += 1

        jong = ""
        next_index = i + consumed
        if next_index < len(jamos) and jamos[next_index] in JONGSUNG_LIST[1:]:
            next_char = jamos[next_index]
            after_next = next_index + 1

            if after_next < len(jamos) and jamos[after_next] in JUNGSUNG_LIST:
                jong = ""
            elif (
                after_next < len(jamos)
                and (next_char, jamos[after_next]) in COMPOUND_FINAL_MAP
                and not (after_next + 1 < len(jamos) and jamos[after_next + 1] in JUNGSUNG_LIST)
            ):
                jong = COMPOUND_FINAL_MAP[(next_char, jamos[after_next])]
                consumed += 2
            else:
                jong = next_char
                consumed += 1

        result.append(compose_syllable(cho, jung, jong))
        i += consumed

    return "".join(result)


def combine_vowels(vowel1: str, vowel2: str, join_on_fail: bool = False) -> Optional[str]:
    """
    두 모음을 결합해 복합 모음을 만듭니다.

    :param vowel1: 첫 번째 모음
    :param vowel2: 두 번째 모음
    :return: 결합 가능한 경우 복합 모음, 아니면 None
    """
    combined = VOWEL_COMBO.get((vowel1, vowel2))
    if combined is not None:
        return combined
    if join_on_fail:
        return vowel1 + vowel2
    return None


def combine_character(cho: str, jung: str, jong: str = "") -> str:
    """
    초성, 중성, 종성을 한 음절로 결합합니다.

    :param cho: 초성
    :param jung: 중성
    :param jong: 종성
    :return: 완성형 한글 음절
    """
    return compose_syllable(cho, jung, jong)


def disassemble_to_groups(text: str) -> List[List[str]]:
    """
    문자열을 글자별 자모 그룹으로 분해합니다.

    :param text: 분해할 문자열
    :return: 글자별 자모 그룹
    """
    return [[part for part in split_hangul_string(char) if part] for char in text]


def disassemble_complete_character(char: str) -> Optional[Dict[str, str]]:
    """
    완성형 한글 한 글자를 초성, 중성, 종성 문자열로 분해합니다.

    :param char: 완성형 한글 한 글자
    :return: 구성 요소 딕셔너리, 완성형 한글이 아니면 None
    """
    if len(char) != 1:
        return None

    parts = split_hangul_string(char)
    if len(parts) < 2 or parts[0] not in CHOSUNG_LIST or parts[1] not in JUNGSUNG_LIST:
        return None

    jung = parts[1]
    jong_start = 2
    if len(parts) > 2 and (jung, parts[2]) in VOWEL_COMBO:
        jung = VOWEL_COMBO[(jung, parts[2])]
        jong_start = 3

    return {
        "choseong": parts[0],
        "jungseong": jung,
        "jongseong": "".join(parts[jong_start:]),
    }


def remove_last_character(text: str) -> str:
    """
    마지막 글자의 마지막 자모를 제거합니다.

    :param text: 대상 문자열
    :return: 마지막 자모가 제거된 문자열
    """
    if not text:
        return ""

    groups = disassemble_to_groups(text)
    if not groups:
        return ""

    groups[-1] = groups[-1][:-1]
    flattened = [part for group in groups for part in group]
    return join_jamos(flattened)


def disassemble(text: str, output_format: str = "list") -> Union[List[str], str]:
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

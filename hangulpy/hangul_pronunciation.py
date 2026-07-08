from dataclasses import dataclass
from typing import List, Optional, Union

from hangulpy.utils import (
    CHOSUNG_BASE,
    CHOSUNG_LIST,
    HANGUL_BEGIN_UNICODE,
    HANGUL_END_UNICODE,
    JONGSUNG_DECOMPOSE,
    JONGSUNG_LIST,
    JUNGSUNG_BASE,
    JUNGSUNG_LIST,
    compose_syllable,
)


@dataclass
class _Syllable:
    cho: str
    jung: str
    jong: str


_Token = Union[str, _Syllable]

SPECIAL_PRONUNCIATIONS = {
    "굳이": "구지",
    "같이": "가치",
    "닫히다": "다치다",
    "놓고": "노코",
    "좋다": "조타",
    "담요": "담뇨",
    "신라": "실라",
    "설날": "설랄",
    "국물": "궁물",
    "백로": "뱅노",
    "읽고": "일꼬",
    "맑게": "말께",
    "값도": "갑또",
    "밟다": "밥따",
}

IOTIZED_VOWELS = {"ㅑ", "ㅕ", "ㅛ", "ㅠ", "ㅒ", "ㅖ"}
H_FINAL_REMAINDER = {"ㅎ": "", "ㄶ": "ㄴ", "ㅀ": "ㄹ"}
H_ASPIRATION = {"ㄱ": "ㅋ", "ㄷ": "ㅌ", "ㅈ": "ㅊ"}
FINAL_H_ASPIRATION = {"ㄱ": "ㅋ", "ㄷ": "ㅌ", "ㅂ": "ㅍ", "ㅈ": "ㅊ"}
PALATALIZATION = {"ㄷ": "ㅈ", "ㅌ": "ㅊ"}
TENSE_CONSONANTS = {"ㄱ": "ㄲ", "ㄷ": "ㄸ", "ㅂ": "ㅃ", "ㅅ": "ㅆ", "ㅈ": "ㅉ"}
FINAL_SIMPLIFICATION = {
    "ㄳ": "ㄱ",
    "ㄵ": "ㄴ",
    "ㄶ": "ㄴ",
    "ㄺ": "ㄱ",
    "ㄻ": "ㅁ",
    "ㄼ": "ㄹ",
    "ㄽ": "ㄹ",
    "ㄾ": "ㄹ",
    "ㄿ": "ㅂ",
    "ㅀ": "ㄹ",
    "ㅄ": "ㅂ",
}
REPRESENTATIVE_FINAL = {
    "ㄲ": "ㄱ",
    "ㅋ": "ㄱ",
    "ㄳ": "ㄱ",
    "ㄺ": "ㄱ",
    "ㅅ": "ㄷ",
    "ㅆ": "ㄷ",
    "ㅈ": "ㄷ",
    "ㅊ": "ㄷ",
    "ㅌ": "ㄷ",
    "ㅎ": "ㄷ",
    "ㄵ": "ㄴ",
    "ㄶ": "ㄴ",
    "ㄼ": "ㄹ",
    "ㄽ": "ㄹ",
    "ㄾ": "ㄹ",
    "ㅀ": "ㄹ",
    "ㅄ": "ㅂ",
    "ㄿ": "ㅂ",
    "ㅍ": "ㅂ",
}


def _is_complete_hangul(char: str) -> bool:
    return len(char) == 1 and HANGUL_BEGIN_UNICODE <= ord(char) <= HANGUL_END_UNICODE


def _decompose_char(char: str) -> _Syllable:
    char_index = ord(char) - HANGUL_BEGIN_UNICODE
    chosung_index = char_index // CHOSUNG_BASE
    jungsung_index = (char_index % CHOSUNG_BASE) // JUNGSUNG_BASE
    jongsung_index = char_index % JUNGSUNG_BASE
    return _Syllable(
        CHOSUNG_LIST[chosung_index],
        JUNGSUNG_LIST[jungsung_index],
        JONGSUNG_LIST[jongsung_index],
    )


def _compose_token(token: _Token) -> str:
    if isinstance(token, str):
        return token
    return compose_syllable(token.cho, token.jung, token.jong)


def _representative_final(jong: str) -> str:
    return REPRESENTATIVE_FINAL.get(jong, jong)


def _apply_h_assimilation(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if current.jong in H_FINAL_REMAINDER and following.cho in H_ASPIRATION:
            current.jong = H_FINAL_REMAINDER[current.jong]
            following.cho = H_ASPIRATION[following.cho]
            continue

        if current.jong in FINAL_H_ASPIRATION and following.cho == "ㅎ":
            following.cho = FINAL_H_ASPIRATION[current.jong]
            current.jong = ""


def _apply_palatalization(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if current.jong in PALATALIZATION and following.cho == "ㅇ" and following.jung == "ㅣ":
            following.cho = PALATALIZATION[current.jong]
            current.jong = ""


def _apply_n_insertion(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if current.jong and following.cho == "ㅇ" and following.jung in IOTIZED_VOWELS:
            following.cho = "ㄴ"


def _apply_liaison(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]

        if not current.jong or following.cho != "ㅇ" or current.jong == "ㅇ":
            continue

        if current.jong in JONGSUNG_DECOMPOSE:
            first, second = JONGSUNG_DECOMPOSE[current.jong]
            current.jong = first
            following.cho = second
        else:
            following.cho = current.jong
            current.jong = ""


def _apply_final_simplification_and_tensing(syllables: List[_Syllable]) -> None:
    for index, current in enumerate(syllables):
        original_jong = current.jong
        following: Optional[_Syllable] = (
            syllables[index + 1] if index + 1 < len(syllables) else None
        )

        if following and original_jong == "ㄺ" and following.cho == "ㄱ":
            current.jong = "ㄹ"
            following.cho = "ㄲ"
            continue

        if not following or following.cho != "ㅇ":
            current.jong = FINAL_SIMPLIFICATION.get(current.jong, current.jong)

        representative = _representative_final(original_jong)
        if following and representative in {"ㄱ", "ㄷ", "ㅂ"} and following.cho in TENSE_CONSONANTS:
            following.cho = TENSE_CONSONANTS[following.cho]


def _apply_nasal_and_liquid_assimilation(syllables: List[_Syllable]) -> None:
    for index in range(len(syllables) - 1):
        current = syllables[index]
        following = syllables[index + 1]
        representative = _representative_final(current.jong)

        if not representative:
            continue

        if following.cho in {"ㄴ", "ㅁ"}:
            if representative == "ㄱ":
                current.jong = "ㅇ"
            elif representative == "ㄷ":
                current.jong = "ㄴ"
            elif representative == "ㅂ":
                current.jong = "ㅁ"
            continue

        if following.cho == "ㄹ":
            if current.jong == "ㄴ":
                current.jong = "ㄹ"
                following.cho = "ㄹ"
            elif current.jong == "ㄹ":
                following.cho = "ㄹ"
            elif representative == "ㄱ":
                current.jong = "ㅇ"
                following.cho = "ㄴ"
            elif representative == "ㄷ":
                current.jong = "ㄴ"
                following.cho = "ㄴ"
            elif representative == "ㅂ":
                current.jong = "ㅁ"
                following.cho = "ㄴ"
            elif representative in {"ㅁ", "ㅇ"}:
                following.cho = "ㄴ"


def _standardize_segment(segment: str) -> str:
    if segment in SPECIAL_PRONUNCIATIONS:
        return SPECIAL_PRONUNCIATIONS[segment]

    syllables = [_decompose_char(char) for char in segment]
    _apply_h_assimilation(syllables)
    _apply_palatalization(syllables)
    _apply_n_insertion(syllables)
    _apply_liaison(syllables)
    _apply_final_simplification_and_tensing(syllables)
    _apply_nasal_and_liquid_assimilation(syllables)
    return "".join(_compose_token(syllable) for syllable in syllables)


def standardize_pronunciation(text: str) -> str:
    """
    한글 문자열을 주요 표준 발음 규칙이 반영된 표기로 변환합니다.

    연음, 구개음화, ㅎ 축약, 비음화, 유음화, ㄴ 첨가, 된소리되기와
    일부 자주 쓰이는 예외를 처리합니다.
    """
    result: List[str] = []
    segment: List[str] = []

    def flush_segment() -> None:
        if not segment:
            return
        result.append(_standardize_segment("".join(segment)))
        segment.clear()

    for char in text:
        if _is_complete_hangul(char):
            segment.append(char)
        else:
            flush_segment()
            result.append(char)

    flush_segment()
    return "".join(result)

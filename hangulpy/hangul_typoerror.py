# hangul_typoerror.py

import unicodedata
from typing import List, Optional, TypedDict, overload

from hangulpy._deprecated import resolve_legacy_bool
from hangulpy.utils import (
    CHOSUNG_LIST,
    COMPOUND_FINAL_DECOMP,
    COMPOUND_FINAL_MAP,
    CONSONANT_MAP,
    CONSONANT_RMAP,
    DOUBLE_INITIAL_MAP,
    JONGSUNG_LIST,
    JUNGSUNG_LIST,
    VOWEL_COMBO,
    VOWEL_MAP,
    VOWEL_RMAP,
    compose_syllable,
    is_hangul,
)


class _EnkoState(TypedDict):
    cho: Optional[str]
    jung: Optional[str]
    jong: str
    jong_combined: bool


_LEGACY_DOUBLE_CONSONANT = "allowDoubleConsonant"


@overload
def enko(eng_text: str, allow_double_consonant: bool = False) -> str: ...


@overload
def enko(eng_text: str, *, allowDoubleConsonant: bool) -> str: ...


def enko(
    eng_text: str,
    allow_double_consonant: Optional[bool] = None,
    **legacy_kwargs: object,
) -> str:
    """
    영문 키보드 입력값을 한글 자모 조합으로 변환합니다.

    :param eng_text: 변환할 영문 문자열
    :param allow_double_consonant: 두 개의 초성 결합(쌍자음) 허용 여부
    :return: 한글 자판 입력 문자열
    """
    allow_double = resolve_legacy_bool(
        allow_double_consonant,
        legacy_kwargs,
        _LEGACY_DOUBLE_CONSONANT,
        "allow_double_consonant",
    )

    result: List[str] = []
    state: _EnkoState = {"cho": None, "jung": None, "jong": "", "jong_combined": False}

    def flush() -> None:
        nonlocal state, result
        if state["cho"] is not None:
            if state["jung"] is not None:
                syll = compose_syllable(state["cho"], state["jung"], state["jong"] or "")
                result.append(syll)
            else:
                result.append(state["cho"])
        state = {"cho": None, "jung": None, "jong": "", "jong_combined": False}

    i = 0
    N = len(eng_text)
    while i < N:
        # 공백 문자면 현재 음절 flush 후 공백 추가
        if eng_text[i] == " ":
            flush()
            result.append(" ")
            i += 1
            continue

        token = None
        # 두 글자 조합(예: "hk", "nj" 등)으로 된 모음 먼저 처리
        if i + 1 < N and eng_text[i : i + 2] in VOWEL_MAP:
            token = VOWEL_MAP[eng_text[i : i + 2]]
            i += 2
        else:
            ch = eng_text[i]
            if ch in VOWEL_MAP:
                token = VOWEL_MAP[ch]
            elif ch in CONSONANT_MAP:
                token = CONSONANT_MAP[ch]
            else:
                flush()
                result.append(ch)
                i += 1
                continue
            i += 1

        if token in JUNGSUNG_LIST:
            current_jung = state["jung"]
            if state["cho"] is None:
                # 중성이 들어왔는데 초성이 없으면 기본 초성 'ㅇ' 사용
                state["cho"] = "ㅇ"
                state["jung"] = token
            elif current_jung is None:
                state["jung"] = token
            elif state["jong"]:
                # 겹받침은 첫 자음만 받침으로 남기고 둘째 자음을 다음 초성으로 옮긴다.
                current_jong = state["jong"]
                assert state["cho"] is not None
                if state["jong_combined"] and current_jong in COMPOUND_FINAL_DECOMP:
                    remaining_jong, next_cho = COMPOUND_FINAL_DECOMP[current_jong]
                else:
                    remaining_jong, next_cho = "", current_jong
                syll = compose_syllable(state["cho"], current_jung, remaining_jong)
                result.append(syll)
                state = {
                    "cho": next_cho,
                    "jung": token,
                    "jong": "",
                    "jong_combined": False,
                }
            elif (current_jung, token) in VOWEL_COMBO:
                state["jung"] = VOWEL_COMBO[(current_jung, token)]
            else:
                assert state["cho"] is not None
                syll = compose_syllable(state["cho"], current_jung, "")
                result.append(syll)
                state = {"cho": "ㅇ", "jung": token, "jong": "", "jong_combined": False}
        else:  # token이 자음인 경우
            if state["cho"] is None:
                state["cho"] = token
            elif state["jung"] is None:
                if allow_double and (state["cho"], token) in DOUBLE_INITIAL_MAP:
                    state["cho"] = DOUBLE_INITIAL_MAP[(state["cho"], token)]
                else:
                    flush()
                    state["cho"] = token
            else:
                if not state["jong"]:
                    if token in JONGSUNG_LIST[1:]:
                        state["jong"] = token
                        state["jong_combined"] = False
                    else:
                        flush()
                        state["cho"] = token
                else:
                    if (state["jong"], token) in COMPOUND_FINAL_MAP:
                        state["jong"] = COMPOUND_FINAL_MAP[(state["jong"], token)]
                        state["jong_combined"] = True
                    else:
                        flush()
                        state["cho"] = token
    flush()
    return "".join(result)


def _normalize_qwerty_case(text: str) -> str:
    normalized: List[str] = []
    for char in text:
        if char in CONSONANT_MAP or char in VOWEL_MAP:
            normalized.append(char)
        else:
            normalized.append(char.lower())
    return "".join(normalized)


@overload
def convert_qwerty_to_hangul(text: str, allow_double_consonant: bool = False) -> str: ...


@overload
def convert_qwerty_to_hangul(text: str, *, allowDoubleConsonant: bool) -> str: ...


def convert_qwerty_to_hangul(
    text: str,
    allow_double_consonant: Optional[bool] = None,
    **legacy_kwargs: object,
) -> str:
    """
    QWERTY 자판 입력을 한글 문장으로 변환합니다.

    :param text: 변환할 QWERTY 문자열
    :param allow_double_consonant: 두 개의 초성 허용 여부
    :return: 한글 문자열
    """
    allow_double = resolve_legacy_bool(
        allow_double_consonant,
        legacy_kwargs,
        _LEGACY_DOUBLE_CONSONANT,
        "allow_double_consonant",
    )

    if allow_double:
        return enko(_normalize_qwerty_case(text), allow_double_consonant=True)

    from hangulpy.hangul_assemble import join_jamos

    return join_jamos(convert_qwerty_to_alphabet(text))


def convert_qwerty_to_alphabet(text: str) -> str:
    """
    QWERTY 자판 입력을 조합하지 않고 한글 자모로 변환합니다.

    :param text: 변환할 QWERTY 문자열
    :return: 한글 자모 문자열
    """
    result: List[str] = []
    for char in _normalize_qwerty_case(text):
        if char in CONSONANT_MAP:
            result.append(CONSONANT_MAP[char])
        elif char in VOWEL_MAP and len(char) == 1:
            result.append(VOWEL_MAP[char])
        else:
            result.append(char)
    return "".join(result)


def _canonical_jamo_to_compat(char: str) -> str:
    code = ord(char)
    if 0x1100 <= code <= 0x1112:
        return CHOSUNG_LIST[code - 0x1100]
    if 0x1161 <= code <= 0x1175:
        return JUNGSUNG_LIST[code - 0x1161]
    if 0x11A8 <= code <= 0x11C2:
        return JONGSUNG_LIST[code - 0x11A7]
    return char


def koen(kor_text: str) -> str:
    """
    한글(자판 입력값)을 영문 키보드 입력값으로 변환합니다.

    :param kor_text: 변환할 한글 문자열
    :return: 영문 키보드 입력 문자열
    """
    result: List[str] = []
    for ch in unicodedata.normalize("NFC", kor_text):
        # 공백은 그대로 추가
        if ch == " ":
            result.append(ch)
            continue
        ch = _canonical_jamo_to_compat(ch)
        # 단독 자모이면 바로 매핑 처리
        if ch in CONSONANT_RMAP:
            result.append(CONSONANT_RMAP[ch])
            continue
        if ch in COMPOUND_FINAL_DECOMP:
            result.extend(CONSONANT_RMAP[part] for part in COMPOUND_FINAL_DECOMP[ch])
            continue
        if ch in VOWEL_RMAP:
            result.append(VOWEL_RMAP[ch])
            continue
        # 완성형 한글 음절이면 분해하여 매핑
        if is_hangul(ch):
            code = ord(ch)
            syl_index = code - 0xAC00
            cho_index = syl_index // (21 * 28)
            jung_index = (syl_index % (21 * 28)) // 28
            jong_index = syl_index % 28
            cho = CHOSUNG_LIST[cho_index]
            jung = JUNGSUNG_LIST[jung_index]
            eng = CONSONANT_RMAP.get(cho, cho) + VOWEL_RMAP.get(jung, jung)
            if jong_index:
                jong = JONGSUNG_LIST[jong_index]
                if jong in COMPOUND_FINAL_DECOMP:
                    for part in COMPOUND_FINAL_DECOMP[jong]:
                        eng += CONSONANT_RMAP.get(part, part)
                else:
                    eng += CONSONANT_RMAP.get(jong, jong)
            result.append(eng)
        else:
            result.append(ch)
    return "".join(result)


def convert_hangul_to_qwerty(text: str) -> str:
    """
    한글을 QWERTY 자판 입력 문자열로 변환합니다.

    :param text: 변환할 한글 문자열
    :return: QWERTY 문자열
    """
    return koen(text)


@overload
def autofix(text: str, allow_double_consonant: bool = False) -> str: ...


@overload
def autofix(text: str, *, allowDoubleConsonant: bool) -> str: ...


def autofix(
    text: str,
    allow_double_consonant: Optional[bool] = None,
    **legacy_kwargs: object,
) -> str:
    """
    입력 문자열의 각 구간(한글, 영문, 기타)을 분리하여
    한글인 부분은 koen, 영문인 부분은 enko를 적용합니다.

    :param text: 변환할 문자열
    :param allow_double_consonant: 두 개의 초성 허용 여부
    :return: 변환된 문자열
    """
    allow_double = resolve_legacy_bool(
        allow_double_consonant,
        legacy_kwargs,
        _LEGACY_DOUBLE_CONSONANT,
        "allow_double_consonant",
    )

    result: List[str] = []
    current_segment = ""
    current_type: Optional[str] = None  # 'hangul', 'roman', 'other'

    def flush_segment(seg: str, seg_type: Optional[str]) -> str:
        if not seg:
            return ""
        if seg_type == "hangul":
            return koen(seg)
        elif seg_type == "roman":
            return enko(seg, allow_double_consonant=allow_double)
        else:
            return seg

    for ch in text:
        # 한글 여부 판단: 단일 문자에 대해 is_hangul() 사용
        if is_hangul(ch):
            ch_type = "hangul"
        elif ch.isalpha() and ch.lower() in "abcdefghijklmnopqrstuvwxyz":
            ch_type = "roman"
        else:
            ch_type = "other"

        if current_type is None:
            current_type = ch_type
            current_segment = ch
        elif ch_type == current_type:
            current_segment += ch
        else:
            result.append(flush_segment(current_segment, current_type))
            current_segment = ch
            current_type = ch_type
    result.append(flush_segment(current_segment, current_type))
    return "".join(result)

# josa.py

import re
import unicodedata
from decimal import Decimal, InvalidOperation
from typing import List, Literal, Optional

from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.hangul_number import number_to_hangul
from hangulpy.utils import (
    HANGUL_BEGIN_UNICODE,
    JONGSUNG_COUNT,
    JONGSUNG_DECOMPOSE,
    JONGSUNG_LIST,
    is_hangul,
)

BatchimKind = Literal["single", "double"]

# Josa rules table: maps particle pattern to (with_jongsung, without_jongsung)
JOSA_RULES = {
    "을/를": ("을", "를"),
    "이/가": ("이", "가"),
    "은/는": ("은", "는"),
    "와/과": ("과", "와"),
    "으로/로": ("으로", "로"),
    "이나/나": ("이나", "나"),
    "이에/에": ("이에", "에"),
    "이란/란": ("이란", "란"),
    "아/야": ("아", "야"),
    "이랑/랑": ("이랑", "랑"),
    "이에요/예요": ("이에요", "예요"),
    "이라/라": ("이라", "라"),
    "으로서/로서": ("으로서", "로서"),
    "으로써/로써": ("으로써", "로써"),
    "으로부터/로부터": ("으로부터", "로부터"),
    "이여/여": ("이여", "여"),
    "이야/야": ("이야", "야"),
    "와서/와": ("와서", "와"),
    "이라서/라서": ("이라서", "라서"),
    "이든/든": ("이든", "든"),
    "이며/며": ("이며", "며"),
    "이라도/라도": ("이라도", "라도"),
    "이니까/니까": ("이니까", "니까"),
    "이지만/지만": ("이지만", "지만"),
    "이랑은/랑은": ("이랑은", "랑은"),
    "이라고/라고": ("이라고", "라고"),
    "이라며/라며": ("이라며", "라며"),
    "이라니/라니": ("이라니", "라니"),
    "이라니까/라니까": ("이라니까", "라니까"),
    "이라거든/라거든": ("이라거든", "라거든"),
    "이라더니/라더니": ("이라더니", "라더니"),
    "이라더군/라더군": ("이라더군", "라더군"),
    "이라던데/라던데": ("이라던데", "라던데"),
    "이라고는/라고는": ("이라고는", "라고는"),
    "이라는데/라는데": ("이라는데", "라는데"),
    "이라면/라면": ("이라면", "라면"),
    "이라서야/라서야": ("이라서야", "라서야"),
    "이라야/라야": ("이라야", "라야"),
    "이라든가/라든가": ("이라든가", "라든가"),
    "이든지/든지": ("이든지", "든지"),
    "이거나/거나": ("이거나", "거나"),
    "이라면야/라면야": ("이라면야", "라면야"),
    "이라면말이지/라면말이지": ("이라면말이지", "라면말이지"),
    "이라야만/라야만": ("이라야만", "라야만"),
    "이었으면/였으면": ("이었으면", "였으면"),
    "이라서도/라서도": ("이라서도", "라서도"),
    "이므로/므로": ("이므로", "므로"),
    "이기에/기에": ("이기에", "기에"),
    "이니/니": ("이니", "니"),
    "이라니깐/라니깐": ("이라니깐", "라니깐"),
    "이면서/면서": ("이면서", "면서"),
    "이자/자": ("이자", "자"),
    "이면서도/면서도": ("이면서도", "면서도"),
    "이라든지/라든지": ("이라든지", "라든지"),
    "이었지만/였지만": ("이었지만", "였지만"),
    "이었으나/였으나": ("이었으나", "였으나"),
    "이긴 하지만/긴 하지만": ("이긴 하지만", "긴 하지만"),
    "이야말로/야말로": ("이야말로", "야말로"),
    "이어야/여야": ("이어야", "여야"),
    "이었고/였고": ("이었고", "였고"),
    "이었는데/였는데": ("이었는데", "였는데"),
    "이었더니/였더니": ("이었더니", "였더니"),
    "이었을 때/였을 때": ("이었을 때", "였을 때"),
    "이었을지라도/였을지라도": ("이었을지라도", "였을지라도"),
    "이었던/였던": ("이었던", "였던"),
    "이었으니까/였으니까": ("이었으니까", "였으니까"),
    "이라고도/라고도": ("이라고도", "라고도"),
    "이라곤 해도/라곤 해도": ("이라곤 해도", "라곤 해도"),
    "이라지/라지": ("이라지", "라지"),
    "이라네/라네": ("이라네", "라네"),
    "이거든/거든": ("이거든", "거든"),
    "이시여/시여": ("이시여", "시여"),
    "이어요/여요": ("이어요", "여요"),
    "이었어요/였어요": ("이었어요", "였어요"),
    "이었어/였어": ("이었어", "였어"),
}


def has_jongsung(text: str, only: Optional[BatchimKind] = None) -> bool:
    """
    주어진 한글 음절에 받침이 있는지 확인합니다.

    :param char: 한글 음절 문자
    :return: 받침이 있으면 True, 없으면 False
    """
    return has_batchim(text, only=only)


def _get_last_valid_char(word: str) -> Optional[str]:
    """
    문자열을 뒤에서부터 탐색하여 조사 판단에 사용할 가장 가까운 유효 문자를 반환합니다.
    유효 문자는 다음을 포함합니다:
      1. 한글 완성형 음절 → 받침 여부로 종성 판단
      2. 숫자 → 숫자 전체를 한글로 변환한 뒤 마지막 한글 음절로 종성 판단
    괄호/기호/공백 등은 무시하며, 알파벳·한자·히라가나·가타카나 등은 받침 없는 것으로 간주합니다.

    :param word: 조사 판단에 사용할 단어 문자열
    :return: 한글 음절 문자(종성 기준), 숫자 변환 후 한글 음절, 혹은 None
    """
    normalized = normalize_hangul(word, "NFC")
    end = len(normalized)
    while end:
        char = normalized[end - 1]
        category = unicodedata.category(char)
        if char.isspace() or category.startswith("P") or category.startswith("S"):
            end -= 1
            continue
        break
    if not end:
        return None

    char = normalized[end - 1]
    if is_hangul(char):
        return char
    if not char.isdigit():
        return None

    start = end - 1
    while start > 0 and (normalized[start - 1].isdigit() or normalized[start - 1] in ",.+-"):
        start -= 1
    number_text = normalized[start:end]
    if not re.fullmatch(r"[+-]?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?", number_text):
        return None
    try:
        number = Decimal(number_text.replace(",", ""))
    except InvalidOperation:
        return None

    hangul_number = number_to_hangul(number)
    return next((item for item in reversed(hangul_number) if is_hangul(item)), None)


def _get_jongsung_char(char: str) -> Optional[str]:
    normalized = normalize_hangul(char, "NFC")
    if len(normalized) != 1 or not is_hangul(normalized):
        return None

    jongsung_index = (ord(normalized) - HANGUL_BEGIN_UNICODE) % JONGSUNG_COUNT
    if jongsung_index == 0:
        return ""

    return JONGSUNG_LIST[jongsung_index]


def _has_jongsung_char(char: str, only: Optional[BatchimKind] = None) -> bool:
    jongsung = _get_jongsung_char(char)
    if not jongsung:
        return False
    if only == "single":
        return jongsung not in JONGSUNG_DECOMPOSE
    if only == "double":
        return jongsung in JONGSUNG_DECOMPOSE
    return True


def has_batchim(text: str, only: Optional[BatchimKind] = None) -> bool:
    """
    문자열의 마지막 유효 한글 음절에 받침이 있는지 확인합니다.

    공백, 문장부호, 기호는 뒤에서부터 건너뛰고, 숫자는 한글 수사로 읽은 뒤
    마지막 음절의 받침을 기준으로 판단합니다.
    """
    if only not in (None, "single", "double"):
        raise ValueError("only must be one of None, 'single', or 'double'")

    last_char = _get_last_valid_char(text)
    if not last_char:
        return False

    return _has_jongsung_char(last_char, only=only)


def _has_ro_exception(last_char: Optional[str]) -> bool:
    if not last_char:
        return False
    return _get_jongsung_char(last_char) == "ㄹ"


def josa_pick(word: str, particle: str) -> str:
    """
    단어에 붙일 조사 형태만 반환합니다.

    :param word: 조사 판단에 사용할 단어
    :param particle: 조사 쌍
    :return: 선택된 조사
    """
    if particle not in JOSA_RULES:
        raise ValueError(f"Unsupported particle: {particle}")

    last_char = _get_last_valid_char(word)
    jongsung_exists = _has_jongsung_char(last_char) if last_char else False
    with_jongsung, without_jongsung = JOSA_RULES[particle]

    if particle.startswith("으로/") and _has_ro_exception(last_char):
        return without_jongsung

    return with_jongsung if jongsung_exists else without_jongsung


def josa(word: str, particle: str) -> str:
    """
    주어진 단어에 적절한 조사를 붙여 반환합니다.

    :param word: 조사와 결합할 단어
    :param particle: 붙일 조사 (예: '을/를', '이/가', '은/는', '와/과', '으로/로', '이나/나', '이에/에',
                    '이란/란', '아/야', '이랑/랑', '이에요/예요', '으로서/로서', '으로써/로써',
                    '으로부터/로부터', '이여/여', '께서', '이야/야', '와서/와', '이라서/라서', '이든/든',
                    '이며/며', '이라도/라도', '이니까/니까', '이지만/지만', '이랑은/랑은', '이라고/라고',
                    '이라며/라며', '이라니/라니', '이라니까/라니까', '이라거든/라거든', '이라더니/라더니',
                    '이라더군/라더군', '이라던데/라던데', '이라고는/라고는', '이라는데/라는데', '이라면/라면',
                    '이라서야/라서야', '이라야/라야', '이라든가/라든가', '이든지/든지', '이거나/거나',
                    '이라면야/라면야', '이라면말이지/라면말이지', '이라야만/라야만', '이었으면/였으면',
                    '이라서도/라서도', '이므로/므로', '이기에/기에', '이니/니', '이라니깐/라니깐',
                    '이면서/면서', '이자/자', '이면서도/면서도', '이라든지/라든지', '이었지만/였지만',
                    '이었으나/였으나', '이긴 하지만/긴 하지만', '이야말로/야말로', '이어야/여야',
                    '이었고/였고', '이었는데/였는데', '이었더니/였더니', '이었을 때/였을 때',
                    '이었을지라도/였을지라도', '이었던/였던', '이었으니까/였으니까', '이라고도/라고도',
                    '이라곤 해도/라곤 해도', '이라지/라지', '이라네/라네', '이거든/거든', '이여/여',
                    '이시여/시여', '아/야', '이야/야', '이에요/예요', '이어요/여요', '이었어요/였어요',
                    '이었어/였어')
    :return: 적절한 조사가 붙은 단어 문자열
    """
    if not word:
        return ""

    return word + josa_pick(word, particle)


def format_josa(template: str, *, strict: bool = False) -> str:
    """문장 안의 ``[조사/조사]`` 표식을 앞말에 맞게 치환합니다.

    ``\\[``와 ``\\]``는 리터럴 대괄호로 처리합니다. 지원하지 않는 표식이나
    닫히지 않은 표식은 기본적으로 그대로 보존하며, ``strict=True``일 때는
    ``ValueError``를 발생시킵니다.
    """
    result: List[str] = []
    literal: List[str] = []
    context = ""
    index = 0

    def flush_literal() -> None:
        nonlocal context
        if not literal:
            return
        value = "".join(literal)
        result.append(value)
        context = _get_last_valid_char(context + value) or ""
        literal.clear()

    while index < len(template):
        char = template[index]
        if char == "\\" and index + 1 < len(template):
            escaped = template[index + 1]
            if escaped in {"[", "]", "\\"}:
                literal.append(escaped)
                index += 2
                continue

        if char != "[":
            literal.append(char)
            index += 1
            continue

        closing = index + 1
        while closing < len(template):
            if template[closing] == "\\" and closing + 1 < len(template):
                closing += 2
                continue
            if template[closing] == "]":
                break
            closing += 1

        if closing >= len(template):
            if strict:
                raise ValueError(f"Unclosed josa marker at index {index}")
            literal.append(template[index:])
            break

        particle = template[index + 1 : closing]
        if particle not in JOSA_RULES:
            if strict:
                raise ValueError(f"Unsupported josa marker: [{particle}]")
            literal.append(template[index : closing + 1])
            index = closing + 1
            continue

        flush_literal()
        selected = josa_pick(context, particle)
        result.append(selected)
        context = _get_last_valid_char(selected) or ""
        index = closing + 1

    flush_literal()
    return "".join(result)

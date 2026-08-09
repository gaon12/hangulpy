# hangul_number.py

import re
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Literal, Optional, Tuple, Union

from hangulpy.utils import NUMBERS

Number = Union[int, float, Decimal]

SMALL_UNITS = ["", "십", "백", "천"]
LARGE_UNITS = [
    "",
    "만",
    "억",
    "조",
    "경",
    "해",
    "자",
    "양",
    "구",
    "간",
    "정",
    "재",
    "극",
    "항하사",
    "아승기",
    "나유타",
    "불가사의",
    "무량대수",
]

DIGIT_NAMES = ["영", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
DIGIT_TO_NUMBER: Dict[str, int] = {name: value for value, name in enumerate(DIGIT_NAMES)}
SMALL_UNIT_TO_NUMBER = {"십": 10, "백": 100, "천": 1000}
LARGE_UNIT_TO_NUMBER = {unit: 10 ** (index * 4) for index, unit in enumerate(LARGE_UNITS) if unit}


def _normalize_number_text(num: Union[int, float, str, Decimal]) -> str:
    def trim_decimal_text(text: str) -> str:
        if "." in text:
            return text.rstrip("0").rstrip(".") or "0"
        return text

    if isinstance(num, bool):
        raise TypeError("bool is not supported")

    if isinstance(num, int):
        return str(num)

    if isinstance(num, Decimal):
        return trim_decimal_text(format(num, "f"))

    if isinstance(num, float):
        if num != num or num in (float("inf"), float("-inf")):
            raise ValueError("nan and infinity are not supported")
        return trim_decimal_text(format(Decimal(str(num)), "f"))

    text = str(num).strip().replace(",", "")
    if not text:
        raise ValueError("empty number")

    try:
        decimal = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"invalid number: {num!r}") from exc

    return trim_decimal_text(format(decimal, "f"))


def _split_number_text(num: Union[int, float, str, Decimal]) -> Tuple[bool, str, str]:
    text = _normalize_number_text(num)
    negative = text.startswith("-")
    if negative:
        text = text[1:]

    if "." in text:
        integer_part, fractional_part = text.split(".", 1)
    else:
        integer_part, fractional_part = text, ""

    integer_part = integer_part.lstrip("0") or "0"
    return negative, integer_part, fractional_part


def _under_10000_to_hangul(value: int) -> str:
    if not 0 <= value < 10000:
        raise ValueError("value must be between 0 and 9999")

    parts: List[str] = []
    for power in range(3, -1, -1):
        divisor = 10**power
        digit = value // divisor
        value %= divisor

        if digit == 0:
            continue

        unit = SMALL_UNITS[power]
        if digit == 1 and unit:
            parts.append(unit)
        else:
            parts.append(NUMBERS[digit] + unit)

    return "".join(parts)


def _integer_to_hangul(integer_text: str, spacing: bool = False) -> str:
    if integer_text == "0":
        return "영"

    groups: List[int] = []
    remaining = integer_text
    while remaining:
        groups.append(int(remaining[-4:]))
        remaining = remaining[:-4]

    if len(groups) > len(LARGE_UNITS):
        raise ValueError("number is too large")

    parts: List[str] = []
    for index in range(len(groups) - 1, -1, -1):
        group = groups[index]
        if group == 0:
            continue
        if group == 1 and index == 1:
            parts.append(LARGE_UNITS[index])
        else:
            parts.append(_under_10000_to_hangul(group) + LARGE_UNITS[index])

    separator = " " if spacing else ""
    return separator.join(parts)


def number_to_hangul(num: Number, spacing: bool = False) -> str:
    """
    숫자를 한자어 한글 읽기로 변환합니다.

    :param num: 변환할 숫자
    :param spacing: True이면 만 단위 그룹 사이에 공백을 넣습니다.
    :return: 한글 숫자 문자열
    """
    negative, integer_part, fractional_part = _split_number_text(num)

    result = _integer_to_hangul(integer_part, spacing=spacing)
    if fractional_part:
        fraction = "".join(DIGIT_NAMES[int(digit)] for digit in fractional_part)
        result = f"{result}점{fraction}"

    return f"마이너스{result}" if negative and result != "영" else result


def float_to_hangul(num: float) -> str:
    """
    소수를 한글 읽기로 변환합니다.

    :param num: 변환할 소수
    :return: 한글 숫자 문자열
    """
    return number_to_hangul(num)


def _read_hangul_integer(integer_part: str) -> int:
    if not integer_part:
        raise ValueError("empty hangul integer")
    if "영" in integer_part and integer_part != "영":
        raise ValueError("'영' must be used alone in an integer")

    total = 0
    group = 0
    pending: Optional[int] = None
    index = 0
    large_units = sorted(LARGE_UNIT_TO_NUMBER, key=len, reverse=True)
    last_small_unit = 10000
    last_large_unit: Optional[int] = None
    saw_token = False

    while index < len(integer_part):
        char = integer_part[index]
        if char.isspace():
            index += 1
            continue

        if char in DIGIT_TO_NUMBER:
            if pending is not None:
                raise ValueError("consecutive digit names are not valid in an integer")
            pending = DIGIT_TO_NUMBER[char]
            saw_token = True
            index += 1
            continue

        if char in SMALL_UNIT_TO_NUMBER:
            unit_value = SMALL_UNIT_TO_NUMBER[char]
            if unit_value >= last_small_unit:
                raise ValueError("small units must appear in descending order")
            if pending == 0:
                raise ValueError("'영' cannot qualify a unit")
            group += (pending if pending is not None else 1) * unit_value
            pending = None
            last_small_unit = unit_value
            saw_token = True
            index += 1
            continue

        matched_unit = ""
        for unit in large_units:
            if integer_part.startswith(unit, index):
                matched_unit = unit
                break

        if matched_unit:
            unit_value = LARGE_UNIT_TO_NUMBER[matched_unit]
            if last_large_unit is not None and unit_value >= last_large_unit:
                raise ValueError("large units must appear in descending order")
            group += pending if pending is not None else 0
            total += (group or 1) * LARGE_UNIT_TO_NUMBER[matched_unit]
            group = 0
            pending = None
            last_small_unit = 10000
            last_large_unit = unit_value
            saw_token = True
            index += len(matched_unit)
            continue

        raise ValueError(f"invalid hangul number token: {char!r}")

    if not saw_token:
        raise ValueError("empty hangul integer")
    return total + group + (pending if pending is not None else 0)


def hangul_to_number(hangul: str) -> Union[int, float]:
    """
    한글 숫자 문자열을 숫자로 변환합니다.

    :param hangul: 변환할 한글 숫자 문자열
    :return: 숫자
    """
    text = hangul.strip().replace(" ", "")
    if not text:
        raise ValueError("empty hangul number")

    negative = text.startswith("마이너스")
    if negative:
        text = text[len("마이너스") :]
        if not text:
            raise ValueError("a minus sign must be followed by a number")

    if text.count("점") > 1:
        raise ValueError("a hangul number can contain only one decimal point")
    if "점" in text:
        integer_part, fractional_part = text.split("점", 1)
        if not integer_part or not fractional_part:
            raise ValueError("both sides of '점' must contain digits")
    else:
        integer_part, fractional_part = text, ""

    integer = _read_hangul_integer(integer_part)
    if not fractional_part:
        return -integer if negative else integer

    fractional_digits: List[str] = []
    for char in fractional_part:
        if char not in DIGIT_TO_NUMBER:
            raise ValueError(f"invalid fractional token: {char!r}")
        fractional_digits.append(str(DIGIT_TO_NUMBER[char]))

    value = float(f"{integer}.{''.join(fractional_digits)}")
    return -value if negative else value


def number_to_hangul_mixed(num: Number, spacing: bool = False) -> str:
    """
    숫자와 한글 단위를 섞어 4자리 그룹 기준으로 표기합니다.

    :param num: 변환할 숫자
    :param spacing: True이면 만 단위 그룹 사이에 공백을 넣습니다.
    :return: 예: 123456780 -> '1억2,345만6,780'
    """
    negative, integer_part, fractional_part = _split_number_text(num)

    groups: List[int] = []
    remaining = integer_part
    while remaining:
        groups.append(int(remaining[-4:]))
        remaining = remaining[:-4]

    if len(groups) > len(LARGE_UNITS):
        raise ValueError("number is too large")

    parts: List[str] = []
    for index in range(len(groups) - 1, -1, -1):
        group = groups[index]
        if group == 0:
            continue
        text = str(group) if index == len(groups) - 1 else f"{group:,}"
        parts.append(text + LARGE_UNITS[index])

    result = (" " if spacing else "").join(parts) if parts else "0"
    if fractional_part:
        result += "." + fractional_part
    if negative and result != "0":
        result = "-" + result
    return result


def amount_to_hangul(amount: Union[str, int, float]) -> str:
    """
    숫자나 숫자가 섞인 금액 문자열을 한글 읽기로 변환합니다.

    :param amount: 숫자 또는 금액 문자열
    :return: 한글 숫자 문자열
    """
    if not isinstance(amount, str):
        return number_to_hangul(amount)

    matches = list(re.finditer(r"[+-]?\d[\d,]*(?:\.\d+)?", amount))
    if len(matches) != 1:
        raise ValueError("amount must contain exactly one number")

    number_text = matches[0].group(0)
    if not re.fullmatch(r"[+-]?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?", number_text):
        raise ValueError(f"invalid amount: {amount!r}")
    return number_to_hangul(Decimal(_normalize_number_text(number_text)))


NATIVE_ONES = {
    1: "하나",
    2: "둘",
    3: "셋",
    4: "넷",
    5: "다섯",
    6: "여섯",
    7: "일곱",
    8: "여덟",
    9: "아홉",
}
NATIVE_ONES_CLASSIFIER = {
    1: "한",
    2: "두",
    3: "세",
    4: "네",
    5: "다섯",
    6: "여섯",
    7: "일곱",
    8: "여덟",
    9: "아홉",
}
NATIVE_TENS = {
    10: "열",
    20: "스물",
    30: "서른",
    40: "마흔",
    50: "쉰",
    60: "예순",
    70: "일흔",
    80: "여든",
    90: "아흔",
}


def _require_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _require_string(value: object, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def susa(num: int, classifier: bool = False) -> str:
    """
    1부터 100까지의 숫자를 순우리말 수사로 변환합니다.

    :param num: 변환할 정수
    :param classifier: True이면 수 관형사형을 반환합니다.
    :return: 순우리말 수사
    """
    num = _require_int(num, "num")
    if not 1 <= num <= 100:
        raise ValueError("susa supports integers from 1 to 100")

    if num == 100:
        return "백"

    if num < 10:
        return (NATIVE_ONES_CLASSIFIER if classifier else NATIVE_ONES)[num]

    tens = (num // 10) * 10
    ones = num % 10
    if ones == 0:
        if classifier and tens == 20:
            return "스무"
        return NATIVE_TENS[tens]

    return NATIVE_TENS[tens] + (NATIVE_ONES_CLASSIFIER if classifier else NATIVE_ONES)[ones]


def counter(
    num: int,
    unit: str,
    *,
    system: Literal["native", "sino"] = "native",
    spacing: bool = True,
) -> str:
    """수 관형사 또는 한자어 수사와 단위를 결합합니다."""
    num = _require_int(num, "num")
    if not unit:
        raise ValueError("unit must not be empty")
    if system == "native":
        number_text = susa(num, classifier=True)
    elif system == "sino":
        if num < 0:
            raise ValueError("sino counters require a non-negative number")
        number_text = number_to_hangul(num)
    else:
        raise ValueError("system must be either 'native' or 'sino'")
    return number_text + (" " if spacing else "") + unit


def months(month: int) -> str:
    """달력의 월을 한글 읽기로 변환하며 유월·시월 예외를 적용합니다."""
    month = _require_int(month, "month")
    if not 1 <= month <= 12:
        raise ValueError("month must be between 1 and 12")
    if month == 6:
        return "유월"
    if month == 10:
        return "시월"
    return number_to_hangul(month) + "월"


_NATIVE_NUMBER_VALUES = {
    form: number
    for number in range(1, 101)
    for form in (susa(number), susa(number, classifier=True))
}


def native_korean_to_number(text: str) -> int:
    """1~100 범위의 고유어 수사·수 관형사를 정수로 변환합니다."""
    text = _require_string(text, "text")
    normalized = "".join(text.split())
    try:
        return _NATIVE_NUMBER_VALUES[normalized]
    except KeyError as exc:
        raise ValueError(f"invalid native Korean number: {text!r}") from exc


def seosusa(num: int) -> str:
    """
    숫자를 한글 서수사로 변환합니다.

    :param num: 변환할 정수
    :return: 서수사
    """
    num = _require_int(num, "num")
    if num < 1:
        raise ValueError("seosusa supports positive integers")

    if num == 1:
        return "첫째"
    if num == 2:
        return "둘째"
    if num == 3:
        return "셋째"
    if num == 4:
        return "넷째"
    if num < 100:
        return susa(num, classifier=True) + "째"
    return number_to_hangul(num) + "째"


DAY_ONES = {
    1: "하루",
    2: "이틀",
    3: "사흘",
    4: "나흘",
    5: "닷새",
    6: "엿새",
    7: "이레",
    8: "여드레",
    9: "아흐레",
}
DAY_TENS = {
    10: "열흘",
    20: "스무",
    30: "서른",
}


def days(num: int) -> str:
    """
    1부터 30까지의 숫자를 순우리말 날짜 수로 변환합니다.

    :param num: 변환할 정수
    :return: 순우리말 날짜 수
    """
    num = _require_int(num, "num")
    if not 1 <= num <= 30:
        raise ValueError("days supports integers from 1 to 30")

    if num < 10:
        return DAY_ONES[num]
    if num == 10:
        return DAY_TENS[10]
    if num < 20:
        return "열" + DAY_ONES[num - 10]
    if num == 20:
        return DAY_TENS[20] + "날"
    if num < 30:
        return DAY_TENS[20] + DAY_ONES[num - 20]
    return DAY_TENS[30] + "날"

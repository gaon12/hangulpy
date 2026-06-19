# tests/test_numbers.py

import pytest

from hangulpy import (
    amount_to_hangul,
    days,
    hangul_to_number,
    number_to_hangul,
    number_to_hangul_mixed,
    seosusa,
    susa,
)


class TestHangulNumbers:
    """한글 숫자 변환 테스트"""

    def test_single_digit_one(self):
        """1은 빈 문자열이 아니라 일이어야 한다"""
        assert number_to_hangul(1) == "일"

    def test_large_unit_leading_one(self):
        """4자리 단위가 정확히 붙는다"""
        assert number_to_hangul(10000) == "만"
        assert number_to_hangul(100000) == "십만"
        assert number_to_hangul(123456789) == "일억이천삼백사십오만육천칠백팔십구"

    def test_negative_and_float(self):
        """음수와 소수 변환 테스트"""
        assert number_to_hangul(-12345.678) == "마이너스만이천삼백사십오점육칠팔"
        assert number_to_hangul(123456780, spacing=True) == "일억 이천삼백사십오만 육천칠백팔십"

    def test_hangul_to_number(self):
        """한글 숫자 역변환 테스트"""
        assert hangul_to_number("십만") == 100000
        assert hangul_to_number("일억이천삼백사십오만육천칠백팔십구") == 123456789
        assert hangul_to_number("마이너스일점이삼") == -1.23

    def test_number_to_hangul_mixed(self):
        """숫자와 한글 단위 혼합 표기 테스트"""
        assert number_to_hangul_mixed(210000) == "21만"
        assert number_to_hangul_mixed(12345) == "1만2,345"
        assert number_to_hangul_mixed(123456780) == "1억2,345만6,780"
        assert number_to_hangul_mixed(-12345.678) == "-1만2,345.678"
        assert number_to_hangul_mixed(123456780, spacing=True) == "1억 2,345만 6,780"

    def test_amount_to_hangul(self):
        """금액 문자열 변환 테스트"""
        assert amount_to_hangul("120,030원") == "십이만삼십"
        assert amount_to_hangul("12345.6789") == "만이천삼백사십오점육칠팔구"

    def test_native_numbers(self):
        """순우리말 수사와 서수사 테스트"""
        assert susa(1) == "하나"
        assert susa(21) == "스물하나"
        assert susa(21, classifier=True) == "스물한"
        assert susa(100) == "백"
        assert seosusa(1) == "첫째"
        assert seosusa(21) == "스물한째"
        assert seosusa(100) == "백째"

    def test_days(self):
        """순우리말 날짜 수 테스트"""
        assert days(1) == "하루"
        assert days(10) == "열흘"
        assert days(20) == "스무날"
        assert days(29) == "스무아흐레"
        assert days(30) == "서른날"

    def test_invalid_native_ranges(self):
        """지원 범위 밖 입력 테스트"""
        with pytest.raises(ValueError):
            susa(0)
        with pytest.raises(ValueError):
            days(31)

# tests/test_numbers.py

from hangulpy import number_to_hangul


class TestHangulNumbers:
    """한글 숫자 변환 테스트"""

    def test_single_digit_one(self):
        """1은 빈 문자열이 아니라 일이어야 한다"""
        assert number_to_hangul(1) == "일"

    def test_large_unit_leading_one(self):
        """큰 단위 앞의 일은 자연스럽게 생략된다"""
        assert number_to_hangul(10000) == "만"

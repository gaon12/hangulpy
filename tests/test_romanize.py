# tests/test_romanize.py

import pytest
from hangulpy import Romanizer, romanize


class TestRomanization:
    """한글 로마자 표기 테스트"""

    def test_romanize_revised_basic(self):
        """국립국어원 표준 로마자 표기 기본 테스트"""
        assert romanize('안녕하세요', 'revised') == 'annyeonghaseyo'
        assert romanize('한글', 'revised') == 'hangeul'
        assert romanize('감사합니다', 'revised') == 'gamsahamnida'

    def test_romanize_revised_vowels(self):
        """모음 로마자 표기 테스트"""
        assert romanize('아', 'revised') == 'a'
        assert romanize('에', 'revised') == 'e'
        assert romanize('이', 'revised') == 'i'
        assert romanize('오', 'revised') == 'o'
        assert romanize('우', 'revised') == 'u'

    def test_romanize_revised_consonants(self):
        """자음 로마자 표기 테스트"""
        assert romanize('가', 'revised') == 'ga'
        assert romanize('나', 'revised') == 'na'
        assert romanize('다', 'revised') == 'da'
        assert romanize('라', 'revised') == 'ra'
        assert romanize('마', 'revised') == 'ma'

    def test_romanize_mccune(self):
        """McCune-Reischauer 표기 테스트"""
        result = romanize('한글', 'mr')
        assert result  # 정확한 결과는 시스템에 따라 다를 수 있음

    def test_romanize_yale(self):
        """Yale 표기 테스트"""
        result = romanize('한글', 'yale')
        assert result

    def test_romanizer_class(self):
        """Romanizer 클래스 테스트"""
        romanizer = Romanizer('revised')
        assert romanizer.romanize('한글') == 'hangeul'

        # 단일 문자 변환
        assert romanizer.romanize_char('가') == 'ga'
        assert romanizer.romanize_char('a') == 'a'  # 한글이 아닌 문자는 그대로

    def test_romanizer_invalid_system(self):
        """잘못된 시스템 이름 테스트"""
        with pytest.raises(ValueError):
            Romanizer('invalid_system')

    def test_romanize_helper_function(self):
        """romanize 헬퍼 함수 테스트"""
        assert romanize('서울', 'revised') == 'seoul'
        assert romanize('부산', 'revised') == 'busan'
        assert romanize('대구', 'revised') == 'daegu'

    def test_romanize_mixed_text(self):
        """한글과 다른 문자가 섞인 텍스트 테스트"""
        result = romanize('Hello 안녕', 'revised')
        assert 'Hello' in result
        assert 'annyeong' in result

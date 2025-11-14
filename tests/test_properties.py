# tests/test_properties.py

from hangulpy import (
    is_complete_hangul,
    is_chosung,
    is_jungsung,
    is_jongsung,
    get_chosung,
    get_jungsung,
    get_jongsung,
    get_hangul_components,
)


class TestHangulProperties:
    """한글 속성 검사 함수 테스트"""

    def test_is_complete_hangul(self):
        """완성형 한글 확인 테스트"""
        assert is_complete_hangul('가') == True
        assert is_complete_hangul('한') == True
        assert is_complete_hangul('ㄱ') == False
        assert is_complete_hangul('ㅏ') == False
        assert is_complete_hangul('a') == False
        assert is_complete_hangul('') == False

    def test_is_chosung(self):
        """초성 확인 테스트"""
        assert is_chosung('ㄱ') == True
        assert is_chosung('ㄴ') == True
        assert is_chosung('ㅎ') == True
        assert is_chosung('ㅏ') == False
        assert is_chosung('가') == False
        assert is_chosung('a') == False

    def test_is_jungsung(self):
        """중성 확인 테스트"""
        assert is_jungsung('ㅏ') == True
        assert is_jungsung('ㅓ') == True
        assert is_jungsung('ㅣ') == True
        assert is_jungsung('ㄱ') == False
        assert is_jungsung('가') == False

    def test_is_jongsung(self):
        """종성 확인 테스트"""
        assert is_jongsung('ㄱ') == True
        assert is_jongsung('ㄴ') == True
        assert is_jongsung('ㄳ') == True  # 겹받침
        assert is_jongsung('ㅏ') == False
        assert is_jongsung('가') == False
        assert is_jongsung('') == False  # 빈 종성

    def test_get_chosung(self):
        """초성 추출 테스트"""
        assert get_chosung('가') == 'ㄱ'
        assert get_chosung('나') == 'ㄴ'
        assert get_chosung('한') == 'ㅎ'
        assert get_chosung('a') is None

    def test_get_jungsung(self):
        """중성 추출 테스트"""
        assert get_jungsung('가') == 'ㅏ'
        assert get_jungsung('너') == 'ㅓ'
        assert get_jungsung('희') == 'ㅢ'
        assert get_jungsung('a') is None

    def test_get_jongsung(self):
        """종성 추출 테스트"""
        assert get_jongsung('각') == 'ㄱ'
        assert get_jongsung('한') == 'ㄴ'
        assert get_jongsung('가') == ''  # 받침 없음
        assert get_jongsung('a') is None

    def test_get_hangul_components(self):
        """한글 성분 추출 테스트"""
        assert get_hangul_components('가') == ('ㄱ', 'ㅏ', '')
        assert get_hangul_components('한') == ('ㅎ', 'ㅏ', 'ㄴ')
        assert get_hangul_components('글') == ('ㄱ', 'ㅡ', 'ㄹ')
        assert get_hangul_components('a') is None

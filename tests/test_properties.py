# tests/test_properties.py

from hangulpy import (
    get_chosung,
    get_hangul_components,
    get_jongsung,
    get_jungsung,
    is_chosung,
    is_complete_hangul,
    is_hangul,
    is_jongsung,
    is_jungsung,
)


class TestHangulProperties:
    """한글 속성 검사 함수 테스트"""

    def test_is_complete_hangul(self):
        """완성형 한글 확인 테스트"""
        assert is_complete_hangul("가")
        assert is_complete_hangul("한")
        assert not is_complete_hangul("ㄱ")
        assert not is_complete_hangul("ㅏ")
        assert not is_complete_hangul("a")
        assert not is_complete_hangul("")

    def test_is_hangul_empty_string(self):
        assert not is_hangul("")

    def test_is_chosung(self):
        """초성 확인 테스트"""
        assert is_chosung("ㄱ")
        assert is_chosung("ㄴ")
        assert is_chosung("ㅎ")
        assert not is_chosung("ㅏ")
        assert not is_chosung("가")
        assert not is_chosung("a")

    def test_is_jungsung(self):
        """중성 확인 테스트"""
        assert is_jungsung("ㅏ")
        assert is_jungsung("ㅓ")
        assert is_jungsung("ㅣ")
        assert not is_jungsung("ㄱ")
        assert not is_jungsung("가")

    def test_is_jongsung(self):
        """종성 확인 테스트"""
        assert is_jongsung("ㄱ")
        assert is_jongsung("ㄴ")
        assert is_jongsung("ㄳ")  # 겹받침
        assert not is_jongsung("ㅏ")
        assert not is_jongsung("가")
        assert not is_jongsung("")  # 빈 종성

    def test_get_chosung(self):
        """초성 추출 테스트"""
        assert get_chosung("가") == "ㄱ"
        assert get_chosung("나") == "ㄴ"
        assert get_chosung("한") == "ㅎ"
        assert get_chosung("a") is None

    def test_get_jungsung(self):
        """중성 추출 테스트"""
        assert get_jungsung("가") == "ㅏ"
        assert get_jungsung("너") == "ㅓ"
        assert get_jungsung("희") == "ㅢ"
        assert get_jungsung("a") is None

    def test_get_jongsung(self):
        """종성 추출 테스트"""
        assert get_jongsung("각") == "ㄱ"
        assert get_jongsung("한") == "ㄴ"
        assert get_jongsung("가") == ""  # 받침 없음
        assert get_jongsung("a") is None

    def test_get_hangul_components(self):
        """한글 성분 추출 테스트"""
        assert get_hangul_components("가") == ("ㄱ", "ㅏ", "")
        assert get_hangul_components("한") == ("ㅎ", "ㅏ", "ㄴ")
        assert get_hangul_components("글") == ("ㄱ", "ㅡ", "ㄹ")
        assert get_hangul_components("a") is None

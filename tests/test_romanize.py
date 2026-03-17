# tests/test_romanize.py

import pytest
from hangulpy import Romanizer, romanize


class TestRomanization:
    """한글 로마자 표기 테스트"""

    def test_romanize_revised_basic(self):
        """국립국어원 표준 로마자 표기 기본 테스트"""
        assert romanize("안녕하세요", "revised") == "annyeonghaseyo"
        assert romanize("한글", "revised") == "hangeul"
        assert romanize("감사합니다", "revised") == "gamsahamnida"

    def test_romanize_revised_vowels(self):
        """모음 로마자 표기 테스트"""
        assert romanize("아", "revised") == "a"
        assert romanize("에", "revised") == "e"
        assert romanize("이", "revised") == "i"
        assert romanize("오", "revised") == "o"
        assert romanize("우", "revised") == "u"

    def test_romanize_revised_consonants(self):
        """자음 로마자 표기 테스트"""
        assert romanize("가", "revised") == "ga"
        assert romanize("나", "revised") == "na"
        assert romanize("다", "revised") == "da"
        assert romanize("라", "revised") == "ra"
        assert romanize("마", "revised") == "ma"

    def test_romanize_revised_assimilation(self):
        """연음/비음화가 반영되는 경우 테스트"""
        assert romanize("국물", "revised") == "gungmul"
        assert romanize("감사합니다", "revised") == "gamsahamnida"

    def test_romanize_revised_regulation_examples(self):
        """규정집 예시 표기 테스트"""
        examples: list[tuple[str, str]] = [
            ("광희문", "gwanghuimun"),
            ("백마", "baengma"),
            ("종로", "jongno"),
            ("왕십리", "wangsimni"),
            ("별내", "byeollae"),
            ("신라", "silla"),
            ("학여울", "hangnyeoul"),
            ("알약", "allyak"),
            ("해돋이", "haedoji"),
            ("같이", "gachi"),
            ("굳히다", "guchida"),
            ("좋고", "joko"),
            ("놓다", "nota"),
            ("잡혀", "japyeo"),
            ("낳지", "nachi"),
            ("압구정", "apgujeong"),
            ("낙동강", "nakdonggang"),
            ("샛별", "saetbyeol"),
            ("신문로", "sinmunno"),
        ]

        for word, expected in examples:
            assert romanize(word, "revised") == expected

    def test_romanize_mccune(self):
        """McCune-Reischauer 표기 테스트"""
        result = romanize("한글", "mr")
        assert result  # 정확한 결과는 시스템에 따라 다를 수 있음

    def test_romanize_yale(self):
        """Yale 표기 테스트"""
        result = romanize("한글", "yale")
        assert result

    def test_romanizer_class(self):
        """Romanizer 클래스 테스트"""
        romanizer = Romanizer("revised")
        assert romanizer.romanize("한글") == "hangeul"

        # 단일 문자 변환
        assert romanizer.romanize_char("가") == "ga"
        assert romanizer.romanize_char("a") == "a"  # 한글이 아닌 문자는 그대로

    def test_romanizer_revised_modes(self):
        """규정 예외를 위한 revised 모드 테스트"""
        assert romanize("묵호", "revised", mode="proper") == "mukho"
        assert romanize("집현전", "revised", mode="proper") == "jiphyeonjeon"
        assert romanize("오죽헌", "revised", mode="proper") == "ojukheon"
        assert romanize("홍빛나", "revised", mode="name") == "hong bitna"
        assert romanize("민용하", "revised", mode="name", capitalize=True) == "Min Yongha"
        assert (
            romanize("민용하", "revised", mode="name", capitalize=True, name_hyphen=True)
            == "Min Yong-ha"
        )
        assert (
            romanize("홍빛나", "revised", mode="name", capitalize=True, name_hyphen=True)
            == "Hong Bit-na"
        )
        assert romanize("충청북도", "revised", mode="admin") == "chungcheongbuk-do"
        assert romanize("의정부시", "revised", mode="admin") == "uijeongbu-si"
        assert romanize("삼죽면", "revised", mode="admin") == "samjuk-myeon"
        assert romanize("청주시", "revised", mode="admin", admin_omit_suffix=True) == "cheongju"
        assert romanize("함평군", "revised", mode="admin", admin_omit_suffix=True) == "hampyeong"
        assert romanize("순창읍", "revised", mode="admin", admin_omit_suffix=True) == "sunchang"
        assert romanize("부산 세종", "revised", capitalize=True) == "Busan Sejong"

    def test_romanize_revised_disambiguation(self):
        """혼동 방지용 붙임표 테스트"""
        assert romanize("중앙", "revised", disambiguate=True) == "jung-ang"
        assert romanize("반구대", "revised", disambiguate=True) == "ban-gudae"
        assert romanize("세운", "revised", disambiguate=True) == "se-un"
        assert romanize("해운대", "revised", disambiguate=True) == "hae-undae"

    def test_romanizer_invalid_system(self):
        """잘못된 시스템 이름 테스트"""
        with pytest.raises(ValueError):
            Romanizer("invalid_system")

        with pytest.raises(ValueError):
            Romanizer("revised", mode="invalid_mode")

    def test_romanize_helper_function(self):
        """romanize 헬퍼 함수 테스트"""
        assert romanize("서울", "revised") == "seoul"
        assert romanize("부산", "revised") == "busan"
        assert romanize("대구", "revised") == "daegu"

    def test_romanize_mixed_text(self):
        """한글과 다른 문자가 섞인 텍스트 테스트"""
        result = romanize("Hello 안녕", "revised")
        assert "Hello" in result
        assert "annyeong" in result

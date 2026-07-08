# tests/test_josa.py

import pytest

from hangulpy import has_batchim, has_jongsung, josa, josa_pick


class TestJosa:
    """조사 붙이기 기능 테스트"""

    def test_eul_reul(self):
        """을/를 조사 테스트"""
        assert josa("사과", "을/를") == "사과를"
        assert josa("책", "을/를") == "책을"
        assert josa("물", "을/를") == "물을"
        assert josa("바나나", "을/를") == "바나나를"

    def test_i_ga(self):
        """이/가 조사 테스트"""
        assert josa("사과", "이/가") == "사과가"
        assert josa("책", "이/가") == "책이"
        assert josa("나무", "이/가") == "나무가"
        assert josa("물", "이/가") == "물이"

    def test_eun_neun(self):
        """은/는 조사 테스트"""
        assert josa("사과", "은/는") == "사과는"
        assert josa("책", "은/는") == "책은"
        assert josa("나무", "은/는") == "나무는"

    def test_with_numbers(self):
        """숫자와 조사 결합 테스트"""
        assert josa("1", "이/가") == "1이"
        assert josa("2", "이/가") == "2가"
        assert josa("3", "이/가") == "3이"
        assert josa("8", "이/가") == "8이"

    def test_empty_word(self):
        """빈 문자열 테스트"""
        assert josa("", "을/를") == ""

    def test_has_jongsung(self):
        """받침 확인 함수 테스트"""
        assert has_jongsung("각")
        assert not has_jongsung("가")
        assert has_jongsung("한")
        assert not has_jongsung("나")

    def test_has_batchim_text_and_options(self):
        assert has_jongsung("사과!") is False
        assert has_jongsung("책!") is True
        assert has_jongsung("값", only="double") is True
        assert has_jongsung("각", only="single") is True
        assert has_jongsung("값", only="single") is False
        assert has_batchim("값", only="double") is True
        assert has_batchim("사과") is False
        assert has_batchim("버전 1.2)") is False

        with pytest.raises(ValueError):
            has_batchim("각", only="invalid")

    def test_unsupported_particle(self):
        """지원하지 않는 조사 테스트"""
        with pytest.raises(ValueError):
            josa("사과", "잘못된조사")

    def test_various_particles(self):
        """다양한 조사 테스트"""
        assert josa("집", "으로/로") == "집으로"
        assert josa("나무", "으로/로") == "나무로"
        assert josa("길", "으로/로") == "길로"
        assert josa("서울", "으로/로") == "서울로"
        assert josa("책", "이나/나") == "책이나"
        assert josa("사과", "이나/나") == "사과나"

    def test_josa_pick(self):
        """조사 선택만 반환하는 함수 테스트"""
        assert josa_pick("사과", "이/가") == "가"
        assert josa_pick("책", "이/가") == "이"
        assert josa_pick("서울", "으로/로") == "로"
        assert josa("사과", "이라/라") == "사과라"

    def test_number_with_trailing_punctuation(self):
        """문장부호 뒤 숫자 조사 판단 테스트"""
        assert josa("버전 1.2)", "이/가") == "버전 1.2)가"

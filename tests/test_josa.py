# tests/test_josa.py

import pytest
from hangulpy import josa, has_jongsung


class TestJosa:
    """조사 붙이기 기능 테스트"""

    def test_eul_reul(self):
        """을/를 조사 테스트"""
        assert josa('사과', '을/를') == '사과를'
        assert josa('책', '을/를') == '책을'
        assert josa('물', '을/를') == '물을'
        assert josa('바나나', '을/를') == '바나나를'

    def test_i_ga(self):
        """이/가 조사 테스트"""
        assert josa('사과', '이/가') == '사과가'
        assert josa('책', '이/가') == '책이'
        assert josa('나무', '이/가') == '나무가'
        assert josa('물', '이/가') == '물이'

    def test_eun_neun(self):
        """은/는 조사 테스트"""
        assert josa('사과', '은/는') == '사과는'
        assert josa('책', '은/는') == '책은'
        assert josa('나무', '은/는') == '나무는'

    def test_with_numbers(self):
        """숫자와 조사 결합 테스트"""
        assert josa('1', '이/가') == '1이'
        assert josa('2', '이/가') == '2가'
        assert josa('3', '이/가') == '3이'
        assert josa('8', '이/가') == '8이'

    def test_empty_word(self):
        """빈 문자열 테스트"""
        assert josa('', '을/를') == ''

    def test_has_jongsung(self):
        """받침 확인 함수 테스트"""
        assert has_jongsung('각') == True
        assert has_jongsung('가') == False
        assert has_jongsung('한') == True
        assert has_jongsung('나') == False

    def test_unsupported_particle(self):
        """지원하지 않는 조사 테스트"""
        with pytest.raises(ValueError):
            josa('사과', '잘못된조사')

    def test_various_particles(self):
        """다양한 조사 테스트"""
        assert josa('집', '으로/로') == '집으로'
        assert josa('나무', '으로/로') == '나무로'
        assert josa('책', '이나/나') == '책이나'
        assert josa('사과', '이나/나') == '사과나'

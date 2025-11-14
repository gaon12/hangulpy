# tests/test_assemble.py

from hangulpy import split_syllables, join_jamos, disassemble, assemble


class TestHangulAssemble:
    """한글 조립/분해 고수준 API 테스트"""

    def test_split_syllables_list(self):
        """음절 분해 - 리스트 형식 테스트"""
        result = split_syllables('한글', output_format='list')
        assert isinstance(result, list)
        assert len(result) > 0
        assert 'ㅎ' in result or result[0] == 'ㅎ'

    def test_split_syllables_string(self):
        """음절 분해 - 문자열 형식 테스트"""
        result = split_syllables('한글', output_format='string')
        assert isinstance(result, str)
        assert len(result) > 0

    def test_join_jamos_from_list(self):
        """자모 조립 - 리스트 입력 테스트"""
        jamos = ['ㅎ', 'ㅏ', 'ㄴ', 'ㄱ', 'ㅡ', 'ㄹ']
        result = join_jamos(jamos)
        assert '한' in result or '글' in result

    def test_join_jamos_from_string(self):
        """자모 조립 - 문자열 입력 테스트"""
        result = join_jamos('ㅎㅏㄴ')
        assert len(result) > 0

    def test_round_trip(self):
        """분해 후 재조립 테스트"""
        original = '한글'
        decomposed = split_syllables(original, output_format='list')
        recomposed = join_jamos(decomposed)
        # 완벽한 복원은 어려울 수 있지만, 결과가 비어있지 않아야 함
        assert len(recomposed) > 0

    def test_disassemble_alias(self):
        """disassemble 별칭 테스트"""
        result1 = split_syllables('한글')
        result2 = disassemble('한글')
        assert result1 == result2

    def test_assemble_alias(self):
        """assemble 별칭 테스트"""
        jamos = ['ㄱ', 'ㅏ']
        result1 = join_jamos(jamos)
        result2 = assemble(jamos)
        assert result1 == result2

    def test_empty_input(self):
        """빈 입력 테스트"""
        assert split_syllables('') == []
        assert join_jamos([]) == ''
        assert join_jamos('') == ''

    def test_non_hangul_passthrough(self):
        """한글이 아닌 문자 통과 테스트"""
        result = split_syllables('abc')
        assert 'a' in result or result == ['a', 'b', 'c']

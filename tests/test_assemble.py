# tests/test_assemble.py

from hangulpy import (
    assemble,
    combine_character,
    combine_vowels,
    disassemble,
    disassemble_complete_character,
    disassemble_to_groups,
    join_jamos,
    remove_last_character,
    split_syllables,
)


class TestHangulAssemble:
    """한글 조립/분해 고수준 API 테스트"""

    def test_split_syllables_list(self):
        """음절 분해 - 리스트 형식 테스트"""
        result = split_syllables("한글", output_format="list")
        assert result == ["ㅎ", "ㅏ", "ㄴ", "ㄱ", "ㅡ", "ㄹ"]

    def test_split_syllables_string(self):
        """음절 분해 - 문자열 형식 테스트"""
        result = split_syllables("한글", output_format="string")
        assert result == "ㅎㅏㄴㄱㅡㄹ"

    def test_join_jamos_from_list(self):
        """자모 조립 - 리스트 입력 테스트"""
        jamos = ["ㅎ", "ㅏ", "ㄴ", "ㄱ", "ㅡ", "ㄹ"]
        result = join_jamos(jamos)
        assert result == "한글"

    def test_join_jamos_from_string(self):
        """자모 조립 - 문자열 입력 테스트"""
        result = join_jamos("ㅎㅏㄴ")
        assert result == "한"

    def test_join_jamos_moves_next_initial(self):
        """뒤에 모음이 있으면 자음을 다음 초성으로 처리한다"""
        assert join_jamos("ㄱㅏㄴㅏ") == "가나"

    def test_round_trip(self):
        """분해 후 재조립 테스트"""
        original = "한글"
        decomposed = split_syllables(original, output_format="list")
        recomposed = join_jamos(decomposed)
        assert recomposed == original

    def test_disassemble_alias(self):
        """disassemble 별칭 테스트"""
        result1 = split_syllables("한글")
        result2 = disassemble("한글")
        assert result1 == result2

    def test_assemble_alias(self):
        """assemble 별칭 테스트"""
        jamos = ["ㄱ", "ㅏ"]
        result1 = join_jamos(jamos)
        result2 = assemble(jamos)
        assert result1 == result2

    def test_empty_input(self):
        """빈 입력 테스트"""
        assert split_syllables("") == []
        assert join_jamos([]) == ""
        assert join_jamos("") == ""

    def test_non_hangul_passthrough(self):
        """한글이 아닌 문자 통과 테스트"""
        result = split_syllables("abc")
        assert result == ["a", "b", "c"]

    def test_combine_vowels_join_on_fail(self):
        assert combine_vowels("ㅗ", "ㅏ") == "ㅘ"
        assert combine_vowels("ㅏ", "ㅗ") is None
        assert combine_vowels("ㅏ", "ㅗ", join_on_fail=True) == "ㅏㅗ"

    def test_disassemble_to_groups_decomposes_compound_jamo(self):
        assert disassemble_to_groups("값괜찮아") == [
            ["ㄱ", "ㅏ", "ㅂ", "ㅅ"],
            ["ㄱ", "ㅗ", "ㅐ", "ㄴ"],
            ["ㅊ", "ㅏ", "ㄴ", "ㅎ"],
            ["ㅇ", "ㅏ"],
        ]

    def test_es_hangul_style_core_helpers(self):
        """es-hangul 스타일 핵심 헬퍼 테스트"""
        assert combine_vowels("ㅗ", "ㅏ") == "ㅘ"
        assert combine_vowels("ㅏ", "ㅗ") is None
        assert combine_character("ㄱ", "ㅏ", "ㅂ") == "갑"
        assert disassemble_to_groups("사과") == [["ㅅ", "ㅏ"], ["ㄱ", "ㅗ", "ㅏ"]]
        assert disassemble_complete_character("값") == {
            "choseong": "ㄱ",
            "jungseong": "ㅏ",
            "jongseong": "ㅂㅅ",
        }
        assert remove_last_character("안녕하세요 값") == "안녕하세요 갑"
        assert remove_last_character("프론트엔드") == "프론트엔ㄷ"
        assert remove_last_character("전화") == "전호"

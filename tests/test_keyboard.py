from hangulpy import (
    convert_hangul_to_qwerty,
    convert_qwerty_to_alphabet,
    convert_qwerty_to_hangul,
    koen,
)


class TestKeyboardConversions:
    """QWERTY/한글 자판 변환 테스트"""

    def test_convert_hangul_to_qwerty(self):
        assert convert_hangul_to_qwerty("뮻") == "abc"
        assert convert_hangul_to_qwerty("찮") == "cksg"
        assert convert_hangul_to_qwerty("서울, 코리아") == "tjdnf, zhfldk"
        assert convert_hangul_to_qwerty("찮") == koen("찮")

    def test_convert_qwerty_to_hangul(self):
        assert convert_qwerty_to_hangul("abc") == "뮻"
        assert convert_qwerty_to_hangul("ABC") == "뮻"
        assert convert_qwerty_to_hangul("RㅏㄱEㅜrl") == "깍뚜기"

    def test_convert_qwerty_to_alphabet(self):
        assert convert_qwerty_to_alphabet("abc") == "ㅁㅠㅊ"
        assert convert_qwerty_to_alphabet("ABC") == "ㅁㅠㅊ"
        assert convert_qwerty_to_alphabet("RㅏㄱEㅜrl") == "ㄲㅏㄱㄸㅜㄱㅣ"

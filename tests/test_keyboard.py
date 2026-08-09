import unicodedata
import warnings
from typing import Callable, Tuple

import pytest

from hangulpy import (
    HangulpyDeprecationWarning,
    autofix,
    convert_hangul_to_qwerty,
    convert_qwerty_to_alphabet,
    convert_qwerty_to_hangul,
    enko,
    koen,
)

KeyboardConverter = Callable[..., str]
KEYBOARD_CONVERTERS: Tuple[KeyboardConverter, ...] = (
    enko,
    convert_qwerty_to_hangul,
    autofix,
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

    def test_enko_moves_only_second_compound_final_before_vowel(self):
        assert enko("rkrtk") == "각사"
        assert enko("rkqtk") == "갑사"
        assert convert_qwerty_to_hangul("rkrtk", allow_double_consonant=True) == "각사"

    def test_enko_does_not_use_initial_only_consonant_as_final(self):
        assert enko("rkE") == "가ㄸ"
        assert enko("rkEk") == "가따"
        assert convert_qwerty_to_hangul("rkEk", allow_double_consonant=True) == "가따"

    def test_koen_accepts_nfd_and_canonical_jamo(self):
        nfd = unicodedata.normalize("NFD", "서울, 코리아")

        assert koen(nfd) == "tjdnf, zhfldk"
        assert convert_hangul_to_qwerty(nfd) == "tjdnf, zhfldk"
        assert koen("각") == "rkr"
        assert koen("값") == "rkqt"
        assert koen("ᆹ") == "qt"

    def test_new_double_consonant_keyword(self):
        for converter in KEYBOARD_CONVERTERS:
            assert converter("rrk", allow_double_consonant=True) == "까"

    def test_legacy_double_consonant_keyword_warns_at_caller(self):
        for converter in KEYBOARD_CONVERTERS:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                result = converter("rrk", allowDoubleConsonant=True)

            assert result == "까"
            assert len(caught) == 1
            assert caught[0].category is HangulpyDeprecationWarning
            assert caught[0].filename == __file__
            assert "allow_double_consonant" in str(caught[0].message)

    def test_double_consonant_keyword_conflicts_and_unknown_kwargs(self):
        for converter in KEYBOARD_CONVERTERS:
            with pytest.raises(TypeError, match="cannot use both"):
                converter(
                    "rrk",
                    allow_double_consonant=True,
                    allowDoubleConsonant=True,
                )

            with pytest.raises(TypeError, match="unexpected keyword argument 'unknown'"):
                converter("rrk", unknown=True)

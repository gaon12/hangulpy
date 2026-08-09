import unicodedata

import pytest

from hangulpy import (
    can_be_jongsung,
    disassemble,
    ends_with_consonant,
    get_hangul_components,
    hangul_contains,
    hangul_search,
    is_complete_hangul,
    is_hangul,
    join_jamos,
    normalize_hangul,
    remove_last_character,
    sort_hangul,
    split_hangul_string,
    split_syllables,
    to_compat_jamo,
    to_jamo,
)


def test_normalize_hangul_across_unicode_forms():
    nfd = unicodedata.normalize("NFD", "한글")

    assert normalize_hangul(nfd) == "한글"
    assert normalize_hangul("ㅎㅏㄴㄱㅡㄹ") == "한글"
    assert normalize_hangul("한글", "NFD") == nfd
    assert normalize_hangul("한글", "HCJ") == "ㅎㅏㄴㄱㅡㄹ"
    assert to_jamo("한글") == nfd
    assert to_jamo("한글", compatibility=True) == "ㅎㅏㄴㄱㅡㄹ"
    assert to_compat_jamo(nfd) == "ㅎㅏㄴㄱㅡㄹ"


def test_normalize_hangul_rejects_invalid_form():
    with pytest.raises(ValueError):
        normalize_hangul("한글", "nfkc")  # type: ignore[arg-type]


def test_all_modern_syllables_round_trip():
    for codepoint in range(0xAC00, 0xD7A4):
        syllable = chr(codepoint)
        assert join_jamos(split_hangul_string(syllable)) == syllable
        assert normalize_hangul(to_jamo(syllable)) == syllable


def test_split_has_no_empty_jamo_and_validates_format():
    assert split_hangul_string("가") == ["ㄱ", "ㅏ"]
    assert split_syllables("사과") == ["ㅅ", "ㅏ", "ㄱ", "ㅗ", "ㅏ"]
    assert split_syllables("사과", "string") == "ㅅㅏㄱㅗㅏ"
    assert disassemble("가", "list") == ["ㄱ", "ㅏ"]
    with pytest.raises(ValueError):
        split_syllables("가", "typo")  # type: ignore[arg-type]


def test_join_jamos_accepts_canonical_jamo():
    assert join_jamos(unicodedata.normalize("NFD", "각사")) == "각사"
    assert join_jamos(["ᄒ", "ᅡ", "ᆫ"]) == "한"


def test_remove_last_character_preserves_syllable_boundaries():
    assert remove_last_character("가나") == "가ㄴ"
    assert remove_last_character("신세계") == "신세ㄱ"
    assert remove_last_character(unicodedata.normalize("NFD", "한")) == "하"


def test_sort_hangul_uses_unicode_component_order_for_mixed_text():
    assert sort_hangul(["갃", "갂"]) == ["갂", "갃"]
    assert sort_hangul(["가", "ㄱ", "각"]) == ["ㄱ", "가", "각"]
    assert sort_hangul([unicodedata.normalize("NFD", "나"), "가"]) == ["가", "나"]


def test_properties_and_search_accept_nfd():
    nfd_ga = unicodedata.normalize("NFD", "가")
    nfd_gak = unicodedata.normalize("NFD", "각")

    assert is_hangul(nfd_ga)
    assert is_hangul("ㄱ", include_jamo=True)
    assert not is_hangul("ㄱ")
    assert is_complete_hangul(nfd_ga)
    assert get_hangul_components(nfd_gak) == ("ㄱ", "ㅏ", "ㄱ")
    assert ends_with_consonant("한글")
    assert ends_with_consonant(nfd_gak)
    assert hangul_contains("한글", unicodedata.normalize("NFD", "한"))
    assert hangul_search(unicodedata.normalize("NFD", "한글"), "글") == 3


def test_empty_string_is_not_a_jongsung():
    assert not can_be_jongsung("")

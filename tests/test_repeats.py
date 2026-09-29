# pyright: basic
import unicodedata

import pytest

from hangulpy import reduce_jamo_repeats


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("ㅋㅋㅋㅋ ㅎㅎㅎ ㅠㅠㅠㅠ ㅜㅜㅜ", "ㅋㅋ ㅎㅎ ㅠㅠ ㅜㅜ"),
        ("ㄱㄱㄱ ㅏㅏㅏ ㄳㄳㄳ", "ㄱㄱ ㅏㅏ ㄳㄳ"),
        ("앜ㅋㅋㅋㅋ", "아ㅋㅋ"),
        ("헣ㅎㅎㅎㅎ", "허ㅎㅎ"),
        ("ㅋㅋㅋㅋ쿠ㅜㅜㅜㅜ", "ㅋㅋㅜㅜ"),
        ("ㅎㅎㅎ휴ㅠㅠㅠ", "ㅎㅎㅠㅠ"),
        ("ㅠㅠㅠ유ㅠㅠㅠ", "ㅠㅠ"),
        ("ㅜㅜ우ㅜㅜㅜ", "ㅜㅜ"),
        ("ㅋㅋㅋ카페 ㅋㅋㅋ쿠키 ㅠㅠㅠ유명", "ㅋㅋ카페 ㅋㅋ쿠키 ㅠㅠ유명"),
        ("앜ㅋ 헣ㅎ", "앜ㅋ 헣ㅎ"),
        ("각ㄱㄱㄱ 밖ㅋㅋㅋㅋ 힝ㅠㅠㅠ", "각ㄱㄱ 밖ㅋㅋ 힝ㅠㅠ"),
        ("1111 AAAA 하하하 고고고 !!! 👩‍💻👩‍💻", "1111 AAAA 하하하 고고고 !!! 👩‍💻👩‍💻"),
        ("ㅋㅋㅋ\tㅋㅋㅋ\nㅋㅋㅋ", "ㅋㅋ\tㅋㅋ\nㅋㅋ"),
        ("\uffbb\uffbb\uffbb", "ㅋㅋ"),
        ("ᄏᄏᄏ ᅲᅲᅲ", "ᄏᄏ ᅲᅲ"),
        ("ㅋᄏ\uffbbㅋ", "ㅋᄏ"),
        ("ᄔᄔᄔ ㅤㅤㅤ", "ᄔᄔᄔ ㅤㅤㅤ"),
        ("ㅋ\u0301ㅋ\u0301ㅋ\u0301 a\u0315\u0300", "ㅋ\u0301ㅋ\u0301ㅋ\u0301 a\u0315\u0300"),
    ],
)
def test_reduces_only_jamo_and_supported_emoticon_contexts(text, expected):
    assert reduce_jamo_repeats(text) == expected
    assert reduce_jamo_repeats(expected) == expected


def test_emoticon_normalization_can_be_disabled():
    assert reduce_jamo_repeats("앜ㅋㅋㅋㅋ", normalize_emoticons=False) == "앜ㅋㅋ"
    assert reduce_jamo_repeats("ㅋㅋㅋ쿠ㅜㅜㅜ", normalize_emoticons=False) == "ㅋㅋ쿠ㅜㅜ"


def test_nfd_emoticons_preserve_the_form_of_surrounding_words_and_the_base():
    prefix = unicodedata.normalize("NFD", "한글 앜")
    expected = unicodedata.normalize("NFD", "한글 아") + "ㅋㅋ"
    assert reduce_jamo_repeats(prefix + "ㅋㅋㅋㅋ") == expected
    bridge = unicodedata.normalize("NFD", "쿠")
    assert reduce_jamo_repeats("ㅋㅋㅋ" + bridge + "ㅜㅜㅜ") == "ㅋㅋㅜㅜ"


@pytest.mark.parametrize("form", ["NFC", "NFD"])
def test_all_complete_modern_syllables_are_preserved(form):
    text = unicodedata.normalize(form, "".join(chr(code) for code in range(0xAC00, 0xD7A4)))
    assert reduce_jamo_repeats(text) == text


@pytest.mark.parametrize("limit", [1, 2, 3, 8])
def test_repeat_limit_applies_to_both_plain_and_attached_jamo(limit):
    assert reduce_jamo_repeats("ㅋ" * 8, max_repeats=limit) == "ㅋ" * limit
    assert reduce_jamo_repeats("앜" + "ㅋ" * 7, max_repeats=limit) == "아" + "ㅋ" * limit


@pytest.mark.parametrize(
    ("limit", "expected"),
    [(1, "ㅋㅎㅋ"), (2, "ㅋㅎㅎㅋㅋ"), (3, "ㅋㅎㅎㅋㅋㅋ"), (4, "ㅋㅎㅎㅋㅋㅋㅋ")],
)
@pytest.mark.parametrize("normalize_emoticons", [True, False])
def test_mixed_laughter_keeps_separate_jamo_runs(limit, expected, normalize_emoticons):
    assert (
        reduce_jamo_repeats(
            "ㅋㅎㅎㅋㅋㅋㅋ", max_repeats=limit, normalize_emoticons=normalize_emoticons
        )
        == expected
    )


def test_long_input_has_no_regex_backtracking_and_keeps_word_boundaries():
    text = "ㅋ" * 20_000 + "하하하" + "ㅠ" * 20_000
    assert reduce_jamo_repeats(text) == "ㅋㅋ하하하ㅠㅠ"


@pytest.mark.parametrize("text", [None, 1, b"text", ["ㅋ"]])
def test_rejects_non_string_inputs(text):
    with pytest.raises(TypeError, match="text.*string"):
        reduce_jamo_repeats(text)


@pytest.mark.parametrize("limit", [True, False, None, 1.5, "2"])
def test_rejects_non_integer_limits_even_for_empty_text(limit):
    with pytest.raises(TypeError, match="max_repeats.*integer"):
        reduce_jamo_repeats("", max_repeats=limit)


@pytest.mark.parametrize("limit", [0, -1])
def test_rejects_non_positive_limits(limit):
    with pytest.raises(ValueError, match="max_repeats.*positive"):
        reduce_jamo_repeats("ㅋ", max_repeats=limit)


@pytest.mark.parametrize("value", [None, 0, 1, "yes"])
def test_rejects_non_boolean_emoticon_options(value):
    with pytest.raises(TypeError, match="normalize_emoticons.*bool"):
        reduce_jamo_repeats("", normalize_emoticons=value)

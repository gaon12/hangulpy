# pyright: basic
import unicodedata

import pytest

from hangulpy import (
    HangulIndex,
    HangulSearcher,
    find_hangul_spans,
    hangul_contains,
    hangul_replace,
    hangul_search,
    normalize_halfwidth_hangul,
    normalize_hangul,
    to_compat_jamo,
    to_jamo,
)

HALFWIDTH_HANGUL = "\uffbe\uffc2\uffa4\uffa1\uffda\uffa9"


def test_all_assigned_halfwidth_hangul_convert_to_compatibility_jamo():
    codes = [
        *range(0xFFA0, 0xFFBF),
        *range(0xFFC2, 0xFFC8),
        *range(0xFFCA, 0xFFD0),
        *range(0xFFD2, 0xFFD8),
        *range(0xFFDA, 0xFFDD),
    ]
    text = "".join(chr(code) for code in codes)
    expected = "ㅤ" + "".join(chr(code) for code in range(0x3131, 0x3164))
    assert normalize_halfwidth_hangul(text) == expected
    assert len(expected) == len(text) == 52
    assert normalize_halfwidth_hangul(expected) == expected


def test_width_conversion_preserves_unrelated_text_and_unassigned_codepoints():
    unrelated = "ＡＢＣ １２３ ① ﬃ ｶ 한글 ㄱ 한 a\u0315\u0300 👩‍💻"
    gaps = "\uffbf\uffc0\uffc1\uffc8\uffc9\uffd0\uffd1\uffd8\uffd9"
    text = unrelated + gaps + "\uffbb\uffbb"
    assert normalize_halfwidth_hangul(text) == unrelated + gaps + "ㅋㅋ"
    assert normalize_halfwidth_hangul("") == ""


@pytest.mark.parametrize("text", [None, 1, True, b"hangul", ["한"]])
def test_halfwidth_conversion_rejects_non_strings(text):
    with pytest.raises(TypeError, match="text.*string"):
        normalize_halfwidth_hangul(text)


def test_normalization_and_jamo_conversion_accept_halfwidth_and_mixed_widths():
    nfd = unicodedata.normalize("NFD", "한글")
    assert normalize_halfwidth_hangul(HALFWIDTH_HANGUL) == "ㅎㅏㄴㄱㅡㄹ"
    assert normalize_hangul(HALFWIDTH_HANGUL) == "한글"
    assert normalize_hangul(HALFWIDTH_HANGUL, "NFD") == nfd
    assert normalize_hangul(HALFWIDTH_HANGUL, "HCJ") == "ㅎㅏㄴㄱㅡㄹ"
    assert to_jamo(HALFWIDTH_HANGUL) == nfd
    assert to_compat_jamo(HALFWIDTH_HANGUL) == "ㅎㅏㄴㄱㅡㄹ"
    assert normalize_hangul("\uffbeㅏᆫ\uffa1ㅡㄹ") == "한글"
    assert normalize_hangul("Ａ①\uffbe\uffc2\uffa4") == "Ａ①한"


@pytest.mark.parametrize("pattern", ["한글", "ㅎㄱ", "\uffbe\uffa1", HALFWIDTH_HANGUL])
def test_search_and_replacement_keep_original_halfwidth_source_spans(pattern):
    text = "Ａ" + HALFWIDTH_HANGUL + "!"
    assert hangul_contains(text, pattern)
    assert hangul_search(text, pattern) == 1
    assert HangulSearcher(pattern).find_index(text) == 1
    matches = find_hangul_spans(text, pattern)
    assert [(match.span(), match.text) for match in matches] == [((1, 7), HALFWIDTH_HANGUL)]
    assert hangul_replace(text, pattern, "X") == "ＡX!"
    result = HangulIndex([text, "다른 말"]).search(pattern, min_score=1.0)
    assert result[0].text == text
    assert result[0].match_index == 1


def test_halfwidth_compound_vowels_do_not_consume_the_next_syllable():
    text = "\uffa1\uffcc\uffc2\uffa4\uffc2"
    assert normalize_hangul(text) == "과나"
    matches = find_hangul_spans(text, "과")
    assert [match.span() for match in matches] == [(0, 3)]
    assert hangul_replace(text, "과", "X") == "X\uffa4\uffc2"

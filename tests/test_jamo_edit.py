import unicodedata

from hangulpy.jamo_edit import jamo_len, jamo_slice, typing_steps


def test_jamo_len_counts_keyboard_parts_and_opaque_graphemes() -> None:
    assert jamo_len("가과값") == 2 + 3 + 4
    assert jamo_len(unicodedata.normalize("NFD", "한글")) == 6
    assert jamo_len("e\u0301👍🏽👨‍👩‍👧‍👦") == 3


def test_jamo_slice_preserves_original_syllable_boundaries() -> None:
    assert jamo_slice("가나", 0, 3) == "가ㄴ"
    assert jamo_slice("가나", 1, 3) == "ㅏㄴ"
    assert jamo_slice("가나", -2, None) == "나"
    assert jamo_slice("가나", 3, 2) == ""


def test_jamo_slice_handles_compound_parts_and_nfd() -> None:
    assert jamo_slice("값", 0, 3) == "갑"
    assert jamo_slice("값", 2, 4) == "ㅂㅅ"
    assert jamo_slice("과", 0, 2) == "고"
    assert jamo_slice(unicodedata.normalize("NFD", "한글"), 0, 3) == "한"


def test_jamo_slice_keeps_non_hangul_graphemes_atomic() -> None:
    family = "👨‍👩‍👧‍👦"
    text = f"가{family}나"

    assert jamo_len(text) == 5
    assert jamo_slice(text, 2, 3) == family
    assert jamo_slice(text, 1, 4) == f"ㅏ{family}ㄴ"


def test_typing_steps_preserve_syllable_and_grapheme_boundaries() -> None:
    assert typing_steps("값") == ["ㄱ", "가", "갑", "값"]
    assert typing_steps("가나") == ["ㄱ", "가", "가ㄴ", "가나"]
    assert typing_steps(unicodedata.normalize("NFD", "과")) == ["ㄱ", "고", "과"]
    assert typing_steps("가👍🏽") == ["ㄱ", "가", "가👍🏽"]

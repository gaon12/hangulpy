# pyright: basic
import unicodedata
import warnings
from pathlib import Path

import pytest

import hangulpy
from hangulpy.chosung import extract_chosung as extract_chosung_char


@pytest.mark.parametrize(
    ("old_name", "new_name", "expected"),
    [
        ("extract_chosung", "get_chosung_string", "ㅎㅅㄱ ㄱ"),
        ("extract_jungsung", "get_jungsung_string", "ㅏㅏㅘ ㅏ"),
        ("extract_jongsung", "get_jongsung_string", "ㄴ "),
    ],
)
@pytest.mark.parametrize("form", ["NFC", "NFD"])
@pytest.mark.parametrize("keep_non_hangul", [False, True])
def test_deprecated_names_preserve_results_and_point_to_caller(
    old_name, new_name, expected, form, keep_non_hangul
):
    text = unicodedata.normalize(form, "A한사과! ㄱㅏ🙂")
    if keep_non_hangul:
        expected = "A" + expected.split(" ")[0] + "! " + expected.split(" ")[1] + "🙂"

    with pytest.warns(DeprecationWarning, match=f"{old_name}.*v1.6.*{new_name}") as caught:
        old_result = getattr(hangulpy, old_name)(text, keep_non_hangul=keep_non_hangul)

    assert old_result == expected
    assert len(caught) == 1
    assert Path(caught[0].filename) == Path(__file__)
    with warnings.catch_warnings(record=True) as new_warnings:
        warnings.simplefilter("always")
        new_result = getattr(hangulpy, new_name)(
            text, keep_spaces=True, keep_non_hangul=keep_non_hangul
        )
    assert new_result == old_result
    assert not new_warnings


def test_existing_chosung_calls_keep_their_original_behavior():
    assert hangulpy.get_chosung("한") == "ㅎ"
    assert hangulpy.get_chosung("한글") is None
    assert hangulpy.get_chosung_string("A한! ㄱ") == "ㅎ"
    assert hangulpy.get_chosung_string("A한! ㄱ", True) == "Aㅎ! ㄱ"
    assert hangulpy.get_chosung_string("ㅎㅏㄴ") == "ㅎ"
    assert hangulpy.get_chosung_string("ㅎㅏㄴ", keep_non_hangul=False) == "ㅎㄴ"


@pytest.mark.parametrize(
    ("getter", "expected"),
    [
        (hangulpy.get_chosung_string, "Aㅎㄱ!ㄱ🙂"),
        (hangulpy.get_jungsung_string, "Aㅏㅡ!ㅏ🙂"),
        (hangulpy.get_jongsung_string, "Aㄴㄹ!🙂"),
    ],
)
def test_new_string_names_control_spaces_independently(getter, expected):
    text = "A한글! ㄱㅏ🙂"
    assert getter(text, keep_non_hangul=True) == expected
    assert getter(text, keep_spaces=True, keep_non_hangul=True) == expected.replace("!", "! ")
    assert getter("") == ""


def test_undocumented_character_helper_warns_without_changing_results():
    with pytest.warns(DeprecationWarning, match="v1.6"):
        assert extract_chosung_char("한") == "ㅎ"
    with pytest.warns(DeprecationWarning, match="v1.6"):
        assert extract_chosung_char("!") == "!"


def test_expired_warning_class_is_removed():
    assert not hasattr(hangulpy, "HangulpyDeprecationWarning")
    assert "HangulpyDeprecationWarning" not in hangulpy.__all__

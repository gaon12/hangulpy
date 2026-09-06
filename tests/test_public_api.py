import hangulpy


def test_all_exports_are_unique_and_importable() -> None:
    assert len(hangulpy.__all__) == len(set(hangulpy.__all__))
    assert all(hasattr(hangulpy, name) for name in hangulpy.__all__)


def test_package_exposes_a_version_string() -> None:
    assert isinstance(hangulpy.__version__, str)
    assert hangulpy.__version__


def test_v15_removes_legacy_names_and_keywords():
    import pytest

    assert not hasattr(hangulpy, "chosungIncludes")
    assert hangulpy.chosung_includes("사과", "ㅅㄱ")
    for function in [hangulpy.hangul_contains, hangulpy.hangul_search, hangulpy.hangul_search_all]:
        with pytest.raises(TypeError, match="notallowempty"):
            function("한글", "", notallowempty=True)
    for method in ["search", "find_index", "find_all"]:
        with pytest.raises(TypeError, match="notallowempty"):
            getattr(hangulpy.HangulSearcher(""), method)("한글", notallowempty=True)
    for function in [hangulpy.enko, hangulpy.autofix, hangulpy.convert_qwerty_to_hangul]:
        with pytest.raises(TypeError, match="allowDoubleConsonant"):
            function("rrk", allowDoubleConsonant=True)
        assert function("rrk", allow_double_consonant=True) == "까"
        with pytest.raises(TypeError, match="bool"):
            function("rrk", allow_double_consonant=1)
    with pytest.raises(TypeError, match="bool"):
        hangulpy.hangul_contains("한글", "", not_allow_empty=1)

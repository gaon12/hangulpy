# pyright: basic
import hangulpy


def test_all_exports_are_unique_and_importable() -> None:
    assert len(hangulpy.__all__) == len(set(hangulpy.__all__))
    assert all(hasattr(hangulpy, name) for name in hangulpy.__all__)


def test_public_modules_export_every_defined_member() -> None:
    import importlib
    import inspect
    import pkgutil
    from pathlib import Path

    # Internal helpers shared across package modules; intentionally not exported.
    internal_members = {
        "hangul_assemble.assemble_fragments",
        "hangul_contains.PreparedSearchText",
        "hangul_contains.prepare_search_text",
    }

    package_dir = Path(hangulpy.__file__).parent
    missing: list[str] = []
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module_name = module_info.name
        if module_name.startswith("_") or module_name == "utils":
            continue
        module = importlib.import_module(f"hangulpy.{module_name}")
        for name, member in inspect.getmembers(module):
            if name.startswith("_"):
                continue
            if not (inspect.isfunction(member) or inspect.isclass(member)):
                continue
            if member.__module__ != module.__name__:
                continue
            qualified = f"{module_name}.{name}"
            if qualified not in internal_members and name not in hangulpy.__all__:
                missing.append(qualified)
    assert not missing, f"public members missing from hangulpy.__all__: {missing}"


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
        hangulpy.hangul_contains("한글", "", not_allow_empty=1)  # type: ignore[arg-type]

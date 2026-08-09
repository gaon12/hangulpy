import hangulpy


def test_all_exports_are_unique_and_importable() -> None:
    assert len(hangulpy.__all__) == len(set(hangulpy.__all__))
    assert all(hasattr(hangulpy, name) for name in hangulpy.__all__)


def test_package_exposes_a_version_string() -> None:
    assert isinstance(hangulpy.__version__, str)
    assert hangulpy.__version__

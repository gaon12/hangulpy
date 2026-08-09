import pytest

from hangulpy.hanja import HanjaRun, is_hanja, split_hanja


def test_is_hanja_covers_unified_extensions_and_compatibility() -> None:
    assert is_hanja("字")
    assert is_hanja("㐀")  # Extension A
    assert is_hanja("𠀀")  # Extension B
    assert is_hanja("金")  # BMP compatibility ideograph
    assert is_hanja("丽")  # Compatibility supplement
    assert is_hanja(chr(0x30000))  # Extension G
    assert is_hanja(chr(0x31350))  # Extension H

    assert not is_hanja("한")
    assert not is_hanja("々")
    assert not is_hanja("")
    assert not is_hanja("漢字")


def test_is_hanja_rejects_non_string_input() -> None:
    with pytest.raises(TypeError, match="char must be a string"):
        is_hanja(1)  # type: ignore[arg-type]


def test_split_hanja_returns_consecutive_typed_runs() -> None:
    assert split_hanja("한字ABC𠀀끝") == [
        HanjaRun("한", False),
        HanjaRun("字", True),
        HanjaRun("ABC", False),
        HanjaRun("𠀀", True),
        HanjaRun("끝", False),
    ]
    assert split_hanja("漢字") == [HanjaRun("漢字", True)]
    assert split_hanja("") == []


def test_hanja_run_is_frozen() -> None:
    run = HanjaRun("漢", True)
    with pytest.raises(AttributeError):
        run.text = "字"  # type: ignore[misc]

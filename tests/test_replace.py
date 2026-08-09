import unicodedata

import pytest

from hangulpy import (
    HangulMatch,
    hangul_partition,
    hangul_replace,
    hangul_rpartition,
    hangul_split,
)


def test_hangul_replace_supports_initials_counts_and_callbacks() -> None:
    assert hangul_replace("가나다가", "ㄱ", "X") == "X나다X"
    assert hangul_replace("가나다가", "ㄱ", "X", count=1) == "X나다가"
    assert hangul_replace("가나다가", "ㄱ", "X", count=0) == "가나다가"
    assert (
        hangul_replace("가나다가", "ㄱ", lambda match: f"<{match.text}:{match.start}>")
        == "<가:0>나다<가:3>"
    )


def test_hangul_replace_preserves_nfd_outside_the_source_match() -> None:
    nfd = unicodedata.normalize("NFD", "한글")

    assert hangul_replace(f"A{nfd}B", "글", "X") == f"A{nfd[:3]}XB"
    assert hangul_replace("사과", "삭", "X") == "X"
    assert hangul_replace("한글", "없음", "X") == "한글"


def test_hangul_split_uses_original_match_boundaries() -> None:
    assert hangul_split("가나다가", "ㄱ") == ["", "나다", ""]
    assert hangul_split("가나다가", "ㄱ", maxsplit=1) == ["", "나다가"]
    assert hangul_split("가나다가", "ㄱ", maxsplit=0) == ["가나다가"]
    assert hangul_split("한글", "없음") == ["한글"]


def test_hangul_partition_and_rpartition_match_string_contracts() -> None:
    assert hangul_partition("가나다가", "ㄱ") == ("", "가", "나다가")
    assert hangul_rpartition("가나다가", "ㄱ") == ("가나다", "가", "")
    assert hangul_partition("한글", "없음") == ("한글", "", "")
    assert hangul_rpartition("한글", "없음") == ("", "", "한글")


@pytest.mark.parametrize(
    "function", [hangul_replace, hangul_split, hangul_partition, hangul_rpartition]
)
def test_source_transformers_reject_empty_patterns(function) -> None:
    if function is hangul_replace:
        with pytest.raises(ValueError, match="pattern"):
            function("한글", "", "X")
    else:
        with pytest.raises(ValueError, match="pattern"):
            function("한글", "")


def test_hangul_replace_and_split_validate_options() -> None:
    with pytest.raises(TypeError, match="replacement"):
        hangul_replace("한글", "ㅎ", 1)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="callable"):
        hangul_replace("한글", "ㅎ", lambda _match: 1)  # type: ignore[arg-type,return-value]
    with pytest.raises(TypeError, match="count"):
        hangul_replace("한글", "ㅎ", "X", count=True)
    with pytest.raises(ValueError, match="count"):
        hangul_replace("한글", "ㅎ", "X", count=-2)
    with pytest.raises(TypeError, match="maxsplit"):
        hangul_split("한글", "ㅎ", maxsplit=True)
    with pytest.raises(ValueError, match="maxsplit"):
        hangul_split("한글", "ㅎ", maxsplit=-2)


def test_hangul_replace_callback_receives_public_match_type() -> None:
    seen = []

    def replace(match: HangulMatch) -> str:
        seen.append(match)
        return "X"

    assert hangul_replace("한글", "ㅎ", replace) == "X글"
    assert seen == [HangulMatch(0, 1, "한")]

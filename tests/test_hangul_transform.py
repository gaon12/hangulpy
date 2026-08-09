import unicodedata
from typing import Any, List, Tuple, Union

import pytest

from hangulpy.hangul_transform import map_hangul


def test_map_hangul_accepts_text_and_component_results() -> None:
    def remove_finals(cho: str, jung: str, jong: str) -> Union[str, Tuple[str, str, str]]:
        if jong:
            return cho, jung, ""
        return f"[{cho}{jung}]"

    assert map_hangul("각 나!", remove_finals) == "가 [ㄴㅏ]!"


def test_map_hangul_normalizes_nfd_and_preserves_non_hangul() -> None:
    nfd = unicodedata.normalize("NFD", "한글")
    seen: List[Tuple[str, str, str]] = []

    def identity(cho: str, jung: str, jong: str) -> Tuple[str, str, str]:
        seen.append((cho, jung, jong))
        return cho, jung, jong

    assert map_hangul(f"A{nfd}🙂", identity) == "A한글🙂"
    assert seen == [("ㅎ", "ㅏ", "ㄴ"), ("ㄱ", "ㅡ", "ㄹ")]


def test_map_hangul_can_expand_or_remove_syllables() -> None:
    assert map_hangul("가1나", lambda _cho, _jung, _jong: "X") == "X1X"
    assert map_hangul("가1나", lambda _cho, _jung, _jong: "") == "1"


def test_map_hangul_rejects_invalid_mapper_results() -> None:
    def list_mapper(_cho: str, _jung: str, _jong: str) -> Any:
        return ["ㄱ", "ㅏ", ""]

    def short_tuple_mapper(_cho: str, _jung: str, _jong: str) -> Any:
        return "ㄱ", "ㅏ"

    def non_string_mapper(_cho: str, _jung: str, _jong: str) -> Any:
        return "ㄱ", "ㅏ", 1

    with pytest.raises(TypeError, match="string or a 3-tuple"):
        map_hangul("가", list_mapper)

    with pytest.raises(ValueError, match="exactly three"):
        map_hangul("가", short_tuple_mapper)

    with pytest.raises(TypeError, match="must all be strings"):
        map_hangul("가", non_string_mapper)

    with pytest.raises(ValueError, match="invalid Hangul components"):
        map_hangul("가", lambda _cho, _jung, _jong: ("ㅏ", "ㄱ", ""))


def test_map_hangul_rejects_non_callable_mapper() -> None:
    with pytest.raises(TypeError, match="mapper must be callable"):
        map_hangul("가", None)  # type: ignore[arg-type]

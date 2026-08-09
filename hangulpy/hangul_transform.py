"""Composable transformations over modern Hangul syllables."""

from typing import Callable, List, Tuple, Union, cast

from hangulpy.hangul_normalize import normalize_hangul
from hangulpy.hangul_properties import get_hangul_components
from hangulpy.utils import compose_syllable

HangulComponents = Tuple[str, str, str]
HangulMapResult = Union[str, HangulComponents]
HangulMapper = Callable[[str, str, str], HangulMapResult]


def _render_mapped_value(value: object) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, tuple):
        raise TypeError("mapper must return a string or a 3-tuple of Hangul components")
    items = cast(Tuple[object, ...], value)
    if len(items) != 3:
        raise ValueError("mapper component tuple must contain exactly three items")

    cho, jung, jong = items
    if not isinstance(cho, str) or not isinstance(jung, str) or not isinstance(jong, str):
        raise TypeError("mapper component tuple items must all be strings")

    try:
        return compose_syllable(cho, jung, jong)
    except ValueError as exc:
        raise ValueError(f"mapper returned invalid Hangul components: {value!r}") from exc


def map_hangul(text: str, mapper: HangulMapper) -> str:
    """Map each complete Hangul syllable while preserving other text.

    ``mapper`` receives ``(choseong, jungseong, jongseong)`` as three
    positional arguments. It may return replacement text or a component tuple
    to be composed into one modern Hangul syllable. Canonical/NFD and HCJ input
    is normalized to NFC before mapping.
    """
    if not callable(mapper):
        raise TypeError("mapper must be callable")

    result: List[str] = []
    for char in normalize_hangul(text, "NFC"):
        components = get_hangul_components(char)
        if components is None:
            result.append(char)
            continue
        result.append(_render_mapped_value(mapper(*components)))
    return "".join(result)

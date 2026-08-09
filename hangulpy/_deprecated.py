"""Internal helpers for one-release compatibility shims."""

import warnings
from typing import Dict, Optional


class HangulpyDeprecationWarning(DeprecationWarning):
    """hangulpy compatibility APIs scheduled for removal."""


def resolve_legacy_bool(
    value: Optional[bool],
    legacy_options: Dict[str, object],
    legacy_name: str,
    replacement: str,
) -> bool:
    """Resolve a renamed bool keyword and emit a targeted deprecation warning."""
    if legacy_name in legacy_options:
        if value is not None:
            raise TypeError(f"cannot use both {replacement!r} and {legacy_name!r}")
        legacy_value = legacy_options.pop(legacy_name)
        if not isinstance(legacy_value, bool):
            raise TypeError(f"{legacy_name!r} must be a bool")
        warnings.warn(
            f"{legacy_name!r} is deprecated and will be removed in the next release; "
            f"use {replacement!r} instead",
            HangulpyDeprecationWarning,
            stacklevel=3,
        )
        value = legacy_value

    if legacy_options:
        unexpected = next(iter(legacy_options))
        raise TypeError(f"unexpected keyword argument {unexpected!r}")
    if value is None:
        return False
    if not isinstance(value, bool):
        raise TypeError(f"{replacement!r} must be a bool")
    return value

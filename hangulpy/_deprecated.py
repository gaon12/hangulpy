"""Boolean validation and the historical public deprecation-warning category."""


class HangulpyDeprecationWarning(DeprecationWarning):
    """Retained so warning filters written for hangulpy 1.4 remain importable."""


def require_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name!r} must be a bool")
    return value

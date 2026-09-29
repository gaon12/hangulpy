"""Runtime validation helpers for public API arguments."""


def require_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name!r} must be a bool")
    return value


def require_str(value: object, name: str = "text") -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name!r} must be a string")
    return value


def require_positive_int(value: object, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name!r} must be an integer")
    if value < 1:
        raise ValueError(f"{name!r} must be positive")
    return value

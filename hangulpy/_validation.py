"""Runtime validation helpers for public API arguments."""


def require_bool(value: object, name: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name!r} must be a bool")
    return value

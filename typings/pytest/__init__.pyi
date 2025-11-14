from __future__ import annotations

from collections.abc import Callable
from types import TracebackType
from typing import Any, ContextManager, TypeVar

_T = TypeVar("_T")


class _RaisesContext(ContextManager[None]):
    def __enter__(self) -> None: ...
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...


def raises(
    expected_exception: type[BaseException] | tuple[type[BaseException], ...],
    *args: Any,
    **kwargs: Any,
) -> _RaisesContext: ...


def mark(*args: Any, **kwargs: Any) -> Any: ...


def fixture(*args: Any, **kwargs: Any) -> Callable[[Callable[..., _T]], Callable[..., _T]]: ...

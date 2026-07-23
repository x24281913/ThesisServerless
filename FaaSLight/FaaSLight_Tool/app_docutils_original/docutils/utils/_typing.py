"""Private helpers for the ``typing`` module."""

from __future__ import annotations
TYPE_CHECKING = False
if TYPE_CHECKING:
    import sys
    from collections.abc import Callable
    from typing import Any, Final, TypeVar, final, overload
    if sys.version_info[:2] >= (3, 11):
        from typing import Self
    else:
        from typing_extensions import Self
    if sys.version_info[:2] >= (3, 12):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias
    _F = TypeVar('_F', bound=Callable[(..., Any)])
    _T = TypeVar('_T')
else:
    
    def final(f: _T) -> _T:
        return f
    
    def _overload_inner(*args, **kwds):
        raise NotImplementedError
    
    def overload(func: _F) -> _F:
        return _overload_inner
__all__: Final = ('final', 'overload')


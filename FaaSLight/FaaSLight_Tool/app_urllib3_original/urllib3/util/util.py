from __future__ import annotations
import typing
from types import TracebackType

def to_bytes(x: str | bytes, encoding: str | None = None, errors: str | None = None) -> bytes:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.util.to_bytes', 'to_bytes(x, encoding=None, errors=None)', {'x': x, 'encoding': encoding, 'errors': errors, 'str': str, 'bytes': bytes, 'str': str, 'str': str}, 1)

def to_str(x: str | bytes, encoding: str | None = None, errors: str | None = None) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.util.to_str', 'to_str(x, encoding=None, errors=None)', {'x': x, 'encoding': encoding, 'errors': errors, 'str': str, 'bytes': bytes, 'str': str, 'str': str}, 1)

def reraise(tp: type[BaseException] | None, value: BaseException, tb: TracebackType | None = None) -> typing.NoReturn:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.util.util.reraise', 'reraise(tp, value, tb=None)', {'tp': tp, 'value': value, 'tb': tb, 'type': type, 'BaseException': BaseException, 'TracebackType': TracebackType, 'typing': typing}, 0)


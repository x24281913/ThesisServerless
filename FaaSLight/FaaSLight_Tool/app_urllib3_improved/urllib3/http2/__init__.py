from __future__ import annotations
from importlib.metadata import version
__all__ = ['inject_into_urllib3', 'extract_from_urllib3']
import typing
orig_HTTPSConnection: typing.Any = None

def inject_into_urllib3() -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.http2.__init__.inject_into_urllib3', 'inject_into_urllib3()', {'version': version}, 0)

def extract_from_urllib3() -> None:
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.http2.__init__.extract_from_urllib3', 'extract_from_urllib3()', {'orig_HTTPSConnection': orig_HTTPSConnection}, 0)


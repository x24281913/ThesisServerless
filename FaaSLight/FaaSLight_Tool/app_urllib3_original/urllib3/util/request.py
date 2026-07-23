from __future__ import annotations
import io
import sys
import typing
from base64 import b64encode
from enum import Enum
from ..exceptions import UnrewindableBodyError
from .util import to_bytes
if typing.TYPE_CHECKING:
    from typing import Final
SKIP_HEADER = '@@@SKIP_HEADER@@@'
SKIPPABLE_HEADERS = frozenset(['accept-encoding', 'host', 'user-agent'])
ACCEPT_ENCODING = 'gzip,deflate'
try:
    try:
        import brotlicffi as _unused_module_brotli
    except ImportError:
        import brotli as _unused_module_brotli
except ImportError:
    pass
else:
    ACCEPT_ENCODING += ',br'
try:
    if sys.version_info >= (3, 14):
        from compression import zstd as _unused_module_zstd
    else:
        from backports import zstd as _unused_module_zstd
except ImportError:
    pass
else:
    ACCEPT_ENCODING += ',zstd'


class _TYPE_FAILEDTELL(Enum):
    token = 0

_FAILEDTELL: Final[_TYPE_FAILEDTELL] = _TYPE_FAILEDTELL.token
_TYPE_BODY_POSITION = typing.Union[(int, _TYPE_FAILEDTELL)]
_METHODS_NOT_EXPECTING_BODY = {'GET', 'HEAD', 'DELETE', 'TRACE', 'OPTIONS', 'CONNECT'}

def make_headers(keep_alive: bool | None = None, accept_encoding: bool | list[str] | str | None = None, user_agent: str | None = None, basic_auth: str | None = None, proxy_basic_auth: str | None = None, disable_cache: bool | None = None) -> dict[(str, str)]:
    """
    Shortcuts for generating request headers.

    :param keep_alive:
        If ``True``, adds 'connection: keep-alive' header.

    :param accept_encoding:
        Can be a boolean, list, or string.
        ``True`` translates to 'gzip,deflate'.  If the dependencies for
        Brotli (either the ``brotli`` or ``brotlicffi`` package) and/or
        Zstandard (the ``backports.zstd`` package for Python before 3.14)
        algorithms are installed, then their encodings are
        included in the string ('br' and 'zstd', respectively).
        List will get joined by comma.
        String will be used as provided.

    :param user_agent:
        String representing the user-agent you want, such as
        "python-urllib3/0.6"

    :param basic_auth:
        Colon-separated username:password string for 'authorization: basic ...'
        auth header.

    :param proxy_basic_auth:
        Colon-separated username:password string for 'proxy-authorization: basic ...'
        auth header.

    :param disable_cache:
        If ``True``, adds 'cache-control: no-cache' header.

    Example:

    .. code-block:: python

        import urllib3

        print(urllib3.util.make_headers(keep_alive=True, user_agent="Batman/1.0"))
        # {'connection': 'keep-alive', 'user-agent': 'Batman/1.0'}
        print(urllib3.util.make_headers(accept_encoding=True))
        # {'accept-encoding': 'gzip,deflate'}
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.request.make_headers', 'make_headers(keep_alive=None, accept_encoding=None, user_agent=None, basic_auth=None, proxy_basic_auth=None, disable_cache=None)', {'ACCEPT_ENCODING': ACCEPT_ENCODING, 'b64encode': b64encode, 'keep_alive': keep_alive, 'accept_encoding': accept_encoding, 'user_agent': user_agent, 'basic_auth': basic_auth, 'proxy_basic_auth': proxy_basic_auth, 'disable_cache': disable_cache, 'bool': bool, 'str': str, 'str': str, 'str': str, 'str': str, 'bool': bool, 'dict': dict, 'str': str, 'str': str}, 1)

def set_file_position(body: typing.Any, pos: _TYPE_BODY_POSITION | None) -> _TYPE_BODY_POSITION | None:
    """
    If a position is provided, move file to that point.
    Otherwise, we'll attempt to record a position for future use.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.request.set_file_position', 'set_file_position(body, pos)', {'rewind_body': rewind_body, '_FAILEDTELL': _FAILEDTELL, 'body': body, 'pos': pos, 'typing': typing, '_TYPE_BODY_POSITION': _TYPE_BODY_POSITION, '_TYPE_BODY_POSITION': _TYPE_BODY_POSITION}, 1)

def rewind_body(body: typing.IO[typing.AnyStr], body_pos: _TYPE_BODY_POSITION) -> None:
    """
    Attempt to rewind body to a certain position.
    Primarily used for request redirects and retries.

    :param body:
        File-like object that supports seek.

    :param int pos:
        Position to seek to in file.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.util.request.rewind_body', 'rewind_body(body, body_pos)', {'UnrewindableBodyError': UnrewindableBodyError, '_FAILEDTELL': _FAILEDTELL, 'body': body, 'body_pos': body_pos, 'typing': typing, 'typing': typing}, 0)


class ChunksAndContentLength(typing.NamedTuple):
    chunks: typing.Iterable[bytes] | None
    content_length: int | None


def body_to_chunks(body: typing.Any | None, method: str, blocksize: int) -> ChunksAndContentLength:
    """Takes the HTTP request method, body, and blocksize and
    transforms them into an iterable of chunks to pass to
    socket.sendall() and an optional 'Content-Length' header.

    A 'Content-Length' of 'None' indicates the length of the body
    can't be determined so should use 'Transfer-Encoding: chunked'
    for framing instead.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.request.body_to_chunks', 'body_to_chunks(body, method, blocksize)', {'typing': typing, '_METHODS_NOT_EXPECTING_BODY': _METHODS_NOT_EXPECTING_BODY, 'io': io, 'ChunksAndContentLength': ChunksAndContentLength, 'body': body, 'method': method, 'blocksize': blocksize, 'typing': typing}, 1)


from __future__ import annotations
import socket
import typing
from ..exceptions import LocationParseError
from .timeout import _DEFAULT_TIMEOUT, _TYPE_TIMEOUT
_TYPE_SOCKET_OPTIONS = list[tuple[(int, int, typing.Union[(int, bytes)])]]
if typing.TYPE_CHECKING:
    from .._base_connection import BaseHTTPConnection

def is_connection_dropped(conn: BaseHTTPConnection) -> bool:
    """
    Returns True if the connection is dropped and should be closed.
    :param conn: :class:`urllib3.connection.HTTPConnection` object.
    """
    return not conn.is_connected

def create_connection(address: tuple[(str, int)], timeout: _TYPE_TIMEOUT = _DEFAULT_TIMEOUT, source_address: tuple[(str, int)] | None = None, socket_options: _TYPE_SOCKET_OPTIONS | None = None) -> socket.socket:
    """Connect to *address* and return the socket object.

    Convenience function.  Connect to *address* (a 2-tuple ``(host,
    port)``) and return the socket object.  Passing the optional
    *timeout* parameter will set the timeout on the socket instance
    before attempting to connect.  If no *timeout* is supplied, the
    global default timeout setting returned by :func:`socket.getdefaulttimeout`
    is used.  If *source_address* is set it must be a tuple of (host, port)
    for the socket to bind as a source address before making the connection.
    An host of '' or port 0 tells the OS to use the default.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.connection.create_connection', 'create_connection(address, timeout=_DEFAULT_TIMEOUT, source_address=None, socket_options=None)', {'allowed_gai_family': allowed_gai_family, 'LocationParseError': LocationParseError, 'socket': socket, '_set_socket_options': _set_socket_options, 'address': address, 'timeout': timeout, 'source_address': source_address, 'socket_options': socket_options, '_DEFAULT_TIMEOUT': _DEFAULT_TIMEOUT, 'tuple': tuple, 'str': str, 'int': int, 'tuple': tuple, '_TYPE_SOCKET_OPTIONS': _TYPE_SOCKET_OPTIONS, 'socket': socket}, 1)

def _set_socket_options(sock: socket.socket, options: _TYPE_SOCKET_OPTIONS | None) -> None:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.connection._set_socket_options', '_set_socket_options(sock, options)', {'sock': sock, 'options': options, 'socket': socket, '_TYPE_SOCKET_OPTIONS': _TYPE_SOCKET_OPTIONS}, 1)

def allowed_gai_family() -> socket.AddressFamily:
    """This function is designed to work in the context of
    getaddrinfo, where family=socket.AF_UNSPEC is the default and
    will perform a DNS search for both IPv6 and IPv4 records."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.connection.allowed_gai_family', 'allowed_gai_family()', {'socket': socket, 'HAS_IPV6': HAS_IPV6, 'socket': socket}, 1)

def _has_ipv6(host: str) -> bool:
    """Returns True if the system can bind an IPv6 address."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.connection._has_ipv6', '_has_ipv6(host)', {'socket': socket, 'host': host}, 1)
HAS_IPV6 = _has_ipv6('::1')


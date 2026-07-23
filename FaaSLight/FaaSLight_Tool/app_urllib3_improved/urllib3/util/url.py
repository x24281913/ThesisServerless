from __future__ import annotations
import re
import typing
from ..exceptions import LocationParseError
from .util import to_str
_NORMALIZABLE_SCHEMES = ('http', 'https', None)
_PERCENT_RE = re.compile('%[a-fA-F0-9]{2}')
_SCHEME_RE = re.compile('^(?:[a-zA-Z][a-zA-Z0-9+-]*:|/)')
_URI_RE = re.compile('^(?:([a-zA-Z][a-zA-Z0-9+.-]*):)?(?://([^\\\\/?#]*))?([^?#]*)(?:\\?([^#]*))?(?:#(.*))?$', re.UNICODE | re.DOTALL)
_IPV4_PAT = '(?:[0-9]{1,3}\\.){3}[0-9]{1,3}'
_HEX_PAT = '[0-9A-Fa-f]{1,4}'
_LS32_PAT = '(?:{hex}:{hex}|{ipv4})'.format(hex=_HEX_PAT, ipv4=_IPV4_PAT)
_subs = {'hex': _HEX_PAT, 'ls32': _LS32_PAT}
_variations = ['(?:%(hex)s:){6}%(ls32)s', '::(?:%(hex)s:){5}%(ls32)s', '(?:%(hex)s)?::(?:%(hex)s:){4}%(ls32)s', '(?:(?:%(hex)s:)?%(hex)s)?::(?:%(hex)s:){3}%(ls32)s', '(?:(?:%(hex)s:){0,2}%(hex)s)?::(?:%(hex)s:){2}%(ls32)s', '(?:(?:%(hex)s:){0,3}%(hex)s)?::%(hex)s:%(ls32)s', '(?:(?:%(hex)s:){0,4}%(hex)s)?::%(ls32)s', '(?:(?:%(hex)s:){0,5}%(hex)s)?::%(hex)s', '(?:(?:%(hex)s:){0,6}%(hex)s)?::']
_UNRESERVED_PAT = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._\\-~'
_IPV6_PAT = '(?:' + '|'.join([x % _subs for x in _variations]) + ')'
_ZONE_ID_PAT = '(?:%25|%)(?:[' + _UNRESERVED_PAT + ']|%[a-fA-F0-9]{2})+'
_IPV6_ADDRZ_PAT = '\\[' + _IPV6_PAT + '(?:' + _ZONE_ID_PAT + ')?\\]'
_REG_NAME_PAT = '(?:[^\\[\\]%:/?#]|%[a-fA-F0-9]{2})*'
_TARGET_RE = re.compile('^(/[^?#]*)(?:\\?([^#]*))?(?:#.*)?$')
_IPV4_RE = re.compile('^' + _IPV4_PAT + '$')
_IPV6_RE = re.compile('^' + _IPV6_PAT + '$')
_IPV6_ADDRZ_RE = re.compile('^' + _IPV6_ADDRZ_PAT + '$')
_BRACELESS_IPV6_ADDRZ_RE = re.compile('^' + _IPV6_ADDRZ_PAT[2:-2] + '$')
_ZONE_ID_RE = re.compile('(' + _ZONE_ID_PAT + ')\\]$')
_HOST_PORT_PAT = '^(%s|%s|%s)(?::0*?(|0|[1-9][0-9]{0,4}))?$' % (_REG_NAME_PAT, _IPV4_PAT, _IPV6_ADDRZ_PAT)
_HOST_PORT_RE = re.compile(_HOST_PORT_PAT, re.UNICODE | re.DOTALL)
_UNRESERVED_CHARS = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-~')
_SUB_DELIM_CHARS = set("!$&'()*+,;=")
_USERINFO_CHARS = _UNRESERVED_CHARS | _SUB_DELIM_CHARS | {':'}
_PATH_CHARS = _USERINFO_CHARS | {'@', '/'}
_QUERY_CHARS = _FRAGMENT_CHARS = _PATH_CHARS | {'?'}


class Url(typing.NamedTuple('Url', [('scheme', typing.Optional[str]), ('auth', typing.Optional[str]), ('host', typing.Optional[str]), ('port', typing.Optional[int]), ('path', typing.Optional[str]), ('query', typing.Optional[str]), ('fragment', typing.Optional[str])])):
    """
    Data structure for representing an HTTP URL. Used as a return value for
    :func:`parse_url`. Both the scheme and host are normalized as they are
    both case-insensitive according to RFC 3986.
    """
    
    def __new__(cls, scheme: str | None = None, auth: str | None = None, host: str | None = None, port: int | None = None, path: str | None = None, query: str | None = None, fragment: str | None = None):
        if (path and not path.startswith('/')):
            path = '/' + path
        if scheme is not None:
            scheme = scheme.lower()
        return super().__new__(cls, scheme, auth, host, port, path, query, fragment)
    
    @property
    def hostname(self) -> str | None:
        """For backwards-compatibility with urlparse. We're nice like that."""
        return self.host
    
    @property
    def request_uri(self) -> str:
        """Absolute path including the query string."""
        uri = (self.path or '/')
        if self.query is not None:
            uri += '?' + self.query
        return uri
    
    @property
    def authority(self) -> str | None:
        """
        Authority component as defined in RFC 3986 3.2.
        This includes userinfo (auth), host and port.

        i.e.
            userinfo@host:port
        """
        userinfo = self.auth
        netloc = self.netloc
        if (netloc is None or userinfo is None):
            return netloc
        else:
            return f'{userinfo}@{netloc}'
    
    @property
    def netloc(self) -> str | None:
        """
        Network location including host and port.

        If you need the equivalent of urllib.parse's ``netloc``,
        use the ``authority`` property instead.
        """
        if self.host is None:
            return None
        if self.port:
            return f'{self.host}:{self.port}'
        return self.host
    
    @property
    def url(self) -> str:
        """
        Convert self into a url

        This function should more or less round-trip with :func:`.parse_url`. The
        returned url may not be exactly the same as the url inputted to
        :func:`.parse_url`, but it should be equivalent by the RFC (e.g., urls
        with a blank port will have : removed).

        Example:

        .. code-block:: python

            import urllib3

            U = urllib3.util.parse_url("https://google.com/mail/")

            print(U.url)
            # "https://google.com/mail/"

            print( urllib3.util.Url("https", "username:password",
                                    "host.com", 80, "/path", "query", "fragment"
                                    ).url
                )
            # "https://username:password@host.com:80/path?query#fragment"
        """
        (scheme, auth, host, port, path, query, fragment) = self
        url = ''
        if scheme is not None:
            url += scheme + '://'
        if auth is not None:
            url += auth + '@'
        if host is not None:
            url += host
        if port is not None:
            url += ':' + str(port)
        if path is not None:
            url += path
        if query is not None:
            url += '?' + query
        if fragment is not None:
            url += '#' + fragment
        return url
    
    def __str__(self) -> str:
        return self.url


@typing.overload
def _encode_invalid_chars(component: str, allowed_chars: typing.Container[str]) -> str:
    ...

@typing.overload
def _encode_invalid_chars(component: None, allowed_chars: typing.Container[str]) -> None:
    ...

def _encode_invalid_chars(component: str | None, allowed_chars: typing.Container[str]) -> str | None:
    """Percent-encodes a URI component without reapplying
    onto an already percent-encoded component.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.url._encode_invalid_chars', '_encode_invalid_chars(component, allowed_chars)', {'to_str': to_str, '_PERCENT_RE': _PERCENT_RE, 'component': component, 'allowed_chars': allowed_chars, 'str': str, 'typing': typing, 'str': str, 'str': str}, 1)

def _remove_path_dot_segments(path: str) -> str:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.url._remove_path_dot_segments', '_remove_path_dot_segments(path)', {'path': path}, 1)

@typing.overload
def _normalize_host(host: None, scheme: str | None) -> None:
    ...

@typing.overload
def _normalize_host(host: str, scheme: str | None) -> str:
    ...

def _normalize_host(host: str | None, scheme: str | None) -> str | None:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.url._normalize_host', '_normalize_host(host, scheme)', {'_NORMALIZABLE_SCHEMES': _NORMALIZABLE_SCHEMES, '_IPV6_ADDRZ_RE': _IPV6_ADDRZ_RE, '_ZONE_ID_RE': _ZONE_ID_RE, '_encode_invalid_chars': _encode_invalid_chars, '_UNRESERVED_CHARS': _UNRESERVED_CHARS, '_IPV4_RE': _IPV4_RE, 'to_str': to_str, '_idna_encode': _idna_encode, 'host': host, 'scheme': scheme, 'str': str, 'str': str, 'str': str}, 1)

def _idna_encode(name: str) -> bytes:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.url._idna_encode', '_idna_encode(name)', {'LocationParseError': LocationParseError, 'name': name}, 1)

def _encode_target(target: str) -> str:
    """Percent-encodes a request target so that there are no invalid characters

    Pre-condition for this function is that 'target' must start with '/'.
    If that is the case then _TARGET_RE will always produce a match.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.url._encode_target', '_encode_target(target)', {'_TARGET_RE': _TARGET_RE, 'LocationParseError': LocationParseError, '_encode_invalid_chars': _encode_invalid_chars, '_PATH_CHARS': _PATH_CHARS, '_QUERY_CHARS': _QUERY_CHARS, 'target': target}, 1)

def parse_url(url: str) -> Url:
    """
    Given a url, return a parsed :class:`.Url` namedtuple. Best-effort is
    performed to parse incomplete urls. Fields not provided will be None.
    This parser is RFC 3986 and RFC 6874 compliant.

    The parser logic and helper functions are based heavily on
    work done in the ``rfc3986`` module.

    :param str url: URL to parse into a :class:`.Url` namedtuple.

    Partly backwards-compatible with :mod:`urllib.parse`.

    Example:

    .. code-block:: python

        import urllib3

        print( urllib3.util.parse_url('http://google.com/mail/'))
        # Url(scheme='http', host='google.com', port=None, path='/mail/', ...)

        print( urllib3.util.parse_url('google.com:80'))
        # Url(scheme=None, host='google.com', port=80, path=None, ...)

        print( urllib3.util.parse_url('/foo?bar'))
        # Url(scheme=None, host=None, port=None, path='/foo', query='bar', ...)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.url.parse_url', 'parse_url(url)', {'Url': Url, '_SCHEME_RE': _SCHEME_RE, '_URI_RE': _URI_RE, '_NORMALIZABLE_SCHEMES': _NORMALIZABLE_SCHEMES, '_HOST_PORT_RE': _HOST_PORT_RE, '_encode_invalid_chars': _encode_invalid_chars, '_USERINFO_CHARS': _USERINFO_CHARS, 'LocationParseError': LocationParseError, '_normalize_host': _normalize_host, '_remove_path_dot_segments': _remove_path_dot_segments, '_PATH_CHARS': _PATH_CHARS, '_QUERY_CHARS': _QUERY_CHARS, '_FRAGMENT_CHARS': _FRAGMENT_CHARS, 'url': url}, 1)


"""
requests.utils
~~~~~~~~~~~~~~

This module provides utility functions that are used within Requests
that are also useful for external consumption.
"""

import codecs
import contextlib
import io
import os
import re
import socket
import struct
import sys
import tempfile
import warnings
import zipfile
from collections import OrderedDict
from urllib3.util import make_headers, parse_url
from . import certs
from .__version__ import __version__
from ._internal_utils import _HEADER_VALIDATORS_BYTE, _HEADER_VALIDATORS_STR, HEADER_VALIDATORS, to_native_string
from .compat import Mapping, basestring, bytes, getproxies, getproxies_environment, integer_types, is_urllib3_1
from .compat import parse_http_list as _parse_list_header
from .compat import proxy_bypass, proxy_bypass_environment, quote, str, unquote, urlparse, urlunparse
from .cookies import cookiejar_from_dict
from .exceptions import FileModeWarning, InvalidHeader, InvalidURL, UnrewindableBodyError
from .structures import CaseInsensitiveDict
NETRC_FILES = ('.netrc', '_netrc')
DEFAULT_CA_BUNDLE_PATH = certs.where()
DEFAULT_PORTS = {'http': 80, 'https': 443}
DEFAULT_ACCEPT_ENCODING = ', '.join(re.split(',\\s*', make_headers(accept_encoding=True)['accept-encoding']))
if sys.platform == 'win32':
    
    def proxy_bypass_registry(host):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('requests.utils.proxy_bypass_registry', 'proxy_bypass_registry(host)', {'re': re, 'host': host}, 1)
    
    def proxy_bypass(host):
        """Return True, if the host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.
        """
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('requests.utils.proxy_bypass', 'proxy_bypass(host)', {'getproxies_environment': getproxies_environment, 'proxy_bypass_environment': proxy_bypass_environment, 'proxy_bypass_registry': proxy_bypass_registry, 'host': host}, 1)

def dict_to_sequence(d):
    """Returns an internal sequence dictionary update."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.dict_to_sequence', 'dict_to_sequence(d)', {'d': d}, 1)

def super_len(o):
    total_length = None
    current_position = 0
    if (not is_urllib3_1 and isinstance(o, str)):
        o = o.encode('utf-8')
    if hasattr(o, '__len__'):
        total_length = len(o)
    elif hasattr(o, 'len'):
        total_length = o.len
    elif hasattr(o, 'fileno'):
        try:
            fileno = o.fileno()
        except (io.UnsupportedOperation, AttributeError):
            pass
        else:
            total_length = os.fstat(fileno).st_size
            if 'b' not in o.mode:
                warnings.warn("Requests has determined the content-length for this request using the binary size of the file: however, the file has been opened in text mode (i.e. without the 'b' flag in the mode). This may lead to an incorrect content-length. In Requests 3.0, support will be removed for files in text mode.", FileModeWarning)
    if hasattr(o, 'tell'):
        try:
            current_position = o.tell()
        except OSError:
            if total_length is not None:
                current_position = total_length
        else:
            if (hasattr(o, 'seek') and total_length is None):
                try:
                    o.seek(0, 2)
                    total_length = o.tell()
                    o.seek((current_position or 0))
                except OSError:
                    total_length = 0
    if total_length is None:
        total_length = 0
    return max(0, total_length - current_position)

def get_netrc_auth(url, raise_errors=False):
    """Returns the Requests tuple auth for a given url from netrc."""
    netrc_file = os.environ.get('NETRC')
    if netrc_file is not None:
        netrc_locations = (netrc_file, )
    else:
        netrc_locations = (f'~/{f}' for f in NETRC_FILES)
    try:
        from netrc import NetrcParseError, netrc
        netrc_path = None
        for f in netrc_locations:
            loc = os.path.expanduser(f)
            if os.path.exists(loc):
                netrc_path = loc
                break
        if netrc_path is None:
            return
        ri = urlparse(url)
        host = ri.hostname
        try:
            _netrc = netrc(netrc_path).authenticators(host)
            if _netrc:
                login_i = (0 if _netrc[0] else 1)
                return (_netrc[login_i], _netrc[2])
        except (NetrcParseError, OSError):
            if raise_errors:
                raise
    except (ImportError, AttributeError):
        pass

def guess_filename(obj):
    """Tries to guess the filename of the given object."""
    name = getattr(obj, 'name', None)
    if (name and isinstance(name, basestring) and name[0] != '<' and name[-1] != '>'):
        return os.path.basename(name)

def extract_zipped_paths(path):
    """Replace nonexistent paths that look like they refer to a member of a zip
    archive with the location of an extracted copy of the target, or else
    just return the provided path unchanged.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.extract_zipped_paths', 'extract_zipped_paths(path)', {'os': os, 'zipfile': zipfile, 'tempfile': tempfile, 'atomic_open': atomic_open, 'path': path}, 1)

@contextlib.contextmanager
def atomic_open(filename):
    """Write a file to the disk in an atomic fashion"""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('requests.utils.atomic_open', 'atomic_open(filename)', {'tempfile': tempfile, 'os': os, 'contextlib': contextlib, 'filename': filename}, 0)

def from_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. Unless it can not be represented as such, return an
    OrderedDict, e.g.,

    ::

        >>> from_key_val_list([('key', 'val')])
        OrderedDict([('key', 'val')])
        >>> from_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples
        >>> from_key_val_list({'key': 'val'})
        OrderedDict([('key', 'val')])

    :rtype: OrderedDict
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.from_key_val_list', 'from_key_val_list(value)', {'OrderedDict': OrderedDict, 'value': value}, 1)

def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        Traceback (most recent call last):
        ...
        ValueError: cannot encode objects that are not 2-tuples

    :rtype: list
    """
    if value is None:
        return None
    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')
    if isinstance(value, Mapping):
        value = value.items()
    return list(value)

def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    :rtype: list
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.parse_list_header', 'parse_list_header(value)', {'_parse_list_header': _parse_list_header, 'unquote_header_value': unquote_header_value, 'value': value}, 1)

def parse_dict_header(value):
    """Parse lists of key, value pairs as described by RFC 2068 Section 2 and
    convert them into a python dict:

    >>> d = parse_dict_header('foo="is a fish", bar="as well"')
    >>> type(d) is dict
    True
    >>> sorted(d.items())
    [('bar', 'as well'), ('foo', 'is a fish')]

    If there is no value for a key it will be `None`:

    >>> parse_dict_header('key_without_value')
    {'key_without_value': None}

    To create a header from the :class:`dict` again, use the
    :func:`dump_header` function.

    :param value: a string with a dict header.
    :return: :class:`dict`
    :rtype: dict
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.parse_dict_header', 'parse_dict_header(value)', {'_parse_list_header': _parse_list_header, 'unquote_header_value': unquote_header_value, 'value': value}, 1)

def unquote_header_value(value, is_filename=False):
    """Unquotes a header value.  (Reversal of :func:`quote_header_value`).
    This does not use the real unquoting but what browsers are actually
    using for quoting.

    :param value: the header value to unquote.
    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.unquote_header_value', 'unquote_header_value(value, is_filename=False)', {'value': value, 'is_filename': is_filename}, 1)

def dict_from_cookiejar(cj):
    """Returns a key/value dictionary from a CookieJar.

    :param cj: CookieJar object to extract cookies from.
    :rtype: dict
    """
    cookie_dict = {cookie.name: cookie.value for cookie in cj}
    return cookie_dict

def add_dict_to_cookiejar(cj, cookie_dict):
    """Returns a CookieJar from a key/value dictionary.

    :param cj: CookieJar to insert cookies into.
    :param cookie_dict: Dict of key/values to insert into CookieJar.
    :rtype: CookieJar
    """
    return cookiejar_from_dict(cookie_dict, cj)

def get_encodings_from_content(content):
    """Returns encodings from given content string.

    :param content: bytestring to extract encodings from.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.get_encodings_from_content', 'get_encodings_from_content(content)', {'warnings': warnings, 're': re, 'content': content}, 1)

def _parse_content_type_header(header):
    """Returns content type and parameters from given header

    :param header: string
    :return: tuple containing content type and dictionary of
         parameters
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils._parse_content_type_header', '_parse_content_type_header(header)', {'header': header}, 2)

def get_encoding_from_headers(headers):
    """Returns encodings from given HTTP Header Dict.

    :param headers: dictionary to extract encoding from.
    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.get_encoding_from_headers', 'get_encoding_from_headers(headers)', {'_parse_content_type_header': _parse_content_type_header, 'headers': headers}, 1)

def stream_decode_response_unicode(iterator, r):
    """Stream decodes an iterator."""
    if r.encoding is None:
        yield from iterator
        return
    decoder = codecs.getincrementaldecoder(r.encoding)(errors='replace')
    for chunk in iterator:
        rv = decoder.decode(chunk)
        if rv:
            yield rv
    rv = decoder.decode(b'', final=True)
    if rv:
        yield rv

def iter_slices(string, slice_length):
    """Iterate over slices of a string."""
    pos = 0
    if (slice_length is None or slice_length <= 0):
        slice_length = len(string)
    while pos < len(string):
        yield string[pos:pos + slice_length]
        pos += slice_length

def get_unicode_from_response(r):
    """Returns the requested content back in unicode.

    :param r: Response object to get unicode content from.

    Tried:

    1. charset from content-type
    2. fall back and replace all unicode characters

    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.get_unicode_from_response', 'get_unicode_from_response(r)', {'warnings': warnings, 'get_encoding_from_headers': get_encoding_from_headers, 'r': r}, 1)
UNRESERVED_SET = frozenset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' + '0123456789-._~')

def unquote_unreserved(uri):
    """Un-escape any percent-escape sequences in a URI that are unreserved
    characters. This leaves all reserved, illegal and non-ASCII bytes encoded.

    :rtype: str
    """
    parts = uri.split('%')
    for i in range(1, len(parts)):
        h = parts[i][0:2]
        if (len(h) == 2 and h.isalnum()):
            try:
                c = chr(int(h, 16))
            except ValueError:
                raise InvalidURL(f"Invalid percent-escape sequence: '{h}'")
            if c in UNRESERVED_SET:
                parts[i] = c + parts[i][2:]
            else:
                parts[i] = f'%{parts[i]}'
        else:
            parts[i] = f'%{parts[i]}'
    return ''.join(parts)

def requote_uri(uri):
    """Re-quote the given URI.

    This function passes the given URI through an unquote/quote cycle to
    ensure that it is fully and consistently quoted.

    :rtype: str
    """
    safe_with_percent = "!#$%&'()*+,/:;=?@[]~"
    safe_without_percent = "!#$&'()*+,/:;=?@[]~"
    try:
        return quote(unquote_unreserved(uri), safe=safe_with_percent)
    except InvalidURL:
        return quote(uri, safe=safe_without_percent)

def address_in_network(ip, net):
    """This function allows you to check if an IP belongs to a network subnet

    Example: returns True if ip = 192.168.1.1 and net = 192.168.1.0/24
             returns False if ip = 192.168.1.1 and net = 192.168.100.0/24

    :rtype: bool
    """
    ipaddr = struct.unpack('=L', socket.inet_aton(ip))[0]
    (netaddr, bits) = net.split('/')
    netmask = struct.unpack('=L', socket.inet_aton(dotted_netmask(int(bits))))[0]
    network = struct.unpack('=L', socket.inet_aton(netaddr))[0] & netmask
    return ipaddr & netmask == network & netmask

def dotted_netmask(mask):
    """Converts mask from /xx format to xxx.xxx.xxx.xxx

    Example: if mask is 24 function returns 255.255.255.0

    :rtype: str
    """
    bits = 4294967295 ^ (1 << 32 - mask) - 1
    return socket.inet_ntoa(struct.pack('>I', bits))

def is_ipv4_address(string_ip):
    """
    :rtype: bool
    """
    try:
        socket.inet_aton(string_ip)
    except OSError:
        return False
    return True

def is_valid_cidr(string_network):
    """
    Very simple check of the cidr format in no_proxy variable.

    :rtype: bool
    """
    if string_network.count('/') == 1:
        try:
            mask = int(string_network.split('/')[1])
        except ValueError:
            return False
        if (mask < 1 or mask > 32):
            return False
        try:
            socket.inet_aton(string_network.split('/')[0])
        except OSError:
            return False
    else:
        return False
    return True

@contextlib.contextmanager
def set_environ(env_name, value):
    """Set the environment variable 'env_name' to 'value'

    Save previous value, yield, and then restore the previous value stored in
    the environment variable 'env_name'.

    If 'value' is None, do nothing"""
    value_changed = value is not None
    if value_changed:
        old_value = os.environ.get(env_name)
        os.environ[env_name] = value
    try:
        yield
    finally:
        if value_changed:
            if old_value is None:
                del os.environ[env_name]
            else:
                os.environ[env_name] = old_value

def should_bypass_proxies(url, no_proxy):
    """
    Returns whether we should bypass proxies or not.

    :rtype: bool
    """
    
    def get_proxy(key):
        return (os.environ.get(key) or os.environ.get(key.upper()))
    no_proxy_arg = no_proxy
    if no_proxy is None:
        no_proxy = get_proxy('no_proxy')
    parsed = urlparse(url)
    if parsed.hostname is None:
        return True
    if no_proxy:
        no_proxy = (host for host in no_proxy.replace(' ', '').split(',') if host)
        if is_ipv4_address(parsed.hostname):
            for proxy_ip in no_proxy:
                if is_valid_cidr(proxy_ip):
                    if address_in_network(parsed.hostname, proxy_ip):
                        return True
                elif parsed.hostname == proxy_ip:
                    return True
        else:
            host_with_port = parsed.hostname
            if parsed.port:
                host_with_port += f':{parsed.port}'
            for host in no_proxy:
                if (parsed.hostname.endswith(host) or host_with_port.endswith(host)):
                    return True
    with set_environ('no_proxy', no_proxy_arg):
        try:
            bypass = proxy_bypass(parsed.hostname)
        except (TypeError, socket.gaierror):
            bypass = False
    if bypass:
        return True
    return False

def get_environ_proxies(url, no_proxy=None):
    """
    Return a dict of environment proxies.

    :rtype: dict
    """
    if should_bypass_proxies(url, no_proxy=no_proxy):
        return {}
    else:
        return getproxies()

def select_proxy(url, proxies):
    """Select a proxy for the url, if applicable.

    :param url: The url being for the request
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.select_proxy', 'select_proxy(url, proxies)', {'urlparse': urlparse, 'url': url, 'proxies': proxies}, 1)

def resolve_proxies(request, proxies, trust_env=True):
    """This method takes proxy information from a request and configuration
    input to resolve a mapping of target proxies. This will consider settings
    such as NO_PROXY to strip proxy configurations.

    :param request: Request or PreparedRequest
    :param proxies: A dictionary of schemes or schemes and hosts to proxy URLs
    :param trust_env: Boolean declaring whether to trust environment configs

    :rtype: dict
    """
    proxies = (proxies if proxies is not None else {})
    url = request.url
    scheme = urlparse(url).scheme
    no_proxy = proxies.get('no_proxy')
    new_proxies = proxies.copy()
    if (trust_env and not should_bypass_proxies(url, no_proxy=no_proxy)):
        environ_proxies = get_environ_proxies(url, no_proxy=no_proxy)
        proxy = environ_proxies.get(scheme, environ_proxies.get('all'))
        if proxy:
            new_proxies.setdefault(scheme, proxy)
    return new_proxies

def default_user_agent(name='python-requests'):
    """
    Return a string representing the default user agent.

    :rtype: str
    """
    return f'{name}/{__version__}'

def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({'User-Agent': default_user_agent(), 'Accept-Encoding': DEFAULT_ACCEPT_ENCODING, 'Accept': '*/*', 'Connection': 'keep-alive'})

def parse_header_links(value):
    """Return a list of parsed link headers proxies.

    i.e. Link: <http:/.../front.jpeg>; rel=front; type="image/jpeg",<http://.../back.jpeg>; rel=back;type="image/jpeg"

    :rtype: list
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.parse_header_links', 'parse_header_links(value)', {'re': re, 'value': value}, 1)
_null = '\x00'.encode('ascii')
_null2 = _null * 2
_null3 = _null * 3

def guess_json_utf(data):
    """
    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.guess_json_utf', 'guess_json_utf(data)', {'codecs': codecs, '_null': _null, '_null2': _null2, '_null3': _null3, 'data': data}, 1)

def prepend_scheme_if_needed(url, new_scheme):
    """Given a URL that may or may not have a scheme, prepend the given scheme.
    Does not replace a present scheme with the one provided as an argument.

    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.prepend_scheme_if_needed', 'prepend_scheme_if_needed(url, new_scheme)', {'parse_url': parse_url, 'urlunparse': urlunparse, 'url': url, 'new_scheme': new_scheme}, 1)

def get_auth_from_url(url):
    """Given a url with authentication components, extract them into a tuple of
    username,password.

    :rtype: (str,str)
    """
    parsed = urlparse(url)
    try:
        auth = (unquote(parsed.username), unquote(parsed.password))
    except (AttributeError, TypeError):
        auth = ('', '')
    return auth

def check_header_validity(header):
    """Verifies that header parts don't contain leading whitespace
    reserved characters, or return characters.

    :param header: tuple, in the format (name, value).
    """
    (name, value) = header
    _validate_header_part(header, name, 0)
    _validate_header_part(header, value, 1)

def _validate_header_part(header, header_part, header_validator_index):
    if isinstance(header_part, str):
        validator = _HEADER_VALIDATORS_STR[header_validator_index]
    elif isinstance(header_part, bytes):
        validator = _HEADER_VALIDATORS_BYTE[header_validator_index]
    else:
        raise InvalidHeader(f'Header part ({header_part!r}) from {header} must be of type str or bytes, not {type(header_part)}')
    if not validator.match(header_part):
        header_kind = ('name' if header_validator_index == 0 else 'value')
        raise InvalidHeader(f'Invalid leading whitespace, reserved character(s), or return character(s) in header {header_kind}: {header_part!r}')

def urldefragauth(url):
    """
    Given a url remove the fragment and the authentication part.

    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('requests.utils.urldefragauth', 'urldefragauth(url)', {'urlparse': urlparse, 'urlunparse': urlunparse, 'url': url}, 1)

def rewind_body(prepared_request):
    """Move file pointer back to its recorded starting position
    so it can be read again on redirect.
    """
    body_seek = getattr(prepared_request.body, 'seek', None)
    if (body_seek is not None and isinstance(prepared_request._body_position, integer_types)):
        try:
            body_seek(prepared_request._body_position)
        except OSError:
            raise UnrewindableBodyError('An error occurred when rewinding request body for redirect.')
    else:
        raise UnrewindableBodyError('Unable to rewind request body for redirect.')


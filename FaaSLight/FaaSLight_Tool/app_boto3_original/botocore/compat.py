import copy
import datetime
import sys
import inspect
import warnings
import hashlib
from http.client import HTTPMessage
import logging
import shlex
import re
import os
from collections import OrderedDict
from collections.abc import MutableMapping
from math import floor
from botocore.vendored import six
from botocore.exceptions import MD5UnavailableError
from dateutil.tz import tzlocal
from urllib3 import exceptions
logger = logging.getLogger(__name__)


class HTTPHeaders(HTTPMessage):
    pass

from urllib.parse import quote, urlencode, unquote, unquote_plus, urlparse, urlsplit, urlunsplit, urljoin, parse_qsl, parse_qs
from http.client import HTTPResponse
from io import IOBase as _IOBase
from base64 import encodebytes
from email.utils import formatdate
from itertools import zip_longest
file_type = _IOBase
zip = zip
unquote_str = unquote_plus

def set_socket_timeout(http_response, timeout):
    """Set the timeout of the socket from an HTTPResponse.

    :param http_response: An instance of ``httplib.HTTPResponse``

    """
    http_response._fp.fp.raw._sock.settimeout(timeout)

def accepts_kwargs(func):
    return inspect.getfullargspec(func)[2]

def ensure_unicode(s, encoding=None, errors=None):
    return s

def ensure_bytes(s, encoding='utf-8', errors='strict'):
    if isinstance(s, str):
        return s.encode(encoding, errors)
    if isinstance(s, bytes):
        return s
    raise ValueError(f'Expected str or bytes, received {type(s)}.')
import xml.etree.ElementTree as ETree
XMLParseError = ETree.ParseError
import json

def filter_ssl_warnings():
    warnings.filterwarnings('ignore', message='A true SSLContext object is not available.*', category=exceptions.InsecurePlatformWarning, module='.*urllib3\\.util\\.ssl_')

@classmethod
def from_dict(cls, d):
    new_instance = cls()
    for (key, value) in d.items():
        new_instance[key] = value
    return new_instance

@classmethod
def from_pairs(cls, pairs):
    new_instance = cls()
    for (key, value) in pairs:
        new_instance[key] = value
    return new_instance
HTTPHeaders.from_dict = from_dict
HTTPHeaders.from_pairs = from_pairs

def copy_kwargs(kwargs):
    """
    This used to be a compat shim for 2.6 but is now just an alias.
    """
    copy_kwargs = copy.copy(kwargs)
    return copy_kwargs

def total_seconds(delta):
    """
    Returns the total seconds in a ``datetime.timedelta``.

    This used to be a compat shim for 2.6 but is now just an alias.

    :param delta: The timedelta object
    :type delta: ``datetime.timedelta``
    """
    return delta.total_seconds()
try:
    hashlib.md5(usedforsecurity=False)
    MD5_AVAILABLE = True
except (AttributeError, ValueError):
    MD5_AVAILABLE = False

def get_md5(*args, **kwargs):
    """
    Attempts to get an md5 hashing object.

    :param args: Args to pass to the MD5 constructor
    :param kwargs: Key word arguments to pass to the MD5 constructor
    :return: An MD5 hashing object if available. If it is unavailable, None
        is returned if raise_error_if_unavailable is set to False.
    """
    if MD5_AVAILABLE:
        return hashlib.md5(*args, **kwargs)
    else:
        raise MD5UnavailableError()

def compat_shell_split(s, platform=None):
    if platform is None:
        platform = sys.platform
    if platform == 'win32':
        return _windows_shell_split(s)
    else:
        return shlex.split(s)

def _windows_shell_split(s):
    """Splits up a windows command as the built-in command parser would.

    Windows has potentially bizarre rules depending on where you look. When
    spawning a process via the Windows C runtime (which is what python does
    when you call popen) the rules are as follows:

    https://docs.microsoft.com/en-us/cpp/cpp/parsing-cpp-command-line-arguments

    To summarize:

    * Only space and tab are valid delimiters
    * Double quotes are the only valid quotes
    * Backslash is interpreted literally unless it is part of a chain that
      leads up to a double quote. Then the backslashes escape the backslashes,
      and if there is an odd number the final backslash escapes the quote.

    :param s: The command string to split up into parts.
    :return: A list of command components.
    """
    if not s:
        return []
    components = []
    buff = []
    is_quoted = False
    num_backslashes = 0
    for character in s:
        if character == '\\':
            num_backslashes += 1
        elif character == '"':
            if num_backslashes > 0:
                buff.append('\\' * int(floor(num_backslashes / 2)))
                remainder = num_backslashes % 2
                num_backslashes = 0
                if remainder == 1:
                    buff.append('"')
                    continue
            is_quoted = not is_quoted
            buff.append('')
        elif (character in [' ', '\t'] and not is_quoted):
            if num_backslashes > 0:
                buff.append('\\' * num_backslashes)
                num_backslashes = 0
            if buff:
                components.append(''.join(buff))
                buff = []
        else:
            if num_backslashes > 0:
                buff.append('\\' * num_backslashes)
                num_backslashes = 0
            buff.append(character)
    if is_quoted:
        raise ValueError(f'No closing quotation in string: {s}')
    if num_backslashes > 0:
        buff.append('\\' * num_backslashes)
    if buff:
        components.append(''.join(buff))
    return components

def get_tzinfo_options():
    if sys.platform == 'win32':
        from dateutil.tz import tzwinlocal
        return (tzlocal, tzwinlocal)
    else:
        return (tzlocal, )
try:
    import awscrt.auth
    disabled = os.environ.get('BOTO_DISABLE_CRT', 'false')
    HAS_CRT = not disabled.lower() == 'true'
except ImportError:
    HAS_CRT = False

def has_minimum_crt_version(minimum_version):
    """Not intended for use outside botocore."""
    if not HAS_CRT:
        return False
    crt_version_str = awscrt.__version__
    try:
        crt_version_ints = map(int, crt_version_str.split('.'))
        crt_version_tuple = tuple(crt_version_ints)
    except (TypeError, ValueError):
        return False
    return crt_version_tuple >= minimum_version

def get_current_datetime(remove_tzinfo=True):
    """Retrieve the current timezone in UTC, with or without an explicit timezone."""
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    if remove_tzinfo:
        datetime_now = datetime_now.replace(tzinfo=None)
    return datetime_now
IPV4_PAT = '(?:[0-9]{1,3}\\.){3}[0-9]{1,3}'
IPV4_RE = re.compile('^' + IPV4_PAT + '$')
HEX_PAT = '[0-9A-Fa-f]{1,4}'
LS32_PAT = '(?:{hex}:{hex}|{ipv4})'.format(hex=HEX_PAT, ipv4=IPV4_PAT)
_subs = {'hex': HEX_PAT, 'ls32': LS32_PAT}
_variations = ['(?:%(hex)s:){6}%(ls32)s', '::(?:%(hex)s:){5}%(ls32)s', '(?:%(hex)s)?::(?:%(hex)s:){4}%(ls32)s', '(?:(?:%(hex)s:)?%(hex)s)?::(?:%(hex)s:){3}%(ls32)s', '(?:(?:%(hex)s:){0,2}%(hex)s)?::(?:%(hex)s:){2}%(ls32)s', '(?:(?:%(hex)s:){0,3}%(hex)s)?::%(hex)s:%(ls32)s', '(?:(?:%(hex)s:){0,4}%(hex)s)?::%(ls32)s', '(?:(?:%(hex)s:){0,5}%(hex)s)?::%(hex)s', '(?:(?:%(hex)s:){0,6}%(hex)s)?::']
UNRESERVED_PAT = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._!\\-~'
IPV6_PAT = '(?:' + '|'.join([x % _subs for x in _variations]) + ')'
ZONE_ID_PAT = '(?:%25|%)(?:[' + UNRESERVED_PAT + ']|%[a-fA-F0-9]{2})+'
IPV6_ADDRZ_PAT = '\\[' + IPV6_PAT + '(?:' + ZONE_ID_PAT + ')?\\]'
IPV6_ADDRZ_RE = re.compile('^' + IPV6_ADDRZ_PAT + '$')
UNSAFE_URL_CHARS = frozenset('\t\r\n')
try:
    import gzip
    HAS_GZIP = True
except ImportError:
    HAS_GZIP = False
if (HAS_CRT and has_minimum_crt_version((0, 28, 4))):
    from awscrt.crypto import EC
else:
    EC = None


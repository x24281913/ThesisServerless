from __future__ import annotations
import hashlib
import hmac
import os
import socket
import sys
import typing
import warnings
from binascii import unhexlify
from ..exceptions import ProxySchemeUnsupported, SSLError
from .url import _BRACELESS_IPV6_ADDRZ_RE, _IPV4_RE
SSLContext = None
SSLTransport = None
HAS_NEVER_CHECK_COMMON_NAME = False
IS_PYOPENSSL = False
ALPN_PROTOCOLS = ['http/1.1']
_TYPE_VERSION_INFO = tuple[(int, int, int, str, int)]
HASHFUNC_MAP = {length: getattr(hashlib, algorithm, None) for (length, algorithm) in ((32, 'md5'), (40, 'sha1'), (64, 'sha256'))}

def _is_bpo_43522_fixed(implementation_name: str, version_info: _TYPE_VERSION_INFO, pypy_version_info: _TYPE_VERSION_INFO | None) -> bool:
    """Return True for CPython 3.9.3+ or 3.10+ and PyPy 7.3.8+ where
    setting SSLContext.hostname_checks_common_name to False works.

    Outside of CPython and PyPy we don't know which implementations work
    or not so we conservatively use our hostname matching as we know that works
    on all implementations.

    https://github.com/urllib3/urllib3/issues/2192#issuecomment-821832963
    https://foss.heptapod.net/pypy/pypy/-/issues/3539
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_._is_bpo_43522_fixed', '_is_bpo_43522_fixed(implementation_name, version_info, pypy_version_info)', {'implementation_name': implementation_name, 'version_info': version_info, 'pypy_version_info': pypy_version_info, '_TYPE_VERSION_INFO': _TYPE_VERSION_INFO}, 1)

def _is_has_never_check_common_name_reliable(openssl_version: str, openssl_version_number: int, implementation_name: str, version_info: _TYPE_VERSION_INFO, pypy_version_info: _TYPE_VERSION_INFO | None) -> bool:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_._is_has_never_check_common_name_reliable', '_is_has_never_check_common_name_reliable(openssl_version, openssl_version_number, implementation_name, version_info, pypy_version_info)', {'_is_bpo_43522_fixed': _is_bpo_43522_fixed, 'openssl_version': openssl_version, 'openssl_version_number': openssl_version_number, 'implementation_name': implementation_name, 'version_info': version_info, 'pypy_version_info': pypy_version_info, '_TYPE_VERSION_INFO': _TYPE_VERSION_INFO}, 1)
if typing.TYPE_CHECKING:
    from ssl import VerifyMode
    from typing import TypedDict
    from .ssltransport import SSLTransport as SSLTransportType
    
    
    class _TYPE_PEER_CERT_RET_DICT(TypedDict, total=False):
        subjectAltName: tuple[(tuple[(str, str)], ...)]
        subject: tuple[(tuple[(tuple[(str, str)], ...)], ...)]
        serialNumber: str
    
_SSL_VERSION_TO_TLS_VERSION: dict[(int, int)] = {}
try:
    import ssl
    from ssl import CERT_REQUIRED, HAS_NEVER_CHECK_COMMON_NAME, OP_NO_COMPRESSION, OP_NO_TICKET, OPENSSL_VERSION, OPENSSL_VERSION_NUMBER, PROTOCOL_TLS, PROTOCOL_TLS_CLIENT, VERIFY_X509_STRICT, OP_NO_SSLv2, OP_NO_SSLv3, SSLContext, TLSVersion
    PROTOCOL_SSLv23 = PROTOCOL_TLS
    VERIFY_X509_PARTIAL_CHAIN = getattr(ssl, 'VERIFY_X509_PARTIAL_CHAIN', 524288)
    if (HAS_NEVER_CHECK_COMMON_NAME and not _is_has_never_check_common_name_reliable(OPENSSL_VERSION, OPENSSL_VERSION_NUMBER, sys.implementation.name, sys.version_info, (sys.pypy_version_info if sys.implementation.name == 'pypy' else None))):
        HAS_NEVER_CHECK_COMMON_NAME = False
    for attr in ('TLSv1', 'TLSv1_1', 'TLSv1_2'):
        try:
            _SSL_VERSION_TO_TLS_VERSION[getattr(ssl, f'PROTOCOL_{attr}')] = getattr(TLSVersion, attr)
        except AttributeError:
            continue
    from .ssltransport import SSLTransport
except ImportError:
    OP_NO_COMPRESSION = 131072
    OP_NO_TICKET = 16384
    OP_NO_SSLv2 = 16777216
    OP_NO_SSLv3 = 33554432
    PROTOCOL_SSLv23 = PROTOCOL_TLS = 2
    PROTOCOL_TLS_CLIENT = 16
    VERIFY_X509_PARTIAL_CHAIN = 524288
    VERIFY_X509_STRICT = 32
_TYPE_PEER_CERT_RET = typing.Union[('_TYPE_PEER_CERT_RET_DICT', bytes, None)]

def assert_fingerprint(cert: bytes | None, fingerprint: str) -> None:
    """
    Checks if given fingerprint matches the supplied certificate.

    :param cert:
        Certificate as bytes object.
    :param fingerprint:
        Fingerprint as string of hexdigits, can be interspersed by colons.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('urllib3.util.ssl_.assert_fingerprint', 'assert_fingerprint(cert, fingerprint)', {'SSLError': SSLError, 'HASHFUNC_MAP': HASHFUNC_MAP, 'unhexlify': unhexlify, 'hmac': hmac, 'cert': cert, 'fingerprint': fingerprint, 'bytes': bytes}, 0)

def resolve_cert_reqs(candidate: None | int | str) -> VerifyMode:
    """
    Resolves the argument to a numeric constant, which can be passed to
    the wrap_socket function/method from the ssl module.
    Defaults to :data:`ssl.CERT_REQUIRED`.
    If given a string it is assumed to be the name of the constant in the
    :mod:`ssl` module or its abbreviation.
    (So you can specify `REQUIRED` instead of `CERT_REQUIRED`.
    If it's neither `None` nor a string we assume it is already the numeric
    constant which can directly be passed to wrap_socket.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_.resolve_cert_reqs', 'resolve_cert_reqs(candidate)', {'CERT_REQUIRED': CERT_REQUIRED, 'ssl': ssl, 'candidate': candidate, 'int': int, 'str': str}, 1)

def resolve_ssl_version(candidate: None | int | str) -> int:
    """
    like resolve_cert_reqs
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_.resolve_ssl_version', 'resolve_ssl_version(candidate)', {'PROTOCOL_TLS': PROTOCOL_TLS, 'ssl': ssl, 'typing': typing, 'candidate': candidate, 'int': int, 'str': str}, 1)

def create_urllib3_context(ssl_version: int | None = None, cert_reqs: int | None = None, options: int | None = None, ciphers: str | None = None, ssl_minimum_version: int | None = None, ssl_maximum_version: int | None = None, verify_flags: int | None = None) -> ssl.SSLContext:
    """Creates and configures an :class:`ssl.SSLContext` instance for use with urllib3.

    :param ssl_version:
        The desired protocol version to use. This will default to
        PROTOCOL_SSLv23 which will negotiate the highest protocol that both
        the server and your installation of OpenSSL support.

        This parameter is deprecated instead use 'ssl_minimum_version'.
    :param ssl_minimum_version:
        The minimum version of TLS to be used. Use the 'ssl.TLSVersion' enum for specifying the value.
    :param ssl_maximum_version:
        The maximum version of TLS to be used. Use the 'ssl.TLSVersion' enum for specifying the value.
        Not recommended to set to anything other than 'ssl.TLSVersion.MAXIMUM_SUPPORTED' which is the
        default value.
    :param cert_reqs:
        Whether to require the certificate verification. This defaults to
        ``ssl.CERT_REQUIRED``.
    :param options:
        Specific OpenSSL options. These default to ``ssl.OP_NO_SSLv2``,
        ``ssl.OP_NO_SSLv3``, ``ssl.OP_NO_COMPRESSION``, and ``ssl.OP_NO_TICKET``.
    :param ciphers:
        Which cipher suites to allow the server to select. Defaults to either system configured
        ciphers if OpenSSL 1.1.1+, otherwise uses a secure default set of ciphers.
    :param verify_flags:
        The flags for certificate verification operations. These default to
        ``ssl.VERIFY_X509_PARTIAL_CHAIN`` and ``ssl.VERIFY_X509_STRICT`` for Python 3.13+.
    :returns:
        Constructed SSLContext object with specified options
    :rtype: SSLContext
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_.create_urllib3_context', 'create_urllib3_context(ssl_version=None, cert_reqs=None, options=None, ciphers=None, ssl_minimum_version=None, ssl_maximum_version=None, verify_flags=None)', {'SSLContext': SSLContext, 'PROTOCOL_TLS': PROTOCOL_TLS, 'PROTOCOL_TLS_CLIENT': PROTOCOL_TLS_CLIENT, '_SSL_VERSION_TO_TLS_VERSION': _SSL_VERSION_TO_TLS_VERSION, 'TLSVersion': TLSVersion, 'warnings': warnings, 'ssl': ssl, 'OP_NO_SSLv2': OP_NO_SSLv2, 'OP_NO_SSLv3': OP_NO_SSLv3, 'OP_NO_COMPRESSION': OP_NO_COMPRESSION, 'OP_NO_TICKET': OP_NO_TICKET, 'sys': sys, 'VERIFY_X509_PARTIAL_CHAIN': VERIFY_X509_PARTIAL_CHAIN, 'VERIFY_X509_STRICT': VERIFY_X509_STRICT, 'IS_PYOPENSSL': IS_PYOPENSSL, 'os': os, 'ssl_version': ssl_version, 'cert_reqs': cert_reqs, 'options': options, 'ciphers': ciphers, 'ssl_minimum_version': ssl_minimum_version, 'ssl_maximum_version': ssl_maximum_version, 'verify_flags': verify_flags, 'int': int, 'int': int, 'int': int, 'str': str, 'int': int, 'int': int, 'int': int, 'ssl': ssl}, 1)

@typing.overload
def ssl_wrap_socket(sock: socket.socket, keyfile: str | None = ..., certfile: str | None = ..., cert_reqs: int | None = ..., ca_certs: str | None = ..., server_hostname: str | None = ..., ssl_version: int | None = ..., ciphers: str | None = ..., ssl_context: ssl.SSLContext | None = ..., ca_cert_dir: str | None = ..., key_password: str | None = ..., ca_cert_data: None | str | bytes = ..., tls_in_tls: typing.Literal[False] = ...) -> ssl.SSLSocket:
    ...

@typing.overload
def ssl_wrap_socket(sock: socket.socket, keyfile: str | None = ..., certfile: str | None = ..., cert_reqs: int | None = ..., ca_certs: str | None = ..., server_hostname: str | None = ..., ssl_version: int | None = ..., ciphers: str | None = ..., ssl_context: ssl.SSLContext | None = ..., ca_cert_dir: str | None = ..., key_password: str | None = ..., ca_cert_data: None | str | bytes = ..., tls_in_tls: bool = ...) -> ssl.SSLSocket | SSLTransportType:
    ...

def ssl_wrap_socket(sock: socket.socket, keyfile: str | None = None, certfile: str | None = None, cert_reqs: int | None = None, ca_certs: str | None = None, server_hostname: str | None = None, ssl_version: int | None = None, ciphers: str | None = None, ssl_context: ssl.SSLContext | None = None, ca_cert_dir: str | None = None, key_password: str | None = None, ca_cert_data: None | str | bytes = None, tls_in_tls: bool = False) -> ssl.SSLSocket | SSLTransportType:
    """
    All arguments except for server_hostname, ssl_context, tls_in_tls, ca_cert_data and
    ca_cert_dir have the same meaning as they do when using
    :func:`ssl.create_default_context`, :meth:`ssl.SSLContext.load_cert_chain`,
    :meth:`ssl.SSLContext.set_ciphers` and :meth:`ssl.SSLContext.wrap_socket`.

    :param server_hostname:
        When SNI is supported, the expected hostname of the certificate
    :param ssl_context:
        A pre-made :class:`SSLContext` object. If none is provided, one will
        be created using :func:`create_urllib3_context`.
    :param ciphers:
        A string of ciphers we wish the client to support.
    :param ca_cert_dir:
        A directory containing CA certificates in multiple separate files, as
        supported by OpenSSL's -CApath flag or the capath argument to
        SSLContext.load_verify_locations().
    :param key_password:
        Optional password if the keyfile is encrypted.
    :param ca_cert_data:
        Optional string containing CA certificates in PEM format suitable for
        passing as the cadata parameter to SSLContext.load_verify_locations()
    :param tls_in_tls:
        Use SSLTransport to wrap the existing socket.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_.ssl_wrap_socket', 'ssl_wrap_socket(sock, keyfile=None, certfile=None, cert_reqs=None, ca_certs=None, server_hostname=None, ssl_version=None, ciphers=None, ssl_context=None, ca_cert_dir=None, key_password=None, ca_cert_data=None, tls_in_tls=False)', {'create_urllib3_context': create_urllib3_context, 'SSLError': SSLError, '_is_key_file_encrypted': _is_key_file_encrypted, 'ALPN_PROTOCOLS': ALPN_PROTOCOLS, '_ssl_wrap_socket_impl': _ssl_wrap_socket_impl, 'sock': sock, 'keyfile': keyfile, 'certfile': certfile, 'cert_reqs': cert_reqs, 'ca_certs': ca_certs, 'server_hostname': server_hostname, 'ssl_version': ssl_version, 'ciphers': ciphers, 'ssl_context': ssl_context, 'ca_cert_dir': ca_cert_dir, 'key_password': key_password, 'ca_cert_data': ca_cert_data, 'tls_in_tls': tls_in_tls, 'socket': socket, 'str': str, 'str': str, 'int': int, 'str': str, 'str': str, 'int': int, 'str': str, 'ssl': ssl, 'str': str, 'str': str, 'str': str, 'bytes': bytes, 'ssl': ssl, 'SSLTransportType': SSLTransportType}, 1)

def is_ipaddress(hostname: str | bytes) -> bool:
    """Detects whether the hostname given is an IPv4 or IPv6 address.
    Also detects IPv6 addresses with Zone IDs.

    :param str hostname: Hostname to examine.
    :return: True if the hostname is an IP address, False otherwise.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_.is_ipaddress', 'is_ipaddress(hostname)', {'_IPV4_RE': _IPV4_RE, '_BRACELESS_IPV6_ADDRZ_RE': _BRACELESS_IPV6_ADDRZ_RE, 'hostname': hostname, 'str': str, 'bytes': bytes}, 1)

def _is_key_file_encrypted(key_file: str) -> bool:
    """Detects if a key file is encrypted or not."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_._is_key_file_encrypted', '_is_key_file_encrypted(key_file)', {'key_file': key_file}, 1)

def _ssl_wrap_socket_impl(sock: socket.socket, ssl_context: ssl.SSLContext, tls_in_tls: bool, server_hostname: str | None = None) -> ssl.SSLSocket | SSLTransportType:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_._ssl_wrap_socket_impl', '_ssl_wrap_socket_impl(sock, ssl_context, tls_in_tls, server_hostname=None)', {'SSLTransport': SSLTransport, 'ProxySchemeUnsupported': ProxySchemeUnsupported, 'sock': sock, 'ssl_context': ssl_context, 'tls_in_tls': tls_in_tls, 'server_hostname': server_hostname, 'socket': socket, 'ssl': ssl, 'str': str, 'ssl': ssl, 'SSLTransportType': SSLTransportType}, 1)


"""The match_hostname() function from Python 3.5, essential when using SSL."""

from __future__ import annotations
import ipaddress
import re
import typing
from ipaddress import IPv4Address, IPv6Address
if typing.TYPE_CHECKING:
    from .ssl_ import _TYPE_PEER_CERT_RET_DICT
__version__ = '3.5.0.1'


class CertificateError(ValueError):
    pass


def _dnsname_match(dn: typing.Any, hostname: str, max_wildcards: int = 1) -> typing.Match[str] | None | bool:
    """Matching according to RFC 6125, section 6.4.3

    http://tools.ietf.org/html/rfc6125#section-6.4.3
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_match_hostname._dnsname_match', '_dnsname_match(dn, hostname, max_wildcards=1)', {'CertificateError': CertificateError, 're': re, 'dn': dn, 'hostname': hostname, 'max_wildcards': max_wildcards, 'typing': typing, 'bool': bool}, 1)

def _ipaddress_match(ipname: str, host_ip: IPv4Address | IPv6Address) -> bool:
    """Exact matching of IP addresses.

    RFC 9110 section 4.3.5: "A reference identity of IP-ID contains the decoded
    bytes of the IP address. An IP version 4 address is 4 octets, and an IP
    version 6 address is 16 octets. [...] A reference identity of type IP-ID
    matches if the address is identical to an iPAddress value of the
    subjectAltName extension of the certificate."
    """
    ip = ipaddress.ip_address(ipname.rstrip())
    return bool(ip.packed == host_ip.packed)

def match_hostname(cert: _TYPE_PEER_CERT_RET_DICT | None, hostname: str, hostname_checks_common_name: bool = False) -> None:
    """Verify that *cert* (in decoded format as returned by
    SSLSocket.getpeercert()) matches the *hostname*.  RFC 2818 and RFC 6125
    rules are followed, but IP addresses are not accepted for *hostname*.

    CertificateError is raised on failure. On success, the function
    returns nothing.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.ssl_match_hostname.match_hostname', 'match_hostname(cert, hostname, hostname_checks_common_name=False)', {'ipaddress': ipaddress, '_dnsname_match': _dnsname_match, '_ipaddress_match': _ipaddress_match, 'CertificateError': CertificateError, 'cert': cert, 'hostname': hostname, 'hostname_checks_common_name': hostname_checks_common_name, '_TYPE_PEER_CERT_RET_DICT': _TYPE_PEER_CERT_RET_DICT}, 1)


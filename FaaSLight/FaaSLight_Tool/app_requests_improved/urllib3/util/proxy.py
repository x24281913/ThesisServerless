from __future__ import annotations
import typing
from .url import Url
if typing.TYPE_CHECKING:
    from ..connection import ProxyConfig

def connection_requires_http_tunnel(proxy_url: Url | None = None, proxy_config: ProxyConfig | None = None, destination_scheme: str | None = None) -> bool:
    """
    Returns True if the connection requires an HTTP CONNECT through the proxy.

    :param URL proxy_url:
        URL of the proxy.
    :param ProxyConfig proxy_config:
        Proxy configuration from poolmanager.py
    :param str destination_scheme:
        The scheme of the destination. (i.e https, http, etc)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('urllib3.util.proxy.connection_requires_http_tunnel', 'connection_requires_http_tunnel(proxy_url=None, proxy_config=None, destination_scheme=None)', {'proxy_url': proxy_url, 'proxy_config': proxy_config, 'destination_scheme': destination_scheme, 'Url': Url, 'ProxyConfig': ProxyConfig, 'str': str}, 1)


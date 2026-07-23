import urllib3
from urllib3 import HTTPConnectionPool
from urllib3 import HTTPSConnectionPool
from urllib3 import PoolManager
from urllib3 import ProxyManager
from urllib3.util import retry
from urllib3.util import timeout
from urllib3.util import url
from urllib3.exceptions import HTTPError
from urllib3.exceptions import ConnectTimeoutError
from urllib3.exceptions import MaxRetryError
from urllib3.response import HTTPResponse

def lambda_handler(event, context):
    http = urllib3.PoolManager()
    url_str = event.get('url', 'http://httpbin.org/get')
    method = event.get('method', 'GET')
    timeout_val = urllib3.util.timeout.Timeout(connect=2.0, read=7.0)
    retry_val = urllib3.util.retry.Retry(total=3, backoff_factor=0.3)
    return {'statusCode': 200, 'body': {'url': url_str, 'method': method}}


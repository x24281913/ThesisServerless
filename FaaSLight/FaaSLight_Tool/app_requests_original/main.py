import requests
from requests import Session
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import HTTPError

def lambda_handler(event, context):
    session = Session()
    url = event.get('url', 'https://httpbin.org/get')
    method = event.get('method', 'GET')
    headers = {'Content-Type': 'application/json'}
    try:
        response = session.request(method=method, url=url, headers=headers, timeout=10)
        return {'statusCode': 200, 'body': {'status': response.status_code, 'url': url}}
    except Timeout:
        return {'statusCode': 408, 'body': 'Timeout'}
    except ConnectionError:
        return {'statusCode': 503, 'body': 'Connection Error'}


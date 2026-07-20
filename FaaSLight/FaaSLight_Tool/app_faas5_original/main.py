import time
import requests
from lxml import html

def lambda_handler(event, context):
    fun_st = time.time() * 1000
    url = event.get('url', 'https://www.baidu.com/')
    response = requests.request('GET', url)
    tree = html.fromstring(response.content)
    fun_ed = time.time() * 1000
    return {'statusCode': 200, 'body': {'url': url, 'function_time_ms': round(fun_ed - fun_st, 2)}}


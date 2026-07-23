import parso
from parso import parse
from parso.python import token
from parso.python import tokenize
from parso.python.diff import compute_diff
from parso.normalizer import NormalizerWrapper
from parso.utils import PythonVersionInfo
from parso.cache import parser_cache

def lambda_handler(event, context):
    code = event.get('code', 'def hello(): return "world"')
    module = parso.parse(code)
    version = PythonVersionInfo(3, 9)
    children = (module.children if hasattr(module, 'children') else [])
    return {'statusCode': 200, 'body': {'code': code, 'type': module.type, 'children_count': len(children)}}


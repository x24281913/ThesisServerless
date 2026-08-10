import pygments
from pygments import lexers
from pygments import formatters
from pygments import filters
from pygments import styles
from pygments import token
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.formatters import TerminalFormatter
from pygments.styles import get_style_by_name
from pygments.filters import NameHighlightFilter
from pygments.token import Token

def lambda_handler(event, context):
    code = event.get('code', 'def hello():\n    return "world"')
    language = event.get('language', 'python')
    style = event.get('style', 'monokai')
    lexer = PythonLexer()
    formatter = HtmlFormatter(style=style)
    style_obj = get_style_by_name(style)
    return {'statusCode': 200, 'body': {'language': language, 'style': style, 'css': formatter.get_style_defs()[:100]}}


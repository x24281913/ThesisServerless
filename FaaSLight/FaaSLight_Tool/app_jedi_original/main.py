import jedi
from jedi import api
from jedi import cache
from jedi import debug
from jedi import settings
from jedi.api import classes
from jedi.api import helpers
from jedi.api import keywords
from jedi.api import project
from jedi.inference import compiled
from jedi.inference import imports
from jedi.inference import analysis

def lambda_handler(event, context):
    code = event.get('code', 'import os\nos.path.')
    line = event.get('line', 2)
    column = event.get('column', 8)
    script = jedi.Script(code)
    completions = script.complete(line, column)
    names = [c.name for c in completions[:5]]
    infer = script.infer(line, column)
    return {'statusCode': 200, 'body': {'code': code, 'completions': names, 'inferred': [str(i) for i in infer[:3]]}}


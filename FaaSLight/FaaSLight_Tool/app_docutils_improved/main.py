import docutils
from docutils import parsers
from docutils import transforms
from docutils import writers
from docutils import frontend
from docutils import utils
from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
from docutils.writers import html4css1
from docutils.transforms import universal

def lambda_handler(event, context):
    text = event.get('text', '**Hello World**')
    settings = frontend.OptionParser(components=(rst.Parser, )).get_default_values()
    document = utils.new_document('test', settings)
    parser = rst.Parser()
    parser.parse(text, document)
    return {'statusCode': 200, 'body': {'input': text, 'parsed': document.asdom().toxml()}}


"""
    pygments.lexers.data
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for data file format.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import Lexer, ExtendedRegexLexer, LexerContext, include, bygroups
from pygments.token import Comment, Error, Keyword, Literal, Name, Number, Punctuation, String, Whitespace
__all__ = ['YamlLexer', 'JsonLexer', 'JsonBareObjectLexer', 'JsonLdLexer']


class YamlLexerContext(LexerContext):
    """Indentation context for the YAML lexer."""
    
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.indent_stack = []
        self.indent = -1
        self.next_indent = 0
        self.block_scalar_indent = None



class YamlLexer(ExtendedRegexLexer):
    """
    Lexer for YAML, a human-friendly data serialization
    language.
    """
    name = 'YAML'
    url = 'http://yaml.org/'
    aliases = ['yaml']
    filenames = ['*.yaml', '*.yml']
    mimetypes = ['text/x-yaml']
    version_added = '0.11'
    
    def something(token_class):
        """Do not produce empty tokens."""
        
        def callback(lexer, match, context):
            text = match.group()
            if not text:
                return
            yield (match.start(), token_class, text)
            context.pos = match.end()
        return callback
    
    def reset_indent(token_class):
        """Reset the indentation levels."""
        
        def callback(lexer, match, context):
            text = match.group()
            context.indent_stack = []
            context.indent = -1
            context.next_indent = 0
            context.block_scalar_indent = None
            yield (match.start(), token_class, text)
            context.pos = match.end()
        return callback
    
    def save_indent(token_class, start=False):
        """Save a possible indentation level."""
        
        def callback(lexer, match, context):
            text = match.group()
            extra = ''
            if start:
                context.next_indent = len(text)
                if context.next_indent < context.indent:
                    while context.next_indent < context.indent:
                        context.indent = context.indent_stack.pop()
                    if context.next_indent > context.indent:
                        extra = text[context.indent:]
                        text = text[:context.indent]
            else:
                context.next_indent += len(text)
            if text:
                yield (match.start(), token_class, text)
            if extra:
                yield (match.start() + len(text), token_class.Error, extra)
            context.pos = match.end()
        return callback
    
    def set_indent(token_class, implicit=False):
        """Set the previously saved indentation level."""
        
        def callback(lexer, match, context):
            text = match.group()
            if context.indent < context.next_indent:
                context.indent_stack.append(context.indent)
                context.indent = context.next_indent
            if not implicit:
                context.next_indent += len(text)
            yield (match.start(), token_class, text)
            context.pos = match.end()
        return callback
    
    def set_block_scalar_indent(token_class):
        """Set an explicit indentation level for a block scalar."""
        
        def callback(lexer, match, context):
            text = match.group()
            context.block_scalar_indent = None
            if not text:
                return
            increment = match.group(1)
            if increment:
                current_indent = max(context.indent, 0)
                increment = int(increment)
                context.block_scalar_indent = current_indent + increment
            if text:
                yield (match.start(), token_class, text)
                context.pos = match.end()
        return callback
    
    def parse_block_scalar_empty_line(indent_token_class, content_token_class):
        """Process an empty line in a block scalar."""
        
        def callback(lexer, match, context):
            text = match.group()
            if (context.block_scalar_indent is None or len(text) <= context.block_scalar_indent):
                if text:
                    yield (match.start(), indent_token_class, text)
            else:
                indentation = text[:context.block_scalar_indent]
                content = text[context.block_scalar_indent:]
                yield (match.start(), indent_token_class, indentation)
                yield (match.start() + context.block_scalar_indent, content_token_class, content)
            context.pos = match.end()
        return callback
    
    def parse_block_scalar_indent(token_class):
        """Process indentation spaces in a block scalar."""
        
        def callback(lexer, match, context):
            text = match.group()
            if context.block_scalar_indent is None:
                if len(text) <= max(context.indent, 0):
                    context.stack.pop()
                    context.stack.pop()
                    return
                context.block_scalar_indent = len(text)
            elif len(text) < context.block_scalar_indent:
                context.stack.pop()
                context.stack.pop()
                return
            if text:
                yield (match.start(), token_class, text)
                context.pos = match.end()
        return callback
    
    def parse_plain_scalar_indent(token_class):
        """Process indentation spaces in a plain scalar."""
        
        def callback(lexer, match, context):
            text = match.group()
            if len(text) <= context.indent:
                context.stack.pop()
                context.stack.pop()
                return
            if text:
                yield (match.start(), token_class, text)
                context.pos = match.end()
        return callback
    tokens = {'root': [('[ ]+(?=#|$)', Whitespace), ('\\n+', Whitespace), ('#[^\\n]*', Comment.Single), ('^%YAML(?=[ ]|$)', reset_indent(Name.Tag), 'yaml-directive'), ('^%TAG(?=[ ]|$)', reset_indent(Name.Tag), 'tag-directive'), ('^(?:---|\\.\\.\\.)(?=[ ]|$)', reset_indent(Name.Namespace), 'block-line'), ('[ ]*(?!\\s|$)', save_indent(Whitespace, start=True), ('block-line', 'indentation'))], 'ignored-line': [('[ ]+(?=#|$)', Whitespace), ('#[^\\n]*', Comment.Single), ('\\n', Whitespace, '#pop:2')], 'yaml-directive': [('([ ]+)([0-9]+\\.[0-9]+)', bygroups(Whitespace, Number), 'ignored-line')], 'tag-directive': [("([ ]+)(!|![\\w-]*!)([ ]+)(!|!?[\\w;/?:@&=+$,.!~*\\'()\\[\\]%-]+)", bygroups(Whitespace, Keyword.Type, Whitespace, Keyword.Type), 'ignored-line')], 'indentation': [('[ ]*$', something(Whitespace), '#pop:2'), ('[ ]+(?=[?:-](?:[ ]|$))', save_indent(Whitespace)), ('[?:-](?=[ ]|$)', set_indent(Punctuation.Indicator)), ('[ ]*', save_indent(Whitespace), '#pop')], 'block-line': [('[ ]*(?=#|$)', something(Whitespace), '#pop'), ('[ ]+', Whitespace), ('([^#,?\\[\\]{}"\'\\n]+)(:)(?=[ ]|$)', bygroups(Name.Tag, set_indent(Punctuation, implicit=True))), include('descriptors'), include('block-nodes'), include('flow-nodes'), ('(?=[^\\s?:,\\[\\]{}#&*!|>\\\'"%@`-]|[?:-]\\S)', something(Name.Variable), 'plain-scalar-in-block-context')], 'descriptors': [("!<[\\w#;/?:@&=+$,.!~*\\'()\\[\\]%-]+>", Keyword.Type), ("!(?:[\\w-]+!)?[\\w#;/?:@&=+$,.!~*\\'()\\[\\]%-]*", Keyword.Type), ('&[\\w-]+', Name.Label), ('\\*[\\w-]+', Name.Variable)], 'block-nodes': [(':(?=[ ]|$)', set_indent(Punctuation.Indicator, implicit=True)), ('[|>]', Punctuation.Indicator, ('block-scalar-content', 'block-scalar-header'))], 'flow-nodes': [('\\[', Punctuation.Indicator, 'flow-sequence'), ('\\{', Punctuation.Indicator, 'flow-mapping'), ("\\'", String, 'single-quoted-scalar'), ('\\"', String, 'double-quoted-scalar')], 'flow-collection': [('[ ]+', Whitespace), ('\\n+', Whitespace), ('#[^\\n]*', Comment.Single), ('[?:,]', Punctuation.Indicator), include('descriptors'), include('flow-nodes'), ('(?=[^\\s?:,\\[\\]{}#&*!|>\\\'"%@`])', something(Name.Variable), 'plain-scalar-in-flow-context')], 'flow-sequence': [include('flow-collection'), ('\\]', Punctuation.Indicator, '#pop')], 'flow-mapping': [('([^,:?\\[\\]{}"\'\\n]+)(:)(?=[ ]|$)', bygroups(Name.Tag, Punctuation)), include('flow-collection'), ('\\}', Punctuation.Indicator, '#pop')], 'block-scalar-content': [('\\n', Whitespace), ('^[ ]+$', parse_block_scalar_empty_line(Whitespace, Name.Constant)), ('^[ ]*', parse_block_scalar_indent(Whitespace)), ('[\\S\\t ]+', Name.Constant)], 'block-scalar-header': [('([1-9])?[+-]?(?=[ ]|$)', set_block_scalar_indent(Punctuation.Indicator), 'ignored-line'), ('[+-]?([1-9])?(?=[ ]|$)', set_block_scalar_indent(Punctuation.Indicator), 'ignored-line')], 'quoted-scalar-whitespaces': [('^[ ]+', Whitespace), ('[ ]+$', Whitespace), ('\\n+', Whitespace), ('[ ]+', Name.Variable)], 'single-quoted-scalar': [include('quoted-scalar-whitespaces'), ("\\'\\'", String.Escape), ("[^\\s\\']+", String), ("\\'", String, '#pop')], 'double-quoted-scalar': [include('quoted-scalar-whitespaces'), ('\\\\[0abt\\tn\\nvfre "\\\\N_LP]', String), ('\\\\(?:x[0-9A-Fa-f]{2}|u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8})', String.Escape), ('[^\\s"\\\\]+', String), ('"', String, '#pop')], 'plain-scalar-in-block-context-new-line': [('^[ ]+$', Whitespace), ('\\n+', Whitespace), ('^(?=---|\\.\\.\\.)', something(Name.Namespace), '#pop:3'), ('^[ ]*', parse_plain_scalar_indent(Whitespace), '#pop')], 'plain-scalar-in-block-context': [('[ ]*(?=:[ ]|:$)', something(Whitespace), '#pop'), ('[ ]+(?=#)', Whitespace, '#pop'), ('[ ]+$', Whitespace), ('\\n+', Whitespace, 'plain-scalar-in-block-context-new-line'), ('[ ]+', Literal.Scalar.Plain), ('(?::(?!\\s)|[^\\s:])+', Literal.Scalar.Plain)], 'plain-scalar-in-flow-context': [('[ ]*(?=[,:?\\[\\]{}])', something(Whitespace), '#pop'), ('[ ]+(?=#)', Whitespace, '#pop'), ('^[ ]+', Whitespace), ('[ ]+$', Whitespace), ('\\n+', Whitespace), ('[ ]+', Name.Variable), ('[^\\s,:?\\[\\]{}]+', Name.Variable)]}
    
    def get_tokens_unprocessed(self, text=None, context=None):
        if context is None:
            context = YamlLexerContext(text, 0)
        return super().get_tokens_unprocessed(text, context)



class JsonLexer(Lexer):
    """
    For JSON data structures.

    Javascript-style comments are supported (like ``/* */`` and ``//``),
    though comments are not part of the JSON specification.
    This allows users to highlight JSON as it is used in the wild.

    No validation is performed on the input JSON document.
    """
    name = 'JSON'
    url = 'https://www.json.org'
    aliases = ['json', 'json-object']
    filenames = ['*.json', '*.jsonl', '*.ndjson', 'Pipfile.lock', '*.module', '*.xc']
    mimetypes = ['application/json', 'application/json-object', 'application/x-ndjson', 'application/jsonl', 'application/json-seq']
    version_added = '1.5'
    integers = set('-0123456789')
    floats = set('.eE+')
    constants = set('truefalsenull')
    hexadecimals = set('0123456789abcdefABCDEF')
    punctuations = set('{}[],')
    whitespaces = {' ', '\n', '\r', '\t'}
    
    def get_tokens_unprocessed(self, text):
        """Parse JSON data."""
        in_string = False
        in_escape = False
        in_unicode_escape = 0
        in_whitespace = False
        in_constant = False
        in_number = False
        in_float = False
        in_punctuation = False
        in_comment_single = False
        in_comment_multiline = False
        expecting_second_comment_opener = False
        expecting_second_comment_closer = False
        start = 0
        queue = []
        for (stop, character) in enumerate(text):
            if in_string:
                if in_unicode_escape:
                    if character in self.hexadecimals:
                        in_unicode_escape -= 1
                        if not in_unicode_escape:
                            in_escape = False
                    else:
                        in_unicode_escape = 0
                        in_escape = False
                elif in_escape:
                    if character == 'u':
                        in_unicode_escape = 4
                    else:
                        in_escape = False
                elif character == '\\':
                    in_escape = True
                elif character == '"':
                    queue.append((start, String.Double, text[start:stop + 1]))
                    in_string = False
                    in_escape = False
                    in_unicode_escape = 0
                continue
            elif in_whitespace:
                if character in self.whitespaces:
                    continue
                if queue:
                    queue.append((start, Whitespace, text[start:stop]))
                else:
                    yield (start, Whitespace, text[start:stop])
                in_whitespace = False
            elif in_constant:
                if character in self.constants:
                    continue
                yield (start, Keyword.Constant, text[start:stop])
                in_constant = False
            elif in_number:
                if character in self.integers:
                    continue
                elif character in self.floats:
                    in_float = True
                    continue
                if in_float:
                    yield (start, Number.Float, text[start:stop])
                else:
                    yield (start, Number.Integer, text[start:stop])
                in_number = False
                in_float = False
            elif in_punctuation:
                if character in self.punctuations:
                    continue
                yield (start, Punctuation, text[start:stop])
                in_punctuation = False
            elif in_comment_single:
                if character != '\n':
                    continue
                if queue:
                    queue.append((start, Comment.Single, text[start:stop]))
                else:
                    yield (start, Comment.Single, text[start:stop])
                in_comment_single = False
            elif in_comment_multiline:
                if character == '*':
                    expecting_second_comment_closer = True
                elif expecting_second_comment_closer:
                    expecting_second_comment_closer = False
                    if character == '/':
                        if queue:
                            queue.append((start, Comment.Multiline, text[start:stop + 1]))
                        else:
                            yield (start, Comment.Multiline, text[start:stop + 1])
                        in_comment_multiline = False
                continue
            elif expecting_second_comment_opener:
                expecting_second_comment_opener = False
                if character == '/':
                    in_comment_single = True
                    continue
                elif character == '*':
                    in_comment_multiline = True
                    continue
                yield from queue
                queue.clear()
                yield (start, Error, text[start:stop])
            start = stop
            if character == '"':
                in_string = True
            elif character in self.whitespaces:
                in_whitespace = True
            elif character in {'f', 'n', 't'}:
                yield from queue
                queue.clear()
                in_constant = True
            elif character in self.integers:
                yield from queue
                queue.clear()
                in_number = True
            elif character == ':':
                for (_start, _token, _text) in queue:
                    if _token is String.Double:
                        yield (_start, Name.Tag, _text)
                    else:
                        yield (_start, _token, _text)
                queue.clear()
                in_punctuation = True
            elif character in self.punctuations:
                yield from queue
                queue.clear()
                in_punctuation = True
            elif character == '/':
                expecting_second_comment_opener = True
            else:
                yield from queue
                queue.clear()
                yield (start, Error, character)
        yield from queue
        if in_string:
            yield (start, Error, text[start:])
        elif in_float:
            yield (start, Number.Float, text[start:])
        elif in_number:
            yield (start, Number.Integer, text[start:])
        elif in_constant:
            yield (start, Keyword.Constant, text[start:])
        elif in_whitespace:
            yield (start, Whitespace, text[start:])
        elif in_punctuation:
            yield (start, Punctuation, text[start:])
        elif in_comment_single:
            yield (start, Comment.Single, text[start:])
        elif in_comment_multiline:
            yield (start, Error, text[start:])
        elif expecting_second_comment_opener:
            yield (start, Error, text[start:])



class JsonBareObjectLexer(JsonLexer):
    """
    For JSON data structures (with missing object curly braces).

    .. deprecated:: 2.8.0

       Behaves the same as `JsonLexer` now.
    """
    name = 'JSONBareObject'
    aliases = []
    filenames = []
    mimetypes = []
    version_added = '2.2'



class JsonLdLexer(JsonLexer):
    """
    For JSON-LD linked data.
    """
    name = 'JSON-LD'
    url = 'https://json-ld.org/'
    aliases = ['jsonld', 'json-ld']
    filenames = ['*.jsonld']
    mimetypes = ['application/ld+json']
    version_added = '2.0'
    json_ld_keywords = {f'"@{keyword}"' for keyword in ('base', 'container', 'context', 'direction', 'graph', 'id', 'import', 'included', 'index', 'json', 'language', 'list', 'nest', 'none', 'prefix', 'propagate', 'protected', 'reverse', 'set', 'type', 'value', 'version', 'vocab')}
    
    def get_tokens_unprocessed(self, text):
        for (start, token, value) in super().get_tokens_unprocessed(text):
            if (token is Name.Tag and value in self.json_ld_keywords):
                yield (start, Name.Decorator, value)
            else:
                yield (start, token, value)



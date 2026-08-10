"""
    pygments.lexers.webmisc
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for misc. web stuff.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, bygroups, default, using
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Literal, Whitespace
from pygments.lexers.css import _indentation, _starts_block
from pygments.lexers.html import HtmlLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.ruby import RubyLexer
__all__ = ['DuelLexer', 'SlimLexer', 'XQueryLexer', 'QmlLexer', 'CirruLexer']


class DuelLexer(RegexLexer):
    """
    Lexer for Duel Views Engine (formerly JBST) markup with JavaScript code blocks.
    """
    name = 'Duel'
    url = 'http://duelengine.org/'
    aliases = ['duel', 'jbst', 'jsonml+bst']
    filenames = ['*.duel', '*.jbst']
    mimetypes = ['text/x-duel', 'text/x-jbst']
    version_added = '1.4'
    flags = re.DOTALL
    tokens = {'root': [('(<%[@=#!:]?)(.*?)(%>)', bygroups(Name.Tag, using(JavascriptLexer), Name.Tag)), ('(<%\\$)(.*?)(:)(.*?)(%>)', bygroups(Name.Tag, Name.Function, Punctuation, String, Name.Tag)), ('(<%--)(.*?)(--%>)', bygroups(Name.Tag, Comment.Multiline, Name.Tag)), ('(<script.*?>)(.*?)(</script>)', bygroups(using(HtmlLexer), using(JavascriptLexer), using(HtmlLexer))), ('(.+?)(?=<)', using(HtmlLexer)), ('.+', using(HtmlLexer))]}



class XQueryLexer(ExtendedRegexLexer):
    """
    An XQuery lexer, parsing a stream and outputting the tokens needed to
    highlight xquery code.
    """
    name = 'XQuery'
    url = 'https://www.w3.org/XML/Query/'
    aliases = ['xquery', 'xqy', 'xq', 'xql', 'xqm']
    filenames = ['*.xqy', '*.xquery', '*.xq', '*.xql', '*.xqm']
    mimetypes = ['text/xquery', 'application/xquery']
    version_added = '1.4'
    xquery_parse_state = []
    ncnamestartchar = '(?:[A-Z]|_|[a-z])'
    ncnamechar = '(?:' + ncnamestartchar + '|-|\\.|[0-9])'
    ncname = f'(?:{ncnamestartchar}+{ncnamechar}*)'
    pitarget_namestartchar = '(?:[A-KN-WYZ]|_|:|[a-kn-wyz])'
    pitarget_namechar = '(?:' + pitarget_namestartchar + '|-|\\.|[0-9])'
    pitarget = f'{pitarget_namestartchar}+{pitarget_namechar}*'
    prefixedname = f'{ncname}:{ncname}'
    unprefixedname = ncname
    qname = f'(?:{prefixedname}|{unprefixedname})'
    entityref = '(?:&(?:lt|gt|amp|quot|apos|nbsp);)'
    charref = '(?:&#[0-9]+;|&#x[0-9a-fA-F]+;)'
    stringdouble = '(?:"(?:' + entityref + '|' + charref + '|""|[^&"])*")'
    stringsingle = "(?:'(?:" + entityref + '|' + charref + "|''|[^&'])*')"
    elementcontentchar = '[A-Za-z]|\\s|\\d|[!"#$%()*+,\\-./:;=?@\\[\\\\\\]^_\\\'`|~]'
    quotattrcontentchar = "[A-Za-z]|\\s|\\d|[!#$%()*+,\\-./:;=?@\\[\\\\\\]^_\\'`|~]"
    aposattrcontentchar = '[A-Za-z]|\\s|\\d|[!"#$%()*+,\\-./:;=?@\\[\\\\\\]^_`|~]'
    flags = re.DOTALL | re.MULTILINE
    
    def punctuation_root_callback(lexer, match, ctx):
        yield (match.start(), Punctuation, match.group(1))
        ctx.stack = ['root']
        ctx.pos = match.end()
    
    def operator_root_callback(lexer, match, ctx):
        yield (match.start(), Operator, match.group(1))
        ctx.stack = ['root']
        ctx.pos = match.end()
    
    def popstate_tag_callback(lexer, match, ctx):
        yield (match.start(), Name.Tag, match.group(1))
        if lexer.xquery_parse_state:
            ctx.stack.append(lexer.xquery_parse_state.pop())
        ctx.pos = match.end()
    
    def popstate_xmlcomment_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append(lexer.xquery_parse_state.pop())
        ctx.pos = match.end()
    
    def popstate_kindtest_callback(lexer, match, ctx):
        yield (match.start(), Punctuation, match.group(1))
        next_state = lexer.xquery_parse_state.pop()
        if next_state == 'occurrenceindicator':
            if re.match('[?*+]+', match.group(2)):
                yield (match.start(), Punctuation, match.group(2))
                ctx.stack.append('operator')
                ctx.pos = match.end()
            else:
                ctx.stack.append('operator')
                ctx.pos = match.end(1)
        else:
            ctx.stack.append(next_state)
            ctx.pos = match.end(1)
    
    def popstate_callback(lexer, match, ctx):
        yield (match.start(), Punctuation, match.group(1))
        if len(lexer.xquery_parse_state) == 0:
            ctx.stack.pop()
            if not ctx.stack:
                ctx.stack = ['root']
        elif len(ctx.stack) > 1:
            ctx.stack.append(lexer.xquery_parse_state.pop())
        else:
            ctx.stack = ['root']
        ctx.pos = match.end()
    
    def pushstate_element_content_starttag_callback(lexer, match, ctx):
        yield (match.start(), Name.Tag, match.group(1))
        lexer.xquery_parse_state.append('element_content')
        ctx.stack.append('start_tag')
        ctx.pos = match.end()
    
    def pushstate_cdata_section_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('cdata_section')
        lexer.xquery_parse_state.append(ctx.state.pop)
        ctx.pos = match.end()
    
    def pushstate_starttag_callback(lexer, match, ctx):
        yield (match.start(), Name.Tag, match.group(1))
        lexer.xquery_parse_state.append(ctx.state.pop)
        ctx.stack.append('start_tag')
        ctx.pos = match.end()
    
    def pushstate_operator_order_callback(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_operator_map_callback(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_operator_root_validate(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_operator_root_validate_withmode(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Keyword, match.group(3))
        ctx.stack = ['root']
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_operator_processing_instruction_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('processing_instruction')
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_element_content_processing_instruction_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('processing_instruction')
        lexer.xquery_parse_state.append('element_content')
        ctx.pos = match.end()
    
    def pushstate_element_content_cdata_section_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('cdata_section')
        lexer.xquery_parse_state.append('element_content')
        ctx.pos = match.end()
    
    def pushstate_operator_cdata_section_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('cdata_section')
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_element_content_xmlcomment_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('xml_comment')
        lexer.xquery_parse_state.append('element_content')
        ctx.pos = match.end()
    
    def pushstate_operator_xmlcomment_callback(lexer, match, ctx):
        yield (match.start(), String.Doc, match.group(1))
        ctx.stack.append('xml_comment')
        lexer.xquery_parse_state.append('operator')
        ctx.pos = match.end()
    
    def pushstate_kindtest_callback(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('kindtest')
        ctx.stack.append('kindtest')
        ctx.pos = match.end()
    
    def pushstate_operator_kindtestforpi_callback(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.stack.append('kindtestforpi')
        ctx.pos = match.end()
    
    def pushstate_operator_kindtest_callback(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.stack.append('kindtest')
        ctx.pos = match.end()
    
    def pushstate_occurrenceindicator_kindtest_callback(lexer, match, ctx):
        yield (match.start(), Name.Tag, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('occurrenceindicator')
        ctx.stack.append('kindtest')
        ctx.pos = match.end()
    
    def pushstate_operator_starttag_callback(lexer, match, ctx):
        yield (match.start(), Name.Tag, match.group(1))
        lexer.xquery_parse_state.append('operator')
        ctx.stack.append('start_tag')
        ctx.pos = match.end()
    
    def pushstate_operator_root_callback(lexer, match, ctx):
        yield (match.start(), Punctuation, match.group(1))
        lexer.xquery_parse_state.append('operator')
        ctx.stack = ['root']
        ctx.pos = match.end()
    
    def pushstate_operator_root_construct_callback(lexer, match, ctx):
        yield (match.start(), Keyword, match.group(1))
        yield (match.start(), Whitespace, match.group(2))
        yield (match.start(), Punctuation, match.group(3))
        lexer.xquery_parse_state.append('operator')
        ctx.stack = ['root']
        ctx.pos = match.end()
    
    def pushstate_root_callback(lexer, match, ctx):
        yield (match.start(), Punctuation, match.group(1))
        cur_state = ctx.stack.pop()
        lexer.xquery_parse_state.append(cur_state)
        ctx.stack = ['root']
        ctx.pos = match.end()
    
    def pushstate_operator_attribute_callback(lexer, match, ctx):
        yield (match.start(), Name.Attribute, match.group(1))
        ctx.stack.append('operator')
        ctx.pos = match.end()
    tokens = {'comment': [('[^:()]+', Comment), ('\\(:', Comment, '#push'), (':\\)', Comment, '#pop'), ('[:()]', Comment)], 'whitespace': [('\\s+', Whitespace)], 'operator': [include('whitespace'), ('(\\})', popstate_callback), ('\\(:', Comment, 'comment'), ('(\\{)', pushstate_root_callback), ('then|else|external|at|div|except', Keyword, 'root'), ('order by', Keyword, 'root'), ('group by', Keyword, 'root'), ('is|mod|order\\s+by|stable\\s+order\\s+by', Keyword, 'root'), ('and|or', Operator.Word, 'root'), ('(eq|ge|gt|le|lt|ne|idiv|intersect|in)(?=\\b)', Operator.Word, 'root'), ('return|satisfies|to|union|where|count|preserve\\s+strip', Keyword, 'root'), ('(>=|>>|>|<=|<<|<|-|\\*|!=|\\+|\\|\\||\\||:=|=|!)', operator_root_callback), ('(::|:|;|\\[|//|/|,)', punctuation_root_callback), ('(castable|cast)(\\s+)(as)\\b', bygroups(Keyword, Whitespace, Keyword), 'singletype'), ('(instance)(\\s+)(of)\\b', bygroups(Keyword, Whitespace, Keyword), 'itemtype'), ('(treat)(\\s+)(as)\\b', bygroups(Keyword, Whitespace, Keyword), 'itemtype'), ('(case)(\\s+)(' + stringdouble + ')', bygroups(Keyword, Whitespace, String.Double), 'itemtype'), ('(case)(\\s+)(' + stringsingle + ')', bygroups(Keyword, Whitespace, String.Single), 'itemtype'), ('(case|as)\\b', Keyword, 'itemtype'), ('(\\))(\\s*)(as)', bygroups(Punctuation, Whitespace, Keyword), 'itemtype'), ('\\$', Name.Variable, 'varname'), ('(for|let|previous|next)(\\s+)(\\$)', bygroups(Keyword, Whitespace, Name.Variable), 'varname'), ('(for)(\\s+)(tumbling|sliding)(\\s+)(window)(\\s+)(\\$)', bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword, Whitespace, Name.Variable), 'varname'), ('\\)|\\?|\\]', Punctuation), ('(empty)(\\s+)(greatest|least)', bygroups(Keyword, Whitespace, Keyword)), ('ascending|descending|default', Keyword, '#push'), ('(allowing)(\\s+)(empty)', bygroups(Keyword, Whitespace, Keyword)), ('external', Keyword), ('(start|when|end)', Keyword, 'root'), ('(only)(\\s+)(end)', bygroups(Keyword, Whitespace, Keyword), 'root'), ('collation', Keyword, 'uritooperator'), ('(into|following|preceding|with)', Keyword, 'root'), ('\\.', Operator), (stringdouble, String.Double), (stringsingle, String.Single), ('(catch)(\\s*)', bygroups(Keyword, Whitespace), 'root')], 'uritooperator': [(stringdouble, String.Double, '#pop'), (stringsingle, String.Single, '#pop')], 'namespacedecl': [include('whitespace'), ('\\(:', Comment, 'comment'), ('(at)(\\s+)(' + stringdouble + ')', bygroups(Keyword, Whitespace, String.Double)), ('(at)(\\s+)(' + stringsingle + ')', bygroups(Keyword, Whitespace, String.Single)), (stringdouble, String.Double), (stringsingle, String.Single), (',', Punctuation), ('=', Operator), (';', Punctuation, 'root'), (ncname, Name.Namespace)], 'namespacekeyword': [include('whitespace'), ('\\(:', Comment, 'comment'), (stringdouble, String.Double, 'namespacedecl'), (stringsingle, String.Single, 'namespacedecl'), ('inherit|no-inherit', Keyword, 'root'), ('namespace', Keyword, 'namespacedecl'), ('(default)(\\s+)(element)', bygroups(Keyword, Text, Keyword)), ('preserve|no-preserve', Keyword), (',', Punctuation)], 'annotationname': [('\\(:', Comment, 'comment'), (qname, Name.Decorator), ('(\\()(' + stringdouble + ')', bygroups(Punctuation, String.Double)), ('(\\()(' + stringsingle + ')', bygroups(Punctuation, String.Single)), ('(\\,)(\\s+)(' + stringdouble + ')', bygroups(Punctuation, Text, String.Double)), ('(\\,)(\\s+)(' + stringsingle + ')', bygroups(Punctuation, Text, String.Single)), ('\\)', Punctuation), ('(\\s+)(\\%)', bygroups(Text, Name.Decorator), 'annotationname'), ('(\\s+)(variable)(\\s+)(\\$)', bygroups(Text, Keyword.Declaration, Text, Name.Variable), 'varname'), ('(\\s+)(function)(\\s+)', bygroups(Text, Keyword.Declaration, Text), 'root')], 'varname': [('\\(:', Comment, 'comment'), ('(' + qname + ')(\\()?', bygroups(Name, Punctuation), 'operator')], 'singletype': [include('whitespace'), ('\\(:', Comment, 'comment'), (ncname + '(:\\*)', Name.Variable, 'operator'), (qname, Name.Variable, 'operator')], 'itemtype': [include('whitespace'), ('\\(:', Comment, 'comment'), ('\\$', Name.Variable, 'varname'), ('(void)(\\s*)(\\()(\\s*)(\\))', bygroups(Keyword, Text, Punctuation, Text, Punctuation), 'operator'), ('(element|attribute|schema-element|schema-attribute|comment|text|node|binary|document-node|empty-sequence)(\\s*)(\\()', pushstate_occurrenceindicator_kindtest_callback), ('(processing-instruction)(\\s*)(\\()', bygroups(Keyword, Text, Punctuation), ('occurrenceindicator', 'kindtestforpi')), ('(item)(\\s*)(\\()(\\s*)(\\))(?=[*+?])', bygroups(Keyword, Text, Punctuation, Text, Punctuation), 'occurrenceindicator'), ('(\\(\\#)(\\s*)', bygroups(Punctuation, Text), 'pragma'), (';', Punctuation, '#pop'), ('then|else', Keyword, '#pop'), ('(at)(\\s+)(' + stringdouble + ')', bygroups(Keyword, Text, String.Double), 'namespacedecl'), ('(at)(\\s+)(' + stringsingle + ')', bygroups(Keyword, Text, String.Single), 'namespacedecl'), ('except|intersect|in|is|return|satisfies|to|union|where|count', Keyword, 'root'), ('and|div|eq|ge|gt|le|lt|ne|idiv|mod|or', Operator.Word, 'root'), (':=|=|,|>=|>>|>|\\[|\\(|<=|<<|<|-|!=|\\|\\||\\|', Operator, 'root'), ('external|at', Keyword, 'root'), ('(stable)(\\s+)(order)(\\s+)(by)', bygroups(Keyword, Text, Keyword, Text, Keyword), 'root'), ('(castable|cast)(\\s+)(as)', bygroups(Keyword, Text, Keyword), 'singletype'), ('(treat)(\\s+)(as)', bygroups(Keyword, Text, Keyword)), ('(instance)(\\s+)(of)', bygroups(Keyword, Text, Keyword)), ('(case)(\\s+)(' + stringdouble + ')', bygroups(Keyword, Text, String.Double), 'itemtype'), ('(case)(\\s+)(' + stringsingle + ')', bygroups(Keyword, Text, String.Single), 'itemtype'), ('case|as', Keyword, 'itemtype'), ('(\\))(\\s*)(as)', bygroups(Operator, Text, Keyword), 'itemtype'), (ncname + ':\\*', Keyword.Type, 'operator'), ('(function|map|array)(\\()', bygroups(Keyword.Type, Punctuation)), (qname, Keyword.Type, 'occurrenceindicator')], 'kindtest': [('\\(:', Comment, 'comment'), ('\\{', Punctuation, 'root'), ('(\\))([*+?]?)', popstate_kindtest_callback), ('\\*', Name, 'closekindtest'), (qname, Name, 'closekindtest'), ('(element|schema-element)(\\s*)(\\()', pushstate_kindtest_callback)], 'kindtestforpi': [('\\(:', Comment, 'comment'), ('\\)', Punctuation, '#pop'), (ncname, Name.Variable), (stringdouble, String.Double), (stringsingle, String.Single)], 'closekindtest': [('\\(:', Comment, 'comment'), ('(\\))', popstate_callback), (',', Punctuation), ('(\\{)', pushstate_operator_root_callback), ('\\?', Punctuation)], 'xml_comment': [('(-->)', popstate_xmlcomment_callback), ('[^-]{1,2}', Literal), ('\\t|\\r|\\n|[\\u0020-\\uD7FF]|[\\uE000-\\uFFFD]|[\\U00010000-\\U0010FFFF]', Literal)], 'processing_instruction': [('\\s+', Text, 'processing_instruction_content'), ('\\?>', String.Doc, '#pop'), (pitarget, Name)], 'processing_instruction_content': [('\\?>', String.Doc, '#pop'), ('\\t|\\r|\\n|[\\u0020-\\uD7FF]|[\\uE000-\\uFFFD]|[\\U00010000-\\U0010FFFF]', Literal)], 'cdata_section': [(']]>', String.Doc, '#pop'), ('\\t|\\r|\\n|[\\u0020-\\uD7FF]|[\\uE000-\\uFFFD]|[\\U00010000-\\U0010FFFF]', Literal)], 'start_tag': [include('whitespace'), ('(/>)', popstate_tag_callback), ('>', Name.Tag, 'element_content'), ('"', Punctuation, 'quot_attribute_content'), ("'", Punctuation, 'apos_attribute_content'), ('=', Operator), (qname, Name.Tag)], 'quot_attribute_content': [('"', Punctuation, 'start_tag'), ('(\\{)', pushstate_root_callback), ('""', Name.Attribute), (quotattrcontentchar, Name.Attribute), (entityref, Name.Attribute), (charref, Name.Attribute), ('\\{\\{|\\}\\}', Name.Attribute)], 'apos_attribute_content': [("'", Punctuation, 'start_tag'), ('\\{', Punctuation, 'root'), ("''", Name.Attribute), (aposattrcontentchar, Name.Attribute), (entityref, Name.Attribute), (charref, Name.Attribute), ('\\{\\{|\\}\\}', Name.Attribute)], 'element_content': [('</', Name.Tag, 'end_tag'), ('(\\{)', pushstate_root_callback), ('(<!--)', pushstate_element_content_xmlcomment_callback), ('(<\\?)', pushstate_element_content_processing_instruction_callback), ('(<!\\[CDATA\\[)', pushstate_element_content_cdata_section_callback), ('(<)', pushstate_element_content_starttag_callback), (elementcontentchar, Literal), (entityref, Literal), (charref, Literal), ('\\{\\{|\\}\\}', Literal)], 'end_tag': [include('whitespace'), ('(>)', popstate_tag_callback), (qname, Name.Tag)], 'xmlspace_decl': [include('whitespace'), ('\\(:', Comment, 'comment'), ('preserve|strip', Keyword, '#pop')], 'declareordering': [('\\(:', Comment, 'comment'), include('whitespace'), ('ordered|unordered', Keyword, '#pop')], 'xqueryversion': [include('whitespace'), ('\\(:', Comment, 'comment'), (stringdouble, String.Double), (stringsingle, String.Single), ('encoding', Keyword), (';', Punctuation, '#pop')], 'pragma': [(qname, Name.Variable, 'pragmacontents')], 'pragmacontents': [('#\\)', Punctuation, 'operator'), ('\\t|\\r|\\n|[\\u0020-\\uD7FF]|[\\uE000-\\uFFFD]|[\\U00010000-\\U0010FFFF]', Literal), ('(\\s+)', Whitespace)], 'occurrenceindicator': [include('whitespace'), ('\\(:', Comment, 'comment'), ('\\*|\\?|\\+', Operator, 'operator'), (':=', Operator, 'root'), default('operator')], 'option': [include('whitespace'), (qname, Name.Variable, '#pop')], 'qname_braren': [include('whitespace'), ('(\\{)', pushstate_operator_root_callback), ('(\\()', Punctuation, 'root')], 'element_qname': [(qname, Name.Variable, 'root')], 'attribute_qname': [(qname, Name.Variable, 'root')], 'root': [include('whitespace'), ('\\(:', Comment, 'comment'), ('\\d+(\\.\\d*)?[eE][+-]?\\d+', Number.Float, 'operator'), ('(\\.\\d+)[eE][+-]?\\d+', Number.Float, 'operator'), ('(\\.\\d+|\\d+\\.\\d*)', Number.Float, 'operator'), ('(\\d+)', Number.Integer, 'operator'), ('(\\.\\.|\\.|\\))', Punctuation, 'operator'), ('(declare)(\\s+)(construction)', bygroups(Keyword.Declaration, Text, Keyword.Declaration), 'operator'), ('(declare)(\\s+)(default)(\\s+)(order)', bygroups(Keyword.Declaration, Text, Keyword.Declaration, Text, Keyword.Declaration), 'operator'), ('(declare)(\\s+)(context)(\\s+)(item)', bygroups(Keyword.Declaration, Text, Keyword.Declaration, Text, Keyword.Declaration), 'operator'), (ncname + ':\\*', Name, 'operator'), ('\\*:' + ncname, Name.Tag, 'operator'), ('\\*', Name.Tag, 'operator'), (stringdouble, String.Double, 'operator'), (stringsingle, String.Single, 'operator'), ('(\\}|\\])', popstate_callback), ('(declare)(\\s+)(default)(\\s+)(collation)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration, Whitespace, Keyword.Declaration)), ('(module|declare)(\\s+)(namespace)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'namespacedecl'), ('(declare)(\\s+)(base-uri)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'namespacedecl'), ('(declare)(\\s+)(default)(\\s+)(element|function)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration, Whitespace, Keyword.Declaration), 'namespacekeyword'), ('(import)(\\s+)(schema|module)', bygroups(Keyword.Pseudo, Whitespace, Keyword.Pseudo), 'namespacekeyword'), ('(declare)(\\s+)(copy-namespaces)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'namespacekeyword'), ('(for|let|some|every)(\\s+)(\\$)', bygroups(Keyword, Whitespace, Name.Variable), 'varname'), ('(for)(\\s+)(tumbling|sliding)(\\s+)(window)(\\s+)(\\$)', bygroups(Keyword, Whitespace, Keyword, Whitespace, Keyword, Whitespace, Name.Variable), 'varname'), ('\\$', Name.Variable, 'varname'), ('(declare)(\\s+)(variable)(\\s+)(\\$)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration, Whitespace, Name.Variable), 'varname'), ('(declare)(\\s+)(\\%)', bygroups(Keyword.Declaration, Whitespace, Name.Decorator), 'annotationname'), ('(\\))(\\s+)(as)', bygroups(Operator, Whitespace, Keyword), 'itemtype'), ('(element|attribute|schema-element|schema-attribute|comment|text|node|document-node|empty-sequence)(\\s+)(\\()', pushstate_operator_kindtest_callback), ('(processing-instruction)(\\s+)(\\()', pushstate_operator_kindtestforpi_callback), ('(<!--)', pushstate_operator_xmlcomment_callback), ('(<\\?)', pushstate_operator_processing_instruction_callback), ('(<!\\[CDATA\\[)', pushstate_operator_cdata_section_callback), ('(<)', pushstate_operator_starttag_callback), ('(declare)(\\s+)(boundary-space)', bygroups(Keyword.Declaration, Text, Keyword.Declaration), 'xmlspace_decl'), ('(validate)(\\s+)(lax|strict)', pushstate_operator_root_validate_withmode), ('(validate)(\\s*)(\\{)', pushstate_operator_root_validate), ('(typeswitch)(\\s*)(\\()', bygroups(Keyword, Whitespace, Punctuation)), ('(switch)(\\s*)(\\()', bygroups(Keyword, Whitespace, Punctuation)), ('(element|attribute|namespace)(\\s*)(\\{)', pushstate_operator_root_construct_callback), ('(document|text|processing-instruction|comment)(\\s*)(\\{)', pushstate_operator_root_construct_callback), ('(attribute)(\\s+)(?=' + qname + ')', bygroups(Keyword, Whitespace), 'attribute_qname'), ('(element)(\\s+)(?=' + qname + ')', bygroups(Keyword, Whitespace), 'element_qname'), ('(processing-instruction|namespace)(\\s+)(' + ncname + ')(\\s*)(\\{)', bygroups(Keyword, Whitespace, Name.Variable, Whitespace, Punctuation), 'operator'), ('(declare|define)(\\s+)(function)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration)), ('(\\{|\\[)', pushstate_operator_root_callback), ('(unordered|ordered)(\\s*)(\\{)', pushstate_operator_order_callback), ('(map|array)(\\s*)(\\{)', pushstate_operator_map_callback), ('(declare)(\\s+)(ordering)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'declareordering'), ('(xquery)(\\s+)(version)', bygroups(Keyword.Pseudo, Whitespace, Keyword.Pseudo), 'xqueryversion'), ('(\\(#)(\\s*)', bygroups(Punctuation, Whitespace), 'pragma'), ('return', Keyword), ('(declare)(\\s+)(option)', bygroups(Keyword.Declaration, Whitespace, Keyword.Declaration), 'option'), ('(at)(\\s+)(' + stringdouble + ')', String.Double, 'namespacedecl'), ('(at)(\\s+)(' + stringsingle + ')', String.Single, 'namespacedecl'), ('(ancestor-or-self|ancestor|attribute|child|descendant-or-self)(::)', bygroups(Keyword, Punctuation)), ('(descendant|following-sibling|following|parent|preceding-sibling|preceding|self)(::)', bygroups(Keyword, Punctuation)), ('(if)(\\s*)(\\()', bygroups(Keyword, Whitespace, Punctuation)), ('then|else', Keyword), ('(update)(\\s*)(insert|delete|replace|value|rename)', bygroups(Keyword, Whitespace, Keyword)), ('(into|following|preceding|with)', Keyword), ('(try)(\\s*)', bygroups(Keyword, Whitespace), 'root'), ('(catch)(\\s*)(\\()(\\$)', bygroups(Keyword, Whitespace, Punctuation, Name.Variable), 'varname'), ('(@' + qname + ')', Name.Attribute, 'operator'), ('(@' + ncname + ')', Name.Attribute, 'operator'), ('@\\*:' + ncname, Name.Attribute, 'operator'), ('@\\*', Name.Attribute, 'operator'), ('(@)', Name.Attribute, 'operator'), ('//|/|\\+|-|;|,|\\(|\\)', Punctuation), (qname + '(?=\\s*\\{)', Name.Tag, 'qname_braren'), (qname + '(?=\\s*\\([^:])', Name.Function, 'qname_braren'), ('(' + qname + ')(#)([0-9]+)', bygroups(Name.Function, Keyword.Type, Number.Integer)), (qname, Name.Tag, 'operator')]}



class QmlLexer(RegexLexer):
    """
    For QML files.
    """
    name = 'QML'
    url = 'https://doc.qt.io/qt-6/qmlapplications.html'
    aliases = ['qml', 'qbs']
    filenames = ['*.qml', '*.qbs']
    mimetypes = ['application/x-qml', 'application/x-qt.qbs+qml']
    version_added = '1.6'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'commentsandwhitespace': [('\\s+', Text), ('<!--', Comment), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline)], 'slashstartsregex': [include('commentsandwhitespace'), ('/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)', String.Regex, '#pop'), ('(?=/)', Text, ('#pop', 'badregex')), default('#pop')], 'badregex': [('\\n', Text, '#pop')], 'root': [('^(?=\\s|/|<!--)', Text, 'slashstartsregex'), include('commentsandwhitespace'), ('\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?', Operator, 'slashstartsregex'), ('[{(\\[;,]', Punctuation, 'slashstartsregex'), ('[})\\].]', Punctuation), ('\\bid\\s*:\\s*[A-Za-z][\\w.]*', Keyword.Declaration, 'slashstartsregex'), ('\\b[A-Za-z][\\w.]*\\s*:', Keyword, 'slashstartsregex'), ('(for|in|while|do|break|return|continue|switch|case|default|if|else|throw|try|catch|finally|new|delete|typeof|instanceof|void|this)\\b', Keyword, 'slashstartsregex'), ('(var|let|with|function)\\b', Keyword.Declaration, 'slashstartsregex'), ('(abstract|boolean|byte|char|class|const|debugger|double|enum|export|extends|final|float|goto|implements|import|int|interface|long|native|package|private|protected|public|short|static|super|synchronized|throws|transient|volatile)\\b', Keyword.Reserved), ('(true|false|null|NaN|Infinity|undefined)\\b', Keyword.Constant), ('(Array|Boolean|Date|Error|Function|Math|netscape|Number|Object|Packages|RegExp|String|sun|decodeURI|decodeURIComponent|encodeURI|encodeURIComponent|Error|eval|isFinite|isNaN|parseFloat|parseInt|document|this|window)\\b', Name.Builtin), ('[$a-zA-Z_]\\w*', Name.Other), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+', Number.Integer), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single)]}



class CirruLexer(RegexLexer):
    """
    * using ``()`` for expressions, but restricted in a same line
    * using ``""`` for strings, with ``\`` for escaping chars
    * using ``$`` as folding operator
    * using ``,`` as unfolding operator
    * using indentations for nested blocks
    """
    name = 'Cirru'
    url = 'http://cirru.org/'
    aliases = ['cirru']
    filenames = ['*.cirru']
    mimetypes = ['text/x-cirru']
    version_added = '2.0'
    flags = re.MULTILINE
    tokens = {'string': [('[^"\\\\\\n]+', String), ('\\\\', String.Escape, 'escape'), ('"', String, '#pop')], 'escape': [('.', String.Escape, '#pop')], 'function': [('\\,', Operator, '#pop'), ('[^\\s"()]+', Name.Function, '#pop'), ('\\)', Operator, '#pop'), ('(?=\\n)', Text, '#pop'), ('\\(', Operator, '#push'), ('"', String, ('#pop', 'string')), ('[ ]+', Text.Whitespace)], 'line': [('(?<!\\w)\\$(?!\\w)', Operator, 'function'), ('\\(', Operator, 'function'), ('\\)', Operator), ('\\n', Text, '#pop'), ('"', String, 'string'), ('[ ]+', Text.Whitespace), ('[+-]?[\\d.]+\\b', Number), ('[^\\s"()]+', Name.Variable)], 'root': [('^\\n+', Text.Whitespace), default(('line', 'function'))]}



class SlimLexer(ExtendedRegexLexer):
    """
    For Slim markup.
    """
    name = 'Slim'
    aliases = ['slim']
    filenames = ['*.slim']
    mimetypes = ['text/x-slim']
    url = 'https://slim-template.github.io'
    version_added = '2.0'
    flags = re.IGNORECASE
    _dot = '(?: \\|\\n(?=.* \\|)|.)'
    tokens = {'root': [('[ \\t]*\\n', Text), ('[ \\t]*', _indentation)], 'css': [('\\.[\\w:-]+', Name.Class, 'tag'), ('\\#[\\w:-]+', Name.Function, 'tag')], 'eval-or-plain': [('([ \\t]*==?)(.*\\n)', bygroups(Punctuation, using(RubyLexer)), 'root'), ('[ \\t]+[\\w:-]+(?==)', Name.Attribute, 'html-attributes'), default('plain')], 'content': [include('css'), ('[\\w:-]+:[ \\t]*\\n', Text, 'plain'), ('(-)(.*\\n)', bygroups(Punctuation, using(RubyLexer)), '#pop'), ('\\|' + _dot + '*\\n', _starts_block(Text, 'plain'), '#pop'), ('/' + _dot + '*\\n', _starts_block(Comment.Preproc, 'slim-comment-block'), '#pop'), ('[\\w:-]+', Name.Tag, 'tag'), include('eval-or-plain')], 'tag': [include('css'), ('[<>]{1,2}(?=[ \\t=])', Punctuation), ('[ \\t]+\\n', Punctuation, '#pop:2'), include('eval-or-plain')], 'plain': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text), ('(#\\{)(.*?)(\\})', bygroups(String.Interpol, using(RubyLexer), String.Interpol)), ('\\n', Text, 'root')], 'html-attributes': [('=', Punctuation), ('"[^"]+"', using(RubyLexer), 'tag'), ("\\'[^\\']+\\'", using(RubyLexer), 'tag'), ('\\w+', Text, 'tag')], 'slim-comment-block': [(_dot + '+', Comment.Preproc), ('\\n', Text, 'root')]}



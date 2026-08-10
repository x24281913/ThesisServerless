"""
    pygments.lexers.html
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for HTML, XML and related markup.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, ExtendedRegexLexer, include, bygroups, default, using, inherit, this
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Punctuation, Whitespace
from pygments.util import looks_like_xml, html_doctype_matches
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.jvm import ScalaLexer
from pygments.lexers.css import CssLexer, _indentation, _starts_block
from pygments.lexers.ruby import RubyLexer
__all__ = ['HtmlLexer', 'DtdLexer', 'XmlLexer', 'XsltLexer', 'HamlLexer', 'ScamlLexer', 'PugLexer', 'VueLexer', 'UrlEncodedLexer']


class HtmlLexer(RegexLexer):
    """
    For HTML 4 and XHTML 1 markup. Nested JavaScript and CSS is highlighted
    by the appropriate lexer.
    """
    name = 'HTML'
    url = 'https://html.spec.whatwg.org/'
    aliases = ['html']
    filenames = ['*.html', '*.htm', '*.xhtml', '*.xslt']
    mimetypes = ['text/html', 'application/xhtml+xml']
    version_added = ''
    flags = re.IGNORECASE | re.DOTALL
    tokens = {'root': [('[^<&]+', Text), ('&\\S*?;', Name.Entity), ('\\<\\!\\[CDATA\\[.*?\\]\\]\\>', Comment.Preproc), ('<!--.*?-->', Comment.Multiline), ('<\\?.*?\\?>', Comment.Preproc), ('<![^>]*>', Comment.Preproc), ('(<)(\\s*)(script)(\\s*)', bygroups(Punctuation, Text, Name.Tag, Text), ('script-content', 'tag')), ('(<)(\\s*)(style)(\\s*)', bygroups(Punctuation, Text, Name.Tag, Text), ('style-content', 'tag')), ('(<)(\\s*)([\\w:.-]+)', bygroups(Punctuation, Text, Name.Tag), 'tag'), ('(<)(\\s*)(/)(\\s*)([\\w:.-]+)(\\s*)(>)', bygroups(Punctuation, Text, Punctuation, Text, Name.Tag, Text, Punctuation))], 'tag': [('\\s+', Text), ('([\\w:-]+\\s*)(=)(\\s*)', bygroups(Name.Attribute, Operator, Text), 'attr'), ('[\\w:-]+', Name.Attribute), ('(/?)(\\s*)(>)', bygroups(Punctuation, Text, Punctuation), '#pop')], 'script-content': [('(<)(\\s*)(/)(\\s*)(script)(\\s*)(>)', bygroups(Punctuation, Text, Punctuation, Text, Name.Tag, Text, Punctuation), '#pop'), ('.+?(?=<\\s*/\\s*script\\s*>)', using(JavascriptLexer)), ('.+?\\n', using(JavascriptLexer), '#pop'), ('.+', using(JavascriptLexer), '#pop')], 'style-content': [('(<)(\\s*)(/)(\\s*)(style)(\\s*)(>)', bygroups(Punctuation, Text, Punctuation, Text, Name.Tag, Text, Punctuation), '#pop'), ('.+?(?=<\\s*/\\s*style\\s*>)', using(CssLexer)), ('.+?\\n', using(CssLexer), '#pop'), ('.+', using(CssLexer), '#pop')], 'attr': [('".*?"', String, '#pop'), ("'.*?'", String, '#pop'), ('[^\\s>]+', String, '#pop')]}
    
    def analyse_text(text):
        if html_doctype_matches(text):
            return 0.5



class DtdLexer(RegexLexer):
    """
    A lexer for DTDs (Document Type Definitions).
    """
    flags = re.MULTILINE | re.DOTALL
    name = 'DTD'
    aliases = ['dtd']
    filenames = ['*.dtd']
    mimetypes = ['application/xml-dtd']
    url = 'https://en.wikipedia.org/wiki/Document_type_definition'
    version_added = '1.5'
    tokens = {'root': [include('common'), ('(<!ELEMENT)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Tag), 'element'), ('(<!ATTLIST)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Tag), 'attlist'), ('(<!ENTITY)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Entity), 'entity'), ('(<!NOTATION)(\\s+)(\\S+)', bygroups(Keyword, Text, Name.Tag), 'notation'), ('(<!\\[)([^\\[\\s]+)(\\s*)(\\[)', bygroups(Keyword, Name.Entity, Text, Keyword)), ('(<!DOCTYPE)(\\s+)([^>\\s]+)', bygroups(Keyword, Text, Name.Tag)), ('PUBLIC|SYSTEM', Keyword.Constant), ('[\\[\\]>]', Keyword)], 'common': [('\\s+', Text), ('(%|&)[^;]*;', Name.Entity), ('<!--', Comment, 'comment'), ('[(|)*,?+]', Operator), ('"[^"]*"', String.Double), ("\\'[^\\']*\\'", String.Single)], 'comment': [('[^-]+', Comment), ('-->', Comment, '#pop'), ('-', Comment)], 'element': [include('common'), ('EMPTY|ANY|#PCDATA', Keyword.Constant), ('[^>\\s|()?+*,]+', Name.Tag), ('>', Keyword, '#pop')], 'attlist': [include('common'), ('CDATA|IDREFS|IDREF|ID|NMTOKENS|NMTOKEN|ENTITIES|ENTITY|NOTATION', Keyword.Constant), ('#REQUIRED|#IMPLIED|#FIXED', Keyword.Constant), ('xml:space|xml:lang', Keyword.Reserved), ('[^>\\s|()?+*,]+', Name.Attribute), ('>', Keyword, '#pop')], 'entity': [include('common'), ('SYSTEM|PUBLIC|NDATA', Keyword.Constant), ('[^>\\s|()?+*,]+', Name.Entity), ('>', Keyword, '#pop')], 'notation': [include('common'), ('SYSTEM|PUBLIC', Keyword.Constant), ('[^>\\s|()?+*,]+', Name.Attribute), ('>', Keyword, '#pop')]}
    
    def analyse_text(text):
        if (not looks_like_xml(text) and (('<!ELEMENT' in text or '<!ATTLIST' in text or '<!ENTITY' in text))):
            return 0.8



class XmlLexer(RegexLexer):
    """
    Generic lexer for XML (eXtensible Markup Language).
    """
    flags = re.MULTILINE | re.DOTALL
    name = 'XML'
    aliases = ['xml']
    filenames = ['*.xml', '*.xsl', '*.rss', '*.xslt', '*.xsd', '*.wsdl', '*.wsf', '*.xbrl', '*.pom']
    mimetypes = ['text/xml', 'application/xml', 'image/svg+xml', 'application/rss+xml', 'application/atom+xml']
    url = 'https://www.w3.org/XML'
    version_added = ''
    tokens = {'root': [('[^<&\\s]+', Text), ('[^<&\\S]+', Whitespace), ('&\\S*?;', Name.Entity), ('\\<\\!\\[CDATA\\[.*?\\]\\]\\>', Comment.Preproc), ('<!--.*?-->', Comment.Multiline), ('<\\?.*?\\?>', Comment.Preproc), ('<![^>]*>', Comment.Preproc), ('<\\s*[\\w:.-]+', Name.Tag, 'tag'), ('<\\s*/\\s*[\\w:.-]+\\s*>', Name.Tag)], 'tag': [('\\s+', Whitespace), ('[\\w.:-]+\\s*=', Name.Attribute, 'attr'), ('/?\\s*>', Name.Tag, '#pop')], 'attr': [('\\s+', Whitespace), ('".*?"', String, '#pop'), ("'.*?'", String, '#pop'), ('[^\\s>]+', String, '#pop')]}
    
    def analyse_text(text):
        if looks_like_xml(text):
            return 0.45



class XsltLexer(XmlLexer):
    """
    A lexer for XSLT.
    """
    name = 'XSLT'
    aliases = ['xslt']
    filenames = ['*.xsl', '*.xslt', '*.xpl']
    mimetypes = ['application/xsl+xml', 'application/xslt+xml']
    url = 'https://www.w3.org/TR/xslt-30'
    version_added = '0.10'
    EXTRA_KEYWORDS = {'apply-imports', 'apply-templates', 'attribute', 'attribute-set', 'call-template', 'choose', 'comment', 'copy', 'copy-of', 'decimal-format', 'element', 'fallback', 'for-each', 'if', 'import', 'include', 'key', 'message', 'namespace-alias', 'number', 'otherwise', 'output', 'param', 'preserve-space', 'processing-instruction', 'sort', 'strip-space', 'stylesheet', 'template', 'text', 'transform', 'value-of', 'variable', 'when', 'with-param'}
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in XmlLexer.get_tokens_unprocessed(self, text):
            m = re.match('</?xsl:([^>]*)/?>?', value)
            if (token is Name.Tag and m and m.group(1) in self.EXTRA_KEYWORDS):
                yield (index, Keyword, value)
            else:
                yield (index, token, value)
    
    def analyse_text(text):
        if (looks_like_xml(text) and '<xsl' in text):
            return 0.8



class HamlLexer(ExtendedRegexLexer):
    """
    For Haml markup.
    """
    name = 'Haml'
    aliases = ['haml']
    filenames = ['*.haml']
    mimetypes = ['text/x-haml']
    url = 'https://haml.info'
    version_added = '1.3'
    flags = re.IGNORECASE
    _dot = '(?: \\|\\n(?=.* \\|)|.)'
    _comma_dot = '(?:,\\s*\\n|' + _dot + ')'
    tokens = {'root': [('[ \\t]*\\n', Text), ('[ \\t]*', _indentation)], 'css': [('\\.[\\w:-]+', Name.Class, 'tag'), ('\\#[\\w:-]+', Name.Function, 'tag')], 'eval-or-plain': [('[&!]?==', Punctuation, 'plain'), ('([&!]?[=~])(' + _comma_dot + '*\\n)', bygroups(Punctuation, using(RubyLexer)), 'root'), default('plain')], 'content': [include('css'), ('%[\\w:-]+', Name.Tag, 'tag'), ('!!!' + _dot + '*\\n', Name.Namespace, '#pop'), ('(/)(\\[' + _dot + '*?\\])(' + _dot + '*\\n)', bygroups(Comment, Comment.Special, Comment), '#pop'), ('/' + _dot + '*\\n', _starts_block(Comment, 'html-comment-block'), '#pop'), ('-#' + _dot + '*\\n', _starts_block(Comment.Preproc, 'haml-comment-block'), '#pop'), ('(-)(' + _comma_dot + '*\\n)', bygroups(Punctuation, using(RubyLexer)), '#pop'), (':' + _dot + '*\\n', _starts_block(Name.Decorator, 'filter-block'), '#pop'), include('eval-or-plain')], 'tag': [include('css'), ('\\{(,\\n|' + _dot + ')*?\\}', using(RubyLexer)), ('\\[' + _dot + '*?\\]', using(RubyLexer)), ('\\(', Text, 'html-attributes'), ('/[ \\t]*\\n', Punctuation, '#pop:2'), ('[<>]{1,2}(?=[ \\t=])', Punctuation), include('eval-or-plain')], 'plain': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text), ('(#\\{)(' + _dot + '*?)(\\})', bygroups(String.Interpol, using(RubyLexer), String.Interpol)), ('\\n', Text, 'root')], 'html-attributes': [('\\s+', Text), ('[\\w:-]+[ \\t]*=', Name.Attribute, 'html-attribute-value'), ('[\\w:-]+', Name.Attribute), ('\\)', Text, '#pop')], 'html-attribute-value': [('[ \\t]+', Text), ('\\w+', Name.Variable, '#pop'), ('@\\w+', Name.Variable.Instance, '#pop'), ('\\$\\w+', Name.Variable.Global, '#pop'), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\\\n])*'", String, '#pop'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\\\n])*"', String, '#pop')], 'html-comment-block': [(_dot + '+', Comment), ('\\n', Text, 'root')], 'haml-comment-block': [(_dot + '+', Comment.Preproc), ('\\n', Text, 'root')], 'filter-block': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Name.Decorator), ('(#\\{)(' + _dot + '*?)(\\})', bygroups(String.Interpol, using(RubyLexer), String.Interpol)), ('\\n', Text, 'root')]}



class ScamlLexer(ExtendedRegexLexer):
    """
    For Scaml markup.  Scaml is Haml for Scala.
    """
    name = 'Scaml'
    aliases = ['scaml']
    filenames = ['*.scaml']
    mimetypes = ['text/x-scaml']
    url = 'https://scalate.github.io/scalate/'
    version_added = '1.4'
    flags = re.IGNORECASE
    _dot = '.'
    tokens = {'root': [('[ \\t]*\\n', Text), ('[ \\t]*', _indentation)], 'css': [('\\.[\\w:-]+', Name.Class, 'tag'), ('\\#[\\w:-]+', Name.Function, 'tag')], 'eval-or-plain': [('[&!]?==', Punctuation, 'plain'), ('([&!]?[=~])(' + _dot + '*\\n)', bygroups(Punctuation, using(ScalaLexer)), 'root'), default('plain')], 'content': [include('css'), ('%[\\w:-]+', Name.Tag, 'tag'), ('!!!' + _dot + '*\\n', Name.Namespace, '#pop'), ('(/)(\\[' + _dot + '*?\\])(' + _dot + '*\\n)', bygroups(Comment, Comment.Special, Comment), '#pop'), ('/' + _dot + '*\\n', _starts_block(Comment, 'html-comment-block'), '#pop'), ('-#' + _dot + '*\\n', _starts_block(Comment.Preproc, 'scaml-comment-block'), '#pop'), ('(-@\\s*)(import)?(' + _dot + '*\\n)', bygroups(Punctuation, Keyword, using(ScalaLexer)), '#pop'), ('(-)(' + _dot + '*\\n)', bygroups(Punctuation, using(ScalaLexer)), '#pop'), (':' + _dot + '*\\n', _starts_block(Name.Decorator, 'filter-block'), '#pop'), include('eval-or-plain')], 'tag': [include('css'), ('\\{(,\\n|' + _dot + ')*?\\}', using(ScalaLexer)), ('\\[' + _dot + '*?\\]', using(ScalaLexer)), ('\\(', Text, 'html-attributes'), ('/[ \\t]*\\n', Punctuation, '#pop:2'), ('[<>]{1,2}(?=[ \\t=])', Punctuation), include('eval-or-plain')], 'plain': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text), ('(#\\{)(' + _dot + '*?)(\\})', bygroups(String.Interpol, using(ScalaLexer), String.Interpol)), ('\\n', Text, 'root')], 'html-attributes': [('\\s+', Text), ('[\\w:-]+[ \\t]*=', Name.Attribute, 'html-attribute-value'), ('[\\w:-]+', Name.Attribute), ('\\)', Text, '#pop')], 'html-attribute-value': [('[ \\t]+', Text), ('\\w+', Name.Variable, '#pop'), ('@\\w+', Name.Variable.Instance, '#pop'), ('\\$\\w+', Name.Variable.Global, '#pop'), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\\\n])*'", String, '#pop'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\\\n])*"', String, '#pop')], 'html-comment-block': [(_dot + '+', Comment), ('\\n', Text, 'root')], 'scaml-comment-block': [(_dot + '+', Comment.Preproc), ('\\n', Text, 'root')], 'filter-block': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Name.Decorator), ('(#\\{)(' + _dot + '*?)(\\})', bygroups(String.Interpol, using(ScalaLexer), String.Interpol)), ('\\n', Text, 'root')]}



class PugLexer(ExtendedRegexLexer):
    """
    For Pug markup.
    Pug is a variant of Scaml, see:
    http://scalate.fusesource.org/documentation/scaml-reference.html
    """
    name = 'Pug'
    aliases = ['pug', 'jade']
    filenames = ['*.pug', '*.jade']
    mimetypes = ['text/x-pug', 'text/x-jade']
    url = 'https://pugjs.org'
    version_added = '1.4'
    flags = re.IGNORECASE
    _dot = '.'
    tokens = {'root': [('[ \\t]*\\n', Text), ('[ \\t]*', _indentation)], 'css': [('\\.[\\w:-]+', Name.Class, 'tag'), ('\\#[\\w:-]+', Name.Function, 'tag')], 'eval-or-plain': [('[&!]?==', Punctuation, 'plain'), ('([&!]?[=~])(' + _dot + '*\\n)', bygroups(Punctuation, using(ScalaLexer)), 'root'), default('plain')], 'content': [include('css'), ('!!!' + _dot + '*\\n', Name.Namespace, '#pop'), ('(/)(\\[' + _dot + '*?\\])(' + _dot + '*\\n)', bygroups(Comment, Comment.Special, Comment), '#pop'), ('/' + _dot + '*\\n', _starts_block(Comment, 'html-comment-block'), '#pop'), ('-#' + _dot + '*\\n', _starts_block(Comment.Preproc, 'scaml-comment-block'), '#pop'), ('(-@\\s*)(import)?(' + _dot + '*\\n)', bygroups(Punctuation, Keyword, using(ScalaLexer)), '#pop'), ('(-)(' + _dot + '*\\n)', bygroups(Punctuation, using(ScalaLexer)), '#pop'), (':' + _dot + '*\\n', _starts_block(Name.Decorator, 'filter-block'), '#pop'), ('[\\w:-]+', Name.Tag, 'tag'), ('\\|', Text, 'eval-or-plain')], 'tag': [include('css'), ('\\{(,\\n|' + _dot + ')*?\\}', using(ScalaLexer)), ('\\[' + _dot + '*?\\]', using(ScalaLexer)), ('\\(', Text, 'html-attributes'), ('/[ \\t]*\\n', Punctuation, '#pop:2'), ('[<>]{1,2}(?=[ \\t=])', Punctuation), include('eval-or-plain')], 'plain': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Text), ('(#\\{)(' + _dot + '*?)(\\})', bygroups(String.Interpol, using(ScalaLexer), String.Interpol)), ('\\n', Text, 'root')], 'html-attributes': [('\\s+', Text), ('[\\w:-]+[ \\t]*=', Name.Attribute, 'html-attribute-value'), ('[\\w:-]+', Name.Attribute), ('\\)', Text, '#pop')], 'html-attribute-value': [('[ \\t]+', Text), ('\\w+', Name.Variable, '#pop'), ('@\\w+', Name.Variable.Instance, '#pop'), ('\\$\\w+', Name.Variable.Global, '#pop'), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\\\n])*'", String, '#pop'), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\\\n])*"', String, '#pop')], 'html-comment-block': [(_dot + '+', Comment), ('\\n', Text, 'root')], 'scaml-comment-block': [(_dot + '+', Comment.Preproc), ('\\n', Text, 'root')], 'filter-block': [('([^#\\n]|#[^{\\n]|(\\\\\\\\)*\\\\#\\{)+', Name.Decorator), ('(#\\{)(' + _dot + '*?)(\\})', bygroups(String.Interpol, using(ScalaLexer), String.Interpol)), ('\\n', Text, 'root')]}

JadeLexer = PugLexer


class UrlEncodedLexer(RegexLexer):
    """
    Lexer for urlencoded data
    """
    name = 'urlencoded'
    aliases = ['urlencoded']
    mimetypes = ['application/x-www-form-urlencoded']
    url = 'https://en.wikipedia.org/wiki/Percent-encoding'
    version_added = '2.16'
    tokens = {'root': [('([^&=]*)(=)([^=&]*)(&?)', bygroups(Name.Tag, Operator, String, Punctuation))]}



class VueLexer(HtmlLexer):
    """
    For Vue Single-File Component.
    """
    name = 'Vue'
    url = 'https://vuejs.org/api/sfc-spec.html'
    aliases = ['vue']
    filenames = ['*.vue']
    mimetypes = []
    version_added = '2.19'
    flags = re.IGNORECASE | re.DOTALL
    tokens = {'root': [('(\\{\\{)(.*?)(\\}\\})', bygroups(Comment.Preproc, using(JavascriptLexer), Comment.Preproc)), ('[^<&{]+', Text), inherit], 'tag': [('\\s+', Text), ('((?:[@:]|v-)(?:[.\\w:-]|\\[[^\\]]*?\\])+\\s*)(=)(\\s*)', bygroups(using(this, state=['name']), Operator, Text), 'attr-directive'), ('([\\w:-]+\\s*)(=)(\\s*)', bygroups(Name.Attribute, Operator, Text), 'attr'), ('[\\w:-]+', Name.Attribute), ('(/?)(\\s*)(>)', bygroups(Punctuation, Text, Punctuation), '#pop')], 'name': [('[\\w-]+', Name.Attribute), ('[:@.]', Punctuation), ('(\\[)([^\\]]*?)(\\])', bygroups(Comment.Preproc, using(JavascriptLexer), Comment.Preproc))], 'attr-directive': [('(["\\\'])(.*?)(\\1)', bygroups(String, using(JavascriptLexer), String), '#pop'), ('[^\\s>]+', using(JavascriptLexer), '#pop')]}



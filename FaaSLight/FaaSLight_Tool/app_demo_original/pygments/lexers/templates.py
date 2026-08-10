"""
    pygments.lexers.templates
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for various template engines' markup.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexers.html import HtmlLexer, XmlLexer
from pygments.lexers.javascript import JavascriptLexer, LassoLexer
from pygments.lexers.css import CssLexer
from pygments.lexers.php import PhpLexer
from pygments.lexers.python import PythonLexer
from pygments.lexers.perl import PerlLexer
from pygments.lexers.jvm import JavaLexer, TeaLangLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers.sql import SqlLexer
from pygments.lexer import Lexer, DelegatingLexer, RegexLexer, bygroups, include, using, this, default, combined
from pygments.token import Error, Punctuation, Whitespace, Text, Comment, Operator, Keyword, Name, String, Number, Other, Token
from pygments.util import html_doctype_matches, looks_like_xml
__all__ = ['HtmlPhpLexer', 'XmlPhpLexer', 'CssPhpLexer', 'JavascriptPhpLexer', 'ErbLexer', 'RhtmlLexer', 'XmlErbLexer', 'CssErbLexer', 'JavascriptErbLexer', 'SmartyLexer', 'HtmlSmartyLexer', 'XmlSmartyLexer', 'CssSmartyLexer', 'JavascriptSmartyLexer', 'DjangoLexer', 'HtmlDjangoLexer', 'CssDjangoLexer', 'XmlDjangoLexer', 'JavascriptDjangoLexer', 'GenshiLexer', 'HtmlGenshiLexer', 'GenshiTextLexer', 'CssGenshiLexer', 'JavascriptGenshiLexer', 'MyghtyLexer', 'MyghtyHtmlLexer', 'MyghtyXmlLexer', 'MyghtyCssLexer', 'MyghtyJavascriptLexer', 'MasonLexer', 'MakoLexer', 'MakoHtmlLexer', 'MakoXmlLexer', 'MakoJavascriptLexer', 'MakoCssLexer', 'JspLexer', 'CheetahLexer', 'CheetahHtmlLexer', 'CheetahXmlLexer', 'CheetahJavascriptLexer', 'EvoqueLexer', 'EvoqueHtmlLexer', 'EvoqueXmlLexer', 'ColdfusionLexer', 'ColdfusionHtmlLexer', 'ColdfusionCFCLexer', 'VelocityLexer', 'VelocityHtmlLexer', 'VelocityXmlLexer', 'SspLexer', 'TeaTemplateLexer', 'LassoHtmlLexer', 'LassoXmlLexer', 'LassoCssLexer', 'LassoJavascriptLexer', 'HandlebarsLexer', 'HandlebarsHtmlLexer', 'YamlJinjaLexer', 'LiquidLexer', 'TwigLexer', 'TwigHtmlLexer', 'Angular2Lexer', 'Angular2HtmlLexer', 'SqlJinjaLexer']


class ErbLexer(Lexer):
    """
    Generic ERB (Ruby Templating) lexer.

    Just highlights ruby code between the preprocessor directives, other data
    is left untouched by the lexer.

    All options are also forwarded to the `RubyLexer`.
    """
    name = 'ERB'
    url = 'https://github.com/ruby/erb'
    aliases = ['erb']
    mimetypes = ['application/x-ruby-templating']
    version_added = ''
    _block_re = re.compile('(<%%|%%>|<%=|<%#|<%-|<%|-%>|%>|^%[^%].*?$)', re.M)
    
    def __init__(self, **options):
        from pygments.lexers.ruby import RubyLexer
        self.ruby_lexer = RubyLexer(**options)
        Lexer.__init__(self, **options)
    
    def get_tokens_unprocessed(self, text):
        """
        Since ERB doesn't allow "<%" and other tags inside of ruby
        blocks we have to use a split approach here that fails for
        that too.
        """
        tokens = self._block_re.split(text)
        tokens.reverse()
        state = idx = 0
        try:
            while True:
                if state == 0:
                    val = tokens.pop()
                    yield (idx, Other, val)
                    idx += len(val)
                    state = 1
                elif state == 1:
                    tag = tokens.pop()
                    if tag in ('<%%', '%%>'):
                        yield (idx, Other, tag)
                        idx += 3
                        state = 0
                    elif tag == '<%#':
                        yield (idx, Comment.Preproc, tag)
                        val = tokens.pop()
                        yield (idx + 3, Comment, val)
                        idx += 3 + len(val)
                        state = 2
                    elif tag in ('<%', '<%=', '<%-'):
                        yield (idx, Comment.Preproc, tag)
                        idx += len(tag)
                        data = tokens.pop()
                        r_idx = 0
                        for (r_idx, r_token, r_value) in self.ruby_lexer.get_tokens_unprocessed(data):
                            yield (r_idx + idx, r_token, r_value)
                        idx += len(data)
                        state = 2
                    elif tag in ('%>', '-%>'):
                        yield (idx, Error, tag)
                        idx += len(tag)
                        state = 0
                    else:
                        yield (idx, Comment.Preproc, tag[0])
                        r_idx = 0
                        for (r_idx, r_token, r_value) in self.ruby_lexer.get_tokens_unprocessed(tag[1:]):
                            yield (idx + 1 + r_idx, r_token, r_value)
                        idx += len(tag)
                        state = 0
                elif state == 2:
                    tag = tokens.pop()
                    if tag not in ('%>', '-%>'):
                        yield (idx, Other, tag)
                    else:
                        yield (idx, Comment.Preproc, tag)
                    idx += len(tag)
                    state = 0
        except IndexError:
            return
    
    def analyse_text(text):
        if ('<%' in text and '%>' in text):
            return 0.4



class SmartyLexer(RegexLexer):
    """
    Generic Smarty template lexer.

    Just highlights smarty code between the preprocessor directives, other
    data is left untouched by the lexer.
    """
    name = 'Smarty'
    url = 'https://www.smarty.net/'
    aliases = ['smarty']
    filenames = ['*.tpl']
    mimetypes = ['application/x-smarty']
    version_added = ''
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('[^{]+', Other), ('(\\{)(\\*.*?\\*)(\\})', bygroups(Comment.Preproc, Comment, Comment.Preproc)), ('(\\{php\\})(.*?)(\\{/php\\})', bygroups(Comment.Preproc, using(PhpLexer, startinline=True), Comment.Preproc)), ('(\\{)(/?[a-zA-Z_]\\w*)(\\s*)', bygroups(Comment.Preproc, Name.Function, Text), 'smarty'), ('\\{', Comment.Preproc, 'smarty')], 'smarty': [('\\s+', Text), ('\\{', Comment.Preproc, '#push'), ('\\}', Comment.Preproc, '#pop'), ('#[a-zA-Z_]\\w*#', Name.Variable), ('\\$[a-zA-Z_]\\w*(\\.\\w+)*', Name.Variable), ('[~!%^&*()+=|\\[\\]:;,.<>/?@-]', Operator), ('(true|false|null)\\b', Keyword.Constant), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[a-zA-Z_]\\w*', Name.Attribute)]}
    
    def analyse_text(text):
        rv = 0.0
        if re.search('\\{if\\s+.*?\\}.*?\\{/if\\}', text):
            rv += 0.15
        if re.search('\\{include\\s+file=.*?\\}', text):
            rv += 0.15
        if re.search('\\{foreach\\s+.*?\\}.*?\\{/foreach\\}', text):
            rv += 0.15
        if re.search('\\{\\$.*?\\}', text):
            rv += 0.01
        return rv



class VelocityLexer(RegexLexer):
    """
    Generic Velocity template lexer.

    Just highlights velocity directives and variable references, other
    data is left untouched by the lexer.
    """
    name = 'Velocity'
    url = 'https://velocity.apache.org/'
    aliases = ['velocity']
    filenames = ['*.vm', '*.fhtml']
    version_added = ''
    flags = re.MULTILINE | re.DOTALL
    identifier = '[a-zA-Z_]\\w*'
    tokens = {'root': [('[^{#$]+', Other), ('(#)(\\*.*?\\*)(#)', bygroups(Comment.Preproc, Comment, Comment.Preproc)), ('(##)(.*?$)', bygroups(Comment.Preproc, Comment)), ('(#\\{?)(' + identifier + ')(\\}?)(\\s?\\()', bygroups(Comment.Preproc, Name.Function, Comment.Preproc, Punctuation), 'directiveparams'), ('(#\\{?)(' + identifier + ')(\\}|\\b)', bygroups(Comment.Preproc, Name.Function, Comment.Preproc)), ('\\$!?\\{?', Punctuation, 'variable')], 'variable': [(identifier, Name.Variable), ('\\(', Punctuation, 'funcparams'), ('(\\.)(' + identifier + ')', bygroups(Punctuation, Name.Variable), '#push'), ('\\}', Punctuation, '#pop'), default('#pop')], 'directiveparams': [('(&&|\\|\\||==?|!=?|[-<>+*%&|^/])|\\b(eq|ne|gt|lt|ge|le|not|in)\\b', Operator), ('\\[', Operator, 'rangeoperator'), ('\\b' + identifier + '\\b', Name.Function), include('funcparams')], 'rangeoperator': [('\\.\\.', Operator), include('funcparams'), ('\\]', Operator, '#pop')], 'funcparams': [('\\$!?\\{?', Punctuation, 'variable'), ('\\s+', Text), ('[,:]', Punctuation), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('0[xX][0-9a-fA-F]+[Ll]?', Number), ('\\b[0-9]+\\b', Number), ('(true|false|null)\\b', Keyword.Constant), ('\\(', Punctuation, '#push'), ('\\)', Punctuation, '#pop'), ('\\{', Punctuation, '#push'), ('\\}', Punctuation, '#pop'), ('\\[', Punctuation, '#push'), ('\\]', Punctuation, '#pop')]}
    
    def analyse_text(text):
        rv = 0.0
        if re.search('#\\{?macro\\}?\\(.*?\\).*?#\\{?end\\}?', text, re.DOTALL):
            rv += 0.25
        if re.search('#\\{?if\\}?\\(.+?\\).*?#\\{?end\\}?', text, re.DOTALL):
            rv += 0.15
        if re.search('#\\{?foreach\\}?\\(.+?\\).*?#\\{?end\\}?', text, re.DOTALL):
            rv += 0.15
        if re.search('\\$!?\\{?[a-zA-Z_]\\w*(\\([^)]*\\))?(\\.\\w+(\\([^)]*\\))?)*\\}?', text):
            rv += 0.01
        return rv



class VelocityHtmlLexer(DelegatingLexer):
    """
    Subclass of the `VelocityLexer` that highlights unlexed data
    with the `HtmlLexer`.

    """
    name = 'HTML+Velocity'
    aliases = ['html+velocity']
    version_added = ''
    alias_filenames = ['*.html', '*.fhtml']
    mimetypes = ['text/html+velocity']
    url = 'https://velocity.apache.org/'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, VelocityLexer, **options)



class VelocityXmlLexer(DelegatingLexer):
    """
    Subclass of the `VelocityLexer` that highlights unlexed data
    with the `XmlLexer`.

    """
    name = 'XML+Velocity'
    aliases = ['xml+velocity']
    version_added = ''
    alias_filenames = ['*.xml', '*.vm']
    mimetypes = ['application/xml+velocity']
    url = 'https://velocity.apache.org/'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, VelocityLexer, **options)
    
    def analyse_text(text):
        rv = VelocityLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv



class DjangoLexer(RegexLexer):
    """
    Generic `Django <https://www.djangoproject.com/documentation/templates/>`_
    and `Jinja <https://jinja.palletsprojects.com>`_ template lexer.

    It just highlights django/jinja code between the preprocessor directives,
    other data is left untouched by the lexer.
    """
    name = 'Django/Jinja'
    aliases = ['django', 'jinja']
    mimetypes = ['application/x-django-templating', 'application/x-jinja']
    url = 'https://www.djangoproject.com/documentation/templates'
    version_added = ''
    flags = re.M | re.S
    tokens = {'root': [('[^{]+', Other), ('\\{\\{', Comment.Preproc, 'var'), ('\\{#.*?#\\}', Comment), ('(\\{%)(-?\\s*)(comment)(\\s*-?)(%\\})(.*?)(\\{%)(-?\\s*)(endcomment)(\\s*-?)(%\\})', bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc, Comment, Comment.Preproc, Text, Keyword, Text, Comment.Preproc)), ('(\\{%)(-?\\s*)(raw)(\\s*-?)(%\\})(.*?)(\\{%)(-?\\s*)(endraw)(\\s*-?)(%\\})', bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc, Text, Comment.Preproc, Text, Keyword, Text, Comment.Preproc)), ('(\\{%)(-?\\s*)(filter)(\\s+)([a-zA-Z_]\\w*)', bygroups(Comment.Preproc, Text, Keyword, Text, Name.Function), 'block'), ('(\\{%)(-?\\s*)([a-zA-Z_]\\w*)', bygroups(Comment.Preproc, Text, Keyword), 'block'), ('\\{', Other)], 'varnames': [('(\\|)(\\s*)([a-zA-Z_]\\w*)', bygroups(Operator, Text, Name.Function)), ('(is)(\\s+)(not)?(\\s+)?([a-zA-Z_]\\w*)', bygroups(Keyword, Text, Keyword, Text, Name.Function)), ('(_|true|false|none|True|False|None)\\b', Keyword.Pseudo), ('(in|as|reversed|recursive|not|and|or|is|if|else|import|with(?:(?:out)?\\s*context)?|scoped|ignore\\s+missing)\\b', Keyword), ('(loop|block|super|forloop)\\b', Name.Builtin), ('[a-zA-Z_][\\w-]*', Name.Variable), ('\\.\\w+', Name.Variable), (':?"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), (":?'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('([{}()\\[\\]+\\-*/%,:~]|[><=]=?|!=)', Operator), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number)], 'var': [('\\s+', Text), ('(-?)(\\}\\})', bygroups(Text, Comment.Preproc), '#pop'), include('varnames')], 'block': [('\\s+', Text), ('(-?)(%\\})', bygroups(Text, Comment.Preproc), '#pop'), include('varnames'), ('.', Punctuation)]}
    
    def analyse_text(text):
        rv = 0.0
        if re.search('\\{%\\s*(block|extends)', text) is not None:
            rv += 0.4
        if re.search('\\{%\\s*if\\s*.*?%\\}', text) is not None:
            rv += 0.1
        if re.search('\\{\\{.*?\\}\\}', text) is not None:
            rv += 0.1
        return rv



class MyghtyLexer(RegexLexer):
    """
    Generic myghty templates lexer. Code that isn't Myghty
    markup is yielded as `Token.Other`.
    """
    name = 'Myghty'
    url = 'http://www.myghty.org/'
    aliases = ['myghty']
    filenames = ['*.myt', 'autodelegate']
    mimetypes = ['application/x-myghty']
    version_added = '0.6'
    tokens = {'root': [('\\s+', Text), ('(?s)(<%(?:def|method))(\\s*)(.*?)(>)(.*?)(</%\\2\\s*>)', bygroups(Name.Tag, Text, Name.Function, Name.Tag, using(this), Name.Tag)), ('(?s)(<%\\w+)(.*?)(>)(.*?)(</%\\2\\s*>)', bygroups(Name.Tag, Name.Function, Name.Tag, using(PythonLexer), Name.Tag)), ('(<&[^|])(.*?)(,.*?)?(&>)', bygroups(Name.Tag, Name.Function, using(PythonLexer), Name.Tag)), ('(?s)(<&\\|)(.*?)(,.*?)?(&>)', bygroups(Name.Tag, Name.Function, using(PythonLexer), Name.Tag)), ('</&>', Name.Tag), ('(?s)(<%!?)(.*?)(%>)', bygroups(Name.Tag, using(PythonLexer), Name.Tag)), ('(?<=^)#[^\\n]*(\\n|\\Z)', Comment), ('(?<=^)(%)([^\\n]*)(\\n|\\Z)', bygroups(Name.Tag, using(PythonLexer), Other)), ("(?sx)\n                 (.+?)               # anything, followed by:\n                 (?:\n                  (?<=\\n)(?=[%#]) |  # an eval or comment line\n                  (?=</?[%&]) |      # a substitution or block or\n                                     # call start or end\n                                     # - don't consume\n                  (\\\\\\n) |           # an escaped newline\n                  \\Z                 # end of string\n                 )", bygroups(Other, Operator))]}



class MyghtyHtmlLexer(DelegatingLexer):
    """
    Subclass of the `MyghtyLexer` that highlights unlexed data
    with the `HtmlLexer`.
    """
    name = 'HTML+Myghty'
    aliases = ['html+myghty']
    mimetypes = ['text/html+myghty']
    url = 'http://www.myghty.org/'
    version_added = '0.6'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, MyghtyLexer, **options)



class MyghtyXmlLexer(DelegatingLexer):
    """
    Subclass of the `MyghtyLexer` that highlights unlexed data
    with the `XmlLexer`.
    """
    name = 'XML+Myghty'
    aliases = ['xml+myghty']
    mimetypes = ['application/xml+myghty']
    url = 'http://www.myghty.org/'
    version_added = '0.6'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, MyghtyLexer, **options)



class MyghtyJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `MyghtyLexer` that highlights unlexed data
    with the `JavascriptLexer`.
    """
    name = 'JavaScript+Myghty'
    aliases = ['javascript+myghty', 'js+myghty']
    mimetypes = ['application/x-javascript+myghty', 'text/x-javascript+myghty', 'text/javascript+mygthy']
    url = 'http://www.myghty.org/'
    version_added = '0.6'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, MyghtyLexer, **options)



class MyghtyCssLexer(DelegatingLexer):
    """
    Subclass of the `MyghtyLexer` that highlights unlexed data
    with the `CssLexer`.
    """
    name = 'CSS+Myghty'
    aliases = ['css+myghty']
    mimetypes = ['text/css+myghty']
    url = 'http://www.myghty.org/'
    version_added = '0.6'
    
    def __init__(self, **options):
        super().__init__(CssLexer, MyghtyLexer, **options)



class MasonLexer(RegexLexer):
    """
    Generic mason templates lexer. Stolen from Myghty lexer. Code that isn't
    Mason markup is HTML.
    """
    name = 'Mason'
    url = 'http://www.masonhq.com/'
    aliases = ['mason']
    filenames = ['*.m', '*.mhtml', '*.mc', '*.mi', 'autohandler', 'dhandler']
    mimetypes = ['application/x-mason']
    version_added = '1.4'
    tokens = {'root': [('\\s+', Whitespace), ('(?s)(<%doc>)(.*?)(</%doc>)', bygroups(Name.Tag, Comment.Multiline, Name.Tag)), ('(?s)(<%(?:def|method))(\\s*)(.*?)(>)(.*?)(</%\\2\\s*>)', bygroups(Name.Tag, Whitespace, Name.Function, Name.Tag, using(this), Name.Tag)), ('(?s)(<%(\\w+)(.*?)(>))(.*?)(</%\\2\\s*>)', bygroups(Name.Tag, None, None, None, using(PerlLexer), Name.Tag)), ('(?s)(<&[^|])(.*?)(,.*?)?(&>)', bygroups(Name.Tag, Name.Function, using(PerlLexer), Name.Tag)), ('(?s)(<&\\|)(.*?)(,.*?)?(&>)', bygroups(Name.Tag, Name.Function, using(PerlLexer), Name.Tag)), ('</&>', Name.Tag), ('(?s)(<%!?)(.*?)(%>)', bygroups(Name.Tag, using(PerlLexer), Name.Tag)), ('(?<=^)#[^\\n]*(\\n|\\Z)', Comment), ('(?<=^)(%)([^\\n]*)(\\n|\\Z)', bygroups(Name.Tag, using(PerlLexer), Other)), ("(?sx)\n                 (.+?)               # anything, followed by:\n                 (?:\n                  (?<=\\n)(?=[%#]) |  # an eval or comment line\n                  (?=</?[%&]) |      # a substitution or block or\n                                     # call start or end\n                                     # - don't consume\n                  (\\\\\\n) |           # an escaped newline\n                  \\Z                 # end of string\n                 )", bygroups(using(HtmlLexer), Operator))]}
    
    def analyse_text(text):
        result = 0.0
        if re.search('</%(class|doc|init)>', text) is not None:
            result = 1.0
        elif re.search('<&.+&>', text, re.DOTALL) is not None:
            result = 0.11
        return result



class MakoLexer(RegexLexer):
    """
    Generic mako templates lexer. Code that isn't Mako
    markup is yielded as `Token.Other`.
    """
    name = 'Mako'
    url = 'http://www.makotemplates.org/'
    aliases = ['mako']
    filenames = ['*.mao']
    mimetypes = ['application/x-mako']
    version_added = '0.7'
    tokens = {'root': [('(\\s*)(%)(\\s*end(?:\\w+))(\\n|\\Z)', bygroups(Text.Whitespace, Comment.Preproc, Keyword, Other)), ('(\\s*)(%)([^\\n]*)(\\n|\\Z)', bygroups(Text.Whitespace, Comment.Preproc, using(PythonLexer), Other)), ('(\\s*)(##[^\\n]*)(\\n|\\Z)', bygroups(Text.Whitespace, Comment.Single, Text.Whitespace)), ('(?s)<%doc>.*?</%doc>', Comment.Multiline), ('(<%)([\\w.:]+)', bygroups(Comment.Preproc, Name.Builtin), 'tag'), ('(</%)([\\w.:]+)(>)', bygroups(Comment.Preproc, Name.Builtin, Comment.Preproc)), ('<%(?=([\\w.:]+))', Comment.Preproc, 'ondeftags'), ('(?s)(<%(?:!?))(.*?)(%>)', bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)), ('(\\$\\{)(.*?)(\\})', bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)), ("(?sx)\n                (.+?)                # anything, followed by:\n                (?:\n                 (?<=\\n)(?=%|\\#\\#) | # an eval or comment line\n                 (?=\\#\\*) |          # multiline comment\n                 (?=</?%) |          # a python block\n                                     # call start or end\n                 (?=\\$\\{) |          # a substitution\n                 (?<=\\n)(?=\\s*%) |\n                                     # - don't consume\n                 (\\\\\\n) |            # an escaped newline\n                 \\Z                  # end of string\n                )\n            ", bygroups(Other, Operator)), ('\\s+', Text)], 'ondeftags': [('<%', Comment.Preproc), ('(?<=<%)(include|inherit|namespace|page)', Name.Builtin), include('tag')], 'tag': [('((?:\\w+)\\s*=)(\\s*)(".*?")', bygroups(Name.Attribute, Text, String)), ('/?\\s*>', Comment.Preproc, '#pop'), ('\\s+', Text)], 'attr': [('".*?"', String, '#pop'), ("'.*?'", String, '#pop'), ('[^\\s>]+', String, '#pop')]}



class MakoHtmlLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `HtmlLexer`.
    """
    name = 'HTML+Mako'
    aliases = ['html+mako']
    mimetypes = ['text/html+mako']
    url = 'http://www.makotemplates.org/'
    version_added = '0.7'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, MakoLexer, **options)



class MakoXmlLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `XmlLexer`.
    """
    name = 'XML+Mako'
    aliases = ['xml+mako']
    mimetypes = ['application/xml+mako']
    url = 'http://www.makotemplates.org/'
    version_added = '0.7'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, MakoLexer, **options)



class MakoJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `JavascriptLexer`.
    """
    name = 'JavaScript+Mako'
    aliases = ['javascript+mako', 'js+mako']
    mimetypes = ['application/x-javascript+mako', 'text/x-javascript+mako', 'text/javascript+mako']
    url = 'http://www.makotemplates.org/'
    version_added = '0.7'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, MakoLexer, **options)



class MakoCssLexer(DelegatingLexer):
    """
    Subclass of the `MakoLexer` that highlights unlexed data
    with the `CssLexer`.
    """
    name = 'CSS+Mako'
    aliases = ['css+mako']
    mimetypes = ['text/css+mako']
    url = 'http://www.makotemplates.org/'
    version_added = '0.7'
    
    def __init__(self, **options):
        super().__init__(CssLexer, MakoLexer, **options)



class CheetahPythonLexer(Lexer):
    """
    Lexer for handling Cheetah's special $ tokens in Python syntax.
    """
    
    def get_tokens_unprocessed(self, text):
        pylexer = PythonLexer(**self.options)
        for (pos, type_, value) in pylexer.get_tokens_unprocessed(text):
            if (type_ == Token.Error and value == '$'):
                type_ = Comment.Preproc
            yield (pos, type_, value)



class CheetahLexer(RegexLexer):
    """
    Generic cheetah templates lexer. Code that isn't Cheetah
    markup is yielded as `Token.Other`.  This also works for
    `spitfire templates`_ which use the same syntax.

    .. _spitfire templates: http://code.google.com/p/spitfire/
    """
    name = 'Cheetah'
    url = 'http://www.cheetahtemplate.org/'
    aliases = ['cheetah', 'spitfire']
    filenames = ['*.tmpl', '*.spt']
    mimetypes = ['application/x-cheetah', 'application/x-spitfire']
    version_added = ''
    tokens = {'root': [('(##[^\\n]*)$', bygroups(Comment)), ('#[*](.|\\n)*?[*]#', Comment), ('#end[^#\\n]*(?:#|$)', Comment.Preproc), ('#slurp$', Comment.Preproc), ('(#[a-zA-Z]+)([^#\\n]*)(#|$)', bygroups(Comment.Preproc, using(CheetahPythonLexer), Comment.Preproc)), ('(\\$)([a-zA-Z_][\\w.]*\\w)', bygroups(Comment.Preproc, using(CheetahPythonLexer))), ('(?s)(\\$\\{!?)(.*?)(\\})', bygroups(Comment.Preproc, using(CheetahPythonLexer), Comment.Preproc)), ('(?sx)\n                (.+?)               # anything, followed by:\n                (?:\n                 (?=\\#[#a-zA-Z]*) | # an eval comment\n                 (?=\\$[a-zA-Z_{]) | # a substitution\n                 \\Z                 # end of string\n                )\n            ', Other), ('\\s+', Text)]}



class CheetahHtmlLexer(DelegatingLexer):
    """
    Subclass of the `CheetahLexer` that highlights unlexed data
    with the `HtmlLexer`.
    """
    name = 'HTML+Cheetah'
    aliases = ['html+cheetah', 'html+spitfire', 'htmlcheetah']
    mimetypes = ['text/html+cheetah', 'text/html+spitfire']
    url = 'http://www.cheetahtemplate.org/'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, CheetahLexer, **options)



class CheetahXmlLexer(DelegatingLexer):
    """
    Subclass of the `CheetahLexer` that highlights unlexed data
    with the `XmlLexer`.
    """
    name = 'XML+Cheetah'
    aliases = ['xml+cheetah', 'xml+spitfire']
    mimetypes = ['application/xml+cheetah', 'application/xml+spitfire']
    url = 'http://www.cheetahtemplate.org/'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(XmlLexer, CheetahLexer, **options)



class CheetahJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `CheetahLexer` that highlights unlexed data
    with the `JavascriptLexer`.
    """
    name = 'JavaScript+Cheetah'
    aliases = ['javascript+cheetah', 'js+cheetah', 'javascript+spitfire', 'js+spitfire']
    mimetypes = ['application/x-javascript+cheetah', 'text/x-javascript+cheetah', 'text/javascript+cheetah', 'application/x-javascript+spitfire', 'text/x-javascript+spitfire', 'text/javascript+spitfire']
    url = 'http://www.cheetahtemplate.org/'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, CheetahLexer, **options)



class GenshiTextLexer(RegexLexer):
    """
    A lexer that highlights genshi text templates.
    """
    name = 'Genshi Text'
    url = 'https://genshi.edgewall.org/'
    aliases = ['genshitext']
    mimetypes = ['application/x-genshi-text', 'text/x-genshi']
    version_added = ''
    tokens = {'root': [('[^#$\\s]+', Other), ('^(\\s*)(##.*)$', bygroups(Text, Comment)), ('^(\\s*)(#)', bygroups(Text, Comment.Preproc), 'directive'), include('variable'), ('[#$\\s]', Other)], 'directive': [('\\n', Text, '#pop'), ('(?:def|for|if)\\s+.*', using(PythonLexer), '#pop'), ('(choose|when|with)([^\\S\\n]+)(.*)', bygroups(Keyword, Text, using(PythonLexer)), '#pop'), ('(choose|otherwise)\\b', Keyword, '#pop'), ('(end\\w*)([^\\S\\n]*)(.*)', bygroups(Keyword, Text, Comment), '#pop')], 'variable': [('(?<!\\$)(\\$\\{)(.+?)(\\})', bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)), ('(?<!\\$)(\\$)([a-zA-Z_][\\w.]*)', Name.Variable)]}



class GenshiMarkupLexer(RegexLexer):
    """
    Base lexer for Genshi markup, used by `HtmlGenshiLexer` and
    `GenshiLexer`.
    """
    flags = re.DOTALL
    tokens = {'root': [('[^<$]+', Other), ('(<\\?python)(.*?)(\\?>)', bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)), ('<\\s*(script|style)\\s*.*?>.*?<\\s*/\\1\\s*>', Other), ('<\\s*py:[a-zA-Z0-9]+', Name.Tag, 'pytag'), ('<\\s*[a-zA-Z0-9:.]+', Name.Tag, 'tag'), include('variable'), ('[<$]', Other)], 'pytag': [('\\s+', Text), ('[\\w:-]+\\s*=', Name.Attribute, 'pyattr'), ('/?\\s*>', Name.Tag, '#pop')], 'pyattr': [('(")(.*?)(")', bygroups(String, using(PythonLexer), String), '#pop'), ("(')(.*?)(')", bygroups(String, using(PythonLexer), String), '#pop'), ('[^\\s>]+', String, '#pop')], 'tag': [('\\s+', Text), ('py:[\\w-]+\\s*=', Name.Attribute, 'pyattr'), ('[\\w:-]+\\s*=', Name.Attribute, 'attr'), ('/?\\s*>', Name.Tag, '#pop')], 'attr': [('"', String, 'attr-dstring'), ("'", String, 'attr-sstring'), ('[^\\s>]*', String, '#pop')], 'attr-dstring': [('"', String, '#pop'), include('strings'), ("'", String)], 'attr-sstring': [("'", String, '#pop'), include('strings'), ("'", String)], 'strings': [('[^"\'$]+', String), include('variable')], 'variable': [('(?<!\\$)(\\$\\{)(.+?)(\\})', bygroups(Comment.Preproc, using(PythonLexer), Comment.Preproc)), ('(?<!\\$)(\\$)([a-zA-Z_][\\w\\.]*)', Name.Variable)]}



class HtmlGenshiLexer(DelegatingLexer):
    """
    A lexer that highlights `genshi <https://genshi.edgewall.org/>`_ and
    `kid <http://kid-templating.org/>`_ kid HTML templates.
    """
    name = 'HTML+Genshi'
    aliases = ['html+genshi', 'html+kid']
    version_added = ''
    alias_filenames = ['*.html', '*.htm', '*.xhtml']
    mimetypes = ['text/html+genshi']
    url = 'https://genshi.edgewall.org/'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, GenshiMarkupLexer, **options)
    
    def analyse_text(text):
        rv = 0.0
        if re.search('\\$\\{.*?\\}', text) is not None:
            rv += 0.2
        if re.search('py:(.*?)=["\\\']', text) is not None:
            rv += 0.2
        return rv + HtmlLexer.analyse_text(text) - 0.01



class GenshiLexer(DelegatingLexer):
    """
    A lexer that highlights `genshi <https://genshi.edgewall.org/>`_ and
    `kid <http://kid-templating.org/>`_ kid XML templates.
    """
    name = 'Genshi'
    aliases = ['genshi', 'kid', 'xml+genshi', 'xml+kid']
    filenames = ['*.kid']
    version_added = ''
    alias_filenames = ['*.xml']
    mimetypes = ['application/x-genshi', 'application/x-kid']
    url = 'https://genshi.edgewall.org/'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, GenshiMarkupLexer, **options)
    
    def analyse_text(text):
        rv = 0.0
        if re.search('\\$\\{.*?\\}', text) is not None:
            rv += 0.2
        if re.search('py:(.*?)=["\\\']', text) is not None:
            rv += 0.2
        return rv + XmlLexer.analyse_text(text) - 0.01



class JavascriptGenshiLexer(DelegatingLexer):
    """
    A lexer that highlights javascript code in genshi text templates.
    """
    name = 'JavaScript+Genshi Text'
    aliases = ['js+genshitext', 'js+genshi', 'javascript+genshitext', 'javascript+genshi']
    version_added = ''
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+genshi', 'text/x-javascript+genshi', 'text/javascript+genshi']
    url = 'https://genshi.edgewall.org'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, GenshiTextLexer, **options)
    
    def analyse_text(text):
        return GenshiLexer.analyse_text(text) - 0.05



class CssGenshiLexer(DelegatingLexer):
    """
    A lexer that highlights CSS definitions in genshi text templates.
    """
    name = 'CSS+Genshi Text'
    aliases = ['css+genshitext', 'css+genshi']
    version_added = ''
    alias_filenames = ['*.css']
    mimetypes = ['text/css+genshi']
    url = 'https://genshi.edgewall.org'
    
    def __init__(self, **options):
        super().__init__(CssLexer, GenshiTextLexer, **options)
    
    def analyse_text(text):
        return GenshiLexer.analyse_text(text) - 0.05



class RhtmlLexer(DelegatingLexer):
    """
    Subclass of the ERB lexer that highlights the unlexed data with the
    html lexer.

    Nested Javascript and CSS is highlighted too.
    """
    name = 'RHTML'
    aliases = ['rhtml', 'html+erb', 'html+ruby']
    filenames = ['*.rhtml']
    version_added = ''
    alias_filenames = ['*.html', '*.htm', '*.xhtml']
    mimetypes = ['text/html+ruby']
    url = 'https://github.com/ruby/erb'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, ErbLexer, **options)
    
    def analyse_text(text):
        rv = ErbLexer.analyse_text(text) - 0.01
        if html_doctype_matches(text):
            rv += 0.5
        return rv



class XmlErbLexer(DelegatingLexer):
    """
    Subclass of `ErbLexer` which highlights data outside preprocessor
    directives with the `XmlLexer`.
    """
    name = 'XML+Ruby'
    aliases = ['xml+ruby', 'xml+erb']
    version_added = ''
    alias_filenames = ['*.xml']
    mimetypes = ['application/xml+ruby']
    url = 'https://github.com/ruby/erb'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, ErbLexer, **options)
    
    def analyse_text(text):
        rv = ErbLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv



class CssErbLexer(DelegatingLexer):
    """
    Subclass of `ErbLexer` which highlights unlexed data with the `CssLexer`.
    """
    name = 'CSS+Ruby'
    aliases = ['css+ruby', 'css+erb']
    version_added = ''
    alias_filenames = ['*.css']
    mimetypes = ['text/css+ruby']
    url = 'https://github.com/ruby/erb'
    
    def __init__(self, **options):
        super().__init__(CssLexer, ErbLexer, **options)
    
    def analyse_text(text):
        return ErbLexer.analyse_text(text) - 0.05



class JavascriptErbLexer(DelegatingLexer):
    """
    Subclass of `ErbLexer` which highlights unlexed data with the
    `JavascriptLexer`.
    """
    name = 'JavaScript+Ruby'
    aliases = ['javascript+ruby', 'js+ruby', 'javascript+erb', 'js+erb']
    version_added = ''
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+ruby', 'text/x-javascript+ruby', 'text/javascript+ruby']
    url = 'https://github.com/ruby/erb'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, ErbLexer, **options)
    
    def analyse_text(text):
        return ErbLexer.analyse_text(text) - 0.05



class HtmlPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` that highlights unhandled data with the `HtmlLexer`.

    Nested Javascript and CSS is highlighted too.
    """
    name = 'HTML+PHP'
    aliases = ['html+php']
    filenames = ['*.phtml']
    version_added = ''
    alias_filenames = ['*.php', '*.html', '*.htm', '*.xhtml', '*.php[345]']
    mimetypes = ['application/x-php', 'application/x-httpd-php', 'application/x-httpd-php3', 'application/x-httpd-php4', 'application/x-httpd-php5']
    url = 'https://www.php.net'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, PhpLexer, **options)
    
    def analyse_text(text):
        rv = PhpLexer.analyse_text(text) - 0.01
        if html_doctype_matches(text):
            rv += 0.5
        return rv



class XmlPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` that highlights unhandled data with the `XmlLexer`.
    """
    name = 'XML+PHP'
    aliases = ['xml+php']
    version_added = ''
    alias_filenames = ['*.xml', '*.php', '*.php[345]']
    mimetypes = ['application/xml+php']
    url = 'https://www.php.net'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, PhpLexer, **options)
    
    def analyse_text(text):
        rv = PhpLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv



class CssPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` which highlights unmatched data with the `CssLexer`.
    """
    name = 'CSS+PHP'
    aliases = ['css+php']
    version_added = ''
    alias_filenames = ['*.css']
    mimetypes = ['text/css+php']
    url = 'https://www.php.net'
    
    def __init__(self, **options):
        super().__init__(CssLexer, PhpLexer, **options)
    
    def analyse_text(text):
        return PhpLexer.analyse_text(text) - 0.05



class JavascriptPhpLexer(DelegatingLexer):
    """
    Subclass of `PhpLexer` which highlights unmatched data with the
    `JavascriptLexer`.
    """
    name = 'JavaScript+PHP'
    aliases = ['javascript+php', 'js+php']
    version_added = ''
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+php', 'text/x-javascript+php', 'text/javascript+php']
    url = 'https://www.php.net'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, PhpLexer, **options)
    
    def analyse_text(text):
        return PhpLexer.analyse_text(text)



class HtmlSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `HtmlLexer`.

    Nested Javascript and CSS is highlighted too.
    """
    name = 'HTML+Smarty'
    aliases = ['html+smarty']
    version_added = ''
    alias_filenames = ['*.html', '*.htm', '*.xhtml', '*.tpl']
    mimetypes = ['text/html+smarty']
    url = 'https://www.smarty.net/'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, SmartyLexer, **options)
    
    def analyse_text(text):
        rv = SmartyLexer.analyse_text(text) - 0.01
        if html_doctype_matches(text):
            rv += 0.5
        return rv



class XmlSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `XmlLexer`.
    """
    name = 'XML+Smarty'
    aliases = ['xml+smarty']
    version_added = ''
    alias_filenames = ['*.xml', '*.tpl']
    mimetypes = ['application/xml+smarty']
    url = 'https://www.smarty.net/'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, SmartyLexer, **options)
    
    def analyse_text(text):
        rv = SmartyLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv



class CssSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `CssLexer`.
    """
    name = 'CSS+Smarty'
    aliases = ['css+smarty']
    version_added = ''
    alias_filenames = ['*.css', '*.tpl']
    mimetypes = ['text/css+smarty']
    url = 'https://www.smarty.net/'
    
    def __init__(self, **options):
        super().__init__(CssLexer, SmartyLexer, **options)
    
    def analyse_text(text):
        return SmartyLexer.analyse_text(text) - 0.05



class JavascriptSmartyLexer(DelegatingLexer):
    """
    Subclass of the `SmartyLexer` that highlights unlexed data with the
    `JavascriptLexer`.
    """
    name = 'JavaScript+Smarty'
    aliases = ['javascript+smarty', 'js+smarty']
    version_added = ''
    alias_filenames = ['*.js', '*.tpl']
    mimetypes = ['application/x-javascript+smarty', 'text/x-javascript+smarty', 'text/javascript+smarty']
    url = 'https://www.smarty.net/'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, SmartyLexer, **options)
    
    def analyse_text(text):
        return SmartyLexer.analyse_text(text) - 0.05



class HtmlDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `HtmlLexer`.

    Nested Javascript and CSS is highlighted too.
    """
    name = 'HTML+Django/Jinja'
    aliases = ['html+django', 'html+jinja', 'htmldjango']
    filenames = ['*.html.j2', '*.htm.j2', '*.xhtml.j2', '*.html.jinja2', '*.htm.jinja2', '*.xhtml.jinja2']
    version_added = ''
    alias_filenames = ['*.html', '*.htm', '*.xhtml']
    mimetypes = ['text/html+django', 'text/html+jinja']
    url = 'https://www.djangoproject.com/documentation/templates'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, DjangoLexer, **options)
    
    def analyse_text(text):
        rv = DjangoLexer.analyse_text(text) - 0.01
        if html_doctype_matches(text):
            rv += 0.5
        return rv



class XmlDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `XmlLexer`.
    """
    name = 'XML+Django/Jinja'
    aliases = ['xml+django', 'xml+jinja']
    filenames = ['*.xml.j2', '*.xml.jinja2']
    version_added = ''
    alias_filenames = ['*.xml']
    mimetypes = ['application/xml+django', 'application/xml+jinja']
    url = 'https://www.djangoproject.com/documentation/templates'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, DjangoLexer, **options)
    
    def analyse_text(text):
        rv = DjangoLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv



class CssDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `CssLexer`.
    """
    name = 'CSS+Django/Jinja'
    aliases = ['css+django', 'css+jinja']
    filenames = ['*.css.j2', '*.css.jinja2']
    version_added = ''
    alias_filenames = ['*.css']
    mimetypes = ['text/css+django', 'text/css+jinja']
    url = 'https://www.djangoproject.com/documentation/templates'
    
    def __init__(self, **options):
        super().__init__(CssLexer, DjangoLexer, **options)
    
    def analyse_text(text):
        return DjangoLexer.analyse_text(text) - 0.05



class JavascriptDjangoLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `JavascriptLexer`.
    """
    name = 'JavaScript+Django/Jinja'
    aliases = ['javascript+django', 'js+django', 'javascript+jinja', 'js+jinja']
    filenames = ['*.js.j2', '*.js.jinja2']
    version_added = ''
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+django', 'application/x-javascript+jinja', 'text/x-javascript+django', 'text/x-javascript+jinja', 'text/javascript+django', 'text/javascript+jinja']
    url = 'https://www.djangoproject.com/documentation/templates'
    
    def __init__(self, **options):
        super().__init__(JavascriptLexer, DjangoLexer, **options)
    
    def analyse_text(text):
        return DjangoLexer.analyse_text(text) - 0.05



class JspRootLexer(RegexLexer):
    """
    Base for the `JspLexer`. Yields `Token.Other` for area outside of
    JSP tags.

    .. versionadded:: 0.7
    """
    tokens = {'root': [('<%\\S?', Keyword, 'sec'), ('</?jsp:(forward|getProperty|include|plugin|setProperty|useBean).*?>', Keyword), ('[^<]+', Other), ('<', Other)], 'sec': [('%>', Keyword, '#pop'), ('[\\w\\W]+?(?=%>|\\Z)', using(JavaLexer))]}



class JspLexer(DelegatingLexer):
    """
    Lexer for Java Server Pages.
    """
    name = 'Java Server Page'
    aliases = ['jsp']
    filenames = ['*.jsp']
    mimetypes = ['application/x-jsp']
    url = 'https://projects.eclipse.org/projects/ee4j.jsp'
    version_added = '0.7'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, JspRootLexer, **options)
    
    def analyse_text(text):
        rv = JavaLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        if ('<%' in text and '%>' in text):
            rv += 0.1
        return rv



class EvoqueLexer(RegexLexer):
    """
    For files using the Evoque templating system.
    """
    name = 'Evoque'
    aliases = ['evoque']
    filenames = ['*.evoque']
    mimetypes = ['application/x-evoque']
    url = 'https://gizmojo.org/templating'
    version_added = '1.1'
    flags = re.DOTALL
    tokens = {'root': [('[^#$]+', Other), ('#\\[', Comment.Multiline, 'comment'), ('\\$\\$', Other), ('\\$\\w+:[^$\\n]*\\$', Comment.Multiline), ('(\\$)(begin|end)(\\{(%)?)(.*?)((?(4)%)\\})', bygroups(Punctuation, Name.Builtin, Punctuation, None, String, Punctuation)), ('(\\$)(evoque|overlay)(\\{(%)?)(\\s*[#\\w\\-"\\\'.]+)?(.*?)((?(4)%)\\})', bygroups(Punctuation, Name.Builtin, Punctuation, None, String, using(PythonLexer), Punctuation)), ('(\\$)(\\w+)(\\{(%)?)(.*?)((?(4)%)\\})', bygroups(Punctuation, Name.Builtin, Punctuation, None, using(PythonLexer), Punctuation)), ('(\\$)(else|rof|fi)', bygroups(Punctuation, Name.Builtin)), ('(\\$\\{(%)?)(.*?)((!)(.*?))?((?(2)%)\\})', bygroups(Punctuation, None, using(PythonLexer), Name.Builtin, None, None, Punctuation)), ('#', Other)], 'comment': [('[^\\]#]', Comment.Multiline), ('#\\[', Comment.Multiline, '#push'), ('\\]#', Comment.Multiline, '#pop'), ('[\\]#]', Comment.Multiline)]}
    
    def analyse_text(text):
        """Evoque templates use $evoque, which is unique."""
        if '$evoque' in text:
            return 1



class EvoqueHtmlLexer(DelegatingLexer):
    """
    Subclass of the `EvoqueLexer` that highlights unlexed data with the
    `HtmlLexer`.
    """
    name = 'HTML+Evoque'
    aliases = ['html+evoque']
    alias_filenames = ['*.html']
    mimetypes = ['text/html+evoque']
    url = 'https://gizmojo.org/templating'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, EvoqueLexer, **options)
    
    def analyse_text(text):
        return EvoqueLexer.analyse_text(text)



class EvoqueXmlLexer(DelegatingLexer):
    """
    Subclass of the `EvoqueLexer` that highlights unlexed data with the
    `XmlLexer`.
    """
    name = 'XML+Evoque'
    aliases = ['xml+evoque']
    alias_filenames = ['*.xml']
    mimetypes = ['application/xml+evoque']
    url = 'https://gizmojo.org/templating'
    version_added = '1.1'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, EvoqueLexer, **options)
    
    def analyse_text(text):
        return EvoqueLexer.analyse_text(text)



class ColdfusionLexer(RegexLexer):
    """
    Coldfusion statements
    """
    name = 'cfstatement'
    aliases = ['cfs']
    filenames = []
    mimetypes = []
    url = 'https://www.adobe.com/products/coldfusion-family.html'
    version_added = ''
    flags = re.IGNORECASE
    tokens = {'root': [('//.*?\\n', Comment.Single), ('/\\*(?:.|\\n)*?\\*/', Comment.Multiline), ('\\+\\+|--', Operator), ('[-+*/^&=!]', Operator), ('<=|>=|<|>|==', Operator), ('mod\\b', Operator), ('(eq|lt|gt|lte|gte|not|is|and|or)\\b', Operator), ('\\|\\||&&', Operator), ('\\?', Operator), ('"', String.Double, 'string'), ("'.*?'", String.Single), ('\\d+', Number), ('(if|else|len|var|xml|default|break|switch|component|property|function|do|try|catch|in|continue|for|return|while|required|any|array|binary|boolean|component|date|guid|numeric|query|string|struct|uuid|case)\\b', Keyword), ('(true|false|null)\\b', Keyword.Constant), ('(application|session|client|cookie|super|this|variables|arguments)\\b', Name.Constant), ('([a-z_$][\\w.]*)(\\s*)(\\()', bygroups(Name.Function, Text, Punctuation)), ('[a-z_$][\\w.]*', Name.Variable), ('[()\\[\\]{};:,.\\\\]', Punctuation), ('\\s+', Text)], 'string': [('""', String.Double), ('#.+?#', String.Interp), ('[^"#]+', String.Double), ('#', String.Double), ('"', String.Double, '#pop')]}



class ColdfusionMarkupLexer(RegexLexer):
    """
    Coldfusion markup only
    """
    name = 'Coldfusion'
    aliases = ['cf']
    filenames = []
    mimetypes = []
    url = 'https://www.adobe.com/products/coldfusion-family.html'
    tokens = {'root': [('[^<]+', Other), include('tags'), ('<[^<>]*', Other)], 'tags': [('<!---', Comment.Multiline, 'cfcomment'), ('(?s)<!--.*?-->', Comment), ('<cfoutput.*?>', Name.Builtin, 'cfoutput'), ('(?s)(<cfscript.*?>)(.+?)(</cfscript.*?>)', bygroups(Name.Builtin, using(ColdfusionLexer), Name.Builtin)), ('(?s)(</?cf(?:component|include|if|else|elseif|loop|return|dbinfo|dump|abort|location|invoke|throw|file|savecontent|mailpart|mail|header|content|zip|image|lock|argument|try|catch|break|directory|http|set|function|param)\\b)(.*?)((?<!\\\\)>)', bygroups(Name.Builtin, using(ColdfusionLexer), Name.Builtin))], 'cfoutput': [('[^#<]+', Other), ('(#)(.*?)(#)', bygroups(Punctuation, using(ColdfusionLexer), Punctuation)), ('</cfoutput.*?>', Name.Builtin, '#pop'), include('tags'), ('(?s)<[^<>]*', Other), ('#', Other)], 'cfcomment': [('<!---', Comment.Multiline, '#push'), ('--->', Comment.Multiline, '#pop'), ('([^<-]|<(?!!---)|-(?!-->))+', Comment.Multiline)]}



class ColdfusionHtmlLexer(DelegatingLexer):
    """
    Coldfusion markup in html
    """
    name = 'Coldfusion HTML'
    aliases = ['cfm']
    filenames = ['*.cfm', '*.cfml']
    mimetypes = ['application/x-coldfusion']
    url = 'https://www.adobe.com/products/coldfusion-family.html'
    version_added = ''
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, ColdfusionMarkupLexer, **options)



class ColdfusionCFCLexer(DelegatingLexer):
    """
    Coldfusion markup/script components
    """
    name = 'Coldfusion CFC'
    aliases = ['cfc']
    filenames = ['*.cfc']
    mimetypes = []
    url = 'https://www.adobe.com/products/coldfusion-family.html'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(ColdfusionHtmlLexer, ColdfusionLexer, **options)



class SspLexer(DelegatingLexer):
    """
    Lexer for Scalate Server Pages.
    """
    name = 'Scalate Server Page'
    aliases = ['ssp']
    filenames = ['*.ssp']
    mimetypes = ['application/x-ssp']
    url = 'https://scalate.github.io/scalate/'
    version_added = '1.4'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, JspRootLexer, **options)
    
    def analyse_text(text):
        rv = 0.0
        if re.search('val \\w+\\s*:', text):
            rv += 0.6
        if looks_like_xml(text):
            rv += 0.2
        if ('<%' in text and '%>' in text):
            rv += 0.1
        return rv



class TeaTemplateRootLexer(RegexLexer):
    """
    Base for the `TeaTemplateLexer`. Yields `Token.Other` for area outside of
    code blocks.

    .. versionadded:: 1.5
    """
    tokens = {'root': [('<%\\S?', Keyword, 'sec'), ('[^<]+', Other), ('<', Other)], 'sec': [('%>', Keyword, '#pop'), ('[\\w\\W]+?(?=%>|\\Z)', using(TeaLangLexer))]}



class TeaTemplateLexer(DelegatingLexer):
    """
    Lexer for Tea Templates.
    """
    name = 'Tea'
    aliases = ['tea']
    filenames = ['*.tea']
    mimetypes = ['text/x-tea']
    url = 'https://github.com/teatrove/teatrove'
    version_added = '1.5'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, TeaTemplateRootLexer, **options)
    
    def analyse_text(text):
        rv = TeaLangLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        if ('<%' in text and '%>' in text):
            rv += 0.1
        return rv



class LassoHtmlLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `HtmlLexer`.

    Nested JavaScript and CSS is also highlighted.
    """
    name = 'HTML+Lasso'
    aliases = ['html+lasso']
    version_added = '1.6'
    alias_filenames = ['*.html', '*.htm', '*.xhtml', '*.lasso', '*.lasso[89]', '*.incl', '*.inc', '*.las']
    mimetypes = ['text/html+lasso', 'application/x-httpd-lasso', 'application/x-httpd-lasso[89]']
    url = 'https://www.lassosoft.com'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, LassoLexer, **options)
    
    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.01
        if html_doctype_matches(text):
            rv += 0.5
        return rv



class LassoXmlLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `XmlLexer`.
    """
    name = 'XML+Lasso'
    aliases = ['xml+lasso']
    version_added = '1.6'
    alias_filenames = ['*.xml', '*.lasso', '*.lasso[89]', '*.incl', '*.inc', '*.las']
    mimetypes = ['application/xml+lasso']
    url = 'https://www.lassosoft.com'
    
    def __init__(self, **options):
        super().__init__(XmlLexer, LassoLexer, **options)
    
    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.01
        if looks_like_xml(text):
            rv += 0.4
        return rv



class LassoCssLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `CssLexer`.
    """
    name = 'CSS+Lasso'
    aliases = ['css+lasso']
    version_added = '1.6'
    alias_filenames = ['*.css']
    mimetypes = ['text/css+lasso']
    url = 'https://www.lassosoft.com'
    
    def __init__(self, **options):
        options['requiredelimiters'] = True
        super().__init__(CssLexer, LassoLexer, **options)
    
    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.05
        if re.search('\\w+:[^;]+;', text):
            rv += 0.1
        if 'padding:' in text:
            rv += 0.1
        return rv



class LassoJavascriptLexer(DelegatingLexer):
    """
    Subclass of the `LassoLexer` which highlights unhandled data with the
    `JavascriptLexer`.
    """
    name = 'JavaScript+Lasso'
    aliases = ['javascript+lasso', 'js+lasso']
    version_added = '1.6'
    alias_filenames = ['*.js']
    mimetypes = ['application/x-javascript+lasso', 'text/x-javascript+lasso', 'text/javascript+lasso']
    url = 'https://www.lassosoft.com'
    
    def __init__(self, **options):
        options['requiredelimiters'] = True
        super().__init__(JavascriptLexer, LassoLexer, **options)
    
    def analyse_text(text):
        rv = LassoLexer.analyse_text(text) - 0.05
        return rv



class HandlebarsLexer(RegexLexer):
    """
    Generic handlebars template lexer.

    Highlights only the Handlebars template tags (stuff between `{{` and `}}`).
    Everything else is left for a delegating lexer.
    """
    name = 'Handlebars'
    url = 'https://handlebarsjs.com/'
    aliases = ['handlebars']
    version_added = '2.0'
    tokens = {'root': [('[^{]+', Other), ('\\{\\{!.*\\}\\}', Comment), ('(\\{\\{\\{)(\\s*)', bygroups(Comment.Special, Text), 'tag'), ('(\\{\\{)([#~/]+)([^\\s}]*)', bygroups(Comment.Preproc, Number.Attribute, Number.Attribute), 'tag'), ('(\\{\\{)(\\s*)', bygroups(Comment.Preproc, Text), 'tag')], 'tag': [('\\s+', Text), ('\\}\\}\\}', Comment.Special, '#pop'), ('(~?)(\\}\\})', bygroups(Number, Comment.Preproc), '#pop'), ('([^\\s}]+)(=)', bygroups(Name.Attribute, Operator)), ('(>)(\\s*)(@partial-block)', bygroups(Keyword, Text, Keyword)), ('(#?>)(\\s*)([\\w-]+)', bygroups(Keyword, Text, Name.Variable)), ('(>)(\\s*)(\\()', bygroups(Keyword, Text, Punctuation), 'dynamic-partial'), include('generic')], 'dynamic-partial': [('\\s+', Text), ('\\)', Punctuation, '#pop'), ('(lookup)(\\s+)(\\.|this)(\\s+)', bygroups(Keyword, Text, Name.Variable, Text)), ('(lookup)(\\s+)(\\S+)', bygroups(Keyword, Text, using(this, state='variable'))), ('[\\w-]+', Name.Function), include('generic')], 'variable': [('[()/@a-zA-Z][\\w-]*', Name.Variable), ('\\.[\\w-]+', Name.Variable), ('(this\\/|\\.\\/|(\\.\\.\\/)+)[\\w-]+', Name.Variable)], 'generic': [include('variable'), (':?"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), (":?'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number)]}



class HandlebarsHtmlLexer(DelegatingLexer):
    """
    Subclass of the `HandlebarsLexer` that highlights unlexed data with the
    `HtmlLexer`.
    """
    name = 'HTML+Handlebars'
    aliases = ['html+handlebars']
    filenames = ['*.handlebars', '*.hbs']
    mimetypes = ['text/html+handlebars', 'text/x-handlebars-template']
    url = 'https://handlebarsjs.com/'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, HandlebarsLexer, **options)



class YamlJinjaLexer(DelegatingLexer):
    """
    Subclass of the `DjangoLexer` that highlights unlexed data with the
    `YamlLexer`.

    Commonly used in Saltstack salt states.
    """
    name = 'YAML+Jinja'
    aliases = ['yaml+jinja', 'salt', 'sls']
    filenames = ['*.sls', '*.yaml.j2', '*.yml.j2', '*.yaml.jinja2', '*.yml.jinja2']
    mimetypes = ['text/x-yaml+jinja', 'text/x-sls']
    url = 'https://jinja.palletsprojects.com'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(YamlLexer, DjangoLexer, **options)



class LiquidLexer(RegexLexer):
    """
    Lexer for Liquid templates.
    """
    name = 'liquid'
    url = 'https://www.rubydoc.info/github/Shopify/liquid'
    aliases = ['liquid']
    filenames = ['*.liquid']
    version_added = '2.0'
    tokens = {'root': [('[^{]+', Text), ('(\\{%)(\\s*)', bygroups(Punctuation, Whitespace), 'tag-or-block'), ('(\\{\\{)(\\s*)([^\\s}]+)', bygroups(Punctuation, Whitespace, using(this, state='generic')), 'output'), ('\\{', Text)], 'tag-or-block': [('(if|unless|elsif|case)(?=\\s+)', Keyword.Reserved, 'condition'), ('(when)(\\s+)', bygroups(Keyword.Reserved, Whitespace), combined('end-of-block', 'whitespace', 'generic')), ('(else)(\\s*)(%\\})', bygroups(Keyword.Reserved, Whitespace, Punctuation), '#pop'), ('(capture)(\\s+)([^\\s%]+)(\\s*)(%\\})', bygroups(Name.Tag, Whitespace, using(this, state='variable'), Whitespace, Punctuation), '#pop'), ('(comment)(\\s*)(%\\})', bygroups(Name.Tag, Whitespace, Punctuation), 'comment'), ('(raw)(\\s*)(%\\})', bygroups(Name.Tag, Whitespace, Punctuation), 'raw'), ('(end(case|unless|if))(\\s*)(%\\})', bygroups(Keyword.Reserved, None, Whitespace, Punctuation), '#pop'), ('(end([^\\s%]+))(\\s*)(%\\})', bygroups(Name.Tag, None, Whitespace, Punctuation), '#pop'), ('(cycle)(\\s+)(?:([^\\s:]*)(:))?(\\s*)', bygroups(Name.Tag, Whitespace, using(this, state='generic'), Punctuation, Whitespace), 'variable-tag-markup'), ('([^\\s%]+)(\\s*)', bygroups(Name.Tag, Whitespace), 'tag-markup')], 'output': [include('whitespace'), ('\\}\\}', Punctuation, '#pop'), ('\\|', Punctuation, 'filters')], 'filters': [include('whitespace'), ('\\}\\}', Punctuation, ('#pop', '#pop')), ('([^\\s|:]+)(:?)(\\s*)', bygroups(Name.Function, Punctuation, Whitespace), 'filter-markup')], 'filter-markup': [('\\|', Punctuation, '#pop'), include('end-of-tag'), include('default-param-markup')], 'condition': [include('end-of-block'), include('whitespace'), ('([^\\s=!><]+)(\\s*)([=!><]=?)(\\s*)(\\S+)(\\s*)(%\\})', bygroups(using(this, state='generic'), Whitespace, Operator, Whitespace, using(this, state='generic'), Whitespace, Punctuation)), ('\\b!', Operator), ('\\bnot\\b', Operator.Word), ('([\\w.\\\'"]+)(\\s+)(contains)(\\s+)([\\w.\\\'"]+)', bygroups(using(this, state='generic'), Whitespace, Operator.Word, Whitespace, using(this, state='generic'))), include('generic'), include('whitespace')], 'generic-value': [include('generic'), include('end-at-whitespace')], 'operator': [('(\\s*)((=|!|>|<)=?)(\\s*)', bygroups(Whitespace, Operator, None, Whitespace), '#pop'), ('(\\s*)(\\bcontains\\b)(\\s*)', bygroups(Whitespace, Operator.Word, Whitespace), '#pop')], 'end-of-tag': [('\\}\\}', Punctuation, '#pop')], 'end-of-block': [('%\\}', Punctuation, ('#pop', '#pop'))], 'end-at-whitespace': [('\\s+', Whitespace, '#pop')], 'param-markup': [include('whitespace'), ('([^\\s=:]+)(\\s*)(=|:)', bygroups(Name.Attribute, Whitespace, Operator)), ('(\\{\\{)(\\s*)([^\\s}])(\\s*)(\\}\\})', bygroups(Punctuation, Whitespace, using(this, state='variable'), Whitespace, Punctuation)), include('string'), include('number'), include('keyword'), (',', Punctuation)], 'default-param-markup': [include('param-markup'), ('.', Text)], 'variable-param-markup': [include('param-markup'), include('variable'), ('.', Text)], 'tag-markup': [('%\\}', Punctuation, ('#pop', '#pop')), include('default-param-markup')], 'variable-tag-markup': [('%\\}', Punctuation, ('#pop', '#pop')), include('variable-param-markup')], 'keyword': [('\\b(false|true)\\b', Keyword.Constant)], 'variable': [('[a-zA-Z_]\\w*', Name.Variable), ('(?<=\\w)\\.(?=\\w)', Punctuation)], 'string': [("'[^']*'", String.Single), ('"[^"]*"', String.Double)], 'number': [('\\d+\\.\\d+', Number.Float), ('\\d+', Number.Integer)], 'generic': [include('keyword'), include('string'), include('number'), include('variable')], 'whitespace': [('[ \\t]+', Whitespace)], 'comment': [('(\\{%)(\\s*)(endcomment)(\\s*)(%\\})', bygroups(Punctuation, Whitespace, Name.Tag, Whitespace, Punctuation), ('#pop', '#pop')), ('.', Comment)], 'raw': [('[^{]+', Text), ('(\\{%)(\\s*)(endraw)(\\s*)(%\\})', bygroups(Punctuation, Whitespace, Name.Tag, Whitespace, Punctuation), '#pop'), ('\\{', Text)]}



class TwigLexer(RegexLexer):
    """
    Twig template lexer.

    It just highlights Twig code between the preprocessor directives,
    other data is left untouched by the lexer.
    """
    name = 'Twig'
    aliases = ['twig']
    mimetypes = ['application/x-twig']
    url = 'https://twig.symfony.com'
    version_added = '2.0'
    flags = re.M | re.S
    _ident_char = '[\\\\\\w-]|[^\\x00-\\x7f]'
    _ident_begin = '(?:[\\\\_a-z]|[^\\x00-\\x7f])'
    _ident_end = '(?:' + _ident_char + ')*'
    _ident_inner = _ident_begin + _ident_end
    tokens = {'root': [('[^{]+', Other), ('\\{\\{', Comment.Preproc, 'var'), ('\\{\\#.*?\\#\\}', Comment), ('(\\{%)(-?\\s*)(raw)(\\s*-?)(%\\})(.*?)(\\{%)(-?\\s*)(endraw)(\\s*-?)(%\\})', bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc, Other, Comment.Preproc, Text, Keyword, Text, Comment.Preproc)), ('(\\{%)(-?\\s*)(verbatim)(\\s*-?)(%\\})(.*?)(\\{%)(-?\\s*)(endverbatim)(\\s*-?)(%\\})', bygroups(Comment.Preproc, Text, Keyword, Text, Comment.Preproc, Other, Comment.Preproc, Text, Keyword, Text, Comment.Preproc)), (f'(\\{{%)(-?\\s*)(filter)(\\s+)({_ident_inner})', bygroups(Comment.Preproc, Text, Keyword, Text, Name.Function), 'tag'), ('(\\{%)(-?\\s*)([a-zA-Z_]\\w*)', bygroups(Comment.Preproc, Text, Keyword), 'tag'), ('\\{', Other)], 'varnames': [(f'(\\|)(\\s*)({_ident_inner})', bygroups(Operator, Text, Name.Function)), (f'(is)(\\s+)(not)?(\\s*)({_ident_inner})', bygroups(Keyword, Text, Keyword, Text, Name.Function)), ('(?i)(true|false|none|null)\\b', Keyword.Pseudo), ('(in|not|and|b-and|or|b-or|b-xor|isif|elseif|else|importconstant|defined|divisibleby|empty|even|iterable|odd|sameasmatches|starts\\s+with|ends\\s+with)\\b', Keyword), ('(loop|block|parent)\\b', Name.Builtin), (_ident_inner, Name.Variable), ('\\.' + _ident_inner, Name.Variable), ('\\.[0-9]+', Number), (':?"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), (":?'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('([{}()\\[\\]+\\-*/,:~%]|\\.\\.|\\?|:|\\*\\*|\\/\\/|!=|[><=]=?)', Operator), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number)], 'var': [('\\s+', Text), ('(-?)(\\}\\})', bygroups(Text, Comment.Preproc), '#pop'), include('varnames')], 'tag': [('\\s+', Text), ('(-?)(%\\})', bygroups(Text, Comment.Preproc), '#pop'), include('varnames'), ('.', Punctuation)]}



class TwigHtmlLexer(DelegatingLexer):
    """
    Subclass of the `TwigLexer` that highlights unlexed data with the
    `HtmlLexer`.
    """
    name = 'HTML+Twig'
    aliases = ['html+twig']
    filenames = ['*.twig']
    mimetypes = ['text/html+twig']
    url = 'https://twig.symfony.com'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, TwigLexer, **options)



class Angular2Lexer(RegexLexer):
    """
    Generic angular2 template lexer.

    Highlights only the Angular template tags (stuff between `{{` and `}}` and
    special attributes: '(event)=', '[property]=', '[(twoWayBinding)]=').
    Everything else is left for a delegating lexer.
    """
    name = 'Angular2'
    url = 'https://angular.io/guide/template-syntax'
    aliases = ['ng2']
    version_added = '2.1'
    tokens = {'root': [('[^{([*#]+', Other), ('(\\{\\{)(\\s*)', bygroups(Comment.Preproc, Text), 'ngExpression'), ('([([]+)([\\w:.-]+)([\\])]+)(\\s*)(=)(\\s*)', bygroups(Punctuation, Name.Attribute, Punctuation, Text, Operator, Text), 'attr'), ('([([]+)([\\w:.-]+)([\\])]+)(\\s*)', bygroups(Punctuation, Name.Attribute, Punctuation, Text)), ('([*#])([\\w:.-]+)(\\s*)(=)(\\s*)', bygroups(Punctuation, Name.Attribute, Text, Operator, Text), 'attr'), ('([*#])([\\w:.-]+)(\\s*)', bygroups(Punctuation, Name.Attribute, Text))], 'ngExpression': [('\\s+(\\|\\s+)?', Text), ('\\}\\}', Comment.Preproc, '#pop'), (':?(true|false)', String.Boolean), (':?"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), (":?'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[0-9](\\.[0-9]*)?(eE[+-][0-9])?[flFLdD]?|0[xX][0-9a-fA-F]+[Ll]?', Number), ('[a-zA-Z][\\w-]*(\\(.*\\))?', Name.Variable), ('\\.[\\w-]+(\\(.*\\))?', Name.Variable), ('(\\?)(\\s*)([^}\\s]+)(\\s*)(:)(\\s*)([^}\\s]+)(\\s*)', bygroups(Operator, Text, String, Text, Operator, Text, String, Text))], 'attr': [('".*?"', String, '#pop'), ("'.*?'", String, '#pop'), ('[^\\s>]+', String, '#pop')]}



class Angular2HtmlLexer(DelegatingLexer):
    """
    Subclass of the `Angular2Lexer` that highlights unlexed data with the
    `HtmlLexer`.
    """
    name = 'HTML + Angular2'
    aliases = ['html+ng2']
    filenames = ['*.ng2']
    url = 'https://angular.io/guide/template-syntax'
    version_added = '2.0'
    
    def __init__(self, **options):
        super().__init__(HtmlLexer, Angular2Lexer, **options)



class SqlJinjaLexer(DelegatingLexer):
    """
    Templated SQL lexer.
    """
    name = 'SQL+Jinja'
    aliases = ['sql+jinja']
    filenames = ['*.sql', '*.sql.j2', '*.sql.jinja2']
    url = 'https://jinja.palletsprojects.com'
    version_added = '2.13'
    
    def __init__(self, **options):
        super().__init__(SqlLexer, DjangoLexer, **options)
    
    def analyse_text(text):
        rv = 0.0
        if re.search('\\{\\{\\s*ref\\(.*\\)\\s*\\}\\}', text):
            rv += 0.4
        if re.search('\\{\\{\\s*source\\(.*\\)\\s*\\}\\}', text):
            rv += 0.25
        if re.search('\\{%-?\\s*macro \\w+\\(.*\\)\\s*-?%\\}', text):
            rv += 0.15
        return rv



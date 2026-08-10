"""
    pygments.lexers.minecraft
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Minecraft related languages.

    SNBT. A data communication format used in Minecraft.
    wiki: https://minecraft.wiki/w/NBT_format

    MCFunction. The Function file for Minecraft Data packs and Add-ons.
    official: https://learn.microsoft.com/en-us/minecraft/creator/documents/functionsintroduction
    wiki: https://minecraft.wiki/w/Function

    MCSchema. A kind of data Schema for Minecraft Add-on Development.
    official: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/schemasreference/
    community example: https://www.mcbe-dev.net/addons/data-driven/manifest.html

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, default, include, bygroups
from pygments.token import Comment, Keyword, Literal, Name, Number, Operator, Punctuation, String, Text, Whitespace
__all__ = ['SNBTLexer', 'MCFunctionLexer', 'MCSchemaLexer']


class SNBTLexer(RegexLexer):
    """Lexer for stringified NBT, a data format used in Minecraft
    """
    name = 'SNBT'
    url = 'https://minecraft.wiki/w/NBT_format'
    aliases = ['snbt']
    filenames = ['*.snbt']
    mimetypes = ['text/snbt']
    version_added = '2.12'
    tokens = {'root': [('\\{', Punctuation, 'compound'), ('[^\\{]+', Text)], 'whitespace': [('\\s+', Whitespace)], 'operators': [('[,:;]', Punctuation)], 'literals': [('(true|false)', Keyword.Constant), ('-?\\d+[eE]-?\\d+', Number.Float), ('-?\\d*\\.\\d+[fFdD]?', Number.Float), ('-?\\d+[bBsSlLfFdD]?', Number.Integer), ('"', String.Double, 'literals.string_double'), ("'", String.Single, 'literals.string_single')], 'literals.string_double': [('\\\\.', String.Escape), ('[^\\\\"\\n]+', String.Double), ('"', String.Double, '#pop')], 'literals.string_single': [('\\\\.', String.Escape), ("[^\\\\'\\n]+", String.Single), ("'", String.Single, '#pop')], 'compound': [('[A-Z_a-z]+', Name.Attribute), include('operators'), include('whitespace'), include('literals'), ('\\{', Punctuation, '#push'), ('\\[', Punctuation, 'list'), ('\\}', Punctuation, '#pop')], 'list': [('[A-Z_a-z]+', Name.Attribute), include('literals'), include('operators'), include('whitespace'), ('\\[', Punctuation, '#push'), ('\\{', Punctuation, 'compound'), ('\\]', Punctuation, '#pop')]}



class MCFunctionLexer(RegexLexer):
    """Lexer for the mcfunction scripting language used in Minecraft.

    Modelled somewhat after the `GitHub mcfunction grammar <https://github.com/Arcensoth/language-mcfunction>`_.
    """
    name = 'MCFunction'
    url = 'https://minecraft.wiki/w/Commands'
    aliases = ['mcfunction', 'mcf']
    filenames = ['*.mcfunction']
    mimetypes = ['text/mcfunction']
    version_added = '2.12'
    _block_comment_prefix = '[>!]'
    tokens = {'root': [include('names'), include('comments'), include('literals'), include('whitespace'), include('property'), include('operators'), include('selectors')], 'names': [('^(\\s*)([a-z_]+)', bygroups(Whitespace, Name.Builtin)), ('(?<=run)\\s+[a-z_]+', Name.Builtin), ('\\b[0-9a-fA-F]+(?:-[0-9a-fA-F]+){4}\\b', Name.Variable), include('resource-name'), ('[A-Za-z_][\\w.#%$]+', Keyword.Constant), ('[#%$][\\w.#%$]+', Name.Variable.Magic)], 'resource-name': [('#?[a-z_][a-z_.-]*:[a-z0-9_./-]+', Name.Function), ('#?[a-z0-9_\\.\\-]+\\/[a-z0-9_\\.\\-\\/]+', Name.Function)], 'whitespace': [('\\s+', Whitespace)], 'comments': [(f'^\\s*(#{_block_comment_prefix})', Comment.Multiline, ('comments.block', 'comments.block.emphasized')), ('#.*$', Comment.Single)], 'comments.block': [(f'^\\s*#{_block_comment_prefix}', Comment.Multiline, 'comments.block.emphasized'), ('^\\s*#', Comment.Multiline, 'comments.block.normal'), default('#pop')], 'comments.block.normal': [include('comments.block.special'), ('\\S+', Comment.Multiline), ('\\n', Text, '#pop'), include('whitespace')], 'comments.block.emphasized': [include('comments.block.special'), ('\\S+', String.Doc), ('\\n', Text, '#pop'), include('whitespace')], 'comments.block.special': [('@\\S+', Name.Decorator), include('resource-name'), ('[#%$][\\w.#%$]+', Name.Variable.Magic)], 'operators': [('[\\-~%^?!+*<>\\\\/|&=.]', Operator)], 'literals': [('\\.\\.', Literal), ('(true|false)', Keyword.Pseudo), ('[A-Za-z_]+', Name.Variable.Class), ('[0-7]b', Number.Byte), ('[+-]?\\d*\\.?\\d+([eE]?[+-]?\\d+)?[df]?\\b', Number.Float), ('[+-]?\\d+\\b', Number.Integer), ('"', String.Double, 'literals.string-double'), ("'", String.Single, 'literals.string-single')], 'literals.string-double': [('\\\\.', String.Escape), ('[^\\\\"\\n]+', String.Double), ('"', String.Double, '#pop')], 'literals.string-single': [('\\\\.', String.Escape), ("[^\\\\'\\n]+", String.Single), ("'", String.Single, '#pop')], 'selectors': [('@[a-z]', Name.Variable)], 'property': [('\\{', Punctuation, ('property.curly', 'property.key')), ('\\[', Punctuation, ('property.square', 'property.key'))], 'property.curly': [include('whitespace'), include('property'), ('\\}', Punctuation, '#pop')], 'property.square': [include('whitespace'), include('property'), ('\\]', Punctuation, '#pop'), (',', Punctuation)], 'property.key': [include('whitespace'), ('#?[a-z_][a-z_\\.\\-]*\\:[a-z0-9_\\.\\-/]+(?=\\s*\\=)', Name.Attribute, 'property.delimiter'), ('#?[a-z_][a-z0-9_\\.\\-/]+', Name.Attribute, 'property.delimiter'), ('[A-Za-z_\\-\\+]+', Name.Attribute, 'property.delimiter'), ('"', Name.Attribute, 'property.delimiter', 'literals.string-double'), ("'", Name.Attribute, 'property.delimiter', 'literals.string-single'), ('-?\\d+', Number.Integer, 'property.delimiter'), default('#pop')], 'property.key.string-double': [('\\\\.', String.Escape), ('[^\\\\"\\n]+', Name.Attribute), ('"', Name.Attribute, '#pop')], 'property.key.string-single': [('\\\\.', String.Escape), ("[^\\\\'\\n]+", Name.Attribute), ("'", Name.Attribute, '#pop')], 'property.delimiter': [include('whitespace'), ('[:=]!?', Punctuation, 'property.value'), (',', Punctuation), default('#pop')], 'property.value': [include('whitespace'), ('#?[a-z_][a-z_\\.\\-]*\\:[a-z0-9_\\.\\-/]+', Name.Tag), ('#?[a-z_][a-z0-9_\\.\\-/]+', Name.Tag), include('literals'), include('property'), default('#pop')]}



class MCSchemaLexer(RegexLexer):
    """Lexer for Minecraft Add-ons data Schemas, an interface structure standard used in Minecraft
    """
    name = 'MCSchema'
    url = 'https://learn.microsoft.com/en-us/minecraft/creator/reference/content/schemasreference/'
    aliases = ['mcschema']
    filenames = ['*.mcschema']
    mimetypes = ['text/mcschema']
    version_added = '2.14'
    tokens = {'commentsandwhitespace': [('\\s+', Whitespace), ('//.*?$', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline)], 'slashstartsregex': [include('commentsandwhitespace'), ('/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gimuysd]+\\b|\\B)', String.Regex, '#pop'), ('(?=/)', Text, ('#pop', 'badregex')), default('#pop')], 'badregex': [('\\n', Whitespace, '#pop')], 'singlestring': [('\\\\.', String.Escape), ("'", String.Single, '#pop'), ("[^\\\\']+", String.Single)], 'doublestring': [('\\\\.', String.Escape), ('"', String.Double, '#pop'), ('[^\\\\"]+', String.Double)], 'root': [('^(?=\\s|/|<!--)', Text, 'slashstartsregex'), include('commentsandwhitespace'), ('(?<=: )opt', Operator.Word), ('(?<=\\s)[\\w-]*(?=(\\s+"|\\n))', Keyword.Declaration), ('0[bB][01]+', Number.Bin), ('0[oO]?[0-7]+', Number.Oct), ('0[xX][0-9a-fA-F]+', Number.Hex), ('\\d+', Number.Integer), ('(\\.\\d+|\\d+\\.\\d*|\\d+)([eE][-+]?\\d+)?', Number.Float), ('\\.\\.\\.|=>', Punctuation), ('\\+\\+|--|~|\\?\\?=?|\\?|:|\\\\(?=\\n)|(<<|>>>?|==?|!=?|(?:\\*\\*|\\|\\||&&|[-<>+*%&|^/]))=?', Operator, 'slashstartsregex'), ('[{(\\[;,]', Punctuation, 'slashstartsregex'), ('[})\\].]', Punctuation), ("'", String.Single, 'singlestring'), ('"', String.Double, 'doublestring'), ('[\\w-]*?(?=:\\{?\\n)', String.Symbol), ('([\\w-]*?)(:)(\\d+)(?:(\\.)(\\d+)(?:(\\.)(\\d+)(?:(\\-)((?:[^\\W_]|-)*(?:\\.(?:[^\\W_]|-)*)*))?(?:(\\+)((?:[^\\W_]|-)+(?:\\.(?:[^\\W_]|-)+)*))?)?)?(?=:\\{?\\n)', bygroups(String.Symbol, Operator, Number.Integer, Operator, Number.Integer, Operator, Number.Integer, Operator, String, Operator, String)), ('.*\\n', Text)]}



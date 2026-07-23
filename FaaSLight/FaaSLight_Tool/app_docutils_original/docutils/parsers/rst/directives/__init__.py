"""
This package contains directive implementation modules.
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
import re
import codecs
from importlib import import_module
from docutils import nodes, parsers
from docutils.utils import split_escaped_whitespace, escape2null
from docutils.parsers.rst.languages import en as _fallback_language_module
TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Callable, Sequence
_directive_registry = {'attention': ('admonitions', 'Attention'), 'caution': ('admonitions', 'Caution'), 'code': ('body', 'CodeBlock'), 'danger': ('admonitions', 'Danger'), 'error': ('admonitions', 'Error'), 'important': ('admonitions', 'Important'), 'note': ('admonitions', 'Note'), 'tip': ('admonitions', 'Tip'), 'hint': ('admonitions', 'Hint'), 'warning': ('admonitions', 'Warning'), 'admonition': ('admonitions', 'Admonition'), 'sidebar': ('body', 'Sidebar'), 'topic': ('body', 'Topic'), 'line-block': ('body', 'LineBlock'), 'parsed-literal': ('body', 'ParsedLiteral'), 'math': ('body', 'MathBlock'), 'rubric': ('body', 'Rubric'), 'epigraph': ('body', 'Epigraph'), 'highlights': ('body', 'Highlights'), 'pull-quote': ('body', 'PullQuote'), 'compound': ('body', 'Compound'), 'container': ('body', 'Container'), 'table': ('tables', 'RSTTable'), 'csv-table': ('tables', 'CSVTable'), 'list-table': ('tables', 'ListTable'), 'image': ('images', 'Image'), 'figure': ('images', 'Figure'), 'contents': ('parts', 'Contents'), 'sectnum': ('parts', 'Sectnum'), 'header': ('parts', 'Header'), 'footer': ('parts', 'Footer'), 'target-notes': ('references', 'TargetNotes'), 'meta': ('misc', 'Meta'), 'raw': ('misc', 'Raw'), 'include': ('misc', 'Include'), 'replace': ('misc', 'Replace'), 'unicode': ('misc', 'Unicode'), 'class': ('misc', 'Class'), 'role': ('misc', 'Role'), 'default-role': ('misc', 'DefaultRole'), 'title': ('misc', 'Title'), 'date': ('misc', 'Date'), 'restructuredtext-test-directive': ('misc', 'TestDirective')}
'Mapping of directive name to (module name, class name).  The\ndirective name is canonical & must be lowercase.  Language-dependent\nnames are defined in the ``language`` subpackage.'
_directives = {}
'Cache of imported directives.'

def directive(directive_name, language_module, document):
    """
    Locate and return a directive function from its language-dependent name.
    If not found in the current language, check English.  Return None if the
    named directive cannot be found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.directive', 'directive(directive_name, language_module, document)', {'_directives': _directives, '_fallback_language_module': _fallback_language_module, '_directive_registry': _directive_registry, 'import_module': import_module, 'directive_name': directive_name, 'language_module': language_module, 'document': document}, 2)

def register_directive(name, directive) -> None:
    """
    Register a nonstandard application-defined directive function.
    Language lookups are not needed for such functions.
    """
    _directives[name] = directive

def flag(argument: str) -> None:
    """
    Check for a valid flag option (no argument) and return ``None``.
    (Directive option conversion function.)

    Raise ``ValueError`` if an argument is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.flag', 'flag(argument)', {'argument': argument}, 1)

def unchanged_required(argument: str) -> str:
    """
    Return the argument text, unchanged.

    Directive option conversion function for options that require a value.

    Raise ``ValueError`` if no argument is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.unchanged_required', 'unchanged_required(argument)', {'argument': argument}, 1)

def unchanged(argument: str) -> str:
    """
    Return the argument text, unchanged.
    (Directive option conversion function.)

    No argument implies empty string ("").
    """
    if argument is None:
        return ''
    else:
        return argument

def path(argument: str) -> str:
    """
    Return the path argument unwrapped (with newlines removed).
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.path', 'path(argument)', {'argument': argument}, 1)

def uri(argument: str) -> str:
    """
    Return the URI argument with unescaped whitespace removed.
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.uri', 'uri(argument)', {'split_escaped_whitespace': split_escaped_whitespace, 'escape2null': escape2null, 'nodes': nodes, 'argument': argument}, 1)

def nonnegative_int(argument: str) -> int:
    """
    Check for a nonnegative integer argument; raise ``ValueError`` if not.
    (Directive option conversion function.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.nonnegative_int', 'nonnegative_int(argument)', {'argument': argument}, 1)

def percentage(argument: str) -> int:
    """
    Check for an integer percentage value with optional percent sign.
    (Directive option conversion function.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.percentage', 'percentage(argument)', {'nonnegative_int': nonnegative_int, 'argument': argument}, 1)
CSS3_LENGTH_UNITS = ('em', 'ex', 'ch', 'rem', 'vw', 'vh', 'vmin', 'vmax', 'cm', 'mm', 'Q', 'in', 'pt', 'pc', 'px')
'Length units that are supported by the reStructuredText parser.\n\nCorresponds to the `length units in CSS3`__.\n\n__ https://www.w3.org/TR/css-values-3/#lengths\n'
length_units = [*CSS3_LENGTH_UNITS]
'Deprecated, will be removed in Docutils 0.24 or equivalent.'

def get_measure(argument, units):
    """
    Check for a positive argument of one of the `units`.

    Return a normalized string of the form "<value><unit>"
    (without space inbetween).

    To be called from directive option conversion functions.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.get_measure', 'get_measure(argument, units)', {'nodes': nodes, 'argument': argument, 'units': units}, 1)

def length_or_unitless(argument: str) -> str:
    return get_measure(argument, CSS3_LENGTH_UNITS + ('', ))

def length_or_percentage_or_unitless(argument, default=''):
    """
    Return normalized string of a length or percentage unit.
    (Directive option conversion function.)

    Add <default> if there is no unit. Raise ValueError if the argument is not
    a positive measure of one of the valid CSS units (or without unit).

    >>> length_or_percentage_or_unitless('3 pt')
    '3pt'
    >>> length_or_percentage_or_unitless('3%', 'em')
    '3%'
    >>> length_or_percentage_or_unitless('3')
    '3'
    >>> length_or_percentage_or_unitless('3', 'px')
    '3px'
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.length_or_percentage_or_unitless', "length_or_percentage_or_unitless(argument, default='')", {'get_measure': get_measure, 'CSS3_LENGTH_UNITS': CSS3_LENGTH_UNITS, 'argument': argument, 'default': default}, 1)

def class_option(argument: str) -> list[str]:
    """
    Convert the argument into a list of ID-compatible strings and return it.
    (Directive option conversion function.)

    Raise ``ValueError`` if no argument is found.
    """
    if argument is None:
        raise ValueError('argument required but none supplied')
    names = argument.split()
    class_names = []
    for name in names:
        class_name = nodes.make_id(name)
        if not class_name:
            raise ValueError('cannot make "%s" into a class name' % name)
        class_names.append(class_name)
    return class_names
unicode_pattern = re.compile('(?:0x|x|\\\\x|U\\+?|\\\\u)([0-9a-f]+)$|&#x([0-9a-f]+);$', re.IGNORECASE)

def unicode_code(code):
    """
    Convert a Unicode character code to a Unicode character.
    (Directive option conversion function.)

    Codes may be decimal numbers, hexadecimal numbers (prefixed by ``0x``,
    ``x``, ``\-x``, ``U+``, ``u``, or ``\-u``; e.g. ``U+262E``), or XML-style
    numeric character entities (e.g. ``&#x262E;``).  Other text remains as-is.

    Raise ValueError for illegal Unicode code values.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.unicode_code', 'unicode_code(code)', {'unicode_pattern': unicode_pattern, 'code': code}, 1)

def single_char_or_unicode(argument: str) -> str:
    """
    A single character is returned as-is.  Unicode character codes are
    converted as in `unicode_code`.  (Directive option conversion function.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.single_char_or_unicode', 'single_char_or_unicode(argument)', {'unicode_code': unicode_code, 'argument': argument}, 1)

def single_char_or_whitespace_or_unicode(argument: str) -> str:
    """
    As with `single_char_or_unicode`, but "tab" and "space" are also supported.
    (Directive option conversion function.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.single_char_or_whitespace_or_unicode', 'single_char_or_whitespace_or_unicode(argument)', {'single_char_or_unicode': single_char_or_unicode, 'argument': argument}, 1)

def positive_int(argument: str) -> int:
    """
    Converts the argument into an integer.  Raises ValueError for negative,
    zero, or non-integer values.  (Directive option conversion function.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.positive_int', 'positive_int(argument)', {'argument': argument}, 1)

def positive_int_list(argument: str) -> list[int]:
    """
    Converts a space- or comma-separated list of values into a Python list
    of integers.
    (Directive option conversion function.)

    Raises ValueError for non-positive-integer values.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.positive_int_list', 'positive_int_list(argument)', {'positive_int': positive_int, 'argument': argument, 'list': list, 'int': int}, 1)

def encoding(argument: str) -> str:
    """
    Verifies the encoding argument by lookup.
    (Directive option conversion function.)

    Raises ValueError for unknown encodings.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.encoding', 'encoding(argument)', {'codecs': codecs, 'argument': argument}, 1)

def choice(argument, values):
    """
    Directive option utility function, supplied to enable options whose
    argument must be a member of a finite set of possible values (must be
    lower case).  A custom conversion function must be written to use it.  For
    example::

        from docutils.parsers.rst import directives

        def yesno(argument: str):
            return directives.choice(argument, ('yes', 'no'))

    Raise ``ValueError`` if no argument is found or if the argument's value is
    not valid (not an entry in the supplied list).
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.choice', 'choice(argument, values)', {'format_values': format_values, 'argument': argument, 'values': values}, 1)

def format_values(values) -> str:
    return '%s, or "%s"' % (', '.join(('"%s"' % s for s in values[:-1])), values[-1])

def value_or(values: Sequence[str], other: type) -> Callable:
    """
    Directive option conversion function.

    The argument can be any of `values` or `argument_type`.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.value_or', 'value_or(values, other)', {'values': values, 'other': other, 'Sequence': Sequence, 'str': str}, 1)

def parser_name(argument: str) -> type[parsers.Parser]:
    """
    Return a docutils parser whose name matches the argument.
    (Directive option conversion function.)

    Return `None`, if the argument evaluates to `False`.
    Raise `ValueError` if importing the parser module fails.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.rst.directives.__init__.parser_name', 'parser_name(argument)', {'parsers': parsers, 'argument': argument, 'type': type, 'parsers': parsers}, 1)


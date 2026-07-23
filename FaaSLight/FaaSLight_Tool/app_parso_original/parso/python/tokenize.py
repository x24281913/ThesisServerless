"""
This tokenizer has been copied from the ``tokenize.py`` standard library
tokenizer. The reason was simple: The standard library tokenizer fails
if the indentation is not right. To make it possible to do error recovery the
    tokenizer needed to be rewritten.

Basically this is a stripped down version of the standard library module, so
you can read the documentation there. Additionally we included some speed and
memory optimizations here.
"""

from __future__ import absolute_import
import sys
import re
import itertools as _itertools
from codecs import BOM_UTF8
from typing import NamedTuple, Tuple, Iterator, Iterable, List, Dict, Pattern, Set, Any
from parso.python.token import PythonTokenTypes
from parso.utils import split_lines, PythonVersionInfo, parse_version_string
MAX_UNICODE = '\U0010ffff'
STRING = PythonTokenTypes.STRING
NAME = PythonTokenTypes.NAME
NUMBER = PythonTokenTypes.NUMBER
OP = PythonTokenTypes.OP
NEWLINE = PythonTokenTypes.NEWLINE
INDENT = PythonTokenTypes.INDENT
DEDENT = PythonTokenTypes.DEDENT
ENDMARKER = PythonTokenTypes.ENDMARKER
ERRORTOKEN = PythonTokenTypes.ERRORTOKEN
ERROR_DEDENT = PythonTokenTypes.ERROR_DEDENT
FSTRING_START = PythonTokenTypes.FSTRING_START
FSTRING_STRING = PythonTokenTypes.FSTRING_STRING
FSTRING_END = PythonTokenTypes.FSTRING_END


class TokenCollection(NamedTuple):
    pseudo_token: Pattern
    single_quoted: Set[str]
    triple_quoted: Set[str]
    endpats: Dict[(str, Pattern)]
    whitespace: Pattern
    fstring_pattern_map: Dict[(str, str)]
    always_break_tokens: Set[str]

BOM_UTF8_STRING = BOM_UTF8.decode('utf-8')
_token_collection_cache: Dict[(Tuple[(int, int)], TokenCollection)] = {}

def group(*choices, capture=False, **kwargs):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize.group', 'group(*choices, capture=False, **kwargs)', {'capture': capture, 'choices': choices, 'kwargs': kwargs}, 1)

def maybe(*choices):
    return group(*choices) + '?'

def _all_string_prefixes(*, include_fstring=False, only_fstring=False):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._all_string_prefixes', '_all_string_prefixes(*, include_fstring=False, only_fstring=False)', {'_itertools': _itertools, 'include_fstring': include_fstring, 'only_fstring': only_fstring}, 1)

def _compile(expr):
    return re.compile(expr, re.UNICODE)

def _get_token_collection(version_info):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._get_token_collection', '_get_token_collection(version_info)', {'_token_collection_cache': _token_collection_cache, '_create_token_collection': _create_token_collection, 'version_info': version_info}, 1)
unicode_character_name = '[A-Za-z0-9\\-]+(?: [A-Za-z0-9\\-]+)*'
fstring_string_single_line = _compile('(?:\\{\\{|\\}\\}|\\\\N\\{' + unicode_character_name + '\\}|\\\\(?:\\r\\n?|\\n)|\\\\[^\\r\\nN]|[^{}\\r\\n\\\\])+')
fstring_string_multi_line = _compile('(?:\\{\\{|\\}\\}|\\\\N\\{' + unicode_character_name + '\\}|\\\\[^N]|[^{}\\\\])+')
fstring_format_spec_single_line = _compile('(?:\\\\(?:\\r\\n?|\\n)|[^{}\\r\\n])+')
fstring_format_spec_multi_line = _compile('[^{}]+')

def _create_token_collection(version_info):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._create_token_collection', '_create_token_collection(version_info)', {'_compile': _compile, 'MAX_UNICODE': MAX_UNICODE, 'group': group, 'maybe': maybe, '_all_string_prefixes': _all_string_prefixes, 'TokenCollection': TokenCollection, 'version_info': version_info}, 1)


class Token(NamedTuple):
    type: PythonTokenTypes
    string: str
    start_pos: Tuple[(int, int)]
    prefix: str
    
    @property
    def end_pos(self) -> Tuple[(int, int)]:
        lines = split_lines(self.string)
        if len(lines) > 1:
            return (self.start_pos[0] + len(lines) - 1, 0)
        else:
            return (self.start_pos[0], self.start_pos[1] + len(self.string))



class PythonToken(Token):
    
    def __repr__(self):
        return 'TokenInfo(type=%s, string=%r, start_pos=%r, prefix=%r)' % self._replace(type=self.type.name)



class FStringNode:
    
    def __init__(self, quote):
        self.quote = quote
        self.parentheses_count = 0
        self.previous_lines = ''
        self.last_string_start_pos: Any = None
        self.format_spec_count = 0
    
    def open_parentheses(self, character):
        self.parentheses_count += 1
    
    def close_parentheses(self, character):
        self.parentheses_count -= 1
        if self.parentheses_count == 0:
            self.format_spec_count = 0
    
    def allow_multiline(self):
        return len(self.quote) == 3
    
    def is_in_expr(self):
        return self.parentheses_count > self.format_spec_count
    
    def is_in_format_spec(self):
        return (not self.is_in_expr() and self.format_spec_count)


def _close_fstring_if_necessary(fstring_stack, string, line_nr, column, additional_prefix):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._close_fstring_if_necessary', '_close_fstring_if_necessary(fstring_stack, string, line_nr, column, additional_prefix)', {'PythonToken': PythonToken, 'FSTRING_END': FSTRING_END, 'fstring_stack': fstring_stack, 'string': string, 'line_nr': line_nr, 'column': column, 'additional_prefix': additional_prefix}, 3)

def _find_fstring_string(endpats, fstring_stack, line, lnum, pos):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._find_fstring_string', '_find_fstring_string(endpats, fstring_stack, line, lnum, pos)', {'fstring_format_spec_multi_line': fstring_format_spec_multi_line, 'fstring_format_spec_single_line': fstring_format_spec_single_line, 'fstring_string_multi_line': fstring_string_multi_line, 'fstring_string_single_line': fstring_string_single_line, 'endpats': endpats, 'fstring_stack': fstring_stack, 'line': line, 'lnum': lnum, 'pos': pos}, 2)

def tokenize(code: str, *, version_info: Tuple[(int, int)], start_pos: Tuple[(int, int)] = (1, 0)) -> Iterator[PythonToken]:
    """Generate tokens from a the source code (string)."""
    lines = split_lines(code, keepends=True)
    return tokenize_lines(lines, version_info=version_info, start_pos=start_pos)

def _print_tokens(func):
    """
    A small helper function to help debug the tokenize_lines function.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._print_tokens', '_print_tokens(func)', {'func': func}, 1)

def tokenize_lines(lines: Iterable[str], *, version_info: Tuple[(int, int)], indents: List[int] = None, start_pos: Tuple[(int, int)] = (1, 0), is_first_token=True) -> Iterator[PythonToken]:
    """
    A heavily modified Python standard library tokenizer.

    Additionally to the default information, yields also the prefix of each
    token. This idea comes from lib2to3. The prefix contains all information
    that is irrelevant for the parser like newlines in parentheses or comments.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.python.tokenize.tokenize_lines', 'tokenize_lines(lines, version_info: Tuple[(int, int)], indents: List[int] = None, start_pos: Tuple[(int, int)] = (1, 0), is_first_token=True)', {'PythonToken': PythonToken, 'ERROR_DEDENT': ERROR_DEDENT, 'DEDENT': DEDENT, '_get_token_collection': _get_token_collection, 'Tuple': Tuple, 'Pattern': Pattern, 'List': List, 'FStringNode': FStringNode, 'BOM_UTF8_STRING': BOM_UTF8_STRING, 'STRING': STRING, '_find_fstring_string': _find_fstring_string, 'FSTRING_STRING': FSTRING_STRING, '_close_fstring_if_necessary': _close_fstring_if_necessary, 'INDENT': INDENT, 'ERRORTOKEN': ERRORTOKEN, 'NUMBER': NUMBER, 're': re, 'NAME': NAME, '_split_illegal_unicode_name': _split_illegal_unicode_name, 'NEWLINE': NEWLINE, 'FSTRING_START': FSTRING_START, 'OP': OP, 'ENDMARKER': ENDMARKER, 'lines': lines, 'version_info': version_info, 'indents': indents, 'start_pos': start_pos, 'is_first_token': is_first_token, 'Iterable': Iterable, 'str': str, 'Iterator': Iterator, 'PythonToken': PythonToken}, 0)

def _split_illegal_unicode_name(token, start_pos, prefix):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.python.tokenize._split_illegal_unicode_name', '_split_illegal_unicode_name(token, start_pos, prefix)', {'PythonToken': PythonToken, 'ERRORTOKEN': ERRORTOKEN, 'NAME': NAME, 'token': token, 'start_pos': start_pos, 'prefix': prefix}, 1)
if __name__ == '__main__':
    path = sys.argv[1]
    with open(path) as f:
        code = f.read()
    for token in tokenize(code, version_info=parse_version_string('3.10')):
        print(token)


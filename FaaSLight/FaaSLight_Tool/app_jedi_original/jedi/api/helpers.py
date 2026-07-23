"""
Helpers for the API
"""

import re
from collections import namedtuple
from textwrap import dedent
from itertools import chain
from functools import wraps
from inspect import Parameter
from parso.python.parser import Parser
from parso.python import tree
from jedi.inference.base_value import NO_VALUES
from jedi.inference.syntax_tree import infer_atom
from jedi.inference.helpers import infer_call_of_leaf
from jedi.inference.compiled import get_string_value_set
from jedi.cache import signature_time_cache, memoize_method
from jedi.parser_utils import get_parent_scope
CompletionParts = namedtuple('CompletionParts', ['path', 'has_dot', 'name'])

def _start_match(string, like_name):
    return string.startswith(like_name)

def _fuzzy_match(string, like_name):
    if len(like_name) <= 1:
        return like_name in string
    pos = string.find(like_name[0])
    if pos >= 0:
        return _fuzzy_match(string[pos + 1:], like_name[1:])
    return False

def match(string, like_name, fuzzy=False):
    if fuzzy:
        return _fuzzy_match(string, like_name)
    else:
        return _start_match(string, like_name)

def sorted_definitions(defs):
    return sorted(defs, key=lambda x: (str((x.module_path or '')), (x.line or 0), (x.column or 0), x.name))

def get_on_completion_name(module_node, lines, position):
    leaf = module_node.get_leaf_for_position(position)
    if (leaf is None or leaf.type in ('string', 'error_leaf')):
        line = lines[position[0] - 1]
        return re.search('(?!\\d)\\w+$|$', line[:position[1]]).group(0)
    elif leaf.type not in ('name', 'keyword'):
        return ''
    return leaf.value[:position[1] - leaf.start_pos[1]]

def _get_code(code_lines, start_pos, end_pos):
    lines = code_lines[start_pos[0] - 1:end_pos[0]]
    lines[-1] = lines[-1][:end_pos[1]]
    lines[0] = lines[0][start_pos[1]:]
    return ''.join(lines)


class OnErrorLeaf(Exception):
    
    @property
    def error_leaf(self):
        return self.args[0]


def _get_code_for_stack(code_lines, leaf, position):
    if leaf.start_pos >= position:
        leaf = leaf.get_previous_leaf()
        if leaf is None:
            return ''
    is_after_newline = leaf.type == 'newline'
    while leaf.type == 'newline':
        leaf = leaf.get_previous_leaf()
        if leaf is None:
            return ''
    if (leaf.type == 'error_leaf' or leaf.type == 'string'):
        if leaf.start_pos[0] < position[0]:
            return ''
        raise OnErrorLeaf(leaf)
    else:
        user_stmt = leaf
        while True:
            if user_stmt.parent.type in ('file_input', 'suite', 'simple_stmt'):
                break
            user_stmt = user_stmt.parent
        if is_after_newline:
            if user_stmt.start_pos[1] > position[1]:
                return ''
        return _get_code(code_lines, user_stmt.get_start_pos_of_prefix(), position)

def get_stack_at_position(grammar, code_lines, leaf, pos):
    """
    Returns the possible node names (e.g. import_from, xor_test or yield_stmt).
    """
    
    
    class EndMarkerReached(Exception):
        pass
    
    
    def tokenize_without_endmarker(code):
        tokens = grammar._tokenize(code)
        for token in tokens:
            if token.string == safeword:
                raise EndMarkerReached()
            elif token.prefix.endswith(safeword):
                raise EndMarkerReached()
            elif token.string.endswith(safeword):
                yield token
                raise EndMarkerReached()
            else:
                yield token
    code = dedent(_get_code_for_stack(code_lines, leaf, pos))
    safeword = 'ZZZ_USER_WANTS_TO_COMPLETE_HERE_WITH_JEDI'
    code = code + ' ' + safeword
    p = Parser(grammar._pgen_grammar, error_recovery=True)
    try:
        p.parse(tokens=tokenize_without_endmarker(code))
    except EndMarkerReached:
        return p.stack
    raise SystemError("This really shouldn't happen. There's a bug in Jedi:\n%s" % list(tokenize_without_endmarker(code)))

def infer(inference_state, context, leaf):
    if leaf.type == 'name':
        return inference_state.infer(context, leaf)
    parent = leaf.parent
    definitions = NO_VALUES
    if parent.type == 'atom':
        definitions = context.infer_node(leaf.parent)
    elif parent.type == 'trailer':
        definitions = infer_call_of_leaf(context, leaf)
    elif isinstance(leaf, tree.Literal):
        return infer_atom(context, leaf)
    elif leaf.type in ('fstring_string', 'fstring_start', 'fstring_end'):
        return get_string_value_set(inference_state)
    return definitions

def filter_follow_imports(names, follow_builtin_imports=False):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.api.helpers.filter_follow_imports', 'filter_follow_imports(names, follow_builtin_imports=False)', {'filter_follow_imports': filter_follow_imports, 'names': names, 'follow_builtin_imports': follow_builtin_imports}, 0)


class CallDetails:
    
    def __init__(self, bracket_leaf, children, position):
        self.bracket_leaf = bracket_leaf
        self._children = children
        self._position = position
    
    @property
    def index(self):
        return _get_index_and_key(self._children, self._position)[0]
    
    @property
    def keyword_name_str(self):
        return _get_index_and_key(self._children, self._position)[1]
    
    @memoize_method
    def _list_arguments(self):
        return list(_iter_arguments(self._children, self._position))
    
    def calculate_index(self, param_names):
        positional_count = 0
        used_names = set()
        star_count = -1
        args = self._list_arguments()
        if not args:
            if param_names:
                return 0
            else:
                return None
        is_kwarg = False
        for (i, (star_count, key_start, had_equal)) in enumerate(args):
            is_kwarg |= had_equal | (star_count == 2)
            if star_count:
                pass
            elif i + 1 != len(args):
                if had_equal:
                    used_names.add(key_start)
                else:
                    positional_count += 1
        for (i, param_name) in enumerate(param_names):
            kind = param_name.get_kind()
            if not is_kwarg:
                if kind == Parameter.VAR_POSITIONAL:
                    return i
                if kind in (Parameter.POSITIONAL_OR_KEYWORD, Parameter.POSITIONAL_ONLY):
                    if i == positional_count:
                        return i
            if ((key_start is not None and not star_count == 1) or star_count == 2):
                if (param_name.string_name not in used_names and ((kind == Parameter.KEYWORD_ONLY or (kind == Parameter.POSITIONAL_OR_KEYWORD and positional_count <= i)))):
                    if star_count:
                        return i
                    if had_equal:
                        if param_name.string_name == key_start:
                            return i
                    elif param_name.string_name.startswith(key_start):
                        return i
                if kind == Parameter.VAR_KEYWORD:
                    return i
        return None
    
    def iter_used_keyword_arguments(self):
        for (star_count, key_start, had_equal) in list(self._list_arguments()):
            if (had_equal and key_start):
                yield key_start
    
    def count_positional_arguments(self):
        count = 0
        for (star_count, key_start, had_equal) in self._list_arguments()[:-1]:
            if (star_count or key_start):
                break
            count += 1
        return count


def _iter_arguments(nodes, position):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.helpers._iter_arguments', '_iter_arguments(nodes, position)', {'_iter_arguments': _iter_arguments, 'tree': tree, 'nodes': nodes, 'position': position}, 1)

def _get_index_and_key(nodes, position):
    """
    Returns the amount of commas and the keyword argument string.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.helpers._get_index_and_key', '_get_index_and_key(nodes, position)', {'_get_index_and_key': _get_index_and_key, 'nodes': nodes, 'position': position}, 1)

def _get_signature_details_from_error_node(node, additional_children, position):
    for (index, element) in reversed(list(enumerate(node.children))):
        if (element == '(' and element.end_pos <= position and index > 0):
            children = node.children[index:]
            name = element.get_previous_leaf()
            if name is None:
                continue
            if (name.type == 'name' or name.parent.type in ('trailer', 'atom')):
                return CallDetails(element, children + additional_children, position)

def get_signature_details(module, position):
    leaf = module.get_leaf_for_position(position, include_prefixes=True)
    if leaf.start_pos >= position:
        leaf = leaf.get_previous_leaf()
        if leaf is None:
            return None
    node = leaf.parent
    while node is not None:
        if node.type in ('funcdef', 'classdef', 'decorated', 'async_stmt'):
            return None
        additional_children = []
        for n in reversed(node.children):
            if n.start_pos < position:
                if n.type == 'error_node':
                    result = _get_signature_details_from_error_node(n, additional_children, position)
                    if result is not None:
                        return result
                    additional_children[0:0] = n.children
                    continue
                additional_children.insert(0, n)
        if ((node.type == 'trailer' and node.children[0] == '(') or (node.type == 'decorator' and node.children[2] == '(')):
            if not ((leaf is node.children[-1] and position >= leaf.end_pos)):
                leaf = node.get_previous_leaf()
                if leaf is None:
                    return None
                return CallDetails((node.children[0] if node.type == 'trailer' else node.children[2]), node.children, position)
        node = node.parent
    return None

@signature_time_cache('call_signatures_validity')
def cache_signatures(inference_state, context, bracket_leaf, code_lines, user_pos):
    """This function calculates the cache key."""
    line_index = user_pos[0] - 1
    before_cursor = code_lines[line_index][:user_pos[1]]
    other_lines = code_lines[bracket_leaf.start_pos[0]:line_index]
    whole = ''.join(other_lines + [before_cursor])
    before_bracket = re.match('.*\\(', whole, re.DOTALL)
    module_path = context.get_root_context().py__file__()
    if module_path is None:
        yield None
    else:
        yield (module_path, before_bracket, bracket_leaf.start_pos)
    yield infer(inference_state, context, bracket_leaf.get_previous_leaf())

def validate_line_column(func):
    
    @wraps(func)
    def wrapper(self, line=None, column=None, *args, **kwargs):
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('jedi.api.helpers.validate_line_column.wrapper', 'wrapper(self, line=None, column=None, *args, **kwargs)', {'wraps': wraps, 'func': func, 'self': self, 'line': line, 'column': column, 'args': args, 'kwargs': kwargs}, 1)
    return wrapper

def get_module_names(module, all_scopes, definitions=True, references=False):
    """
    Returns a dictionary with name parts as keys and their call paths as
    values.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.helpers.get_module_names', 'get_module_names(module, all_scopes, definitions=True, references=False)', {'chain': chain, 'get_parent_scope': get_parent_scope, 'module': module, 'all_scopes': all_scopes, 'definitions': definitions, 'references': references}, 1)

def split_search_string(name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.helpers.split_search_string', 'split_search_string(name)', {'name': name}, 2)


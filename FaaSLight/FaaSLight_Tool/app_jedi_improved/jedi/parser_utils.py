import re
import textwrap
from ast import literal_eval
from inspect import cleandoc
from weakref import WeakKeyDictionary
from parso.python import tree
from parso.cache import parser_cache
from parso import split_lines
_EXECUTE_NODES = {'funcdef', 'classdef', 'import_from', 'import_name', 'test', 'or_test', 'and_test', 'not_test', 'comparison', 'expr', 'xor_expr', 'and_expr', 'shift_expr', 'arith_expr', 'atom_expr', 'term', 'factor', 'power', 'atom'}
_FLOW_KEYWORDS = ('try', 'except', 'finally', 'else', 'if', 'elif', 'with', 'for', 'while')

def get_executable_nodes(node, last_added=False):
    """
    For static analysis.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.parser_utils.get_executable_nodes', 'get_executable_nodes(node, last_added=False)', {'get_executable_nodes': get_executable_nodes, '_EXECUTE_NODES': _EXECUTE_NODES, 'node': node, 'last_added': last_added}, 1)

def get_sync_comp_fors(comp_for):
    yield comp_for
    last = comp_for.children[-1]
    while True:
        if last.type == 'comp_for':
            yield last.children[1]
        elif last.type == 'sync_comp_for':
            yield last
        elif not last.type == 'comp_if':
            break
        last = last.children[-1]

def for_stmt_defines_one_name(for_stmt):
    """
    Returns True if only one name is returned: ``for x in y``.
    Returns False if the for loop is more complicated: ``for x, z in y``.

    :returns: bool
    """
    return for_stmt.children[1].type == 'name'

def get_flow_branch_keyword(flow_node, node):
    start_pos = node.start_pos
    if not flow_node.start_pos < start_pos <= flow_node.end_pos:
        raise ValueError('The node is not part of the flow.')
    keyword = None
    for (i, child) in enumerate(flow_node.children):
        if start_pos < child.start_pos:
            return keyword
        first_leaf = child.get_first_leaf()
        if first_leaf in _FLOW_KEYWORDS:
            keyword = first_leaf
    return None

def clean_scope_docstring(scope_node):
    """ Returns a cleaned version of the docstring token. """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.parser_utils.clean_scope_docstring', 'clean_scope_docstring(scope_node)', {'cleandoc': cleandoc, 'safe_literal_eval': safe_literal_eval, 'scope_node': scope_node}, 1)

def find_statement_documentation(tree_node):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.parser_utils.find_statement_documentation', 'find_statement_documentation(tree_node)', {'cleandoc': cleandoc, 'safe_literal_eval': safe_literal_eval, 'tree_node': tree_node}, 1)

def safe_literal_eval(value):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.parser_utils.safe_literal_eval', 'safe_literal_eval(value)', {'literal_eval': literal_eval, 'value': value}, 1)

def get_signature(funcdef, width=72, call_string=None, omit_first_param=False, omit_return_annotation=False):
    """
    Generate a string signature of a function.

    :param width: Fold lines if a line is longer than this value.
    :type width: int
    :arg func_name: Override function name when given.
    :type func_name: str

    :rtype: str
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.parser_utils.get_signature', 'get_signature(funcdef, width=72, call_string=None, omit_first_param=False, omit_return_annotation=False)', {'re': re, 'textwrap': textwrap, 'funcdef': funcdef, 'width': width, 'call_string': call_string, 'omit_first_param': omit_first_param, 'omit_return_annotation': omit_return_annotation}, 1)

def move(node, line_offset):
    """
    Move the `Node` start_pos.
    """
    try:
        children = node.children
    except AttributeError:
        node.line += line_offset
    else:
        for c in children:
            move(c, line_offset)

def get_following_comment_same_line(node):
    """
    returns (as string) any comment that appears on the same line,
    after the node, including the #
    """
    try:
        if node.type == 'for_stmt':
            whitespace = node.children[5].get_first_leaf().prefix
        elif node.type == 'with_stmt':
            whitespace = node.children[3].get_first_leaf().prefix
        elif node.type == 'funcdef':
            whitespace = node.children[4].get_first_leaf().get_next_leaf().prefix
        else:
            whitespace = node.get_last_leaf().get_next_leaf().prefix
    except AttributeError:
        return None
    except ValueError:
        return None
    if '#' not in whitespace:
        return None
    comment = whitespace[whitespace.index('#'):]
    if '\r' in comment:
        comment = comment[:comment.index('\r')]
    if '\n' in comment:
        comment = comment[:comment.index('\n')]
    return comment

def is_scope(node):
    t = node.type
    if t == 'comp_for':
        return node.children[1].type != 'sync_comp_for'
    return t in ('file_input', 'classdef', 'funcdef', 'lambdef', 'sync_comp_for')

def _get_parent_scope_cache(func):
    cache = WeakKeyDictionary()
    
    def wrapper(parso_cache_node, node, include_flows=False):
        if parso_cache_node is None:
            return func(node, include_flows)
        try:
            for_module = cache[parso_cache_node]
        except KeyError:
            for_module = cache[parso_cache_node] = {}
        try:
            return for_module[node]
        except KeyError:
            result = for_module[node] = func(node, include_flows)
            return result
    return wrapper

def get_parent_scope(node, include_flows=False):
    """
    Returns the underlying scope.
    """
    scope = node.parent
    if scope is None:
        return None
    while True:
        if is_scope(scope):
            if scope.type in ('classdef', 'funcdef', 'lambdef'):
                index = scope.children.index(':')
                if scope.children[index].start_pos >= node.start_pos:
                    if (node.parent.type == 'param' and node.parent.name == node):
                        pass
                    elif (node.parent.type == 'tfpdef' and node.parent.children[0] == node):
                        pass
                    else:
                        scope = scope.parent
                        continue
            return scope
        elif (include_flows and isinstance(scope, tree.Flow)):
            if not ((scope.type == 'if_stmt' and any((n.start_pos <= node.start_pos < n.end_pos for n in scope.get_test_nodes())))):
                return scope
        scope = scope.parent
get_cached_parent_scope = _get_parent_scope_cache(get_parent_scope)

def get_cached_code_lines(grammar, path):
    """
    Basically access the cached code lines in parso. This is not the nicest way
    to do this, but we avoid splitting all the lines again.
    """
    return get_parso_cache_node(grammar, path).lines

def get_parso_cache_node(grammar, path):
    """
    This is of course not public. But as long as I control parso, this
    shouldn't be a problem. ~ Dave

    The reason for this is mostly caching. This is obviously also a sign of a
    broken caching architecture.
    """
    return parser_cache[grammar._hashed][path]

def cut_value_at_position(leaf, position):
    """
    Cuts of the value of the leaf at position
    """
    lines = split_lines(leaf.value, keepends=True)[:position[0] - leaf.line + 1]
    column = position[1]
    if leaf.line == position[0]:
        column -= leaf.column
    if not lines:
        return ''
    lines[-1] = lines[-1][:column]
    return ''.join(lines)

def expr_is_dotted(node):
    """
    Checks if a path looks like `name` or `name.foo.bar` and not `name()`.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.parser_utils.expr_is_dotted', 'expr_is_dotted(node)', {'expr_is_dotted': expr_is_dotted, 'node': node}, 1)

def _function_is_x_method(decorator_checker):
    
    def wrapper(function_node):
        """
        This is a heuristic. It will not hold ALL the times, but it will be
        correct pretty much for anyone that doesn't try to beat it.
        staticmethod/classmethod are builtins and unless overwritten, this will
        be correct.
        """
        import custom_funtemplate
        return custom_funtemplate.rewrite_template('jedi.parser_utils._function_is_x_method.wrapper', 'wrapper(function_node)', {'decorator_checker': decorator_checker, 'function_node': function_node}, 1)
    return wrapper
function_is_staticmethod = _function_is_x_method(lambda m: m == 'staticmethod')
function_is_classmethod = _function_is_x_method(lambda m: m == 'classmethod')
function_is_property = _function_is_x_method(lambda m: (m == 'property' or m == 'cached_property' or m.endswith('.setter')))


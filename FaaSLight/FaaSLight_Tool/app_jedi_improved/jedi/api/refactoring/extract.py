from textwrap import dedent
from parso import split_lines
from jedi import debug
from jedi.api.exceptions import RefactoringError
from jedi.api.refactoring import Refactoring, EXPRESSION_PARTS
from jedi.common import indent_block
from jedi.parser_utils import function_is_classmethod, function_is_staticmethod
_DEFINITION_SCOPES = ('suite', 'file_input')
_VARIABLE_EXCTRACTABLE = EXPRESSION_PARTS + 'atom testlist_star_expr testlist test lambdef lambdef_nocond keyword name number string fstring'.split()

def extract_variable(inference_state, path, module_node, name, pos, until_pos):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract.extract_variable', 'extract_variable(inference_state, path, module_node, name, pos, until_pos)', {'_find_nodes': _find_nodes, 'debug': debug, '_is_expression_with_error': _is_expression_with_error, 'RefactoringError': RefactoringError, '_expression_nodes_to_string': _expression_nodes_to_string, '_replace': _replace, 'Refactoring': Refactoring, 'inference_state': inference_state, 'path': path, 'module_node': module_node, 'name': name, 'pos': pos, 'until_pos': until_pos}, 1)

def _is_expression_with_error(nodes):
    """
    Returns a tuple (is_expression, error_string).
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._is_expression_with_error', '_is_expression_with_error(nodes)', {'_VARIABLE_EXCTRACTABLE': _VARIABLE_EXCTRACTABLE, 'nodes': nodes}, 2)

def _find_nodes(module_node, pos, until_pos):
    """
    Looks up a module and tries to find the appropriate amount of nodes that
    are in there.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._find_nodes', '_find_nodes(module_node, pos, until_pos)', {'_is_not_extractable_syntax': _is_not_extractable_syntax, 'EXPRESSION_PARTS': EXPRESSION_PARTS, 'RefactoringError': RefactoringError, '_remove_unwanted_expression_nodes': _remove_unwanted_expression_nodes, 'module_node': module_node, 'pos': pos, 'until_pos': until_pos}, 1)

def _replace(nodes, expression_replacement, extracted, pos, insert_before_leaf=None, remaining_prefix=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._replace', '_replace(nodes, expression_replacement, extracted, pos, insert_before_leaf=None, remaining_prefix=None)', {'_get_parent_definition': _get_parent_definition, 'split_lines': split_lines, 'indent_block': indent_block, '_get_indentation': _get_indentation, 'nodes': nodes, 'expression_replacement': expression_replacement, 'extracted': extracted, 'pos': pos, 'insert_before_leaf': insert_before_leaf, 'remaining_prefix': remaining_prefix}, 1)

def _expression_nodes_to_string(nodes):
    return ''.join((n.get_code(include_prefix=i != 0) for (i, n) in enumerate(nodes)))

def _suite_nodes_to_string(nodes, pos):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._suite_nodes_to_string', '_suite_nodes_to_string(nodes, pos)', {'_split_prefix_at': _split_prefix_at, 'nodes': nodes, 'pos': pos}, 2)

def _split_prefix_at(leaf, until_line):
    """
    Returns a tuple of the leaf's prefix, split at the until_line
    position.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._split_prefix_at', '_split_prefix_at(leaf, until_line)', {'split_lines': split_lines, 'leaf': leaf, 'until_line': until_line}, 2)

def _get_indentation(node):
    return split_lines(node.get_first_leaf().prefix)[-1]

def _get_parent_definition(node):
    """
    Returns the statement where a node is defined.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._get_parent_definition', '_get_parent_definition(node)', {'_DEFINITION_SCOPES': _DEFINITION_SCOPES, 'node': node}, 1)

def _remove_unwanted_expression_nodes(parent_node, pos, until_pos):
    """
    This function makes it so for `1 * 2 + 3` you can extract `2 + 3`, even
    though it is not part of the expression.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._remove_unwanted_expression_nodes', '_remove_unwanted_expression_nodes(parent_node, pos, until_pos)', {'EXPRESSION_PARTS': EXPRESSION_PARTS, '_is_not_extractable_syntax': _is_not_extractable_syntax, '_remove_unwanted_expression_nodes': _remove_unwanted_expression_nodes, 'parent_node': parent_node, 'pos': pos, 'until_pos': until_pos}, 1)

def _is_not_extractable_syntax(node):
    return (node.type == 'operator' or (node.type == 'keyword' and node.value not in ('None', 'True', 'False')))

def extract_function(inference_state, path, module_context, name, pos, until_pos):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract.extract_function', 'extract_function(inference_state, path, module_context, name, pos, until_pos)', {'_find_nodes': _find_nodes, '_is_expression_with_error': _is_expression_with_error, '_find_inputs_and_outputs': _find_inputs_and_outputs, '_get_code_insertion_node': _get_code_insertion_node, '_expression_nodes_to_string': _expression_nodes_to_string, '_is_node_ending_return_stmt': _is_node_ending_return_stmt, '_find_needed_output_variables': _find_needed_output_variables, '_suite_nodes_to_string': _suite_nodes_to_string, '_split_prefix_at': _split_prefix_at, 'dedent': dedent, '_check_for_non_extractables': _check_for_non_extractables, 'function_is_staticmethod': function_is_staticmethod, 'function_is_classmethod': function_is_classmethod, 'indent_block': indent_block, '_replace': _replace, 'Refactoring': Refactoring, 'inference_state': inference_state, 'path': path, 'module_context': module_context, 'name': name, 'pos': pos, 'until_pos': until_pos}, 1)

def _check_for_non_extractables(nodes):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._check_for_non_extractables', '_check_for_non_extractables(nodes)', {'RefactoringError': RefactoringError, '_check_for_non_extractables': _check_for_non_extractables, 'nodes': nodes}, 0)

def _is_name_input(module_context, names, first, last):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._is_name_input', '_is_name_input(module_context, names, first, last)', {'module_context': module_context, 'names': names, 'first': first, 'last': last}, 1)

def _find_inputs_and_outputs(module_context, context, nodes):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._find_inputs_and_outputs', '_find_inputs_and_outputs(module_context, context, nodes)', {'_find_non_global_names': _find_non_global_names, '_is_name_input': _is_name_input, 'module_context': module_context, 'context': context, 'nodes': nodes}, 2)

def _find_non_global_names(nodes):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._find_non_global_names', '_find_non_global_names(nodes)', {'_find_non_global_names': _find_non_global_names, 'nodes': nodes}, 0)

def _get_code_insertion_node(node, is_bound_method):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._get_code_insertion_node', '_get_code_insertion_node(node, is_bound_method)', {'function_is_staticmethod': function_is_staticmethod, 'node': node, 'is_bound_method': is_bound_method}, 1)

def _find_needed_output_variables(context, search_node, at_least_pos, return_variables):
    """
    Searches everything after at_least_pos in a node and checks if any of the
    return_variables are used in there and returns those.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._find_needed_output_variables', '_find_needed_output_variables(context, search_node, at_least_pos, return_variables)', {'_find_non_global_names': _find_non_global_names, 'context': context, 'search_node': search_node, 'at_least_pos': at_least_pos, 'return_variables': return_variables}, 0)

def _is_node_ending_return_stmt(node):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.extract._is_node_ending_return_stmt', '_is_node_ending_return_stmt(node)', {'_is_node_ending_return_stmt': _is_node_ending_return_stmt, 'node': node}, 1)


"""
This module defines the data structures used to represent a grammar.

Specifying grammars in pgen is possible with this grammar::

    grammar: (NEWLINE | rule)* ENDMARKER
    rule: NAME ':' rhs NEWLINE
    rhs: items ('|' items)*
    items: item+
    item: '[' rhs ']' | atom ['+' | '*']
    atom: '(' rhs ')' | NAME | STRING

This grammar is self-referencing.

This parser generator (pgen2) was created by Guido Rossum and used for lib2to3.
Most of the code has been refactored to make it more Pythonic. Since this was a
"copy" of the CPython Parser parser "pgen", there was some work needed to make
it more readable. It should also be slightly faster than the original pgen2,
because we made some optimizations.
"""

from ast import literal_eval
from typing import TypeVar, Generic, Mapping, Sequence, Set, Union
from parso.pgen2.grammar_parser import GrammarParser, NFAState
_TokenTypeT = TypeVar('_TokenTypeT')


class Grammar(Generic[_TokenTypeT]):
    """
    Once initialized, this class supplies the grammar tables for the
    parsing engine implemented by parse.py.  The parsing engine
    accesses the instance variables directly.

    The only important part in this parsers are dfas and transitions between
    dfas.
    """
    
    def __init__(self, start_nonterminal: str, rule_to_dfas: Mapping[(str, Sequence['DFAState[_TokenTypeT]'])], reserved_syntax_strings: Mapping[(str, 'ReservedString')]):
        self.nonterminal_to_dfas = rule_to_dfas
        self.reserved_syntax_strings = reserved_syntax_strings
        self.start_nonterminal = start_nonterminal



class DFAPlan:
    """
    Plans are used for the parser to create stack nodes and do the proper
    DFA state transitions.
    """
    
    def __init__(self, next_dfa: 'DFAState', dfa_pushes: Sequence['DFAState'] = []):
        self.next_dfa = next_dfa
        self.dfa_pushes = dfa_pushes
    
    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, self.next_dfa, self.dfa_pushes)



class DFAState(Generic[_TokenTypeT]):
    """
    The DFAState object is the core class for pretty much anything. DFAState
    are the vertices of an ordered graph while arcs and transitions are the
    edges.

    Arcs are the initial edges, where most DFAStates are not connected and
    transitions are then calculated to connect the DFA state machines that have
    different nonterminals.
    """
    
    def __init__(self, from_rule: str, nfa_set: Set[NFAState], final: NFAState):
        assert isinstance(nfa_set, set)
        assert isinstance(next(iter(nfa_set)), NFAState)
        assert isinstance(final, NFAState)
        self.from_rule = from_rule
        self.nfa_set = nfa_set
        self.arcs: dict[(str, DFAState)] = {}
        self.nonterminal_arcs: dict[(str, DFAState)] = {}
        self.transitions: dict[(Union[(_TokenTypeT, ReservedString)], DFAPlan)] = {}
        self.is_final = final in nfa_set
    
    def add_arc(self, next_, label):
        assert isinstance(label, str)
        assert label not in self.arcs
        assert isinstance(next_, DFAState)
        self.arcs[label] = next_
    
    def unifystate(self, old, new):
        for (label, next_) in self.arcs.items():
            if next_ is old:
                self.arcs[label] = new
    
    def __eq__(self, other):
        assert isinstance(other, DFAState)
        if self.is_final != other.is_final:
            return False
        if len(self.arcs) != len(other.arcs):
            return False
        for (label, next_) in self.arcs.items():
            if next_ is not other.arcs.get(label):
                return False
        return True
    
    def __repr__(self):
        return '<%s: %s is_final=%s>' % (self.__class__.__name__, self.from_rule, self.is_final)



class ReservedString:
    """
    Most grammars will have certain keywords and operators that are mentioned
    in the grammar as strings (e.g. "if") and not token types (e.g. NUMBER).
    This class basically is the former.
    """
    
    def __init__(self, value: str):
        self.value = value
    
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.value)


def _simplify_dfas(dfas):
    """
    This is not theoretically optimal, but works well enough.
    Algorithm: repeatedly look for two states that have the same
    set of arcs (same labels pointing to the same nodes) and
    unify them, until things stop changing.

    dfas is a list of DFAState instances
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.pgen2.generator._simplify_dfas', '_simplify_dfas(dfas)', {'dfas': dfas}, 0)

def _make_dfas(start, finish):
    """
    Uses the powerset construction algorithm to create DFA states from sets of
    NFA states.

    Also does state reduction if some states are not needed.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.pgen2.generator._make_dfas', '_make_dfas(start, finish)', {'NFAState': NFAState, 'DFAState': DFAState, 'start': start, 'finish': finish}, 1)

def _dump_nfa(start, finish):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.pgen2.generator._dump_nfa', '_dump_nfa(start, finish)', {'start': start, 'finish': finish}, 0)

def _dump_dfas(dfas):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.pgen2.generator._dump_dfas', '_dump_dfas(dfas)', {'dfas': dfas}, 0)

def generate_grammar(bnf_grammar: str, token_namespace) -> Grammar:
    """
    ``bnf_text`` is a grammar in extended BNF (using * for repetition, + for
    at-least-once repetition, [] for optional parts, | for alternatives and ()
    for grouping).

    It's not EBNF according to ISO/IEC 14977. It's a dialect Python uses in its
    own parser.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.pgen2.generator.generate_grammar', 'generate_grammar(bnf_grammar, token_namespace)', {'GrammarParser': GrammarParser, '_make_dfas': _make_dfas, '_simplify_dfas': _simplify_dfas, 'ReservedString': ReservedString, '_make_transition': _make_transition, 'DFAPlan': DFAPlan, '_calculate_tree_traversal': _calculate_tree_traversal, 'Grammar': Grammar, 'bnf_grammar': bnf_grammar, 'token_namespace': token_namespace}, 1)

def _make_transition(token_namespace, reserved_syntax_strings, label):
    """
    Creates a reserved string ("if", "for", "*", ...) or returns the token type
    (NUMBER, STRING, ...) for a given grammar terminal.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.pgen2.generator._make_transition', '_make_transition(token_namespace, reserved_syntax_strings, label)', {'literal_eval': literal_eval, 'ReservedString': ReservedString, 'token_namespace': token_namespace, 'reserved_syntax_strings': reserved_syntax_strings, 'label': label}, 1)

def _calculate_tree_traversal(nonterminal_to_dfas):
    """
    By this point we know how dfas can move around within a stack node, but we
    don't know how we can add a new stack node (nonterminal transitions).
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.pgen2.generator._calculate_tree_traversal', '_calculate_tree_traversal(nonterminal_to_dfas)', {'_calculate_first_plans': _calculate_first_plans, 'DFAPlan': DFAPlan, 'nonterminal_to_dfas': nonterminal_to_dfas}, 0)

def _calculate_first_plans(nonterminal_to_dfas, first_plans, nonterminal):
    """
    Calculates the first plan in the first_plans dictionary for every given
    nonterminal. This is going to be used to know when to create stack nodes.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('parso.pgen2.generator._calculate_first_plans', '_calculate_first_plans(nonterminal_to_dfas, first_plans, nonterminal)', {'_calculate_first_plans': _calculate_first_plans, 'nonterminal_to_dfas': nonterminal_to_dfas, 'first_plans': first_plans, 'nonterminal': nonterminal}, 1)


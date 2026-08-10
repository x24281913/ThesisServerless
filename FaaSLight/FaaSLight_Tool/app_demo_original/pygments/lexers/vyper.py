"""
    pygments.lexers.vyper
    ~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Vyper Smart Contract language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, words
from pygments.token import Comment, String, Name, Keyword, Number, Operator, Punctuation, Text, Whitespace
__all__ = ['VyperLexer']


class VyperLexer(RegexLexer):
    """For the Vyper smart contract language.
    """
    name = 'Vyper'
    aliases = ['vyper']
    filenames = ['*.vy']
    url = 'https://vyper.readthedocs.io'
    version_added = '2.17'
    tokens = {'root': [('\\s+', Whitespace), ('(\\\\)(\\n|\\r\\n|\\r)', bygroups(Text, Whitespace)), ('#.*$', Comment.Single), ('\\"\\"\\"', Comment.Multiline, 'multiline-comment'), ("'", String.Single, 'single-string'), ('"', String.Double, 'double-string'), ('(def)(\\s+)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Keyword, Whitespace, Name.Function)), ('(event|struct|interface|log)(\\s+)([a-zA-Z_][a-zA-Z0-9_]*)', bygroups(Keyword, Whitespace, Name.Class)), ('(from)(\\s+)(vyper\\.\\w+)(\\s+)(import)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Namespace, Whitespace, Keyword, Whitespace, Name.Class)), ('\\b0x[0-9a-fA-F]+\\b', Number.Hex), ('\\b(\\d{1,3}(?:_\\d{3})*|\\d+)\\b', Number.Integer), ('\\b\\d+\\.\\d*\\b', Number.Float), (words(('def', 'event', 'pass', 'return', 'for', 'while', 'if', 'elif', 'else', 'assert', 'raise', 'import', 'in', 'struct', 'implements', 'interface', 'from', 'indexed', 'log', 'extcall', 'staticcall'), prefix='\\b', suffix='\\b'), Keyword), (words(('public', 'private', 'view', 'pure', 'constant', 'immutable', 'nonpayable'), prefix='\\b', suffix='\\b'), Keyword.Declaration), (words(('bitwise_and', 'bitwise_not', 'bitwise_or', 'bitwise_xor', 'shift', 'create_minimal_proxy_to', 'create_copy_of', 'create_from_blueprint', 'ecadd', 'ecmul', 'ecrecover', 'keccak256', 'sha256', 'concat', 'convert', 'uint2str', 'extract32', 'slice', 'abs', 'ceil', 'floor', 'max', 'max_value', 'min', 'min_value', 'pow_mod256', 'sqrt', 'isqrt', 'uint256_addmod', 'uint256_mulmod', 'unsafe_add', 'unsafe_sub', 'unsafe_mul', 'unsafe_div', 'as_wei_value', 'blockhash', 'empty', 'len', 'method_id', '_abi_encode', '_abi_decode', 'print', 'range'), prefix='\\b', suffix='\\b'), Name.Builtin), (words(('msg.sender', 'msg.value', 'block.timestamp', 'block.number', 'msg.gas'), prefix='\\b', suffix='\\b'), Name.Builtin.Pseudo), (words(('uint', 'uint8', 'uint16', 'uint32', 'uint64', 'uint128', 'uint256', 'int', 'int8', 'int16', 'int32', 'int64', 'int128', 'int256', 'bool', 'decimal', 'bytes', 'bytes1', 'bytes2', 'bytes3', 'bytes4', 'bytes5', 'bytes6', 'bytes7', 'bytes8', 'bytes9', 'bytes10', 'bytes11', 'bytes12', 'bytes13', 'bytes14', 'bytes15', 'bytes16', 'bytes17', 'bytes18', 'bytes19', 'bytes20', 'bytes21', 'bytes22', 'bytes23', 'bytes24', 'bytes25', 'bytes26', 'bytes27', 'bytes28', 'bytes29', 'bytes30', 'bytes31', 'bytes32', 'string', 'String', 'address', 'enum', 'struct'), prefix='\\b', suffix='\\b'), Keyword.Type), ('\\b(indexed)\\b(\\s*)(\\()(\\s*)(\\w+)(\\s*)(\\))', bygroups(Keyword, Whitespace, Punctuation, Whitespace, Keyword.Type, Punctuation)), ('(\\+|\\-|\\*|\\/|<=?|>=?|==|!=|=|\\||&|%)', Operator), ('[.,:;()\\[\\]{}]', Punctuation), ('@[\\w.]+', Name.Decorator), ('__\\w+__', Name.Magic), ('EMPTY_BYTES32', Name.Constant), ('\\bERC20\\b', Name.Class), ('\\bself\\b', Name.Attribute), ('Bytes\\[\\d+\\]', Keyword.Type), ('\\b[a-zA-Z_]\\w*\\b:', Name.Variable), ('\\b[a-zA-Z_]\\w*\\b', Name)], 'multiline-comment': [('\\"\\"\\"', Comment.Multiline, '#pop'), ('[^"]+', Comment.Multiline), ('\\"', Comment.Multiline)], 'single-string': [("[^\\\\']+", String.Single), ("'", String.Single, '#pop'), ('\\\\.', String.Escape)], 'double-string': [('[^\\\\"]+', String.Double), ('"', String.Double, '#pop'), ('\\\\.', String.Escape)]}



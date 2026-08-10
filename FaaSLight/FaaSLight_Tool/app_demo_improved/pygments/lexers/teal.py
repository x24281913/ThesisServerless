"""
    pygments.lexers.teal
    ~~~~~~~~~~~~~~~~~~~~

    Lexer for TEAL.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import Comment, Name, Number, String, Text, Keyword, Whitespace
__all__ = ['TealLexer']


class TealLexer(RegexLexer):
    """
    For the Transaction Execution Approval Language (TEAL)

    For more information about the grammar, see:
    https://github.com/algorand/go-algorand/blob/master/data/transactions/logic/assembler.go
    """
    name = 'teal'
    url = 'https://developer.algorand.org/docs/reference/teal/specification/'
    aliases = ['teal']
    filenames = ['*.teal']
    version_added = '2.9'
    keywords = words({'Sender', 'Fee', 'FirstValid', 'FirstValidTime', 'LastValid', 'Note', 'Lease', 'Receiver', 'Amount', 'CloseRemainderTo', 'VotePK', 'SelectionPK', 'VoteFirst', 'VoteLast', 'VoteKeyDilution', 'Type', 'TypeEnum', 'XferAsset', 'AssetAmount', 'AssetSender', 'AssetReceiver', 'AssetCloseTo', 'GroupIndex', 'TxID', 'ApplicationID', 'OnCompletion', 'ApplicationArgs', 'NumAppArgs', 'Accounts', 'NumAccounts', 'ApprovalProgram', 'ClearStateProgram', 'RekeyTo', 'ConfigAsset', 'ConfigAssetTotal', 'ConfigAssetDecimals', 'ConfigAssetDefaultFrozen', 'ConfigAssetUnitName', 'ConfigAssetName', 'ConfigAssetURL', 'ConfigAssetMetadataHash', 'ConfigAssetManager', 'ConfigAssetReserve', 'ConfigAssetFreeze', 'ConfigAssetClawback', 'FreezeAsset', 'FreezeAssetAccount', 'FreezeAssetFrozen', 'NoOp', 'OptIn', 'CloseOut', 'ClearState', 'UpdateApplication', 'DeleteApplication', 'MinTxnFee', 'MinBalance', 'MaxTxnLife', 'ZeroAddress', 'GroupSize', 'LogicSigVersion', 'Round', 'LatestTimestamp', 'CurrentApplicationID', 'AssetBalance', 'AssetFrozen', 'AssetTotal', 'AssetDecimals', 'AssetDefaultFrozen', 'AssetUnitName', 'AssetName', 'AssetURL', 'AssetMetadataHash', 'AssetManager', 'AssetReserve', 'AssetFreeze', 'AssetClawback'}, suffix='\\b')
    identifier = '[^ \\t\\n]+(?=\\/\\/)|[^ \\t\\n]+'
    newline = '\\r?\\n'
    tokens = {'root': [include('whitespace'), ('^#pragma .*' + newline, Comment.Directive), ('(' + identifier + ':' + ')' + '([ \t].*)', bygroups(Name.Label, Comment.Single)), (identifier, Name.Function, 'function-args')], 'function-args': [include('whitespace'), ('"', String, 'string'), ('(b(?:ase)?(?:32|64) ?)(\\(?[a-zA-Z0-9+/=]+\\)?)', bygroups(String.Affix, String.Other)), ('[A-Z2-7]{58}', Number), ('0x[\\da-fA-F]+', Number.Hex), ('\\d+', Number.Integer), (keywords, Keyword), (identifier, Name.Attributes), (newline, Text, '#pop')], 'string': [('\\\\(?:["nrt\\\\]|x\\d\\d)', String.Escape), ('[^\\\\\\"\\n]+', String), ('"', String, '#pop')], 'whitespace': [('[ \\t]+', Whitespace), ('//[^\\n]+', Comment.Single)]}



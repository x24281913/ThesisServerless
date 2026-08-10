"""
    pygments.lexers.esoteric
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for esoteric languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Whitespace
__all__ = ['BrainfuckLexer', 'BefungeLexer', 'RedcodeLexer', 'CAmkESLexer', 'CapDLLexer', 'AheuiLexer']


class BrainfuckLexer(RegexLexer):
    """
    Lexer for the esoteric BrainFuck language.
    """
    name = 'Brainfuck'
    url = 'http://www.muppetlabs.com/~breadbox/bf/'
    aliases = ['brainfuck', 'bf']
    filenames = ['*.bf', '*.b']
    mimetypes = ['application/x-brainfuck']
    version_added = ''
    tokens = {'common': [('[.,]+', Name.Tag), ('[+-]+', Name.Builtin), ('[<>]+', Name.Variable), ('[^.,+\\-<>\\[\\]]+', Comment)], 'root': [('\\[', Keyword, 'loop'), ('\\]', Error), include('common')], 'loop': [('\\[', Keyword, '#push'), ('\\]', Keyword, '#pop'), include('common')]}
    
    def analyse_text(text):
        """It's safe to assume that a program which mostly consists of + -
        and < > is brainfuck."""
        plus_minus_count = 0
        greater_less_count = 0
        range_to_check = max(256, len(text))
        for c in text[:range_to_check]:
            if (c == '+' or c == '-'):
                plus_minus_count += 1
            if (c == '<' or c == '>'):
                greater_less_count += 1
        if plus_minus_count > 0.25 * range_to_check:
            return 1.0
        if greater_less_count > 0.25 * range_to_check:
            return 1.0
        result = 0
        if '[-]' in text:
            result += 0.5
        return result



class BefungeLexer(RegexLexer):
    """
    Lexer for the esoteric Befunge language.
    """
    name = 'Befunge'
    url = 'http://en.wikipedia.org/wiki/Befunge'
    aliases = ['befunge']
    filenames = ['*.befunge']
    mimetypes = ['application/x-befunge']
    version_added = '0.7'
    tokens = {'root': [('[0-9a-f]', Number), ('[+*/%!`-]', Operator), ('[<>^v?\\[\\]rxjk]', Name.Variable), ('[:\\\\$.,n]', Name.Builtin), ('[|_mw]', Keyword), ('[{}]', Name.Tag), ('".*?"', String.Double), ("\\'.", String.Single), ('[#;]', Comment), ('[pg&~=@iotsy]', Keyword), ('[()A-Z]', Comment), ('\\s+', Whitespace)]}



class CAmkESLexer(RegexLexer):
    """
    Basic lexer for the input language for the CAmkES component platform.
    """
    name = 'CAmkES'
    url = 'https://sel4.systems/CAmkES/'
    aliases = ['camkes', 'idl4']
    filenames = ['*.camkes', '*.idl4']
    version_added = '2.1'
    tokens = {'root': [('^(\\s*)(#.*)(\\n)', bygroups(Whitespace, Comment.Preproc, Whitespace)), ('\\s+', Whitespace), ('/\\*(.|\\n)*?\\*/', Comment), ('//.*$', Comment), ('[\\[(){},.;\\]]', Punctuation), ('[~!%^&*+=|?:<>/-]', Operator), (words(('assembly', 'attribute', 'component', 'composition', 'configuration', 'connection', 'connector', 'consumes', 'control', 'dataport', 'Dataport', 'Dataports', 'emits', 'event', 'Event', 'Events', 'export', 'from', 'group', 'hardware', 'has', 'interface', 'Interface', 'maybe', 'procedure', 'Procedure', 'Procedures', 'provides', 'template', 'thread', 'threads', 'to', 'uses', 'with'), suffix='\\b'), Keyword), (words(('bool', 'boolean', 'Buf', 'char', 'character', 'double', 'float', 'in', 'inout', 'int', 'int16_6', 'int32_t', 'int64_t', 'int8_t', 'integer', 'mutex', 'out', 'real', 'refin', 'semaphore', 'signed', 'string', 'struct', 'uint16_t', 'uint32_t', 'uint64_t', 'uint8_t', 'uintptr_t', 'unsigned', 'void'), suffix='\\b'), Keyword.Type), ('[a-zA-Z_]\\w*_(priority|domain|buffer)', Keyword.Reserved), (words(('dma_pool', 'from_access', 'to_access'), suffix='\\b'), Keyword.Reserved), ('(import)(\\s+)((?:<[^>]*>|"[^"]*");)', bygroups(Comment.Preproc, Whitespace, Comment.Preproc)), ('(include)(\\s+)((?:<[^>]*>|"[^"]*");)', bygroups(Comment.Preproc, Whitespace, Comment.Preproc)), ('0[xX][\\da-fA-F]+', Number.Hex), ('-?[\\d]+', Number), ('-?[\\d]+\\.[\\d]+', Number.Float), ('"[^"]*"', String), ('[Tt]rue|[Ff]alse', Name.Builtin), ('[a-zA-Z_]\\w*', Name)]}



class CapDLLexer(RegexLexer):
    """
    Basic lexer for CapDL.

    The source of the primary tool that reads such specifications is available
    at https://github.com/seL4/capdl/tree/master/capDL-tool. Note that this
    lexer only supports a subset of the grammar. For example, identifiers can
    shadow type names, but these instances are currently incorrectly
    highlighted as types. Supporting this would need a stateful lexer that is
    considered unnecessarily complex for now.
    """
    name = 'CapDL'
    url = 'https://ssrg.nicta.com.au/publications/nictaabstracts/Kuz_KLW_10.abstract.pml'
    aliases = ['capdl']
    filenames = ['*.cdl']
    version_added = '2.2'
    tokens = {'root': [('^(\\s*)(#.*)(\\n)', bygroups(Whitespace, Comment.Preproc, Whitespace)), ('\\s+', Whitespace), ('/\\*(.|\\n)*?\\*/', Comment), ('(//|--).*$', Comment), ('[<>\\[(){},:;=\\]]', Punctuation), ('\\.\\.', Punctuation), (words(('arch', 'arm11', 'caps', 'child_of', 'ia32', 'irq', 'maps', 'objects'), suffix='\\b'), Keyword), (words(('aep', 'asid_pool', 'cnode', 'ep', 'frame', 'io_device', 'io_ports', 'io_pt', 'notification', 'pd', 'pt', 'tcb', 'ut', 'vcpu'), suffix='\\b'), Keyword.Type), (words(('asid', 'addr', 'badge', 'cached', 'dom', 'domainID', 'elf', 'fault_ep', 'G', 'guard', 'guard_size', 'init', 'ip', 'prio', 'sp', 'R', 'RG', 'RX', 'RW', 'RWG', 'RWX', 'W', 'WG', 'WX', 'level', 'masked', 'master_reply', 'paddr', 'ports', 'reply', 'uncached'), suffix='\\b'), Keyword.Reserved), ('0[xX][\\da-fA-F]+', Number.Hex), ('\\d+(\\.\\d+)?(k|M)?', Number), (words(('bits', ), suffix='\\b'), Number), (words(('cspace', 'vspace', 'reply_slot', 'caller_slot', 'ipc_buffer_slot'), suffix='\\b'), Number), ('[a-zA-Z_][-@\\.\\w]*', Name)]}



class RedcodeLexer(RegexLexer):
    """
    A simple Redcode lexer based on ICWS'94.
    Contributed by Adam Blinkinsop <blinks@acm.org>.
    """
    name = 'Redcode'
    aliases = ['redcode']
    filenames = ['*.cw']
    url = 'https://en.wikipedia.org/wiki/Core_War'
    version_added = '0.8'
    opcodes = ('DAT', 'MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'JMP', 'JMZ', 'JMN', 'DJN', 'CMP', 'SLT', 'SPL', 'ORG', 'EQU', 'END')
    modifiers = ('A', 'B', 'AB', 'BA', 'F', 'X', 'I')
    tokens = {'root': [('\\s+', Whitespace), (';.*$', Comment.Single), ('\\b({})\\b'.format('|'.join(opcodes)), Name.Function), ('\\b({})\\b'.format('|'.join(modifiers)), Name.Decorator), ('[A-Za-z_]\\w+', Name), ('[-+*/%]', Operator), ('[#$@<>]', Operator), ('[.,]', Punctuation), ('[-+]?\\d+', Number.Integer)]}



class AheuiLexer(RegexLexer):
    """
    Aheui is esoteric language based on Korean alphabets.
    """
    name = 'Aheui'
    url = 'http://aheui.github.io/'
    aliases = ['aheui']
    filenames = ['*.aheui']
    version_added = ''
    tokens = {'root': [('[나-낳냐-냫너-넣녀-녛노-놓뇨-눟뉴-닇다-닿댜-댷더-덯뎌-뎧도-돟됴-둫듀-딓따-땋땨-떃떠-떻뗘-뗳또-똫뚀-뚷뜌-띟라-랗랴-럏러-렇려-렿로-롷료-뤃류-릫마-맣먀-먛머-멓며-몋모-뫃묘-뭏뮤-믷바-밯뱌-뱧버-벟벼-볗보-봏뵤-붛뷰-빃빠-빻뺘-뺳뻐-뻫뼈-뼣뽀-뽛뾰-뿧쀼-삏사-샇샤-샿서-섷셔-셯소-솧쇼-숳슈-싛싸-쌓쌰-썋써-쎃쎠-쎻쏘-쏳쑈-쑿쓔-씧자-잫쟈-쟣저-젛져-졓조-좋죠-줗쥬-즿차-챃챠-챻처-첳쳐-쳫초-촣쵸-춯츄-칗카-캏캬-컇커-컿켜-켷코-콯쿄-쿻큐-킣타-탛탸-턓터-텋텨-톃토-톻툐-퉇튜-틯파-팧퍄-퍟퍼-펗펴-폏포-퐇표-풓퓨-픻하-핳햐-햫허-헣혀-혛호-홓효-훟휴-힇]', Operator), ('.', Comment)]}



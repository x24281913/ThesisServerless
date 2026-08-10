"""
    pygments.lexers.objective
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for Objective-C family languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, using, this, words, inherit, default
from pygments.token import Text, Keyword, Name, String, Operator, Number, Punctuation, Literal, Comment, Whitespace
from pygments.lexers.c_cpp import CLexer, CppLexer
__all__ = ['ObjectiveCLexer', 'ObjectiveCppLexer', 'LogosLexer', 'SwiftLexer']

def objective(baselexer):
    """
    Generate a subclass of baselexer that accepts the Objective-C syntax
    extensions.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.objective.objective', 'objective(baselexer)', {'re': re, 'String': String, 'Number': Number, 'Literal': Literal, 'words': words, 'Keyword': Keyword, 'Name': Name, 'bygroups': bygroups, 'Text': Text, 'Punctuation': Punctuation, 'inherit': inherit, 'include': include, 'using': using, 'this': this, 'default': default, 'baselexer': baselexer}, 1)


class ObjectiveCLexer(objective(CLexer)):
    """
    For Objective-C source code with preprocessor directives.
    """
    name = 'Objective-C'
    url = 'https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/ProgrammingWithObjectiveC/Introduction/Introduction.html'
    aliases = ['objective-c', 'objectivec', 'obj-c', 'objc']
    filenames = ['*.m', '*.h']
    mimetypes = ['text/x-objective-c']
    version_added = ''
    priority = 0.05



class ObjectiveCppLexer(objective(CppLexer)):
    """
    For Objective-C++ source code with preprocessor directives.
    """
    name = 'Objective-C++'
    aliases = ['objective-c++', 'objectivec++', 'obj-c++', 'objc++']
    filenames = ['*.mm', '*.hh']
    mimetypes = ['text/x-objective-c++']
    version_added = ''
    priority = 0.05



class LogosLexer(ObjectiveCppLexer):
    """
    For Logos + Objective-C source code with preprocessor directives.
    """
    name = 'Logos'
    aliases = ['logos']
    filenames = ['*.x', '*.xi', '*.xm', '*.xmi']
    mimetypes = ['text/x-logos']
    version_added = '1.6'
    priority = 0.25
    tokens = {'statements': [('(%orig|%log)\\b', Keyword), ('(%c)\\b(\\()(\\s*)([a-zA-Z$_][\\w$]*)(\\s*)(\\))', bygroups(Keyword, Punctuation, Text, Name.Class, Text, Punctuation)), ('(%init)\\b(\\()', bygroups(Keyword, Punctuation), 'logos_init_directive'), ('(%init)(?=\\s*;)', bygroups(Keyword)), ('(%hook|%group)(\\s+)([a-zA-Z$_][\\w$]+)', bygroups(Keyword, Text, Name.Class), '#pop'), ('(%subclass)(\\s+)', bygroups(Keyword, Text), ('#pop', 'logos_classname')), inherit], 'logos_init_directive': [('\\s+', Text), (',', Punctuation, ('logos_init_directive', '#pop')), ('([a-zA-Z$_][\\w$]*)(\\s*)(=)(\\s*)([^);]*)', bygroups(Name.Class, Text, Punctuation, Text, Text)), ('([a-zA-Z$_][\\w$]*)', Name.Class), ('\\)', Punctuation, '#pop')], 'logos_classname': [('([a-zA-Z$_][\\w$]*)(\\s*:\\s*)([a-zA-Z$_][\\w$]*)?', bygroups(Name.Class, Text, Name.Class), '#pop'), ('([a-zA-Z$_][\\w$]*)', Name.Class, '#pop')], 'root': [('(%subclass)(\\s+)', bygroups(Keyword, Text), 'logos_classname'), ('(%hook|%group)(\\s+)([a-zA-Z$_][\\w$]+)', bygroups(Keyword, Text, Name.Class)), ('(%config)(\\s*\\(\\s*)(\\w+)(\\s*=)(.*?)(\\)\\s*)', bygroups(Keyword, Text, Name.Variable, Text, String, Text)), ('(%ctor)(\\s*)(\\{)', bygroups(Keyword, Text, Punctuation), 'function'), ('(%new)(\\s*)(\\()(.*?)(\\))', bygroups(Keyword, Text, Keyword, String, Keyword)), ('(\\s*)(%end)(\\s*)', bygroups(Text, Keyword, Text)), inherit]}
    _logos_keywords = re.compile('%(?:hook|ctor|init|c\\()')
    
    def analyse_text(text):
        if LogosLexer._logos_keywords.search(text):
            return 1.0
        return 0



class SwiftLexer(RegexLexer):
    """
    For Swift source.
    """
    name = 'Swift'
    url = 'https://www.swift.org/'
    filenames = ['*.swift']
    aliases = ['swift']
    mimetypes = ['text/x-swift']
    version_added = '2.0'
    tokens = {'root': [('\\n', Text), ('\\s+', Whitespace), ('//', Comment.Single, 'comment-single'), ('/\\*', Comment.Multiline, 'comment-multi'), ('#(if|elseif|else|endif|available)\\b', Comment.Preproc, 'preproc'), include('keywords'), (words(('Array', 'AutoreleasingUnsafeMutablePointer', 'BidirectionalReverseView', 'Bit', 'Bool', 'CFunctionPointer', 'COpaquePointer', 'CVaListPointer', 'Character', 'ClosedInterval', 'CollectionOfOne', 'ContiguousArray', 'Dictionary', 'DictionaryGenerator', 'DictionaryIndex', 'Double', 'EmptyCollection', 'EmptyGenerator', 'EnumerateGenerator', 'EnumerateSequence', 'FilterCollectionView', 'FilterCollectionViewIndex', 'FilterGenerator', 'FilterSequenceView', 'Float', 'Float80', 'FloatingPointClassification', 'GeneratorOf', 'GeneratorOfOne', 'GeneratorSequence', 'HalfOpenInterval', 'HeapBuffer', 'HeapBufferStorage', 'ImplicitlyUnwrappedOptional', 'IndexingGenerator', 'Int', 'Int16', 'Int32', 'Int64', 'Int8', 'LazyBidirectionalCollection', 'LazyForwardCollection', 'LazyRandomAccessCollection', 'LazySequence', 'MapCollectionView', 'MapSequenceGenerator', 'MapSequenceView', 'MirrorDisposition', 'ObjectIdentifier', 'OnHeap', 'Optional', 'PermutationGenerator', 'QuickLookObject', 'RandomAccessReverseView', 'Range', 'RangeGenerator', 'RawByte', 'Repeat', 'ReverseBidirectionalIndex', 'ReverseRandomAccessIndex', 'SequenceOf', 'SinkOf', 'Slice', 'StaticString', 'StrideThrough', 'StrideThroughGenerator', 'StrideTo', 'StrideToGenerator', 'String', 'UInt', 'UInt16', 'UInt32', 'UInt64', 'UInt8', 'UTF16', 'UTF32', 'UTF8', 'UnicodeDecodingResult', 'UnicodeScalar', 'Unmanaged', 'UnsafeBufferPointer', 'UnsafeBufferPointerGenerator', 'UnsafeMutableBufferPointer', 'UnsafeMutablePointer', 'UnsafePointer', 'Zip2', 'ZipGenerator2', 'AbsoluteValuable', 'AnyObject', 'ArrayLiteralConvertible', 'BidirectionalIndexType', 'BitwiseOperationsType', 'BooleanLiteralConvertible', 'BooleanType', 'CVarArgType', 'CollectionType', 'Comparable', 'DebugPrintable', 'DictionaryLiteralConvertible', 'Equatable', 'ExtendedGraphemeClusterLiteralConvertible', 'ExtensibleCollectionType', 'FloatLiteralConvertible', 'FloatingPointType', 'ForwardIndexType', 'GeneratorType', 'Hashable', 'IntegerArithmeticType', 'IntegerLiteralConvertible', 'IntegerType', 'IntervalType', 'MirrorType', 'MutableCollectionType', 'MutableSliceable', 'NilLiteralConvertible', 'OutputStreamType', 'Printable', 'RandomAccessIndexType', 'RangeReplaceableCollectionType', 'RawOptionSetType', 'RawRepresentable', 'Reflectable', 'SequenceType', 'SignedIntegerType', 'SignedNumberType', 'SinkType', 'Sliceable', 'Streamable', 'Strideable', 'StringInterpolationConvertible', 'StringLiteralConvertible', 'UnicodeCodecType', 'UnicodeScalarLiteralConvertible', 'UnsignedIntegerType', '_ArrayBufferType', '_BidirectionalIndexType', '_CocoaStringType', '_CollectionType', '_Comparable', '_ExtensibleCollectionType', '_ForwardIndexType', '_Incrementable', '_IntegerArithmeticType', '_IntegerType', '_ObjectiveCBridgeable', '_RandomAccessIndexType', '_RawOptionSetType', '_SequenceType', '_Sequence_Type', '_SignedIntegerType', '_SignedNumberType', '_Sliceable', '_Strideable', '_SwiftNSArrayRequiredOverridesType', '_SwiftNSArrayType', '_SwiftNSCopyingType', '_SwiftNSDictionaryRequiredOverridesType', '_SwiftNSDictionaryType', '_SwiftNSEnumeratorType', '_SwiftNSFastEnumerationType', '_SwiftNSStringRequiredOverridesType', '_SwiftNSStringType', '_UnsignedIntegerType', 'C_ARGC', 'C_ARGV', 'Process', 'Any', 'AnyClass', 'BooleanLiteralType', 'CBool', 'CChar', 'CChar16', 'CChar32', 'CDouble', 'CFloat', 'CInt', 'CLong', 'CLongLong', 'CShort', 'CSignedChar', 'CUnsignedInt', 'CUnsignedLong', 'CUnsignedShort', 'CWideChar', 'ExtendedGraphemeClusterType', 'Float32', 'Float64', 'FloatLiteralType', 'IntMax', 'IntegerLiteralType', 'StringLiteralType', 'UIntMax', 'UWord', 'UnicodeScalarType', 'Void', 'Word', 'NSErrorPointer', 'NSObjectProtocol', 'Selector'), suffix='\\b'), Name.Builtin), (words(('abs', 'advance', 'alignof', 'alignofValue', 'assert', 'assertionFailure', 'contains', 'count', 'countElements', 'debugPrint', 'debugPrintln', 'distance', 'dropFirst', 'dropLast', 'dump', 'enumerate', 'equal', 'extend', 'fatalError', 'filter', 'find', 'first', 'getVaList', 'indices', 'insert', 'isEmpty', 'join', 'last', 'lazy', 'lexicographicalCompare', 'map', 'max', 'maxElement', 'min', 'minElement', 'numericCast', 'overlaps', 'partition', 'precondition', 'preconditionFailure', 'prefix', 'print', 'println', 'reduce', 'reflect', 'removeAll', 'removeAtIndex', 'removeLast', 'removeRange', 'reverse', 'sizeof', 'sizeofValue', 'sort', 'sorted', 'splice', 'split', 'startsWith', 'stride', 'strideof', 'strideofValue', 'suffix', 'swap', 'toDebugString', 'toString', 'transcode', 'underestimateCount', 'unsafeAddressOf', 'unsafeBitCast', 'unsafeDowncast', 'withExtendedLifetime', 'withUnsafeMutablePointer', 'withUnsafeMutablePointers', 'withUnsafePointer', 'withUnsafePointers', 'withVaList'), suffix='\\b'), Name.Builtin.Pseudo), ('\\$\\d+', Name.Variable), ('0b[01_]+', Number.Bin), ('0o[0-7_]+', Number.Oct), ('0x[0-9a-fA-F_]+', Number.Hex), ('[0-9][0-9_]*(\\.[0-9_]+[eE][+\\-]?[0-9_]+|\\.[0-9_]*|[eE][+\\-]?[0-9_]+)', Number.Float), ('[0-9][0-9_]*', Number.Integer), ('"""', String, 'string-multi'), ('"', String, 'string'), ('[(){}\\[\\].,:;=@#`?]|->|[<&?](?=\\w)|(?<=\\w)[>!?]', Punctuation), ('[/=\\-+!*%<>&|^?~]+', Operator), ('[a-zA-Z_]\\w*', Name)], 'keywords': [(words(('as', 'async', 'await', 'break', 'case', 'catch', 'continue', 'default', 'defer', 'do', 'else', 'fallthrough', 'for', 'guard', 'if', 'in', 'is', 'repeat', 'return', '#selector', 'switch', 'throw', 'try', 'where', 'while'), suffix='\\b'), Keyword), ('@availability\\([^)]+\\)', Keyword.Reserved), (words(('associativity', 'convenience', 'dynamic', 'didSet', 'final', 'get', 'indirect', 'infix', 'inout', 'lazy', 'left', 'mutating', 'none', 'nonmutating', 'optional', 'override', 'postfix', 'precedence', 'prefix', 'Protocol', 'required', 'rethrows', 'right', 'set', 'throws', 'Type', 'unowned', 'weak', 'willSet', '@availability', '@autoclosure', '@noreturn', '@NSApplicationMain', '@NSCopying', '@NSManaged', '@objc', '@UIApplicationMain', '@IBAction', '@IBDesignable', '@IBInspectable', '@IBOutlet'), suffix='\\b'), Keyword.Reserved), ('(as|dynamicType|false|is|nil|self|Self|super|true|__COLUMN__|__FILE__|__FUNCTION__|__LINE__|_|#(?:file|line|column|function))\\b', Keyword.Constant), ('import\\b', Keyword.Declaration, 'module'), ('(class|enum|extension|struct|protocol)(\\s+)([a-zA-Z_]\\w*)', bygroups(Keyword.Declaration, Whitespace, Name.Class)), ('(func)(\\s+)([a-zA-Z_]\\w*)', bygroups(Keyword.Declaration, Whitespace, Name.Function)), ('(var|let)(\\s+)([a-zA-Z_]\\w*)', bygroups(Keyword.Declaration, Whitespace, Name.Variable)), (words(('actor', 'associatedtype', 'class', 'deinit', 'enum', 'extension', 'func', 'import', 'init', 'internal', 'let', 'operator', 'private', 'protocol', 'public', 'static', 'struct', 'subscript', 'typealias', 'var'), suffix='\\b'), Keyword.Declaration)], 'comment': [(':param: [a-zA-Z_]\\w*|:returns?:|(FIXME|MARK|TODO):', Comment.Special)], 'comment-single': [('\\n', Whitespace, '#pop'), include('comment'), ('[^\\n]+', Comment.Single)], 'comment-multi': [include('comment'), ('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]+', Comment.Multiline)], 'module': [('\\n', Whitespace, '#pop'), ('[a-zA-Z_]\\w*', Name.Class), include('root')], 'preproc': [('\\n', Whitespace, '#pop'), include('keywords'), ('[A-Za-z]\\w*', Comment.Preproc), include('root')], 'string': [('"', String, '#pop'), include('string-common')], 'string-multi': [('"""', String, '#pop'), include('string-common')], 'string-common': [('\\\\\\(', String.Interpol, 'string-intp'), ('\\\\[\'"\\\\nrt]|\\\\x[0-9a-fA-F]{2}|\\\\[0-7]{1,3}|\\\\u[0-9a-fA-F]{4}|\\\\U[0-9a-fA-F]{8}', String.Escape), ('[^\\\\"]+', String), ('\\\\', String)], 'string-intp': [('\\(', String.Interpol, '#push'), ('\\)', String.Interpol, '#pop'), include('root')]}
    
    def get_tokens_unprocessed(self, text):
        from pygments.lexers._cocoa_builtins import COCOA_INTERFACES, COCOA_PROTOCOLS, COCOA_PRIMITIVES
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if (token is Name or token is Name.Class):
                if (value in COCOA_INTERFACES or value in COCOA_PROTOCOLS or value in COCOA_PRIMITIVES):
                    token = Name.Builtin.Pseudo
            yield (index, token, value)



"""
    pygments.lexers.actionscript
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for ActionScript and MXML.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, bygroups, using, this, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
__all__ = ['ActionScriptLexer', 'ActionScript3Lexer', 'MxmlLexer']


class ActionScriptLexer(RegexLexer):
    """
    For ActionScript source code.
    """
    name = 'ActionScript'
    aliases = ['actionscript', 'as']
    filenames = ['*.as']
    mimetypes = ['application/x-actionscript', 'text/x-actionscript', 'text/actionscript']
    url = 'https://en.wikipedia.org/wiki/ActionScript'
    version_added = '0.9'
    flags = re.DOTALL
    tokens = {'root': [('\\s+', Whitespace), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), ('/(\\\\\\\\|\\\\[^\\\\]|[^/\\\\\\n])*/[gim]*', String.Regex), ('[~^*!%&<>|+=:;,/?\\\\-]+', Operator), ('[{}\\[\\]();.]+', Punctuation), (words(('case', 'default', 'for', 'each', 'in', 'while', 'do', 'break', 'return', 'continue', 'if', 'else', 'throw', 'try', 'catch', 'var', 'with', 'new', 'typeof', 'arguments', 'instanceof', 'this', 'switch'), suffix='\\b'), Keyword), (words(('class', 'public', 'final', 'internal', 'native', 'override', 'private', 'protected', 'static', 'import', 'extends', 'implements', 'interface', 'intrinsic', 'return', 'super', 'dynamic', 'function', 'const', 'get', 'namespace', 'package', 'set'), suffix='\\b'), Keyword.Declaration), ('(true|false|null|NaN|Infinity|-Infinity|undefined|Void)\\b', Keyword.Constant), (words(('Accessibility', 'AccessibilityProperties', 'ActionScriptVersion', 'ActivityEvent', 'AntiAliasType', 'ApplicationDomain', 'AsBroadcaster', 'Array', 'AsyncErrorEvent', 'AVM1Movie', 'BevelFilter', 'Bitmap', 'BitmapData', 'BitmapDataChannel', 'BitmapFilter', 'BitmapFilterQuality', 'BitmapFilterType', 'BlendMode', 'BlurFilter', 'Boolean', 'ByteArray', 'Camera', 'Capabilities', 'CapsStyle', 'Class', 'Color', 'ColorMatrixFilter', 'ColorTransform', 'ContextMenu', 'ContextMenuBuiltInItems', 'ContextMenuEvent', 'ContextMenuItem', 'ConvultionFilter', 'CSMSettings', 'DataEvent', 'Date', 'DefinitionError', 'DeleteObjectSample', 'Dictionary', 'DisplacmentMapFilter', 'DisplayObject', 'DisplacmentMapFilterMode', 'DisplayObjectContainer', 'DropShadowFilter', 'Endian', 'EOFError', 'Error', 'ErrorEvent', 'EvalError', 'Event', 'EventDispatcher', 'EventPhase', 'ExternalInterface', 'FileFilter', 'FileReference', 'FileReferenceList', 'FocusDirection', 'FocusEvent', 'Font', 'FontStyle', 'FontType', 'FrameLabel', 'FullScreenEvent', 'Function', 'GlowFilter', 'GradientBevelFilter', 'GradientGlowFilter', 'GradientType', 'Graphics', 'GridFitType', 'HTTPStatusEvent', 'IBitmapDrawable', 'ID3Info', 'IDataInput', 'IDataOutput', 'IDynamicPropertyOutputIDynamicPropertyWriter', 'IEventDispatcher', 'IExternalizable', 'IllegalOperationError', 'IME', 'IMEConversionMode', 'IMEEvent', 'int', 'InteractiveObject', 'InterpolationMethod', 'InvalidSWFError', 'InvokeEvent', 'IOError', 'IOErrorEvent', 'JointStyle', 'Key', 'Keyboard', 'KeyboardEvent', 'KeyLocation', 'LineScaleMode', 'Loader', 'LoaderContext', 'LoaderInfo', 'LoadVars', 'LocalConnection', 'Locale', 'Math', 'Matrix', 'MemoryError', 'Microphone', 'MorphShape', 'Mouse', 'MouseEvent', 'MovieClip', 'MovieClipLoader', 'Namespace', 'NetConnection', 'NetStatusEvent', 'NetStream', 'NewObjectSample', 'Number', 'Object', 'ObjectEncoding', 'PixelSnapping', 'Point', 'PrintJob', 'PrintJobOptions', 'PrintJobOrientation', 'ProgressEvent', 'Proxy', 'QName', 'RangeError', 'Rectangle', 'ReferenceError', 'RegExp', 'Responder', 'Sample', 'Scene', 'ScriptTimeoutError', 'Security', 'SecurityDomain', 'SecurityError', 'SecurityErrorEvent', 'SecurityPanel', 'Selection', 'Shape', 'SharedObject', 'SharedObjectFlushStatus', 'SimpleButton', 'Socket', 'Sound', 'SoundChannel', 'SoundLoaderContext', 'SoundMixer', 'SoundTransform', 'SpreadMethod', 'Sprite', 'StackFrame', 'StackOverflowError', 'Stage', 'StageAlign', 'StageDisplayState', 'StageQuality', 'StageScaleMode', 'StaticText', 'StatusEvent', 'String', 'StyleSheet', 'SWFVersion', 'SyncEvent', 'SyntaxError', 'System', 'TextColorType', 'TextField', 'TextFieldAutoSize', 'TextFieldType', 'TextFormat', 'TextFormatAlign', 'TextLineMetrics', 'TextRenderer', 'TextSnapshot', 'Timer', 'TimerEvent', 'Transform', 'TypeError', 'uint', 'URIError', 'URLLoader', 'URLLoaderDataFormat', 'URLRequest', 'URLRequestHeader', 'URLRequestMethod', 'URLStream', 'URLVariabeles', 'VerifyError', 'Video', 'XML', 'XMLDocument', 'XMLList', 'XMLNode', 'XMLNodeType', 'XMLSocket', 'XMLUI'), suffix='\\b'), Name.Builtin), (words(('decodeURI', 'decodeURIComponent', 'encodeURI', 'escape', 'eval', 'isFinite', 'isNaN', 'isXMLName', 'clearInterval', 'fscommand', 'getTimer', 'getURL', 'getVersion', 'parseFloat', 'parseInt', 'setInterval', 'trace', 'updateAfterEvent', 'unescape'), suffix='\\b'), Name.Function), ('[$a-zA-Z_]\\w*', Name.Other), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-f]+', Number.Hex), ('[0-9]+', Number.Integer), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single)]}
    
    def analyse_text(text):
        """This is only used to disambiguate between ActionScript and
        ActionScript3. We return 0 here; the ActionScript3 lexer will match
        AS3 variable definitions and that will hopefully suffice."""
        return 0



class ActionScript3Lexer(RegexLexer):
    """
    For ActionScript 3 source code.
    """
    name = 'ActionScript 3'
    url = 'https://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/index.html'
    aliases = ['actionscript3', 'as3']
    filenames = ['*.as']
    mimetypes = ['application/x-actionscript3', 'text/x-actionscript3', 'text/actionscript3']
    version_added = '0.11'
    identifier = '[$a-zA-Z_]\\w*'
    typeidentifier = identifier + '(?:\\.<\\w+>)?'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'root': [('\\s+', Whitespace), ('(function\\s+)(' + identifier + ')(\\s*)(\\()', bygroups(Keyword.Declaration, Name.Function, Text, Operator), 'funcparams'), ('(var|const)(\\s+)(' + identifier + ')(\\s*)(:)(\\s*)(' + typeidentifier + ')', bygroups(Keyword.Declaration, Whitespace, Name, Whitespace, Punctuation, Whitespace, Keyword.Type)), ('(import|package)(\\s+)((?:' + identifier + '|\\.)+)(\\s*)', bygroups(Keyword, Whitespace, Name.Namespace, Whitespace)), ('(new)(\\s+)(' + typeidentifier + ')(\\s*)(\\()', bygroups(Keyword, Whitespace, Keyword.Type, Whitespace, Operator)), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), ('/(\\\\\\\\|\\\\[^\\\\]|[^\\\\\\n])*/[gisx]*', String.Regex), ('(\\.)(' + identifier + ')', bygroups(Operator, Name.Attribute)), ('(case|default|for|each|in|while|do|break|return|continue|if|else|throw|try|catch|with|new|typeof|arguments|instanceof|this|switch|import|include|as|is)\\b', Keyword), ('(class|public|final|internal|native|override|private|protected|static|import|extends|implements|interface|intrinsic|return|super|dynamic|function|const|get|namespace|package|set)\\b', Keyword.Declaration), ('(true|false|null|NaN|Infinity|-Infinity|undefined|void)\\b', Keyword.Constant), ('(decodeURI|decodeURIComponent|encodeURI|escape|eval|isFinite|isNaN|isXMLName|clearInterval|fscommand|getTimer|getURL|getVersion|isFinite|parseFloat|parseInt|setInterval|trace|updateAfterEvent|unescape)\\b', Name.Function), (identifier, Name), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-f]+', Number.Hex), ('[0-9]+', Number.Integer), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[~^*!%&<>|+=:;,/?\\\\{}\\[\\]().-]+', Operator)], 'funcparams': [('\\s+', Whitespace), ('(\\s*)(\\.\\.\\.)?(' + identifier + ')(\\s*)(:)(\\s*)(' + typeidentifier + '|\\*)(\\s*)', bygroups(Whitespace, Punctuation, Name, Whitespace, Operator, Whitespace, Keyword.Type, Whitespace), 'defval'), ('\\)', Operator, 'type')], 'type': [('(\\s*)(:)(\\s*)(' + typeidentifier + '|\\*)', bygroups(Whitespace, Operator, Whitespace, Keyword.Type), '#pop:2'), ('\\s+', Text, '#pop:2'), default('#pop:2')], 'defval': [('(=)(\\s*)([^(),]+)(\\s*)(,?)', bygroups(Operator, Whitespace, using(this), Whitespace, Operator), '#pop'), (',', Operator, '#pop'), default('#pop')]}
    
    def analyse_text(text):
        if re.search('\\bimport\\s+flash\\.', text):
            return 0.2
        return 0



class MxmlLexer(RegexLexer):
    """
    For MXML markup.
    Nested AS3 in <script> tags is highlighted by the appropriate lexer.
    """
    flags = re.MULTILINE | re.DOTALL
    name = 'MXML'
    aliases = ['mxml']
    filenames = ['*.mxml']
    url = 'https://en.wikipedia.org/wiki/MXML'
    version_added = '1.1'
    tokens = {'root': [('[^<&]+', Text), ('&\\S*?;', Name.Entity), ('(\\<\\!\\[CDATA\\[)(.*?)(\\]\\]\\>)', bygroups(String, using(ActionScript3Lexer), String)), ('<!--', Comment, 'comment'), ('<\\?.*?\\?>', Comment.Preproc), ('<![^>]*>', Comment.Preproc), ('<\\s*[\\w:.-]+', Name.Tag, 'tag'), ('<\\s*/\\s*[\\w:.-]+\\s*>', Name.Tag)], 'comment': [('[^-]+', Comment), ('-->', Comment, '#pop'), ('-', Comment)], 'tag': [('\\s+', Whitespace), ('[\\w.:-]+\\s*=', Name.Attribute, 'attr'), ('/?\\s*>', Name.Tag, '#pop')], 'attr': [('\\s+', Whitespace), ('".*?"', String, '#pop'), ("'.*?'", String, '#pop'), ('[^\\s>]+', String, '#pop')]}



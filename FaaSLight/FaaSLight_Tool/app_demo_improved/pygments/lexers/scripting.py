"""
    pygments.lexers.scripting
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Lexer for scripting and embedded languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, bygroups, default, combined, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Whitespace, Other
from pygments.util import get_bool_opt, get_list_opt
__all__ = ['LuaLexer', 'LuauLexer', 'MoonScriptLexer', 'ChaiscriptLexer', 'LSLLexer', 'AppleScriptLexer', 'RexxLexer', 'MOOCodeLexer', 'HybrisLexer', 'EasytrieveLexer', 'JclLexer', 'MiniScriptLexer']

def all_lua_builtins():
    from pygments.lexers._lua_builtins import MODULES
    return [w for values in MODULES.values() for w in values]


class LuaLexer(RegexLexer):
    """
    For Lua source code.

    Additional options accepted:

    `func_name_highlighting`
        If given and ``True``, highlight builtin function names
        (default: ``True``).
    `disabled_modules`
        If given, must be a list of module names whose function names
        should not be highlighted. By default all modules are highlighted.

        To get a list of allowed modules have a look into the
        `_lua_builtins` module:

        .. sourcecode:: pycon

            >>> from pygments.lexers._lua_builtins import MODULES
            >>> MODULES.keys()
            ['string', 'coroutine', 'modules', 'io', 'basic', ...]
    """
    name = 'Lua'
    url = 'https://www.lua.org/'
    aliases = ['lua']
    filenames = ['*.lua', '*.wlua']
    mimetypes = ['text/x-lua', 'application/x-lua']
    version_added = ''
    _comment_multiline = '(?:--\\[(?P<level>=*)\\[[\\w\\W]*?\\](?P=level)\\])'
    _comment_single = '(?:--.*$)'
    _space = '(?:\\s+(?!\\s))'
    _s = f'(?:{_comment_multiline}|{_comment_single}|{_space})'
    _s_la = '\\s'
    _name = '(?:[^\\W\\d]\\w*)'
    tokens = {'root': [('#!.*', Comment.Preproc), default('base')], 'ws': [(_comment_multiline, Comment.Multiline), (_comment_single, Comment.Single), (_space, Whitespace)], 'base': [include('ws'), ('(?i)0x[\\da-f]*(\\.[\\da-f]*)?(p[+-]?\\d+)?', Number.Hex), ('(?i)(\\d*\\.\\d+|\\d+\\.\\d*)(e[+-]?\\d+)?', Number.Float), ('(?i)\\d+e[+-]?\\d+', Number.Float), ('\\d+', Number.Integer), ('(?s)\\[(=*)\\[.*?\\]\\1\\]', String), ('::', Punctuation, 'label'), ('\\.{3}', Punctuation), ('[=<>|~&+\\-*/%#^]+|\\.\\.', Operator), ('[\\[\\]{}().,:;]+', Punctuation), ('(and|or|not)\\b', Operator.Word), (words(['break', 'do', 'else', 'elseif', 'end', 'for', 'if', 'in', 'repeat', 'return', 'then', 'until', 'while'], suffix='\\b'), Keyword.Reserved), ('goto\\b', Keyword.Reserved, 'goto'), ('(local)\\b', Keyword.Declaration), ('(true|false|nil)\\b', Keyword.Constant), ('(function)\\b', Keyword.Reserved, 'funcname'), (words(all_lua_builtins(), suffix='\\b'), Name.Builtin), (f'[A-Za-z_]\\w*(?={_s_la}*[.:])', Name.Variable, 'varname'), (f'[A-Za-z_]\\w*(?={_s_la}*\\()', Name.Function), ('[A-Za-z_]\\w*', Name.Variable), ("'", String.Single, combined('stringescape', 'sqs')), ('"', String.Double, combined('stringescape', 'dqs'))], 'varname': [include('ws'), ('\\.\\.', Operator, '#pop'), ('[.:]', Punctuation), (f'{_name}(?={_s_la}*[.:])', Name.Property), (f'{_name}(?={_s_la}*\\()', Name.Function, '#pop'), (_name, Name.Property, '#pop')], 'funcname': [include('ws'), ('[.:]', Punctuation), (f'{_name}(?={_s_la}*[.:])', Name.Class), (_name, Name.Function, '#pop'), ('\\(', Punctuation, '#pop')], 'goto': [include('ws'), (_name, Name.Label, '#pop')], 'label': [include('ws'), ('::', Punctuation, '#pop'), (_name, Name.Label)], 'stringescape': [('\\\\([abfnrtv\\\\"\\\']|[\\r\\n]{1,2}|z\\s*|x[0-9a-fA-F]{2}|\\d{1,3}|u\\{[0-9a-fA-F]+\\})', String.Escape)], 'sqs': [("'", String.Single, '#pop'), ("[^\\\\']+", String.Single)], 'dqs': [('"', String.Double, '#pop'), ('[^\\\\"]+', String.Double)]}
    
    def __init__(self, **options):
        self.func_name_highlighting = get_bool_opt(options, 'func_name_highlighting', True)
        self.disabled_modules = get_list_opt(options, 'disabled_modules', [])
        self._functions = set()
        if self.func_name_highlighting:
            from pygments.lexers._lua_builtins import MODULES
            for (mod, func) in MODULES.items():
                if mod not in self.disabled_modules:
                    self._functions.update(func)
        RegexLexer.__init__(self, **options)
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if (token is Name.Builtin and value not in self._functions):
                if '.' in value:
                    (a, b) = value.split('.')
                    yield (index, Name, a)
                    yield (index + len(a), Punctuation, '.')
                    yield (index + len(a) + 1, Name, b)
                else:
                    yield (index, Name, value)
                continue
            yield (index, token, value)


def _luau_make_expression(should_pop, _s, _s_la):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.scripting._luau_make_expression', '_luau_make_expression(should_pop, _s, _s_la)', {'Number': Number, 'words': words, 'Keyword': Keyword, 'String': String, 'bygroups': bygroups, 'Punctuation': Punctuation, 'Name': Name, 'should_pop': should_pop, '_s': _s, '_s_la': _s_la}, 1)

def _luau_make_expression_special(should_pop):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.lexers.scripting._luau_make_expression_special', '_luau_make_expression_special(should_pop)', {'Punctuation': Punctuation, 'String': String, 'should_pop': should_pop}, 1)


class LuauLexer(RegexLexer):
    """
    For Luau source code.

    Additional options accepted:

    `include_luau_builtins`
        If given and ``True``, automatically highlight Luau builtins
        (default: ``True``).
    `include_roblox_builtins`
        If given and ``True``, automatically highlight Roblox-specific builtins
        (default: ``False``).
    `additional_builtins`
        If given, must be a list of additional builtins to highlight.
    `disabled_builtins`
        If given, must be a list of builtins that will not be highlighted.
    """
    name = 'Luau'
    url = 'https://luau-lang.org/'
    aliases = ['luau']
    filenames = ['*.luau']
    version_added = '2.18'
    _comment_multiline = '(?:--\\[(?P<level>=*)\\[[\\w\\W]*?\\](?P=level)\\])'
    _comment_single = '(?:--.*$)'
    _s = '(?:{}|{}|{})'.format(_comment_multiline, _comment_single, '\\s+')
    _s_la = '\\s'
    tokens = {'root': [('#!.*', Comment.Hashbang, 'base'), default('base')], 'ws': [(_comment_multiline, Comment.Multiline), (_comment_single, Comment.Single), ('\\s+', Whitespace)], 'base': [include('ws'), *_luau_make_expression_special(False), ('\\.\\.\\.', Punctuation), (f'type\\b(?={_s}+[a-zA-Z_])', Keyword.Reserved, 'type_declaration'), (f'export\\b(?={_s}+[a-zA-Z_])', Keyword.Reserved), ('(?:\\.\\.|//|[+\\-*\\/%^<>=])=?', Operator, 'expression'), ('~=', Operator, 'expression'), (words(('and', 'or', 'not'), suffix='\\b'), Operator.Word, 'expression'), (words(('elseif', 'for', 'if', 'in', 'repeat', 'return', 'until', 'while'), suffix='\\b'), Keyword.Reserved, 'expression'), ('local\\b', Keyword.Declaration, 'expression'), ('function\\b', Keyword.Reserved, ('expression', 'func_name')), ('[\\])};]+', Punctuation), include('expression_static'), *_luau_make_expression(False, _s, _s_la), ('[\\[.,]', Punctuation, 'expression')], 'expression_static': [(words(('break', 'continue', 'do', 'else', 'elseif', 'end', 'for', 'if', 'in', 'repeat', 'return', 'then', 'until', 'while'), suffix='\\b'), Keyword.Reserved)], 'expression': [include('ws'), ('if\\b', Keyword.Reserved, ('ternary', 'expression')), ('local\\b', Keyword.Declaration), *_luau_make_expression_special(True), ('\\.\\.\\.', Punctuation, '#pop'), ('function\\b', Keyword.Reserved, 'func_name'), include('expression_static'), *_luau_make_expression(True, _s, _s_la), default('#pop')], 'ternary': [include('ws'), ('else\\b', Keyword.Reserved, '#pop'), (words(('then', 'elseif'), suffix='\\b'), Operator.Reserved, 'expression'), default('#pop')], 'closing_brace_pop': [('\\}', Punctuation, '#pop')], 'closing_parenthesis_pop': [('\\)', Punctuation, '#pop')], 'closing_gt_pop': [('>', Punctuation, '#pop')], 'closing_parenthesis_base': [include('closing_parenthesis_pop'), include('base')], 'closing_parenthesis_type': [include('closing_parenthesis_pop'), include('type')], 'closing_brace_base': [include('closing_brace_pop'), include('base')], 'closing_brace_type': [include('closing_brace_pop'), include('type')], 'closing_gt_type': [include('closing_gt_pop'), include('type')], 'string_escape': [('\\\\z\\s*', String.Escape), ('\\\\(?:[abfnrtvz\\\\"\\\'`\\{\\n])|[\\r\\n]{1,2}|x[\\da-fA-F]{2}|\\d{1,3}|u\\{\\}[\\da-fA-F]*\\}', String.Escape)], 'string_single': [include('string_escape'), ("'", String.Single, '#pop'), ("[^\\\\']+", String.Single)], 'string_double': [include('string_escape'), ('"', String.Double, '#pop'), ('[^\\\\"]+', String.Double)], 'string_interpolated': [include('string_escape'), ('\\{', Punctuation, ('closing_brace_base', 'expression')), ('`', String.Backtick, '#pop'), ('[^\\\\`\\{]+', String.Backtick)], 'func_name': [include('ws'), ('[.:]', Punctuation), (f'[a-zA-Z_]\\w*(?={_s_la}*[.:])', Name.Class), ('[a-zA-Z_]\\w*', Name.Function), ('<', Punctuation, 'closing_gt_type'), ('\\(', Punctuation, '#pop')], 'type': [include('ws'), ('\\(', Punctuation, 'closing_parenthesis_type'), ('\\{', Punctuation, 'closing_brace_type'), ('<', Punctuation, 'closing_gt_type'), ("'", String.Single, 'string_single'), ('"', String.Double, 'string_double'), ('[|&\\.,\\[\\]:=]+', Punctuation), ('->', Punctuation), ('typeof\\(', Name.Builtin, ('closing_parenthesis_base', 'expression')), ('[a-zA-Z_]\\w*', Name.Class)], 'type_start': [include('ws'), ('\\(', Punctuation, ('#pop', 'closing_parenthesis_type')), ('\\{', Punctuation, ('#pop', 'closing_brace_type')), ('<', Punctuation, ('#pop', 'closing_gt_type')), ("'", String.Single, ('#pop', 'string_single')), ('"', String.Double, ('#pop', 'string_double')), ('typeof\\(', Name.Builtin, ('#pop', 'closing_parenthesis_base', 'expression')), ('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'type_end': [include('ws'), ('[|&\\.]', Punctuation, 'type_start'), ('->', Punctuation, 'type_start'), ('<', Punctuation, 'closing_gt_type'), default('#pop')], 'type_declaration': [include('ws'), ('[a-zA-Z_]\\w*', Name.Class), ('<', Punctuation, 'closing_gt_type'), ('=', Punctuation, ('#pop', 'type_end', 'type_start'))]}
    
    def __init__(self, **options):
        self.include_luau_builtins = get_bool_opt(options, 'include_luau_builtins', True)
        self.include_roblox_builtins = get_bool_opt(options, 'include_roblox_builtins', False)
        self.additional_builtins = get_list_opt(options, 'additional_builtins', [])
        self.disabled_builtins = get_list_opt(options, 'disabled_builtins', [])
        self._builtins = set(self.additional_builtins)
        if self.include_luau_builtins:
            from pygments.lexers._luau_builtins import LUAU_BUILTINS
            self._builtins.update(LUAU_BUILTINS)
        if self.include_roblox_builtins:
            from pygments.lexers._luau_builtins import ROBLOX_BUILTINS
            self._builtins.update(ROBLOX_BUILTINS)
        if self.additional_builtins:
            self._builtins.update(self.additional_builtins)
        self._builtins.difference_update(self.disabled_builtins)
        RegexLexer.__init__(self, **options)
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in RegexLexer.get_tokens_unprocessed(self, text):
            if (token is Name or token is Name.Other):
                split_value = value.split('.')
                complete_value = []
                new_index = index
                for position in range(len(split_value), 0, -1):
                    potential_string = '.'.join(split_value[:position])
                    if potential_string in self._builtins:
                        yield (index, Name.Builtin, potential_string)
                        new_index += len(potential_string)
                        if complete_value:
                            yield (new_index, Punctuation, '.')
                            new_index += 1
                        break
                    complete_value.insert(0, split_value[position - 1])
                for (position, substring) in enumerate(complete_value):
                    if position + 1 == len(complete_value):
                        if token is Name:
                            yield (new_index, Name.Variable, substring)
                            continue
                        yield (new_index, Name.Function, substring)
                        continue
                    yield (new_index, Name.Variable, substring)
                    new_index += len(substring)
                    yield (new_index, Punctuation, '.')
                    new_index += 1
                continue
            yield (index, token, value)



class MoonScriptLexer(LuaLexer):
    """
    For MoonScript source code.
    """
    name = 'MoonScript'
    url = 'http://moonscript.org'
    aliases = ['moonscript', 'moon']
    filenames = ['*.moon']
    mimetypes = ['text/x-moonscript', 'application/x-moonscript']
    version_added = '1.5'
    tokens = {'root': [('#!(.*?)$', Comment.Preproc), default('base')], 'base': [('--.*$', Comment.Single), ('(?i)(\\d*\\.\\d+|\\d+\\.\\d*)(e[+-]?\\d+)?', Number.Float), ('(?i)\\d+e[+-]?\\d+', Number.Float), ('(?i)0x[0-9a-f]*', Number.Hex), ('\\d+', Number.Integer), ('\\n', Whitespace), ('[^\\S\\n]+', Text), ('(?s)\\[(=*)\\[.*?\\]\\1\\]', String), ('(->|=>)', Name.Function), (':[a-zA-Z_]\\w*', Name.Variable), ('(==|!=|~=|<=|>=|\\.\\.\\.|\\.\\.|[=+\\-*/%^<>#!.\\\\:])', Operator), ('[;,]', Punctuation), ('[\\[\\]{}()]', Keyword.Type), ('[a-zA-Z_]\\w*:', Name.Variable), (words(('class', 'extends', 'if', 'then', 'super', 'do', 'with', 'import', 'export', 'while', 'elseif', 'return', 'for', 'in', 'from', 'when', 'using', 'else', 'and', 'or', 'not', 'switch', 'break'), suffix='\\b'), Keyword), ('(true|false|nil)\\b', Keyword.Constant), ('(and|or|not)\\b', Operator.Word), ('(self)\\b', Name.Builtin.Pseudo), ('@@?([a-zA-Z_]\\w*)?', Name.Variable.Class), ('[A-Z]\\w*', Name.Class), (words(all_lua_builtins(), suffix='\\b'), Name.Builtin), ('[A-Za-z_]\\w*', Name), ("'", String.Single, combined('stringescape', 'sqs')), ('"', String.Double, combined('stringescape', 'dqs'))], 'stringescape': [('\\\\([abfnrtv\\\\"\']|\\d{1,3})', String.Escape)], 'strings': [('[^#\\\\\\\'"]+', String)], 'interpoling_string': [('\\}', String.Interpol, '#pop'), include('base')], 'dqs': [('"', String.Double, '#pop'), ("\\\\.|\\'", String), ('#\\{', String.Interpol, 'interpoling_string'), ('#', String), include('strings')], 'sqs': [("'", String.Single, '#pop'), ('#|\\\\.|"', String), include('strings')]}
    
    def get_tokens_unprocessed(self, text):
        for (index, token, value) in LuaLexer.get_tokens_unprocessed(self, text):
            if (token == Punctuation and value == '.'):
                token = Operator
            yield (index, token, value)



class ChaiscriptLexer(RegexLexer):
    """
    For ChaiScript source code.
    """
    name = 'ChaiScript'
    url = 'http://chaiscript.com/'
    aliases = ['chaiscript', 'chai']
    filenames = ['*.chai']
    mimetypes = ['text/x-chaiscript', 'application/x-chaiscript']
    version_added = '2.0'
    flags = re.DOTALL | re.MULTILINE
    tokens = {'commentsandwhitespace': [('\\s+', Text), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), ('^\\#.*?\\n', Comment.Single)], 'slashstartsregex': [include('commentsandwhitespace'), ('/(\\\\.|[^[/\\\\\\n]|\\[(\\\\.|[^\\]\\\\\\n])*])+/([gim]+\\b|\\B)', String.Regex, '#pop'), ('(?=/)', Text, ('#pop', 'badregex')), default('#pop')], 'badregex': [('\\n', Text, '#pop')], 'root': [include('commentsandwhitespace'), ('\\n', Text), ('[^\\S\\n]+', Text), ('\\+\\+|--|~|&&|\\?|:|\\|\\||\\\\(?=\\n)|\\.\\.(<<|>>>?|==?|!=?|[-<>+*%&|^/])=?', Operator, 'slashstartsregex'), ('[{(\\[;,]', Punctuation, 'slashstartsregex'), ('[})\\].]', Punctuation), ('[=+\\-*/]', Operator), ('(for|in|while|do|break|return|continue|if|else|throw|try|catch)\\b', Keyword, 'slashstartsregex'), ('(var)\\b', Keyword.Declaration, 'slashstartsregex'), ('(attr|def|fun)\\b', Keyword.Reserved), ('(true|false)\\b', Keyword.Constant), ('(eval|throw)\\b', Name.Builtin), ('`\\S+`', Name.Builtin), ('[$a-zA-Z_]\\w*', Name.Other), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-fA-F]+', Number.Hex), ('[0-9]+', Number.Integer), ('"', String.Double, 'dqstring'), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single)], 'dqstring': [('\\$\\{[^"}]+?\\}', String.Interpol), ('\\$', String.Double), ('\\\\\\\\', String.Double), ('\\\\"', String.Double), ('[^\\\\"$]+', String.Double), ('"', String.Double, '#pop')]}



class LSLLexer(RegexLexer):
    """
    For Second Life's Linden Scripting Language source code.
    """
    name = 'LSL'
    aliases = ['lsl']
    filenames = ['*.lsl']
    mimetypes = ['text/x-lsl']
    url = 'https://wiki.secondlife.com/wiki/Linden_Scripting_Language'
    version_added = '2.0'
    flags = re.MULTILINE
    lsl_keywords = '\\b(?:do|else|for|if|jump|return|while)\\b'
    lsl_types = '\\b(?:float|integer|key|list|quaternion|rotation|string|vector)\\b'
    lsl_states = '\\b(?:(?:state)\\s+\\w+|default)\\b'
    lsl_events = '\\b(?:state_(?:entry|exit)|touch(?:_(?:start|end))?|(?:land_)?collision(?:_(?:start|end))?|timer|listen|(?:no_)?sensor|control|(?:not_)?at_(?:rot_)?target|money|email|run_time_permissions|changed|attach|dataserver|moving_(?:start|end)|link_message|(?:on|object)_rez|remote_data|http_re(?:sponse|quest)|path_update|transaction_result)\\b'
    lsl_functions_builtin = '\\b(?:ll(?:ReturnObjectsBy(?:ID|Owner)|Json(?:2List|[GS]etValue|ValueType)|Sin|Cos|Tan|Atan2|Sqrt|Pow|Abs|Fabs|Frand|Floor|Ceil|Round|Vec(?:Mag|Norm|Dist)|Rot(?:Between|2(?:Euler|Fwd|Left|Up))|(?:Euler|Axes)2Rot|Whisper|(?:Region|Owner)?Say|Shout|Listen(?:Control|Remove)?|Sensor(?:Repeat|Remove)?|Detected(?:Name|Key|Owner|Type|Pos|Vel|Grab|Rot|Group|LinkNumber)|Die|Ground|Wind|(?:[GS]et)(?:AnimationOverride|MemoryLimit|PrimMediaParams|ParcelMusicURL|Object(?:Desc|Name)|PhysicsMaterial|Status|Scale|Color|Alpha|Texture|Pos|Rot|Force|Torque)|ResetAnimationOverride|(?:Scale|Offset|Rotate)Texture|(?:Rot)?Target(?:Remove)?|(?:Stop)?MoveToTarget|Apply(?:Rotational)?Impulse|Set(?:KeyframedMotion|ContentType|RegionPos|(?:Angular)?Velocity|Buoyancy|HoverHeight|ForceAndTorque|TimerEvent|ScriptState|Damage|TextureAnim|Sound(?:Queueing|Radius)|Vehicle(?:Type|(?:Float|Vector|Rotation)Param)|(?:Touch|Sit)?Text|Camera(?:Eye|At)Offset|PrimitiveParams|ClickAction|Link(?:Alpha|Color|PrimitiveParams(?:Fast)?|Texture(?:Anim)?|Camera|Media)|RemoteScriptAccessPin|PayPrice|LocalRot)|ScaleByFactor|Get(?:(?:Max|Min)ScaleFactor|ClosestNavPoint|StaticPath|SimStats|Env|PrimitiveParams|Link(?:PrimitiveParams|Number(?:OfSides)?|Key|Name|Media)|HTTPHeader|FreeURLs|Object(?:Details|PermMask|PrimCount)|Parcel(?:MaxPrims|Details|Prim(?:Count|Owners))|Attached|(?:SPMax|Free|Used)Memory|Region(?:Name|TimeDilation|FPS|Corner|AgentCount)|Root(?:Position|Rotation)|UnixTime|(?:Parcel|Region)Flags|(?:Wall|GMT)clock|SimulatorHostname|BoundingBox|GeometricCenter|Creator|NumberOf(?:Prims|NotecardLines|Sides)|Animation(?:List)?|(?:Camera|Local)(?:Pos|Rot)|Vel|Accel|Omega|Time(?:stamp|OfDay)|(?:Object|CenterOf)?Mass|MassMKS|Energy|Owner|(?:Owner)?Key|SunDirection|Texture(?:Offset|Scale|Rot)|Inventory(?:Number|Name|Key|Type|Creator|PermMask)|Permissions(?:Key)?|StartParameter|List(?:Length|EntryType)|Date|Agent(?:Size|Info|Language|List)|LandOwnerAt|NotecardLine|Script(?:Name|State))|(?:Get|Reset|GetAndReset)Time|PlaySound(?:Slave)?|LoopSound(?:Master|Slave)?|(?:Trigger|Stop|Preload)Sound|(?:(?:Get|Delete)Sub|Insert)String|To(?:Upper|Lower)|Give(?:InventoryList|Money)|RezObject|(?:Stop)?LookAt|Sleep|CollisionFilter|(?:Take|Release)Controls|DetachFromAvatar|AttachToAvatar(?:Temp)?|InstantMessage|(?:GetNext)?Email|StopHover|MinEventDelay|RotLookAt|String(?:Length|Trim)|(?:Start|Stop)Animation|TargetOmega|RequestPermissions|(?:Create|Break)Link|BreakAllLinks|(?:Give|Remove)Inventory|Water|PassTouches|Request(?:Agent|Inventory)Data|TeleportAgent(?:Home|GlobalCoords)?|ModifyLand|CollisionSound|ResetScript|MessageLinked|PushObject|PassCollisions|AxisAngle2Rot|Rot2(?:Axis|Angle)|A(?:cos|sin)|AngleBetween|AllowInventoryDrop|SubStringIndex|List2(?:CSV|Integer|Json|Float|String|Key|Vector|Rot|List(?:Strided)?)|DeleteSubList|List(?:Statistics|Sort|Randomize|(?:Insert|Find|Replace)List)|EdgeOfWorld|AdjustSoundVolume|Key2Name|TriggerSoundLimited|EjectFromLand|(?:CSV|ParseString)2List|OverMyLand|SameGroup|UnSit|Ground(?:Slope|Normal|Contour)|GroundRepel|(?:Set|Remove)VehicleFlags|(?:AvatarOn)?(?:Link)?SitTarget|Script(?:Danger|Profiler)|Dialog|VolumeDetect|ResetOtherScript|RemoteLoadScriptPin|(?:Open|Close)RemoteDataChannel|SendRemoteData|RemoteDataReply|(?:Integer|String)ToBase64|XorBase64|Log(?:10)?|Base64To(?:String|Integer)|ParseStringKeepNulls|RezAtRoot|RequestSimulatorData|ForceMouselook|(?:Load|Release|(?:E|Une)scape)URL|ParcelMedia(?:CommandList|Query)|ModPow|MapDestination|(?:RemoveFrom|AddTo|Reset)Land(?:Pass|Ban)List|(?:Set|Clear)CameraParams|HTTP(?:Request|Response)|TextBox|DetectedTouch(?:UV|Face|Pos|(?:N|Bin)ormal|ST)|(?:MD5|SHA1|DumpList2)String|Request(?:Secure)?URL|Clear(?:Prim|Link)Media|(?:Link)?ParticleSystem|(?:Get|Request)(?:Username|DisplayName)|RegionSayTo|CastRay|GenerateKey|TransferLindenDollars|ManageEstateAccess|(?:Create|Delete)Character|ExecCharacterCmd|Evade|FleeFrom|NavigateTo|PatrolPoints|Pursue|UpdateCharacter|WanderWithin))\\b'
    lsl_constants_float = '\\b(?:DEG_TO_RAD|PI(?:_BY_TWO)?|RAD_TO_DEG|SQRT2|TWO_PI)\\b'
    lsl_constants_integer = '\\b(?:JSON_APPEND|STATUS_(?:PHYSICS|ROTATE_[XYZ]|PHANTOM|SANDBOX|BLOCK_GRAB(?:_OBJECT)?|(?:DIE|RETURN)_AT_EDGE|CAST_SHADOWS|OK|MALFORMED_PARAMS|TYPE_MISMATCH|BOUNDS_ERROR|NOT_(?:FOUND|SUPPORTED)|INTERNAL_ERROR|WHITELIST_FAILED)|AGENT(?:_(?:BY_(?:LEGACY_|USER)NAME|FLYING|ATTACHMENTS|SCRIPTED|MOUSELOOK|SITTING|ON_OBJECT|AWAY|WALKING|IN_AIR|TYPING|CROUCHING|BUSY|ALWAYS_RUN|AUTOPILOT|LIST_(?:PARCEL(?:_OWNER)?|REGION)))?|CAMERA_(?:PITCH|DISTANCE|BEHINDNESS_(?:ANGLE|LAG)|(?:FOCUS|POSITION)(?:_(?:THRESHOLD|LOCKED|LAG))?|FOCUS_OFFSET|ACTIVE)|ANIM_ON|LOOP|REVERSE|PING_PONG|SMOOTH|ROTATE|SCALE|ALL_SIDES|LINK_(?:ROOT|SET|ALL_(?:OTHERS|CHILDREN)|THIS)|ACTIVE|PASSIVE|SCRIPTED|CONTROL_(?:FWD|BACK|(?:ROT_)?(?:LEFT|RIGHT)|UP|DOWN|(?:ML_)?LBUTTON)|PERMISSION_(?:RETURN_OBJECTS|DEBIT|OVERRIDE_ANIMATIONS|SILENT_ESTATE_MANAGEMENT|TAKE_CONTROLS|TRIGGER_ANIMATION|ATTACH|CHANGE_LINKS|(?:CONTROL|TRACK)_CAMERA|TELEPORT)|INVENTORY_(?:TEXTURE|SOUND|OBJECT|SCRIPT|LANDMARK|CLOTHING|NOTECARD|BODYPART|ANIMATION|GESTURE|ALL|NONE)|CHANGED_(?:INVENTORY|COLOR|SHAPE|SCALE|TEXTURE|LINK|ALLOWED_DROP|OWNER|REGION(?:_START)?|TELEPORT|MEDIA)|OBJECT_(?:(?:PHYSICS|SERVER|STREAMING)_COST|UNKNOWN_DETAIL|CHARACTER_TIME|PHANTOM|PHYSICS|TEMP_ON_REZ|NAME|DESC|POS|PRIM_EQUIVALENCE|RETURN_(?:PARCEL(?:_OWNER)?|REGION)|ROO?T|VELOCITY|OWNER|GROUP|CREATOR|ATTACHED_POINT|RENDER_WEIGHT|PATHFINDING_TYPE|(?:RUNNING|TOTAL)_SCRIPT_COUNT|SCRIPT_(?:MEMORY|TIME))|TYPE_(?:INTEGER|FLOAT|STRING|KEY|VECTOR|ROTATION|INVALID)|(?:DEBUG|PUBLIC)_CHANNEL|ATTACH_(?:AVATAR_CENTER|CHEST|HEAD|BACK|PELVIS|MOUTH|CHIN|NECK|NOSE|BELLY|[LR](?:SHOULDER|HAND|FOOT|EAR|EYE|[UL](?:ARM|LEG)|HIP)|(?:LEFT|RIGHT)_PEC|HUD_(?:CENTER_[12]|TOP_(?:RIGHT|CENTER|LEFT)|BOTTOM(?:_(?:RIGHT|LEFT))?))|LAND_(?:LEVEL|RAISE|LOWER|SMOOTH|NOISE|REVERT)|DATA_(?:ONLINE|NAME|BORN|SIM_(?:POS|STATUS|RATING)|PAYINFO)|PAYMENT_INFO_(?:ON_FILE|USED)|REMOTE_DATA_(?:CHANNEL|REQUEST|REPLY)|PSYS_(?:PART_(?:BF_(?:ZERO|ONE(?:_MINUS_(?:DEST_COLOR|SOURCE_(ALPHA|COLOR)))?|DEST_COLOR|SOURCE_(ALPHA|COLOR))|BLEND_FUNC_(DEST|SOURCE)|FLAGS|(?:START|END)_(?:COLOR|ALPHA|SCALE|GLOW)|MAX_AGE|(?:RIBBON|WIND|INTERP_(?:COLOR|SCALE)|BOUNCE|FOLLOW_(?:SRC|VELOCITY)|TARGET_(?:POS|LINEAR)|EMISSIVE)_MASK)|SRC_(?:MAX_AGE|PATTERN|ANGLE_(?:BEGIN|END)|BURST_(?:RATE|PART_COUNT|RADIUS|SPEED_(?:MIN|MAX))|ACCEL|TEXTURE|TARGET_KEY|OMEGA|PATTERN_(?:DROP|EXPLODE|ANGLE(?:_CONE(?:_EMPTY)?)?)))|VEHICLE_(?:REFERENCE_FRAME|TYPE_(?:NONE|SLED|CAR|BOAT|AIRPLANE|BALLOON)|(?:LINEAR|ANGULAR)_(?:FRICTION_TIMESCALE|MOTOR_DIRECTION)|LINEAR_MOTOR_OFFSET|HOVER_(?:HEIGHT|EFFICIENCY|TIMESCALE)|BUOYANCY|(?:LINEAR|ANGULAR)_(?:DEFLECTION_(?:EFFICIENCY|TIMESCALE)|MOTOR_(?:DECAY_)?TIMESCALE)|VERTICAL_ATTRACTION_(?:EFFICIENCY|TIMESCALE)|BANKING_(?:EFFICIENCY|MIX|TIMESCALE)|FLAG_(?:NO_DEFLECTION_UP|LIMIT_(?:ROLL_ONLY|MOTOR_UP)|HOVER_(?:(?:WATER|TERRAIN|UP)_ONLY|GLOBAL_HEIGHT)|MOUSELOOK_(?:STEER|BANK)|CAMERA_DECOUPLED))|PRIM_(?:TYPE(?:_(?:BOX|CYLINDER|PRISM|SPHERE|TORUS|TUBE|RING|SCULPT))?|HOLE_(?:DEFAULT|CIRCLE|SQUARE|TRIANGLE)|MATERIAL(?:_(?:STONE|METAL|GLASS|WOOD|FLESH|PLASTIC|RUBBER))?|SHINY_(?:NONE|LOW|MEDIUM|HIGH)|BUMP_(?:NONE|BRIGHT|DARK|WOOD|BARK|BRICKS|CHECKER|CONCRETE|TILE|STONE|DISKS|GRAVEL|BLOBS|SIDING|LARGETILE|STUCCO|SUCTION|WEAVE)|TEXGEN_(?:DEFAULT|PLANAR)|SCULPT_(?:TYPE_(?:SPHERE|TORUS|PLANE|CYLINDER|MASK)|FLAG_(?:MIRROR|INVERT))|PHYSICS(?:_(?:SHAPE_(?:CONVEX|NONE|PRIM|TYPE)))?|(?:POS|ROT)_LOCAL|SLICE|TEXT|FLEXIBLE|POINT_LIGHT|TEMP_ON_REZ|PHANTOM|POSITION|SIZE|ROTATION|TEXTURE|NAME|OMEGA|DESC|LINK_TARGET|COLOR|BUMP_SHINY|FULLBRIGHT|TEXGEN|GLOW|MEDIA_(?:ALT_IMAGE_ENABLE|CONTROLS|(?:CURRENT|HOME)_URL|AUTO_(?:LOOP|PLAY|SCALE|ZOOM)|FIRST_CLICK_INTERACT|(?:WIDTH|HEIGHT)_PIXELS|WHITELIST(?:_ENABLE)?|PERMS_(?:INTERACT|CONTROL)|PARAM_MAX|CONTROLS_(?:STANDARD|MINI)|PERM_(?:NONE|OWNER|GROUP|ANYONE)|MAX_(?:URL_LENGTH|WHITELIST_(?:SIZE|COUNT)|(?:WIDTH|HEIGHT)_PIXELS)))|MASK_(?:BASE|OWNER|GROUP|EVERYONE|NEXT)|PERM_(?:TRANSFER|MODIFY|COPY|MOVE|ALL)|PARCEL_(?:MEDIA_COMMAND_(?:STOP|PAUSE|PLAY|LOOP|TEXTURE|URL|TIME|AGENT|UNLOAD|AUTO_ALIGN|TYPE|SIZE|DESC|LOOP_SET)|FLAG_(?:ALLOW_(?:FLY|(?:GROUP_)?SCRIPTS|LANDMARK|TERRAFORM|DAMAGE|CREATE_(?:GROUP_)?OBJECTS)|USE_(?:ACCESS_(?:GROUP|LIST)|BAN_LIST|LAND_PASS_LIST)|LOCAL_SOUND_ONLY|RESTRICT_PUSHOBJECT|ALLOW_(?:GROUP|ALL)_OBJECT_ENTRY)|COUNT_(?:TOTAL|OWNER|GROUP|OTHER|SELECTED|TEMP)|DETAILS_(?:NAME|DESC|OWNER|GROUP|AREA|ID|SEE_AVATARS))|LIST_STAT_(?:MAX|MIN|MEAN|MEDIAN|STD_DEV|SUM(?:_SQUARES)?|NUM_COUNT|GEOMETRIC_MEAN|RANGE)|PAY_(?:HIDE|DEFAULT)|REGION_FLAG_(?:ALLOW_DAMAGE|FIXED_SUN|BLOCK_TERRAFORM|SANDBOX|DISABLE_(?:COLLISIONS|PHYSICS)|BLOCK_FLY|ALLOW_DIRECT_TELEPORT|RESTRICT_PUSHOBJECT)|HTTP_(?:METHOD|MIMETYPE|BODY_(?:MAXLENGTH|TRUNCATED)|CUSTOM_HEADER|PRAGMA_NO_CACHE|VERBOSE_THROTTLE|VERIFY_CERT)|STRING_(?:TRIM(?:_(?:HEAD|TAIL))?)|CLICK_ACTION_(?:NONE|TOUCH|SIT|BUY|PAY|OPEN(?:_MEDIA)?|PLAY|ZOOM)|TOUCH_INVALID_FACE|PROFILE_(?:NONE|SCRIPT_MEMORY)|RC_(?:DATA_FLAGS|DETECT_PHANTOM|GET_(?:LINK_NUM|NORMAL|ROOT_KEY)|MAX_HITS|REJECT_(?:TYPES|AGENTS|(?:NON)?PHYSICAL|LAND))|RCERR_(?:CAST_TIME_EXCEEDED|SIM_PERF_LOW|UNKNOWN)|ESTATE_ACCESS_(?:ALLOWED_(?:AGENT|GROUP)_(?:ADD|REMOVE)|BANNED_AGENT_(?:ADD|REMOVE))|DENSITY|FRICTION|RESTITUTION|GRAVITY_MULTIPLIER|KFM_(?:COMMAND|CMD_(?:PLAY|STOP|PAUSE|SET_MODE)|MODE|FORWARD|LOOP|PING_PONG|REVERSE|DATA|ROTATION|TRANSLATION)|ERR_(?:GENERIC|PARCEL_PERMISSIONS|MALFORMED_PARAMS|RUNTIME_PERMISSIONS|THROTTLED)|CHARACTER_(?:CMD_(?:(?:SMOOTH_)?STOP|JUMP)|DESIRED_(?:TURN_)?SPEED|RADIUS|STAY_WITHIN_PARCEL|LENGTH|ORIENTATION|ACCOUNT_FOR_SKIPPED_FRAMES|AVOIDANCE_MODE|TYPE(?:_(?:[A-D]|NONE))?|MAX_(?:DECEL|TURN_RADIUS|(?:ACCEL|SPEED)))|PURSUIT_(?:OFFSET|FUZZ_FACTOR|GOAL_TOLERANCE|INTERCEPT)|REQUIRE_LINE_OF_SIGHT|FORCE_DIRECT_PATH|VERTICAL|HORIZONTAL|AVOID_(?:CHARACTERS|DYNAMIC_OBSTACLES|NONE)|PU_(?:EVADE_(?:HIDDEN|SPOTTED)|FAILURE_(?:DYNAMIC_PATHFINDING_DISABLED|INVALID_(?:GOAL|START)|NO_(?:NAVMESH|VALID_DESTINATION)|OTHER|TARGET_GONE|(?:PARCEL_)?UNREACHABLE)|(?:GOAL|SLOWDOWN_DISTANCE)_REACHED)|TRAVERSAL_TYPE(?:_(?:FAST|NONE|SLOW))?|CONTENT_TYPE_(?:ATOM|FORM|HTML|JSON|LLSD|RSS|TEXT|XHTML|XML)|GCNP_(?:RADIUS|STATIC)|(?:PATROL|WANDER)_PAUSE_AT_WAYPOINTS|OPT_(?:AVATAR|CHARACTER|EXCLUSION_VOLUME|LEGACY_LINKSET|MATERIAL_VOLUME|OTHER|STATIC_OBSTACLE|WALKABLE)|SIM_STAT_PCT_CHARS_STEPPED)\\b'
    lsl_constants_integer_boolean = '\\b(?:FALSE|TRUE)\\b'
    lsl_constants_rotation = '\\b(?:ZERO_ROTATION)\\b'
    lsl_constants_string = '\\b(?:EOF|JSON_(?:ARRAY|DELETE|FALSE|INVALID|NULL|NUMBER|OBJECT|STRING|TRUE)|NULL_KEY|TEXTURE_(?:BLANK|DEFAULT|MEDIA|PLYWOOD|TRANSPARENT)|URL_REQUEST_(?:GRANTED|DENIED))\\b'
    lsl_constants_vector = '\\b(?:TOUCH_INVALID_(?:TEXCOORD|VECTOR)|ZERO_VECTOR)\\b'
    lsl_invalid_broken = '\\b(?:LAND_(?:LARGE|MEDIUM|SMALL)_BRUSH)\\b'
    lsl_invalid_deprecated = '\\b(?:ATTACH_[LR]PEC|DATA_RATING|OBJECT_ATTACHMENT_(?:GEOMETRY_BYTES|SURFACE_AREA)|PRIM_(?:CAST_SHADOWS|MATERIAL_LIGHT|TYPE_LEGACY)|PSYS_SRC_(?:INNER|OUTER)ANGLE|VEHICLE_FLAG_NO_FLY_UP|ll(?:Cloud|Make(?:Explosion|Fountain|Smoke|Fire)|RemoteDataSetRegion|Sound(?:Preload)?|XorBase64Strings(?:Correct)?))\\b'
    lsl_invalid_illegal = '\\b(?:event)\\b'
    lsl_invalid_unimplemented = '\\b(?:CHARACTER_(?:MAX_ANGULAR_(?:ACCEL|SPEED)|TURN_SPEED_MULTIPLIER)|PERMISSION_(?:CHANGE_(?:JOINTS|PERMISSIONS)|RELEASE_OWNERSHIP|REMAP_CONTROLS)|PRIM_PHYSICS_MATERIAL|PSYS_SRC_OBJ_REL_MASK|ll(?:CollisionSprite|(?:Stop)?PointAt|(?:(?:Refresh|Set)Prim)URL|(?:Take|Release)Camera|RemoteLoadScript))\\b'
    lsl_reserved_godmode = '\\b(?:ll(?:GodLikeRezObject|Set(?:Inventory|Object)PermMask))\\b'
    lsl_reserved_log = '\\b(?:print)\\b'
    lsl_operators = '\\+\\+|\\-\\-|<<|>>|&&?|\\|\\|?|\\^|~|[!%<>=*+\\-/]=?'
    tokens = {'root': [('//.*?\\n', Comment.Single), ('/\\*', Comment.Multiline, 'comment'), ('"', String.Double, 'string'), (lsl_keywords, Keyword), (lsl_types, Keyword.Type), (lsl_states, Name.Class), (lsl_events, Name.Builtin), (lsl_functions_builtin, Name.Function), (lsl_constants_float, Keyword.Constant), (lsl_constants_integer, Keyword.Constant), (lsl_constants_integer_boolean, Keyword.Constant), (lsl_constants_rotation, Keyword.Constant), (lsl_constants_string, Keyword.Constant), (lsl_constants_vector, Keyword.Constant), (lsl_invalid_broken, Error), (lsl_invalid_deprecated, Error), (lsl_invalid_illegal, Error), (lsl_invalid_unimplemented, Error), (lsl_reserved_godmode, Keyword.Reserved), (lsl_reserved_log, Keyword.Reserved), ('\\b([a-zA-Z_]\\w*)\\b', Name.Variable), ('(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d*', Number.Float), ('(\\d+\\.\\d*|\\.\\d+)', Number.Float), ('0[xX][0-9a-fA-F]+', Number.Hex), ('\\d+', Number.Integer), (lsl_operators, Operator), (':=?', Error), ('[,;{}()\\[\\]]', Punctuation), ('\\n+', Whitespace), ('\\s+', Whitespace)], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'string': [('\\\\([nt"\\\\])', String.Escape), ('"', String.Double, '#pop'), ('\\\\.', Error), ('[^"\\\\]+', String.Double)]}



class AppleScriptLexer(RegexLexer):
    """
    For AppleScript source code,
    including `AppleScript Studio
    <http://developer.apple.com/documentation/AppleScript/
    Reference/StudioReference>`_.
    Contributed by Andreas Amann <aamann@mac.com>.
    """
    name = 'AppleScript'
    url = 'https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/introduction/ASLR_intro.html'
    aliases = ['applescript']
    filenames = ['*.applescript']
    version_added = '1.0'
    flags = re.MULTILINE | re.DOTALL
    Identifiers = '[a-zA-Z]\\w*'
    Literals = ('AppleScript', 'current application', 'false', 'linefeed', 'missing value', 'pi', 'quote', 'result', 'return', 'space', 'tab', 'text item delimiters', 'true', 'version')
    Classes = ('alias ', 'application ', 'boolean ', 'class ', 'constant ', 'date ', 'file ', 'integer ', 'list ', 'number ', 'POSIX file ', 'real ', 'record ', 'reference ', 'RGB color ', 'script ', 'text ', 'unit types', '(?:Unicode )?text', 'string')
    BuiltIn = ('attachment', 'attribute run', 'character', 'day', 'month', 'paragraph', 'word', 'year')
    HandlerParams = ('about', 'above', 'against', 'apart from', 'around', 'aside from', 'at', 'below', 'beneath', 'beside', 'between', 'for', 'given', 'instead of', 'on', 'onto', 'out of', 'over', 'since')
    Commands = ('ASCII (character|number)', 'activate', 'beep', 'choose URL', 'choose application', 'choose color', 'choose file( name)?', 'choose folder', 'choose from list', 'choose remote application', 'clipboard info', 'close( access)?', 'copy', 'count', 'current date', 'delay', 'delete', 'display (alert|dialog)', 'do shell script', 'duplicate', 'exists', 'get eof', 'get volume settings', 'info for', 'launch', 'list (disks|folder)', 'load script', 'log', 'make', 'mount volume', 'new', 'offset', 'open( (for access|location))?', 'path to', 'print', 'quit', 'random number', 'read', 'round', 'run( script)?', 'say', 'scripting components', 'set (eof|the clipboard to|volume)', 'store script', 'summarize', 'system attribute', 'system info', 'the clipboard', 'time to GMT', 'write', 'quoted form')
    References = ('(in )?back of', '(in )?front of', '[0-9]+(st|nd|rd|th)', 'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'after', 'back', 'before', 'behind', 'every', 'front', 'index', 'last', 'middle', 'some', 'that', 'through', 'thru', 'where', 'whose')
    Operators = ('and', 'or', 'is equal', 'equals', '(is )?equal to', 'is not', "isn't", "isn't equal( to)?", 'is not equal( to)?', "doesn't equal", 'does not equal', '(is )?greater than', 'comes after', 'is not less than or equal( to)?', "isn't less than or equal( to)?", '(is )?less than', 'comes before', 'is not greater than or equal( to)?', "isn't greater than or equal( to)?", '(is  )?greater than or equal( to)?', 'is not less than', "isn't less than", 'does not come before', "doesn't come before", '(is )?less than or equal( to)?', 'is not greater than', "isn't greater than", 'does not come after', "doesn't come after", 'starts? with', 'begins? with', 'ends? with', 'contains?', 'does not contain', "doesn't contain", 'is in', 'is contained by', 'is not in', 'is not contained by', "isn't contained by", 'div', 'mod', 'not', '(a  )?(ref( to)?|reference to)', 'is', 'does')
    Control = ('considering', 'else', 'error', 'exit', 'from', 'if', 'ignoring', 'in', 'repeat', 'tell', 'then', 'times', 'to', 'try', 'until', 'using terms from', 'while', 'whith', 'with timeout( of)?', 'with transaction', 'by', 'continue', 'end', 'its?', 'me', 'my', 'return', 'of', 'as')
    Declarations = ('global', 'local', 'prop(erty)?', 'set', 'get')
    Reserved = ('but', 'put', 'returning', 'the')
    StudioClasses = ('action cell', 'alert reply', 'application', 'box', 'browser( cell)?', 'bundle', 'button( cell)?', 'cell', 'clip view', 'color well', 'color-panel', 'combo box( item)?', 'control', 'data( (cell|column|item|row|source))?', 'default entry', 'dialog reply', 'document', 'drag info', 'drawer', 'event', 'font(-panel)?', 'formatter', 'image( (cell|view))?', 'matrix', 'menu( item)?', 'item', 'movie( view)?', 'open-panel', 'outline view', 'panel', 'pasteboard', 'plugin', 'popup button', 'progress indicator', 'responder', 'save-panel', 'scroll view', 'secure text field( cell)?', 'slider', 'sound', 'split view', 'stepper', 'tab view( item)?', 'table( (column|header cell|header view|view))', 'text( (field( cell)?|view))?', 'toolbar( item)?', 'user-defaults', 'view', 'window')
    StudioEvents = ('accept outline drop', 'accept table drop', 'action', 'activated', 'alert ended', 'awake from nib', 'became key', 'became main', 'begin editing', 'bounds changed', 'cell value', 'cell value changed', 'change cell value', 'change item value', 'changed', 'child of item', 'choose menu item', 'clicked', 'clicked toolbar item', 'closed', 'column clicked', 'column moved', 'column resized', 'conclude drop', 'data representation', 'deminiaturized', 'dialog ended', 'document nib name', 'double clicked', 'drag( (entered|exited|updated))?', 'drop', 'end editing', 'exposed', 'idle', 'item expandable', 'item value', 'item value changed', 'items changed', 'keyboard down', 'keyboard up', 'launched', 'load data representation', 'miniaturized', 'mouse down', 'mouse dragged', 'mouse entered', 'mouse exited', 'mouse moved', 'mouse up', 'moved', 'number of browser rows', 'number of items', 'number of rows', 'open untitled', 'opened', 'panel ended', 'parameters updated', 'plugin loaded', 'prepare drop', 'prepare outline drag', 'prepare outline drop', 'prepare table drag', 'prepare table drop', 'read from file', 'resigned active', 'resigned key', 'resigned main', 'resized( sub views)?', 'right mouse down', 'right mouse dragged', 'right mouse up', 'rows changed', 'scroll wheel', 'selected tab view item', 'selection changed', 'selection changing', 'should begin editing', 'should close', 'should collapse item', 'should end editing', 'should expand item', 'should open( untitled)?', 'should quit( after last window closed)?', 'should select column', 'should select item', 'should select row', 'should select tab view item', 'should selection change', 'should zoom', 'shown', 'update menu item', 'update parameters', 'update toolbar item', 'was hidden', 'was miniaturized', 'will become active', 'will close', 'will dismiss', 'will display browser cell', 'will display cell', 'will display item cell', 'will display outline cell', 'will finish launching', 'will hide', 'will miniaturize', 'will move', 'will open', 'will pop up', 'will quit', 'will resign active', 'will resize( sub views)?', 'will select tab view item', 'will show', 'will zoom', 'write to file', 'zoomed')
    StudioCommands = ('animate', 'append', 'call method', 'center', 'close drawer', 'close panel', 'display', 'display alert', 'display dialog', 'display panel', 'go', 'hide', 'highlight', 'increment', 'item for', 'load image', 'load movie', 'load nib', 'load panel', 'load sound', 'localized string', 'lock focus', 'log', 'open drawer', 'path for', 'pause', 'perform action', 'play', 'register', 'resume', 'scroll', 'select( all)?', 'show', 'size to fit', 'start', 'step back', 'step forward', 'stop', 'synchronize', 'unlock focus', 'update')
    StudioProperties = ('accepts arrow key', 'action method', 'active', 'alignment', 'allowed identifiers', 'allows branch selection', 'allows column reordering', 'allows column resizing', 'allows column selection', 'allows customization', 'allows editing text attributes', 'allows empty selection', 'allows mixed state', 'allows multiple selection', 'allows reordering', 'allows undo', 'alpha( value)?', 'alternate image', 'alternate increment value', 'alternate title', 'animation delay', 'associated file name', 'associated object', 'auto completes', 'auto display', 'auto enables items', 'auto repeat', 'auto resizes( outline column)?', 'auto save expanded items', 'auto save name', 'auto save table columns', 'auto saves configuration', 'auto scroll', 'auto sizes all columns to fit', 'auto sizes cells', 'background color', 'bezel state', 'bezel style', 'bezeled', 'border rect', 'border type', 'bordered', 'bounds( rotation)?', 'box type', 'button returned', 'button type', 'can choose directories', 'can choose files', 'can draw', 'can hide', 'cell( (background color|size|type))?', 'characters', 'class', 'click count', 'clicked( data)? column', 'clicked data item', 'clicked( data)? row', 'closeable', 'collating', 'color( (mode|panel))', 'command key down', 'configuration', 'content(s| (size|view( margins)?))?', 'context', 'continuous', 'control key down', 'control size', 'control tint', 'control view', 'controller visible', 'coordinate system', 'copies( on scroll)?', 'corner view', 'current cell', 'current column', 'current( field)?  editor', 'current( menu)? item', 'current row', 'current tab view item', 'data source', 'default identifiers', 'delta (x|y|z)', 'destination window', 'directory', 'display mode', 'displayed cell', 'document( (edited|rect|view))?', 'double value', 'dragged column', 'dragged distance', 'dragged items', 'draws( cell)? background', 'draws grid', 'dynamically scrolls', 'echos bullets', 'edge', 'editable', 'edited( data)? column', 'edited data item', 'edited( data)? row', 'enabled', 'enclosing scroll view', 'ending page', 'error handling', 'event number', 'event type', 'excluded from windows menu', 'executable path', 'expanded', 'fax number', 'field editor', 'file kind', 'file name', 'file type', 'first responder', 'first visible column', 'flipped', 'floating', 'font( panel)?', 'formatter', 'frameworks path', 'frontmost', 'gave up', 'grid color', 'has data items', 'has horizontal ruler', 'has horizontal scroller', 'has parent data item', 'has resize indicator', 'has shadow', 'has sub menu', 'has vertical ruler', 'has vertical scroller', 'header cell', 'header view', 'hidden', 'hides when deactivated', 'highlights by', 'horizontal line scroll', 'horizontal page scroll', 'horizontal ruler view', 'horizontally resizable', 'icon image', 'id', 'identifier', 'ignores multiple clicks', 'image( (alignment|dims when disabled|frame style|scaling))?', 'imports graphics', 'increment value', 'indentation per level', 'indeterminate', 'index', 'integer value', 'intercell spacing', 'item height', 'key( (code|equivalent( modifier)?|window))?', 'knob thickness', 'label', 'last( visible)? column', 'leading offset', 'leaf', 'level', 'line scroll', 'loaded', 'localized sort', 'location', 'loop mode', 'main( (bunde|menu|window))?', 'marker follows cell', 'matrix mode', 'maximum( content)? size', 'maximum visible columns', 'menu( form representation)?', 'miniaturizable', 'miniaturized', 'minimized image', 'minimized title', 'minimum column width', 'minimum( content)? size', 'modal', 'modified', 'mouse down state', 'movie( (controller|file|rect))?', 'muted', 'name', 'needs display', 'next state', 'next text', 'number of tick marks', 'only tick mark values', 'opaque', 'open panel', 'option key down', 'outline table column', 'page scroll', 'pages across', 'pages down', 'palette label', 'pane splitter', 'parent data item', 'parent window', 'pasteboard', 'path( (names|separator))?', 'playing', 'plays every frame', 'plays selection only', 'position', 'preferred edge', 'preferred type', 'pressure', 'previous text', 'prompt', 'properties', 'prototype cell', 'pulls down', 'rate', 'released when closed', 'repeated', 'requested print time', 'required file type', 'resizable', 'resized column', 'resource path', 'returns records', 'reuses columns', 'rich text', 'roll over', 'row height', 'rulers visible', 'save panel', 'scripts path', 'scrollable', 'selectable( identifiers)?', 'selected cell', 'selected( data)? columns?', 'selected data items?', 'selected( data)? rows?', 'selected item identifier', 'selection by rect', 'send action on arrow key', 'sends action when done editing', 'separates columns', 'separator item', 'sequence number', 'services menu', 'shared frameworks path', 'shared support path', 'sheet', 'shift key down', 'shows alpha', 'shows state by', 'size( mode)?', 'smart insert delete enabled', 'sort case sensitivity', 'sort column', 'sort order', 'sort type', 'sorted( data rows)?', 'sound', 'source( mask)?', 'spell checking enabled', 'starting page', 'state', 'string value', 'sub menu', 'super menu', 'super view', 'tab key traverses cells', 'tab state', 'tab type', 'tab view', 'table view', 'tag', 'target( printer)?', 'text color', 'text container insert', 'text container origin', 'text returned', 'tick mark position', 'time stamp', 'title(d| (cell|font|height|position|rect))?', 'tool tip', 'toolbar', 'trailing offset', 'transparent', 'treat packages as directories', 'truncated labels', 'types', 'unmodified characters', 'update views', 'use sort indicator', 'user defaults', 'uses data source', 'uses ruler', 'uses threaded animation', 'uses title from previous column', 'value wraps', 'version', 'vertical( (line scroll|page scroll|ruler view))?', 'vertically resizable', 'view', 'visible( document rect)?', 'volume', 'width', 'window', 'windows menu', 'wraps', 'zoomable', 'zoomed')
    tokens = {'root': [('\\s+', Text), ('¬\\n', String.Escape), ("'s\\s+", Text), ('(--|#).*?$', Comment), ('\\(\\*', Comment.Multiline, 'comment'), ('[(){}!,.:]', Punctuation), ('(«)([^»]+)(»)', bygroups(Text, Name.Builtin, Text)), ('\\b((?:considering|ignoring)\\s*)(application responses|case|diacriticals|hyphens|numeric strings|punctuation|white space)', bygroups(Keyword, Name.Builtin)), ('(-|\\*|\\+|&|≠|>=?|<=?|=|≥|≤|/|÷|\\^)', Operator), ('\\b({})\\b'.format('|'.join(Operators)), Operator.Word), ('^(\\s*(?:on|end)\\s+)({})'.format('|'.join(StudioEvents[::-1])), bygroups(Keyword, Name.Function)), ('^(\\s*)(in|on|script|to)(\\s+)', bygroups(Text, Keyword, Text)), ('\\b(as )({})\\b'.format('|'.join(Classes)), bygroups(Keyword, Name.Class)), ('\\b({})\\b'.format('|'.join(Literals)), Name.Constant), ('\\b({})\\b'.format('|'.join(Commands)), Name.Builtin), ('\\b({})\\b'.format('|'.join(Control)), Keyword), ('\\b({})\\b'.format('|'.join(Declarations)), Keyword), ('\\b({})\\b'.format('|'.join(Reserved)), Name.Builtin), ('\\b({})s?\\b'.format('|'.join(BuiltIn)), Name.Builtin), ('\\b({})\\b'.format('|'.join(HandlerParams)), Name.Builtin), ('\\b({})\\b'.format('|'.join(StudioProperties)), Name.Attribute), ('\\b({})s?\\b'.format('|'.join(StudioClasses)), Name.Builtin), ('\\b({})\\b'.format('|'.join(StudioCommands)), Name.Builtin), ('\\b({})\\b'.format('|'.join(References)), Name.Builtin), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), (f'\\b({Identifiers})\\b', Name.Variable), ('[-+]?(\\d+\\.\\d*|\\d*\\.\\d+)(E[-+][0-9]+)?', Number.Float), ('[-+]?\\d+', Number.Integer)], 'comment': [('\\(\\*', Comment.Multiline, '#push'), ('\\*\\)', Comment.Multiline, '#pop'), ('[^*(]+', Comment.Multiline), ('[*(]', Comment.Multiline)]}



class RexxLexer(RegexLexer):
    """
    Rexx is a scripting language available for
    a wide range of different platforms with its roots found on mainframe
    systems. It is popular for I/O- and data based tasks and can act as glue
    language to bind different applications together.
    """
    name = 'Rexx'
    url = 'http://www.rexxinfo.org/'
    aliases = ['rexx', 'arexx']
    filenames = ['*.rexx', '*.rex', '*.rx', '*.arexx']
    mimetypes = ['text/x-rexx']
    version_added = '2.0'
    flags = re.IGNORECASE
    tokens = {'root': [('\\s+', Whitespace), ('/\\*', Comment.Multiline, 'comment'), ('"', String, 'string_double'), ("'", String, 'string_single'), ('[0-9]+(\\.[0-9]+)?(e[+-]?[0-9])?', Number), ('([a-z_]\\w*)(\\s*)(:)(\\s*)(procedure)\\b', bygroups(Name.Function, Whitespace, Operator, Whitespace, Keyword.Declaration)), ('([a-z_]\\w*)(\\s*)(:)', bygroups(Name.Label, Whitespace, Operator)), include('function'), include('keyword'), include('operator'), ('[a-z_]\\w*', Text)], 'function': [(words(('abbrev', 'abs', 'address', 'arg', 'b2x', 'bitand', 'bitor', 'bitxor', 'c2d', 'c2x', 'center', 'charin', 'charout', 'chars', 'compare', 'condition', 'copies', 'd2c', 'd2x', 'datatype', 'date', 'delstr', 'delword', 'digits', 'errortext', 'form', 'format', 'fuzz', 'insert', 'lastpos', 'left', 'length', 'linein', 'lineout', 'lines', 'max', 'min', 'overlay', 'pos', 'queued', 'random', 'reverse', 'right', 'sign', 'sourceline', 'space', 'stream', 'strip', 'substr', 'subword', 'symbol', 'time', 'trace', 'translate', 'trunc', 'value', 'verify', 'word', 'wordindex', 'wordlength', 'wordpos', 'words', 'x2b', 'x2c', 'x2d', 'xrange'), suffix='(\\s*)(\\()'), bygroups(Name.Builtin, Whitespace, Operator))], 'keyword': [('(address|arg|by|call|do|drop|else|end|exit|for|forever|if|interpret|iterate|leave|nop|numeric|off|on|options|parse|pull|push|queue|return|say|select|signal|to|then|trace|until|while)\\b', Keyword.Reserved)], 'operator': [('(-|//|/|\\(|\\)|\\*\\*|\\*|\\\\<<|\\\\<|\\\\==|\\\\=|\\\\>>|\\\\>|\\\\|\\|\\||\\||&&|&|%|\\+|<<=|<<|<=|<>|<|==|=|><|>=|>>=|>>|>|¬<<|¬<|¬==|¬=|¬>>|¬>|¬|\\.|,)', Operator)], 'string_double': [('[^"\\n]+', String), ('""', String), ('"', String, '#pop'), ('\\n', Text, '#pop')], 'string_single': [("[^\\'\\n]+", String), ("\\'\\'", String), ("\\'", String, '#pop'), ('\\n', Text, '#pop')], 'comment': [('[^*]+', Comment.Multiline), ('\\*/', Comment.Multiline, '#pop'), ('\\*', Comment.Multiline)]}
    
    def _c(s):
        return re.compile(s, re.MULTILINE)
    _ADDRESS_COMMAND_PATTERN = _c('^\\s*address\\s+command\\b')
    _ADDRESS_PATTERN = _c('^\\s*address\\s+')
    _DO_WHILE_PATTERN = _c('^\\s*do\\s+while\\b')
    _IF_THEN_DO_PATTERN = _c('^\\s*if\\b.+\\bthen\\s+do\\s*$')
    _PROCEDURE_PATTERN = _c('^\\s*([a-z_]\\w*)(\\s*)(:)(\\s*)(procedure)\\b')
    _ELSE_DO_PATTERN = _c('\\belse\\s+do\\s*$')
    _PARSE_ARG_PATTERN = _c('^\\s*parse\\s+(upper\\s+)?(arg|value)\\b')
    PATTERNS_AND_WEIGHTS = ((_ADDRESS_COMMAND_PATTERN, 0.2), (_ADDRESS_PATTERN, 0.05), (_DO_WHILE_PATTERN, 0.1), (_ELSE_DO_PATTERN, 0.1), (_IF_THEN_DO_PATTERN, 0.1), (_PROCEDURE_PATTERN, 0.5), (_PARSE_ARG_PATTERN, 0.2))
    
    def analyse_text(text):
        """
        Check for initial comment and patterns that distinguish Rexx from other
        C-like languages.
        """
        if re.search('/\\*\\**\\s*rexx', text, re.IGNORECASE):
            return 1.0
        elif text.startswith('/*'):
            lowerText = text.lower()
            result = sum((weight for (pattern, weight) in RexxLexer.PATTERNS_AND_WEIGHTS if pattern.search(lowerText))) + 0.01
            return min(result, 1.0)



class MOOCodeLexer(RegexLexer):
    """
    For MOOCode (the MOO scripting language).
    """
    name = 'MOOCode'
    url = 'http://www.moo.mud.org/'
    filenames = ['*.moo']
    aliases = ['moocode', 'moo']
    mimetypes = ['text/x-moocode']
    version_added = '0.9'
    tokens = {'root': [('(0|[1-9][0-9_]*)', Number.Integer), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ('(E_PERM|E_DIV)', Name.Exception), ('((#[-0-9]+)|(\\$\\w+))', Name.Entity), ('\\b(if|else|elseif|endif|for|endfor|fork|endfork|while|endwhile|break|continue|return|try|except|endtry|finally|in)\\b', Keyword), ('(random|length)', Name.Builtin), ('(player|caller|this|args)', Name.Variable.Instance), ('\\s+', Text), ('\\n', Text), ('([!;=,{}&|:.\\[\\]@()<>?]+)', Operator), ('(\\w+)(\\()', bygroups(Name.Function, Operator)), ('(\\w+)', Text)]}



class HybrisLexer(RegexLexer):
    """
    For Hybris source code.
    """
    name = 'Hybris'
    aliases = ['hybris']
    filenames = ['*.hyb']
    mimetypes = ['text/x-hybris', 'application/x-hybris']
    url = 'https://github.com/evilsocket/hybris'
    version_added = '1.4'
    flags = re.MULTILINE | re.DOTALL
    tokens = {'root': [('^(\\s*(?:function|method|operator\\s+)+?)([a-zA-Z_]\\w*)(\\s*)(\\()', bygroups(Keyword, Name.Function, Text, Operator)), ('[^\\S\\n]+', Text), ('//.*?\\n', Comment.Single), ('/\\*.*?\\*/', Comment.Multiline), ('@[a-zA-Z_][\\w.]*', Name.Decorator), ('(break|case|catch|next|default|do|else|finally|for|foreach|of|unless|if|new|return|switch|me|throw|try|while)\\b', Keyword), ('(extends|private|protected|public|static|throws|function|method|operator)\\b', Keyword.Declaration), ('(true|false|null|__FILE__|__LINE__|__VERSION__|__LIB_PATH__|__INC_PATH__)\\b', Keyword.Constant), ('(class|struct)(\\s+)', bygroups(Keyword.Declaration, Text), 'class'), ('(import|include)(\\s+)', bygroups(Keyword.Namespace, Text), 'import'), (words(('gc_collect', 'gc_mm_items', 'gc_mm_usage', 'gc_collect_threshold', 'urlencode', 'urldecode', 'base64encode', 'base64decode', 'sha1', 'crc32', 'sha2', 'md5', 'md5_file', 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'exp', 'fabs', 'floor', 'fmod', 'log', 'log10', 'pow', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'isint', 'isfloat', 'ischar', 'isstring', 'isarray', 'ismap', 'isalias', 'typeof', 'sizeof', 'toint', 'tostring', 'fromxml', 'toxml', 'binary', 'pack', 'load', 'eval', 'var_names', 'var_values', 'user_functions', 'dyn_functions', 'methods', 'call', 'call_method', 'mknod', 'mkfifo', 'mount', 'umount2', 'umount', 'ticks', 'usleep', 'sleep', 'time', 'strtime', 'strdate', 'dllopen', 'dlllink', 'dllcall', 'dllcall_argv', 'dllclose', 'env', 'exec', 'fork', 'getpid', 'wait', 'popen', 'pclose', 'exit', 'kill', 'pthread_create', 'pthread_create_argv', 'pthread_exit', 'pthread_join', 'pthread_kill', 'smtp_send', 'http_get', 'http_post', 'http_download', 'socket', 'bind', 'listen', 'accept', 'getsockname', 'getpeername', 'settimeout', 'connect', 'server', 'recv', 'send', 'close', 'print', 'println', 'printf', 'input', 'readline', 'serial_open', 'serial_fcntl', 'serial_get_attr', 'serial_get_ispeed', 'serial_get_ospeed', 'serial_set_attr', 'serial_set_ispeed', 'serial_set_ospeed', 'serial_write', 'serial_read', 'serial_close', 'xml_load', 'xml_parse', 'fopen', 'fseek', 'ftell', 'fsize', 'fread', 'fwrite', 'fgets', 'fclose', 'file', 'readdir', 'pcre_replace', 'size', 'pop', 'unmap', 'has', 'keys', 'values', 'length', 'find', 'substr', 'replace', 'split', 'trim', 'remove', 'contains', 'join'), suffix='\\b'), Name.Builtin), (words(('MethodReference', 'Runner', 'Dll', 'Thread', 'Pipe', 'Process', 'Runnable', 'CGI', 'ClientSocket', 'Socket', 'ServerSocket', 'File', 'Console', 'Directory', 'Exception'), suffix='\\b'), Keyword.Type), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String), ("'\\\\.'|'[^\\\\]'|'\\\\u[0-9a-f]{4}'", String.Char), ('(\\.)([a-zA-Z_]\\w*)', bygroups(Operator, Name.Attribute)), ('[a-zA-Z_]\\w*:', Name.Label), ('[a-zA-Z_$]\\w*', Name), ('[~^*!%&\\[\\](){}<>|+=:;,./?\\-@]+', Operator), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('0x[0-9a-f]+', Number.Hex), ('[0-9]+L?', Number.Integer), ('\\n', Text)], 'class': [('[a-zA-Z_]\\w*', Name.Class, '#pop')], 'import': [('[\\w.]+\\*?', Name.Namespace, '#pop')]}
    
    def analyse_text(text):
        """public method and private method don't seem to be quite common
        elsewhere."""
        result = 0
        if re.search('\\b(?:public|private)\\s+method\\b', text):
            result += 0.01
        return result



class EasytrieveLexer(RegexLexer):
    """
    Easytrieve Plus is a programming language for extracting, filtering and
    converting sequential data. Furthermore it can layout data for reports.
    It is mainly used on mainframe platforms and can access several of the
    mainframe's native file formats. It is somewhat comparable to awk.
    """
    name = 'Easytrieve'
    aliases = ['easytrieve']
    filenames = ['*.ezt', '*.mac']
    mimetypes = ['text/x-easytrieve']
    url = 'https://www.broadcom.com/products/mainframe/application-development/easytrieve-report-generator'
    version_added = '2.1'
    flags = 0
    _DELIMITERS = " \\'.,():\\n"
    _DELIMITERS_OR_COMENT = _DELIMITERS + '*'
    _DELIMITER_PATTERN = '[' + _DELIMITERS + ']'
    _DELIMITER_PATTERN_CAPTURE = '(' + _DELIMITER_PATTERN + ')'
    _NON_DELIMITER_OR_COMMENT_PATTERN = '[^' + _DELIMITERS_OR_COMENT + ']'
    _OPERATORS_PATTERN = '[.+\\-/=\\[\\](){}<>;,&%¬]'
    _KEYWORDS = ['AFTER-BREAK', 'AFTER-LINE', 'AFTER-SCREEN', 'AIM', 'AND', 'ATTR', 'BEFORE', 'BEFORE-BREAK', 'BEFORE-LINE', 'BEFORE-SCREEN', 'BUSHU', 'BY', 'CALL', 'CASE', 'CHECKPOINT', 'CHKP', 'CHKP-STATUS', 'CLEAR', 'CLOSE', 'COL', 'COLOR', 'COMMIT', 'CONTROL', 'COPY', 'CURSOR', 'D', 'DECLARE', 'DEFAULT', 'DEFINE', 'DELETE', 'DENWA', 'DISPLAY', 'DLI', 'DO', 'DUPLICATE', 'E', 'ELSE', 'ELSE-IF', 'END', 'END-CASE', 'END-DO', 'END-IF', 'END-PROC', 'ENDPAGE', 'ENDTABLE', 'ENTER', 'EOF', 'EQ', 'ERROR', 'EXIT', 'EXTERNAL', 'EZLIB', 'F1', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F2', 'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F3', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'FETCH', 'FILE-STATUS', 'FILL', 'FINAL', 'FIRST', 'FIRST-DUP', 'FOR', 'GE', 'GET', 'GO', 'GOTO', 'GQ', 'GR', 'GT', 'HEADING', 'HEX', 'HIGH-VALUES', 'IDD', 'IDMS', 'IF', 'IN', 'INSERT', 'JUSTIFY', 'KANJI-DATE', 'KANJI-DATE-LONG', 'KANJI-TIME', 'KEY', 'KEY-PRESSED', 'KOKUGO', 'KUN', 'LAST-DUP', 'LE', 'LEVEL', 'LIKE', 'LINE', 'LINE-COUNT', 'LINE-NUMBER', 'LINK', 'LIST', 'LOW-VALUES', 'LQ', 'LS', 'LT', 'MACRO', 'MASK', 'MATCHED', 'MEND', 'MESSAGE', 'MOVE', 'MSTART', 'NE', 'NEWPAGE', 'NOMASK', 'NOPRINT', 'NOT', 'NOTE', 'NOVERIFY', 'NQ', 'NULL', 'OF', 'OR', 'OTHERWISE', 'PA1', 'PA2', 'PA3', 'PAGE-COUNT', 'PAGE-NUMBER', 'PARM-REGISTER', 'PATH-ID', 'PATTERN', 'PERFORM', 'POINT', 'POS', 'PRIMARY', 'PRINT', 'PROCEDURE', 'PROGRAM', 'PUT', 'READ', 'RECORD', 'RECORD-COUNT', 'RECORD-LENGTH', 'REFRESH', 'RELEASE', 'RENUM', 'REPEAT', 'REPORT', 'REPORT-INPUT', 'RESHOW', 'RESTART', 'RETRIEVE', 'RETURN-CODE', 'ROLLBACK', 'ROW', 'S', 'SCREEN', 'SEARCH', 'SECONDARY', 'SELECT', 'SEQUENCE', 'SIZE', 'SKIP', 'SOKAKU', 'SORT', 'SQL', 'STOP', 'SUM', 'SYSDATE', 'SYSDATE-LONG', 'SYSIN', 'SYSIPT', 'SYSLST', 'SYSPRINT', 'SYSSNAP', 'SYSTIME', 'TALLY', 'TERM-COLUMNS', 'TERM-NAME', 'TERM-ROWS', 'TERMINATION', 'TITLE', 'TO', 'TRANSFER', 'TRC', 'UNIQUE', 'UNTIL', 'UPDATE', 'UPPERCASE', 'USER', 'USERID', 'VALUE', 'VERIFY', 'W', 'WHEN', 'WHILE', 'WORK', 'WRITE', 'X', 'XDM', 'XRST']
    tokens = {'root': [('\\*.*\\n', Comment.Single), ('\\n+', Whitespace), ('&' + _NON_DELIMITER_OR_COMMENT_PATTERN + '+\\.', Name.Variable, 'after_macro_argument'), ('%' + _NON_DELIMITER_OR_COMMENT_PATTERN + '+', Name.Variable), ('(FILE|MACRO|REPORT)(\\s+)', bygroups(Keyword.Declaration, Whitespace), 'after_declaration'), ('(JOB|PARM)' + '(' + _DELIMITER_PATTERN + ')', bygroups(Keyword.Declaration, Operator)), (words(_KEYWORDS, suffix=_DELIMITER_PATTERN_CAPTURE), bygroups(Keyword.Reserved, Operator)), (_OPERATORS_PATTERN, Operator), ('(' + _NON_DELIMITER_OR_COMMENT_PATTERN + '+)(\\s*)(\\.?)(\\s*)(PROC)(\\s*\\n)', bygroups(Name.Function, Whitespace, Operator, Whitespace, Keyword.Declaration, Whitespace)), ('[0-9]+\\.[0-9]*', Number.Float), ('[0-9]+', Number.Integer), ("'(''|[^'])*'", String), ('\\s+', Whitespace), (_NON_DELIMITER_OR_COMMENT_PATTERN + '+', Name)], 'after_declaration': [(_NON_DELIMITER_OR_COMMENT_PATTERN + '+', Name.Function), default('#pop')], 'after_macro_argument': [('\\*.*\\n', Comment.Single, '#pop'), ('\\s+', Whitespace, '#pop'), (_OPERATORS_PATTERN, Operator, '#pop'), ("'(''|[^'])*'", String, '#pop'), (_NON_DELIMITER_OR_COMMENT_PATTERN + '+', Name)]}
    _COMMENT_LINE_REGEX = re.compile('^\\s*\\*')
    _MACRO_HEADER_REGEX = re.compile('^\\s*MACRO')
    
    def analyse_text(text):
        """
        Perform a structural analysis for basic Easytrieve constructs.
        """
        result = 0.0
        lines = text.split('\n')
        hasEndProc = False
        hasHeaderComment = False
        hasFile = False
        hasJob = False
        hasProc = False
        hasParm = False
        hasReport = False
        
        def isCommentLine(line):
            return EasytrieveLexer._COMMENT_LINE_REGEX.match(lines[0]) is not None
        
        def isEmptyLine(line):
            return not bool(line.strip())
        while (lines and ((isEmptyLine(lines[0]) or isCommentLine(lines[0])))):
            if not isEmptyLine(lines[0]):
                hasHeaderComment = True
            del lines[0]
        if EasytrieveLexer._MACRO_HEADER_REGEX.match(lines[0]):
            result = 0.4
            if hasHeaderComment:
                result += 0.4
        else:
            for line in lines:
                words = line.split()
                if len(words) >= 2:
                    firstWord = words[0]
                    if not hasReport:
                        if not hasJob:
                            if not hasFile:
                                if not hasParm:
                                    if firstWord == 'PARM':
                                        hasParm = True
                                if firstWord == 'FILE':
                                    hasFile = True
                            if firstWord == 'JOB':
                                hasJob = True
                        elif firstWord == 'PROC':
                            hasProc = True
                        elif firstWord == 'END-PROC':
                            hasEndProc = True
                        elif firstWord == 'REPORT':
                            hasReport = True
            if (hasJob and hasProc == hasEndProc):
                if hasHeaderComment:
                    result += 0.1
                if hasParm:
                    if hasProc:
                        result += 0.8
                    else:
                        result += 0.5
                else:
                    result += 0.11
                    if hasParm:
                        result += 0.2
                    if hasFile:
                        result += 0.01
                    if hasReport:
                        result += 0.01
        assert 0.0 <= result <= 1.0
        return result



class JclLexer(RegexLexer):
    """
    Job Control Language (JCL)
    is a scripting language used on mainframe platforms to instruct the system
    on how to run a batch job or start a subsystem. It is somewhat
    comparable to MS DOS batch and Unix shell scripts.
    """
    name = 'JCL'
    aliases = ['jcl']
    filenames = ['*.jcl']
    mimetypes = ['text/x-jcl']
    url = 'https://en.wikipedia.org/wiki/Job_Control_Language'
    version_added = '2.1'
    flags = re.IGNORECASE
    tokens = {'root': [('//\\*.*\\n', Comment.Single), ('//', Keyword.Pseudo, 'statement'), ('/\\*', Keyword.Pseudo, 'jes2_statement'), ('.*\\n', Other)], 'statement': [('\\s*\\n', Whitespace, '#pop'), ('([a-z]\\w*)(\\s+)(exec|job)(\\s*)', bygroups(Name.Label, Whitespace, Keyword.Reserved, Whitespace), 'option'), ('[a-z]\\w*', Name.Variable, 'statement_command'), ('\\s+', Whitespace, 'statement_command')], 'statement_command': [('\\s+(command|cntl|dd|endctl|endif|else|include|jcllib|output|pend|proc|set|then|xmit)\\s+', Keyword.Reserved, 'option'), include('option')], 'jes2_statement': [('\\s*\\n', Whitespace, '#pop'), ('\\$', Keyword, 'option'), ('\\b(jobparam|message|netacct|notify|output|priority|route|setup|signoff|xeq|xmit)\\b', Keyword, 'option')], 'option': [('\\*', Name.Builtin), ('[\\[\\](){}<>;,]', Punctuation), ('[-+*/=&%]', Operator), ('[a-z_]\\w*', Name), ('\\d+\\.\\d*', Number.Float), ('\\.\\d+', Number.Float), ('\\d+', Number.Integer), ("'", String, 'option_string'), ('[ \\t]+', Whitespace, 'option_comment'), ('\\.', Punctuation)], 'option_string': [('(\\n)(//)', bygroups(Text, Keyword.Pseudo)), ("''", String), ("[^']", String), ("'", String, '#pop')], 'option_comment': [('.+', Comment.Single)]}
    _JOB_HEADER_PATTERN = re.compile('^//[a-z#$@][a-z0-9#$@]{0,7}\\s+job(\\s+.*)?$', re.IGNORECASE)
    
    def analyse_text(text):
        """
        Recognize JCL job by header.
        """
        result = 0.0
        lines = text.split('\n')
        if len(lines) > 0:
            if JclLexer._JOB_HEADER_PATTERN.match(lines[0]):
                result = 1.0
        assert 0.0 <= result <= 1.0
        return result



class MiniScriptLexer(RegexLexer):
    """
    For MiniScript source code.
    """
    name = 'MiniScript'
    url = 'https://miniscript.org'
    aliases = ['miniscript', 'ms']
    filenames = ['*.ms']
    mimetypes = ['text/x-minicript', 'application/x-miniscript']
    version_added = '2.6'
    tokens = {'root': [('#!(.*?)$', Comment.Preproc), default('base')], 'base': [('//.*$', Comment.Single), ('(?i)(\\d*\\.\\d+|\\d+\\.\\d*)(e[+-]?\\d+)?', Number), ('(?i)\\d+e[+-]?\\d+', Number), ('\\d+', Number), ('\\n', Text), ('[^\\S\\n]+', Text), ('"', String, 'string_double'), ('(==|!=|<=|>=|[=+\\-*/%^<>.:])', Operator), ('[;,\\[\\]{}()]', Punctuation), (words(('break', 'continue', 'else', 'end', 'for', 'function', 'if', 'in', 'isa', 'then', 'repeat', 'return', 'while'), suffix='\\b'), Keyword), (words(('abs', 'acos', 'asin', 'atan', 'ceil', 'char', 'cos', 'floor', 'log', 'round', 'rnd', 'pi', 'sign', 'sin', 'sqrt', 'str', 'tan', 'hasIndex', 'indexOf', 'len', 'val', 'code', 'remove', 'lower', 'upper', 'replace', 'split', 'indexes', 'values', 'join', 'sum', 'sort', 'shuffle', 'push', 'pop', 'pull', 'range', 'print', 'input', 'time', 'wait', 'locals', 'globals', 'outer', 'yield'), suffix='\\b'), Name.Builtin), ('(true|false|null)\\b', Keyword.Constant), ('(and|or|not|new)\\b', Operator.Word), ('(self|super|__isa)\\b', Name.Builtin.Pseudo), ('[a-zA-Z_]\\w*', Name.Variable)], 'string_double': [('[^"\\n]+', String), ('""', String), ('"', String, '#pop'), ('\\n', Text, '#pop')]}



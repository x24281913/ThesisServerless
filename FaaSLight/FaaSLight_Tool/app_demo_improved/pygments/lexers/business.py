"""
    pygments.lexers.business
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for "business-oriented" languages.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Error, Whitespace
from pygments.lexers._openedge_builtins import OPENEDGEKEYWORDS
__all__ = ['CobolLexer', 'CobolFreeformatLexer', 'ABAPLexer', 'OpenEdgeLexer', 'GoodDataCLLexer', 'MaqlLexer']


class CobolLexer(RegexLexer):
    """
    Lexer for OpenCOBOL code.
    """
    name = 'COBOL'
    aliases = ['cobol']
    filenames = ['*.cob', '*.COB', '*.cpy', '*.CPY']
    mimetypes = ['text/x-cobol']
    url = 'https://en.wikipedia.org/wiki/COBOL'
    version_added = '1.6'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [include('comment'), include('strings'), include('core'), include('nums'), ('[a-z0-9]([\\w\\-]*[a-z0-9]+)?', Name.Variable), ('[ \\t]+', Whitespace)], 'comment': [('(^.{6}[*/].*\\n|^.{6}|\\*>.*\\n)', Comment)], 'core': [('(^|(?<=[^\\w\\-]))(ALL\\s+)?((ZEROES)|(HIGH-VALUE|LOW-VALUE|QUOTE|SPACE|ZERO)(S)?)\\s*($|(?=[^\\w\\-]))', Name.Constant), (words(('ACCEPT', 'ADD', 'ALLOCATE', 'CALL', 'CANCEL', 'CLOSE', 'COMPUTE', 'CONFIGURATION', 'CONTINUE', 'DATA', 'DELETE', 'DISPLAY', 'DIVIDE', 'DIVISION', 'ELSE', 'END', 'END-ACCEPT', 'END-ADD', 'END-CALL', 'END-COMPUTE', 'END-DELETE', 'END-DISPLAY', 'END-DIVIDE', 'END-EVALUATE', 'END-IF', 'END-MULTIPLY', 'END-OF-PAGE', 'END-PERFORM', 'END-READ', 'END-RETURN', 'END-REWRITE', 'END-SEARCH', 'END-START', 'END-STRING', 'END-SUBTRACT', 'END-UNSTRING', 'END-WRITE', 'ENVIRONMENT', 'EVALUATE', 'EXIT', 'FD', 'FILE', 'FILE-CONTROL', 'FOREVER', 'FREE', 'GENERATE', 'GO', 'GOBACK', 'IDENTIFICATION', 'IF', 'INITIALIZE', 'INITIATE', 'INPUT-OUTPUT', 'INSPECT', 'INVOKE', 'I-O-CONTROL', 'LINKAGE', 'LOCAL-STORAGE', 'MERGE', 'MOVE', 'MULTIPLY', 'OPEN', 'PERFORM', 'PROCEDURE', 'PROGRAM-ID', 'RAISE', 'READ', 'RELEASE', 'RESUME', 'RETURN', 'REWRITE', 'SCREEN', 'SD', 'SEARCH', 'SECTION', 'SET', 'SORT', 'START', 'STOP', 'STRING', 'SUBTRACT', 'SUPPRESS', 'TERMINATE', 'THEN', 'UNLOCK', 'UNSTRING', 'USE', 'VALIDATE', 'WORKING-STORAGE', 'WRITE'), prefix='(^|(?<=[^\\w\\-]))', suffix='\\s*($|(?=[^\\w\\-]))'), Keyword.Reserved), (words(('ACCESS', 'ADDRESS', 'ADVANCING', 'AFTER', 'ALL', 'ALPHABET', 'ALPHABETIC', 'ALPHABETIC-LOWER', 'ALPHABETIC-UPPER', 'ALPHANUMERIC', 'ALPHANUMERIC-EDITED', 'ALSO', 'ALTER', 'ALTERNATEANY', 'ARE', 'AREA', 'AREAS', 'ARGUMENT-NUMBER', 'ARGUMENT-VALUE', 'AS', 'ASCENDING', 'ASSIGN', 'AT', 'AUTO', 'AUTO-SKIP', 'AUTOMATIC', 'AUTOTERMINATE', 'BACKGROUND-COLOR', 'BASED', 'BEEP', 'BEFORE', 'BELL', 'BLANK', 'BLINK', 'BLOCK', 'BOTTOM', 'BY', 'BYTE-LENGTH', 'CHAINING', 'CHARACTER', 'CHARACTERS', 'CLASS', 'CODE', 'CODE-SET', 'COL', 'COLLATING', 'COLS', 'COLUMN', 'COLUMNS', 'COMMA', 'COMMAND-LINE', 'COMMIT', 'COMMON', 'CONSTANT', 'CONTAINS', 'CONTENT', 'CONTROL', 'CONTROLS', 'CONVERTING', 'COPY', 'CORR', 'CORRESPONDING', 'COUNT', 'CRT', 'CURRENCY', 'CURSOR', 'CYCLE', 'DATE', 'DAY', 'DAY-OF-WEEK', 'DE', 'DEBUGGING', 'DECIMAL-POINT', 'DECLARATIVES', 'DEFAULT', 'DELIMITED', 'DELIMITER', 'DEPENDING', 'DESCENDING', 'DETAIL', 'DISK', 'DOWN', 'DUPLICATES', 'DYNAMIC', 'EBCDIC', 'ENTRY', 'ENVIRONMENT-NAME', 'ENVIRONMENT-VALUE', 'EOL', 'EOP', 'EOS', 'ERASE', 'ERROR', 'ESCAPE', 'EXCEPTION', 'EXCLUSIVE', 'EXTEND', 'EXTERNAL', 'FILE-ID', 'FILLER', 'FINAL', 'FIRST', 'FIXED', 'FLOAT-LONG', 'FLOAT-SHORT', 'FOOTING', 'FOR', 'FOREGROUND-COLOR', 'FORMAT', 'FROM', 'FULL', 'FUNCTION', 'FUNCTION-ID', 'GIVING', 'GLOBAL', 'GROUP', 'HEADING', 'HIGHLIGHT', 'I-O', 'ID', 'IGNORE', 'IGNORING', 'IN', 'INDEX', 'INDEXED', 'INDICATE', 'INITIAL', 'INITIALIZED', 'INPUT', 'INTO', 'INTRINSIC', 'INVALID', 'IS', 'JUST', 'JUSTIFIED', 'KEY', 'LABEL', 'LAST', 'LEADING', 'LEFT', 'LENGTH', 'LIMIT', 'LIMITS', 'LINAGE', 'LINAGE-COUNTER', 'LINE', 'LINES', 'LOCALE', 'LOCK', 'LOWLIGHT', 'MANUAL', 'MEMORY', 'MINUS', 'MODE', 'MULTIPLE', 'NATIONAL', 'NATIONAL-EDITED', 'NATIVE', 'NEGATIVE', 'NEXT', 'NO', 'NULL', 'NULLS', 'NUMBER', 'NUMBERS', 'NUMERIC', 'NUMERIC-EDITED', 'OBJECT-COMPUTER', 'OCCURS', 'OF', 'OFF', 'OMITTED', 'ON', 'ONLY', 'OPTIONAL', 'ORDER', 'ORGANIZATION', 'OTHER', 'OUTPUT', 'OVERFLOW', 'OVERLINE', 'PACKED-DECIMAL', 'PADDING', 'PAGE', 'PARAGRAPH', 'PLUS', 'POINTER', 'POSITION', 'POSITIVE', 'PRESENT', 'PREVIOUS', 'PRINTER', 'PRINTING', 'PROCEDURE-POINTER', 'PROCEDURES', 'PROCEED', 'PROGRAM', 'PROGRAM-POINTER', 'PROMPT', 'QUOTE', 'QUOTES', 'RANDOM', 'RD', 'RECORD', 'RECORDING', 'RECORDS', 'RECURSIVE', 'REDEFINES', 'REEL', 'REFERENCE', 'RELATIVE', 'REMAINDER', 'REMOVAL', 'RENAMES', 'REPLACING', 'REPORT', 'REPORTING', 'REPORTS', 'REPOSITORY', 'REQUIRED', 'RESERVE', 'RETURNING', 'REVERSE-VIDEO', 'REWIND', 'RIGHT', 'ROLLBACK', 'ROUNDED', 'RUN', 'SAME', 'SCROLL', 'SECURE', 'SEGMENT-LIMIT', 'SELECT', 'SENTENCE', 'SEPARATE', 'SEQUENCE', 'SEQUENTIAL', 'SHARING', 'SIGN', 'SIGNED', 'SIGNED-INT', 'SIGNED-LONG', 'SIGNED-SHORT', 'SIZE', 'SORT-MERGE', 'SOURCE', 'SOURCE-COMPUTER', 'SPECIAL-NAMES', 'STANDARD', 'STANDARD-1', 'STANDARD-2', 'STATUS', 'SUBKEY', 'SUM', 'SYMBOLIC', 'SYNC', 'SYNCHRONIZED', 'TALLYING', 'TAPE', 'TEST', 'THROUGH', 'THRU', 'TIME', 'TIMES', 'TO', 'TOP', 'TRAILING', 'TRANSFORM', 'TYPE', 'UNDERLINE', 'UNIT', 'UNSIGNED', 'UNSIGNED-INT', 'UNSIGNED-LONG', 'UNSIGNED-SHORT', 'UNTIL', 'UP', 'UPDATE', 'UPON', 'USAGE', 'USING', 'VALUE', 'VALUES', 'VARYING', 'WAIT', 'WHEN', 'WITH', 'WORDS', 'YYYYDDD', 'YYYYMMDD'), prefix='(^|(?<=[^\\w\\-]))', suffix='\\s*($|(?=[^\\w\\-]))'), Keyword.Pseudo), (words(('ACTIVE-CLASS', 'ALIGNED', 'ANYCASE', 'ARITHMETIC', 'ATTRIBUTE', 'B-AND', 'B-NOT', 'B-OR', 'B-XOR', 'BIT', 'BOOLEAN', 'CD', 'CENTER', 'CF', 'CH', 'CHAIN', 'CLASS-ID', 'CLASSIFICATION', 'COMMUNICATION', 'CONDITION', 'DATA-POINTER', 'DESTINATION', 'DISABLE', 'EC', 'EGI', 'EMI', 'ENABLE', 'END-RECEIVE', 'ENTRY-CONVENTION', 'EO', 'ESI', 'EXCEPTION-OBJECT', 'EXPANDS', 'FACTORY', 'FLOAT-BINARY-16', 'FLOAT-BINARY-34', 'FLOAT-BINARY-7', 'FLOAT-DECIMAL-16', 'FLOAT-DECIMAL-34', 'FLOAT-EXTENDED', 'FORMAT', 'FUNCTION-POINTER', 'GET', 'GROUP-USAGE', 'IMPLEMENTS', 'INFINITY', 'INHERITS', 'INTERFACE', 'INTERFACE-ID', 'INVOKE', 'LC_ALL', 'LC_COLLATE', 'LC_CTYPE', 'LC_MESSAGES', 'LC_MONETARY', 'LC_NUMERIC', 'LC_TIME', 'LINE-COUNTER', 'MESSAGE', 'METHOD', 'METHOD-ID', 'NESTED', 'NONE', 'NORMAL', 'OBJECT', 'OBJECT-REFERENCE', 'OPTIONS', 'OVERRIDE', 'PAGE-COUNTER', 'PF', 'PH', 'PROPERTY', 'PROTOTYPE', 'PURGE', 'QUEUE', 'RAISE', 'RAISING', 'RECEIVE', 'RELATION', 'REPLACE', 'REPRESENTS-NOT-A-NUMBER', 'RESET', 'RESUME', 'RETRY', 'RF', 'RH', 'SECONDS', 'SEGMENT', 'SELF', 'SEND', 'SOURCES', 'STATEMENT', 'STEP', 'STRONG', 'SUB-QUEUE-1', 'SUB-QUEUE-2', 'SUB-QUEUE-3', 'SUPER', 'SYMBOL', 'SYSTEM-DEFAULT', 'TABLE', 'TERMINAL', 'TEXT', 'TYPEDEF', 'UCS-4', 'UNIVERSAL', 'USER-DEFAULT', 'UTF-16', 'UTF-8', 'VAL-STATUS', 'VALID', 'VALIDATE', 'VALIDATE-STATUS'), prefix='(^|(?<=[^\\w\\-]))', suffix='\\s*($|(?=[^\\w\\-]))'), Error), ('(^|(?<=[^\\w\\-]))(PIC\\s+.+?(?=(\\s|\\.\\s))|PICTURE\\s+.+?(?=(\\s|\\.\\s))|(COMPUTATIONAL)(-[1-5X])?|(COMP)(-[1-5X])?|BINARY-C-LONG|BINARY-CHAR|BINARY-DOUBLE|BINARY-LONG|BINARY-SHORT|BINARY)\\s*($|(?=[^\\w\\-]))', Keyword.Type), ('(\\*\\*|\\*|\\+|-|/|<=|>=|<|>|==|/=|=)', Operator), ('([(),;:&%.])', Punctuation), ('(^|(?<=[^\\w\\-]))(ABS|ACOS|ANNUITY|ASIN|ATAN|BYTE-LENGTH|CHAR|COMBINED-DATETIME|CONCATENATE|COS|CURRENT-DATE|DATE-OF-INTEGER|DATE-TO-YYYYMMDD|DAY-OF-INTEGER|DAY-TO-YYYYDDD|EXCEPTION-(?:FILE|LOCATION|STATEMENT|STATUS)|EXP10|EXP|E|FACTORIAL|FRACTION-PART|INTEGER-OF-(?:DATE|DAY|PART)|INTEGER|LENGTH|LOCALE-(?:DATE|TIME(?:-FROM-SECONDS)?)|LOG(?:10)?|LOWER-CASE|MAX|MEAN|MEDIAN|MIDRANGE|MIN|MOD|NUMVAL(?:-C)?|ORD(?:-MAX|-MIN)?|PI|PRESENT-VALUE|RANDOM|RANGE|REM|REVERSE|SECONDS-FROM-FORMATTED-TIME|SECONDS-PAST-MIDNIGHT|SIGN|SIN|SQRT|STANDARD-DEVIATION|STORED-CHAR-LENGTH|SUBSTITUTE(?:-CASE)?|SUM|TAN|TEST-DATE-YYYYMMDD|TEST-DAY-YYYYDDD|TRIM|UPPER-CASE|VARIANCE|WHEN-COMPILED|YEAR-TO-YYYY)\\s*($|(?=[^\\w\\-]))', Name.Function), ('(^|(?<=[^\\w\\-]))(true|false)\\s*($|(?=[^\\w\\-]))', Name.Builtin), ('(^|(?<=[^\\w\\-]))(equal|equals|ne|lt|le|gt|ge|greater|less|than|not|and|or)\\s*($|(?=[^\\w\\-]))', Operator.Word)], 'strings': [('"[^"\\n]*("|\\n)', String.Double), ("'[^'\\n]*('|\\n)", String.Single)], 'nums': [('\\d+(\\s*|\\.$|$)', Number.Integer), ('[+-]?\\d*\\.\\d+(E[-+]?\\d+)?', Number.Float), ('[+-]?\\d+\\.\\d*(E[-+]?\\d+)?', Number.Float)]}



class CobolFreeformatLexer(CobolLexer):
    """
    Lexer for Free format OpenCOBOL code.
    """
    name = 'COBOLFree'
    aliases = ['cobolfree']
    filenames = ['*.cbl', '*.CBL']
    mimetypes = []
    url = 'https://opencobol.add1tocobol.com'
    version_added = '1.6'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'comment': [('(\\*>.*\\n|^\\w*\\*.*$)', Comment)]}



class ABAPLexer(RegexLexer):
    """
    Lexer for ABAP, SAP's integrated language.
    """
    name = 'ABAP'
    aliases = ['abap']
    filenames = ['*.abap', '*.ABAP']
    mimetypes = ['text/x-abap']
    url = 'https://community.sap.com/topics/abap'
    version_added = '1.1'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'common': [('\\s+', Whitespace), ('^\\*.*$', Comment.Single), ('\\".*?\\n', Comment.Single), ('##\\w+', Comment.Special)], 'variable-names': [('<\\S+>', Name.Variable), ('\\w[\\w~]*(?:(\\[\\])|->\\*)?', Name.Variable)], 'root': [include('common'), ('CALL\\s+(?:BADI|CUSTOMER-FUNCTION|FUNCTION)', Keyword), ('(CALL\\s+(?:DIALOG|SCREEN|SUBSCREEN|SELECTION-SCREEN|TRANSACTION|TRANSFORMATION))\\b', Keyword), ('(FORM|PERFORM)(\\s+)(\\w+)', bygroups(Keyword, Whitespace, Name.Function)), ('(PERFORM)(\\s+)(\\()(\\w+)(\\))', bygroups(Keyword, Whitespace, Punctuation, Name.Variable, Punctuation)), ('(MODULE)(\\s+)(\\S+)(\\s+)(INPUT|OUTPUT)', bygroups(Keyword, Whitespace, Name.Function, Whitespace, Keyword)), ('(METHOD)(\\s+)([\\w~]+)', bygroups(Keyword, Whitespace, Name.Function)), ('(\\s+)([\\w\\-]+)([=\\-]>)([\\w\\-~]+)', bygroups(Whitespace, Name.Variable, Operator, Name.Function)), ('(?<=(=|-)>)([\\w\\-~]+)(?=\\()', Name.Function), ('(TEXT)(-)(\\d{3})', bygroups(Keyword, Punctuation, Number.Integer)), ('(TEXT)(-)(\\w{3})', bygroups(Keyword, Punctuation, Name.Variable)), ('(ADD-CORRESPONDING|AUTHORITY-CHECK|CLASS-DATA|CLASS-EVENTS|CLASS-METHODS|CLASS-POOL|DELETE-ADJACENT|DIVIDE-CORRESPONDING|EDITOR-CALL|ENHANCEMENT-POINT|ENHANCEMENT-SECTION|EXIT-COMMAND|FIELD-GROUPS|FIELD-SYMBOLS|FIELD-SYMBOL|FUNCTION-POOL|INTERFACE-POOL|INVERTED-DATE|LOAD-OF-PROGRAM|LOG-POINT|MESSAGE-ID|MOVE-CORRESPONDING|MULTIPLY-CORRESPONDING|NEW-LINE|NEW-PAGE|NEW-SECTION|NO-EXTENSION|OUTPUT-LENGTH|PRINT-CONTROL|SELECT-OPTIONS|START-OF-SELECTION|SUBTRACT-CORRESPONDING|SYNTAX-CHECK|SYSTEM-EXCEPTIONS|TYPE-POOL|TYPE-POOLS|NO-DISPLAY)\\b', Keyword), ('(?<![-\\>])(CREATE\\s+(PUBLIC|PRIVATE|DATA|OBJECT)|(PUBLIC|PRIVATE|PROTECTED)\\s+SECTION|(TYPE|LIKE)\\s+((LINE\\s+OF|REF\\s+TO|(SORTED|STANDARD|HASHED)\\s+TABLE\\s+OF))?|FROM\\s+(DATABASE|MEMORY)|CALL\\s+METHOD|(GROUP|ORDER) BY|HAVING|SEPARATED BY|GET\\s+(BADI|BIT|CURSOR|DATASET|LOCALE|PARAMETER|PF-STATUS|(PROPERTY|REFERENCE)\\s+OF|RUN\\s+TIME|TIME\\s+(STAMP)?)?|SET\\s+(BIT|BLANK\\s+LINES|COUNTRY|CURSOR|DATASET|EXTENDED\\s+CHECK|HANDLER|HOLD\\s+DATA|LANGUAGE|LEFT\\s+SCROLL-BOUNDARY|LOCALE|MARGIN|PARAMETER|PF-STATUS|PROPERTY\\s+OF|RUN\\s+TIME\\s+(ANALYZER|CLOCK\\s+RESOLUTION)|SCREEN|TITLEBAR|UPADTE\\s+TASK\\s+LOCAL|USER-COMMAND)|CONVERT\\s+((INVERTED-)?DATE|TIME|TIME\\s+STAMP|TEXT)|(CLOSE|OPEN)\\s+(DATASET|CURSOR)|(TO|FROM)\\s+(DATA BUFFER|INTERNAL TABLE|MEMORY ID|DATABASE|SHARED\\s+(MEMORY|BUFFER))|DESCRIBE\\s+(DISTANCE\\s+BETWEEN|FIELD|LIST|TABLE)|FREE\\s(MEMORY|OBJECT)?|PROCESS\\s+(BEFORE\\s+OUTPUT|AFTER\\s+INPUT|ON\\s+(VALUE-REQUEST|HELP-REQUEST))|AT\\s+(LINE-SELECTION|USER-COMMAND|END\\s+OF|NEW)|AT\\s+SELECTION-SCREEN(\\s+(ON(\\s+(BLOCK|(HELP|VALUE)-REQUEST\\s+FOR|END\\s+OF|RADIOBUTTON\\s+GROUP))?|OUTPUT))?|SELECTION-SCREEN:?\\s+((BEGIN|END)\\s+OF\\s+((TABBED\\s+)?BLOCK|LINE|SCREEN)|COMMENT|FUNCTION\\s+KEY|INCLUDE\\s+BLOCKS|POSITION|PUSHBUTTON|SKIP|ULINE)|LEAVE\\s+(LIST-PROCESSING|PROGRAM|SCREEN|TO LIST-PROCESSING|TO TRANSACTION)(ENDING|STARTING)\\s+AT|FORMAT\\s+(COLOR|INTENSIFIED|INVERSE|HOTSPOT|INPUT|FRAMES|RESET)|AS\\s+(CHECKBOX|SUBSCREEN|WINDOW)|WITH\\s+(((NON-)?UNIQUE)?\\s+KEY|FRAME)|(BEGIN|END)\\s+OF|DELETE(\\s+ADJACENT\\s+DUPLICATES\\sFROM)?|COMPARING(\\s+ALL\\s+FIELDS)?|(INSERT|APPEND)(\\s+INITIAL\\s+LINE\\s+(IN)?TO|\\s+LINES\\s+OF)?|IN\\s+((BYTE|CHARACTER)\\s+MODE|PROGRAM)|END-OF-(DEFINITION|PAGE|SELECTION)|WITH\\s+FRAME(\\s+TITLE)|(REPLACE|FIND)\\s+((FIRST|ALL)\\s+OCCURRENCES?\\s+OF\\s+)?(SUBSTRING|REGEX)?|MATCH\\s+(LENGTH|COUNT|LINE|OFFSET)|(RESPECTING|IGNORING)\\s+CASE|IN\\s+UPDATE\\s+TASK|(SOURCE|RESULT)\\s+(XML)?|REFERENCE\\s+INTO|AND\\s+(MARK|RETURN)|CLIENT\\s+SPECIFIED|CORRESPONDING\\s+FIELDS\\s+OF|IF\\s+FOUND|FOR\\s+EVENT|INHERITING\\s+FROM|LEAVE\\s+TO\\s+SCREEN|LOOP\\s+AT\\s+(SCREEN)?|LOWER\\s+CASE|MATCHCODE\\s+OBJECT|MODIF\\s+ID|MODIFY\\s+SCREEN|NESTING\\s+LEVEL|NO\\s+INTERVALS|OF\\s+STRUCTURE|RADIOBUTTON\\s+GROUP|RANGE\\s+OF|REF\\s+TO|SUPPRESS DIALOG|TABLE\\s+OF|UPPER\\s+CASE|TRANSPORTING\\s+NO\\s+FIELDS|VALUE\\s+CHECK|VISIBLE\\s+LENGTH|HEADER\\s+LINE|COMMON\\s+PART)\\b', Keyword), ('(^|(?<=(\\s|\\.)))(ABBREVIATED|ABSTRACT|ADD|ALIASES|ALIGN|ALPHA|ASSERT|AS|ASSIGN(ING)?|AT(\\s+FIRST)?|BACK|BLOCK|BREAK-POINT|CASE|CAST|CATCH|CHANGING|CHECK|CLASS|CLEAR|COLLECT|COLOR|COMMIT|COND|CONV|CREATE|COMMUNICATION|COMPONENTS?|COMPUTE|CONCATENATE|CONDENSE|CONSTANTS|CONTEXTS|CONTINUE|CONTROLS|COUNTRY|CURRENCY|DATA|DATE|DECIMALS|DEFAULT|DEFINE|DEFINITION|DEFERRED|DEMAND|DETAIL|DIRECTORY|DIVIDE|DO|DUMMY|ELSE(IF)?|ENDAT|ENDCASE|ENDCATCH|ENDCLASS|ENDDO|ENDFORM|ENDFUNCTION|ENDIF|ENDINTERFACE|ENDLOOP|ENDMETHOD|ENDMODULE|ENDSELECT|ENDTRY|ENDWHILE|ENHANCEMENT|EVENTS|EXACT|EXCEPTIONS?|EXIT|EXPONENT|EXPORT|EXPORTING|EXTRACT|FETCH|FIELDS?|FOR|FORM|FORMAT|FREE|FROM|FUNCTION|HIDE|ID|IF|IMPORT|IMPLEMENTATION|IMPORTING|IN|INCLUDE|INCLUDING|INDEX|INFOTYPES|INITIALIZATION|INTERFACE|INTERFACES|INTO|LANGUAGE|LEAVE|LENGTH|LINES|LOAD|LOCAL|JOIN|KEY|NEW|NEXT|MAXIMUM|MESSAGE|METHOD[S]?|MINIMUM|MODULE|MODIFIER|MODIFY|MOVE|MULTIPLY|NODES|NUMBER|OBLIGATORY|OBJECT|OF|OFF|ON|OTHERS|OVERLAY|PACK|PAD|PARAMETERS|PERCENTAGE|POSITION|PROGRAM|PROVIDE|PUBLIC|PUT|PF\\d\\d|RAISE|RAISING|RANGES?|READ|RECEIVE|REDEFINITION|REFRESH|REJECT|REPORT|RESERVE|REF|RESUME|RETRY|RETURN|RETURNING|RIGHT|ROLLBACK|REPLACE|SCROLL|SEARCH|SELECT|SHIFT|SIGN|SINGLE|SIZE|SKIP|SORT|SPLIT|STATICS|STOP|STYLE|SUBMATCHES|SUBMIT|SUBTRACT|SUM(?!\\()|SUMMARY|SUMMING|SUPPLY|SWITCH|TABLE|TABLES|TIMESTAMP|TIMES?|TIMEZONE|TITLE|\\??TO|TOP-OF-PAGE|TRANSFER|TRANSLATE|TRY|TYPES|ULINE|UNDER|UNPACK|UPDATE|USING|VALUE|VALUES|VIA|VARYING|VARY|WAIT|WHEN|WHERE|WIDTH|WHILE|WITH|WINDOW|WRITE|XSD|ZERO)\\b', Keyword), ('(abs|acos|asin|atan|boolc|boolx|bit_set|char_off|charlen|ceil|cmax|cmin|condense|contains|contains_any_of|contains_any_not_of|concat_lines_of|cos|cosh|count|count_any_of|count_any_not_of|dbmaxlen|distance|escape|exp|find|find_end|find_any_of|find_any_not_of|floor|frac|from_mixed|insert|lines|log|log10|match|matches|nmax|nmin|numofchar|repeat|replace|rescale|reverse|round|segment|shift_left|shift_right|sign|sin|sinh|sqrt|strlen|substring|substring_after|substring_from|substring_before|substring_to|tan|tanh|to_upper|to_lower|to_mixed|translate|trunc|xstrlen)(\\()\\b', bygroups(Name.Builtin, Punctuation)), ('&[0-9]', Name), ('[0-9]+', Number.Integer), ('(?<=(\\s|.))(AND|OR|EQ|NE|GT|LT|GE|LE|CO|CN|CA|NA|CS|NOT|NS|CP|NP|BYTE-CO|BYTE-CN|BYTE-CA|BYTE-NA|BYTE-CS|BYTE-NS|IS\\s+(NOT\\s+)?(INITIAL|ASSIGNED|REQUESTED|BOUND))\\b', Operator.Word), include('variable-names'), ('[?*<>=\\-+&]', Operator), ("'(''|[^'])*'", String.Single), ('`([^`])*`', String.Single), ('([|}])([^{}|]*?)([|{])', bygroups(Punctuation, String.Single, Punctuation)), ('[/;:()\\[\\],.]', Punctuation), ('(!)(\\w+)', bygroups(Operator, Name))]}



class OpenEdgeLexer(RegexLexer):
    """
    Lexer for OpenEdge ABL (formerly Progress) source code.
    """
    name = 'OpenEdge ABL'
    aliases = ['openedge', 'abl', 'progress']
    filenames = ['*.p', '*.cls']
    mimetypes = ['text/x-openedge', 'application/x-openedge']
    url = 'https://www.progress.com/openedge/features/abl'
    version_added = '1.5'
    types = '(?i)(^|(?<=[^\\w\\-]))(CHARACTER|CHAR|CHARA|CHARAC|CHARACT|CHARACTE|COM-HANDLE|DATE|DATETIME|DATETIME-TZ|DECIMAL|DEC|DECI|DECIM|DECIMA|HANDLE|INT64|INTEGER|INT|INTE|INTEG|INTEGE|LOGICAL|LONGCHAR|MEMPTR|RAW|RECID|ROWID)\\s*($|(?=[^\\w\\-]))'
    keywords = words(OPENEDGEKEYWORDS, prefix='(?i)(^|(?<=[^\\w\\-]))', suffix='\\s*($|(?=[^\\w\\-]))')
    tokens = {'root': [('/\\*', Comment.Multiline, 'comment'), ('\\{', Comment.Preproc, 'preprocessor'), ('\\s*&.*', Comment.Preproc), ('0[xX][0-9a-fA-F]+[LlUu]*', Number.Hex), ('(?i)(DEFINE|DEF|DEFI|DEFIN)\\b', Keyword.Declaration), (types, Keyword.Type), (keywords, Name.Builtin), ('"(\\\\\\\\|\\\\[^\\\\]|[^"\\\\])*"', String.Double), ("'(\\\\\\\\|\\\\[^\\\\]|[^'\\\\])*'", String.Single), ('[0-9][0-9]*\\.[0-9]+([eE][0-9]+)?[fd]?', Number.Float), ('[0-9]+', Number.Integer), ('\\s+', Whitespace), ('[+*/=-]', Operator), ('[.:()]', Punctuation), ('.', Name.Variable)], 'comment': [('[^*/]', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'preprocessor': [('[^{}]', Comment.Preproc), ('\\{', Comment.Preproc, '#push'), ('\\}', Comment.Preproc, '#pop')]}
    
    def analyse_text(text):
        """Try to identify OpenEdge ABL based on a few common constructs."""
        result = 0
        if 'END.' in text:
            result += 0.05
        if 'END PROCEDURE.' in text:
            result += 0.05
        if 'ELSE DO:' in text:
            result += 0.05
        return result



class GoodDataCLLexer(RegexLexer):
    """
    Lexer for GoodData-CL script files.
    """
    name = 'GoodData-CL'
    aliases = ['gooddata-cl']
    filenames = ['*.gdc']
    mimetypes = ['text/x-gooddata-cl']
    url = 'https://github.com/gooddata/GoodData-CL'
    version_added = '1.4'
    flags = re.IGNORECASE
    tokens = {'root': [('#.*', Comment.Single), ('[a-z]\\w*', Name.Function), ('\\(', Punctuation, 'args-list'), (';', Punctuation), ('\\s+', Text)], 'args-list': [('\\)', Punctuation, '#pop'), (',', Punctuation), ('[a-z]\\w*', Name.Variable), ('=', Operator), ('"', String, 'string-literal'), ('[0-9]+(?:\\.[0-9]+)?(?:e[+-]?[0-9]{1,3})?', Number), ('\\s', Whitespace)], 'string-literal': [('\\\\[tnrfbae"\\\\]', String.Escape), ('"', String, '#pop'), ('[^\\\\"]+', String)]}



class MaqlLexer(RegexLexer):
    """
    Lexer for GoodData MAQL scripts.
    """
    name = 'MAQL'
    aliases = ['maql']
    filenames = ['*.maql']
    mimetypes = ['text/x-gooddata-maql', 'application/x-gooddata-maql']
    url = 'https://help.gooddata.com/doc/enterprise/en/dashboards-and-insights/maql-analytical-query-language'
    version_added = '1.4'
    flags = re.IGNORECASE
    tokens = {'root': [('IDENTIFIER\\b', Name.Builtin), ('\\{[^}]+\\}', Name.Variable), ('[0-9]+(?:\\.[0-9]+)?(?:e[+-]?[0-9]{1,3})?', Number), ('"', String, 'string-literal'), ('\\<\\>|\\!\\=', Operator), ('\\=|\\>\\=|\\>|\\<\\=|\\<', Operator), ('\\:\\=', Operator), ('\\[[^]]+\\]', Name.Variable.Class), (words(('DIMENSION', 'DIMENSIONS', 'BOTTOM', 'METRIC', 'COUNT', 'OTHER', 'FACT', 'WITH', 'TOP', 'OR', 'ATTRIBUTE', 'CREATE', 'PARENT', 'FALSE', 'ROW', 'ROWS', 'FROM', 'ALL', 'AS', 'PF', 'COLUMN', 'COLUMNS', 'DEFINE', 'REPORT', 'LIMIT', 'TABLE', 'LIKE', 'AND', 'BY', 'BETWEEN', 'EXCEPT', 'SELECT', 'MATCH', 'WHERE', 'TRUE', 'FOR', 'IN', 'WITHOUT', 'FILTER', 'ALIAS', 'WHEN', 'NOT', 'ON', 'KEYS', 'KEY', 'FULLSET', 'PRIMARY', 'LABELS', 'LABEL', 'VISUAL', 'TITLE', 'DESCRIPTION', 'FOLDER', 'ALTER', 'DROP', 'ADD', 'DATASET', 'DATATYPE', 'INT', 'BIGINT', 'DOUBLE', 'DATE', 'VARCHAR', 'DECIMAL', 'SYNCHRONIZE', 'TYPE', 'DEFAULT', 'ORDER', 'ASC', 'DESC', 'HYPERLINK', 'INCLUDE', 'TEMPLATE', 'MODIFY'), suffix='\\b'), Keyword), ('[a-z]\\w*\\b', Name.Function), ('#.*', Comment.Single), ('[,;()]', Punctuation), ('\\s+', Whitespace)], 'string-literal': [('\\\\[tnrfbae"\\\\]', String.Escape), ('"', String, '#pop'), ('[^\\\\"]+', String)]}



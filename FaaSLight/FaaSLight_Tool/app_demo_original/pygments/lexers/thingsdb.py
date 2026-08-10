"""
    pygments.lexers.thingsdb
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for the ThingsDB language.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Comment, Keyword, Name, Number, String, Text, Operator, Punctuation, Whitespace
__all__ = ['ThingsDBLexer']


class ThingsDBLexer(RegexLexer):
    """
    Lexer for the ThingsDB programming language.
    """
    name = 'ThingsDB'
    aliases = ['ti', 'thingsdb']
    filenames = ['*.ti']
    url = 'https://www.thingsdb.net'
    version_added = '2.9'
    tokens = {'root': [include('expression')], 'expression': [include('comments'), include('whitespace'), ('[-+]?0b[01]+', Number.Bin), ('[-+]?0o[0-8]+', Number.Oct), ('([-+]?0x[0-9a-fA-F]+)', Number.Hex), ('[-+]?[0-9]+', Number.Integer), ('[-+]?((inf|nan)([^0-9A-Za-z_]|$)|[0-9]*\\.[0-9]+(e[+-][0-9]+)?)', Number.Float), ('(?:"(?:[^"]*)")+', String.Double), ("(?:'(?:[^']*)')+", String.Single), ('(?:`(?:[^`]*)`)+', String.Backtick), ('(true|false|nil)\\b', Keyword.Constant), ('(FULL|USER|GRANT|CHANGE|JOIN|RUN|QUERY|DEBUG|INFO|WARNING|ERROR|CRITICAL|NO_IDS|INT_MIN|INT_MAX|MATH_E|MATH_PI)\\b', Name.Constant), ('(/[^/\\\\]*(?:\\\\.[^/\\\\]*)*/i?)', String.Regex), include('names'), ('[(){}\\[\\],;]', Punctuation), ('[+\\-*/%&|<>^!~@=:?]', Operator)], 'names': [('(\\.)(first|last|then|else|load|at|again_in|again_at|err|cancel|closure|set_closure|args|set_args|owner|set_owner|equals|copy|dup|assign|week|weekday|yday|zone|len|call|doc|emit|extract|choice|code|format|msg|each|every|extend|extend_unique|filter|find|flat|find_index|has|index_of|count|sum|is_unique|unique|join|map|map_id|map_wrap|map_type|vmap|move|pop|push|fill|remove|replace|restrict|restriction|shift|sort|splice|to|add|one|clear|contains|ends_with|name|lower|replace|reverse|starts_with|split|test|trim|trim_left|trim_right|upper|del|ren|to_type|to_thing|get|id|keys|reduce|set|some|value|values|wrap|unshift|unwrap|search|set_name|bit_count)(\\()', bygroups(Name.Function, Name.Function, Punctuation), 'arguments'), ('(alt_raise|assert|base64_encode|base64_decode|bool|bytes|closure|datetime|deep|future|is_future|del_enum|del_type|room|is_room|task|tasks|is_task|is_email|is_url|is_tel|is_time_zone|timeit|enum|enum_info|enum_map|enums_info|err|regex|is_regex|change_id|float|has_enum|has_type|int|is_array|is_ascii|is_float|is_bool|is_bytes|is_closure|is_datetime|is_enum|is_err|is_mpdata|is_inf|is_int|is_list|is_nan|is_nil|is_raw|is_set|is_str|is_thing|is_timeval|is_tuple|is_utf8|json_dump|json_load|list|log|import|export|root|mod_enum|mod_type|new|new_type|now|raise|rand|range|randint|randstr|refs|rename_enum|set|set_enum|set_type|str|thing|timeval|try|type|type_assert|type_all|type_count|type_info|types_info|nse|wse|backup_info|backups_info|backups_ok|counters|del_backup|has_backup|new_backup|node_info|nodes_info|reset_counters|restart_module|set_log_level|shutdown|has_module|del_module|module_info|modules_info|new_module|deploy_module|rename_module|refresh_module|set_module_conf|set_module_scope|collections_info|del_collection|del_expired|del_node|del_token|del_user|grant|has_collection|has_node|has_token|has_user|new_collection|new_node|new_token|new_user|rename_collection|rename_user|restore|revoke|set_password|set_time_zone|set_default_deep|time_zones_info|user_info|users_info|del_procedure|has_procedure|new_procedure|mod_procedure|procedure_doc|procedure_info|procedures_info|rename_procedure|run|assert_err|auth_err|bad_data_err|cancelled_err|rename_type|forbidden_err|lookup_err|max_quota_err|node_err|num_arguments_err|operation_err|overflow_err|syntax_err|collection_info|type_err|value_err|zero_div_err|whitelist_add|whitelist_del|round|abs|ceil|cos|exp|floor|log10|log2|loge|pow|sin|sqrt|tan|is_module|commit|history|set_history|del_history|ano)(\\()', bygroups(Name.Function, Punctuation), 'arguments'), ('(\\.[A-Za-z_][0-9A-Za-z_]*)(\\s*)(=)', bygroups(Name.Attribute, Text, Operator)), ('\\.[A-Za-z_][0-9A-Za-z_]*', Name.Attribute), ('([A-Za-z_][0-9A-Za-z_]*)(\\s*)(=)', bygroups(Name.Variable, Text, Operator)), ('[A-Za-z_][0-9A-Za-z_]*', Name.Variable)], 'whitespace': [('\\n', Whitespace), ('\\s+', Whitespace)], 'comments': [('//(.*?)\\n', Comment.Single), ('/\\*', Comment.Multiline, 'comment')], 'comment': [('[^*/]+', Comment.Multiline), ('/\\*', Comment.Multiline, '#push'), ('\\*/', Comment.Multiline, '#pop'), ('[*/]', Comment.Multiline)], 'arguments': [include('expression'), (',', Punctuation), ('\\(', Punctuation, '#push'), ('\\)', Punctuation, '#pop')]}



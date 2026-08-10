"""
    pygments.lexers.ldap
    ~~~~~~~~~~~~~~~~~~~~

    Pygments lexers for LDAP.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.lexer import RegexLexer, bygroups, default
from pygments.token import Operator, Comment, Keyword, Literal, Name, String, Number, Punctuation, Whitespace, Escape
__all__ = ['LdifLexer', 'LdaprcLexer']


class LdifLexer(RegexLexer):
    """
    Lexer for LDIF
    """
    name = 'LDIF'
    aliases = ['ldif']
    filenames = ['*.ldif']
    mimetypes = ['text/x-ldif']
    url = 'https://datatracker.ietf.org/doc/html/rfc2849'
    version_added = '2.17'
    tokens = {'root': [('\\s*\\n', Whitespace), ('(-)(\\n)', bygroups(Punctuation, Whitespace)), ('(#.*)(\\n)', bygroups(Comment.Single, Whitespace)), ('(version)(:)([ \\t]*)(.*)([ \\t]*\\n)', bygroups(Keyword, Punctuation, Whitespace, Number.Integer, Whitespace)), ('(control)(:)([ \\t]*)([\\.0-9]+)([ \\t]+)((?:true|false)?)([ \\t]*)', bygroups(Keyword, Punctuation, Whitespace, Name.Other, Whitespace, Keyword, Whitespace), 'after-control'), ('(deleteoldrdn)(:)([ \\n]*)([0-1]+)([ \\t]*\\n)', bygroups(Keyword, Punctuation, Whitespace, Number, Whitespace)), ('(add|delete|replace)(::?)(\\s*)(.*)([ \\t]*\\n)', bygroups(Keyword, Punctuation, Whitespace, Name.Attribute, Whitespace)), ('(changetype)(:)([ \\t]*)([a-z]*)([ \\t]*\\n)', bygroups(Keyword, Punctuation, Whitespace, Keyword, Whitespace)), ('(dn|newrdn)(::)', bygroups(Keyword, Punctuation), 'base64-dn'), ('(dn|newrdn)(:)', bygroups(Keyword, Punctuation), 'dn'), ('(objectclass)(:)([ \\t]*)([^ \\t\\n]*)([ \\t]*\\n)', bygroups(Keyword, Punctuation, Whitespace, Name.Class, Whitespace)), ('([a-zA-Z]*|[0-9][0-9\\.]*[0-9])(;)', bygroups(Name.Attribute, Punctuation), 'property'), ('([a-zA-Z]*|[0-9][0-9\\.]*[0-9])(:<)', bygroups(Name.Attribute, Punctuation), 'url'), ('([a-zA-Z]*|[0-9][0-9\\.]*[0-9])(::?)', bygroups(Name.Attribute, Punctuation), 'value')], 'after-control': [(':<', Punctuation, ('#pop', 'url')), ('::?', Punctuation, ('#pop', 'value')), default('#pop')], 'property': [('([-a-zA-Z0-9]*)(;)', bygroups(Name.Property, Punctuation)), ('([-a-zA-Z0-9]*)(:<)', bygroups(Name.Property, Punctuation), ('#pop', 'url')), ('([-a-zA-Z0-9]*)(::?)', bygroups(Name.Property, Punctuation), ('#pop', 'value'))], 'value': [('(\\s*)([^\\n]+\\S)(\\n )', bygroups(Whitespace, String, Whitespace)), ('(\\s*)([^\\n]+\\S)(\\n)', bygroups(Whitespace, String, Whitespace), '#pop')], 'url': [('([ \\t]*)(\\S*)([ \\t]*\\n )', bygroups(Whitespace, Comment.PreprocFile, Whitespace)), ('([ \\t]*)(\\S*)([ \\t]*\\n)', bygroups(Whitespace, Comment.PreprocFile, Whitespace), '#pop')], 'dn': [('([ \\t]*)([-a-zA-Z0-9\\.]+)(=)', bygroups(Whitespace, Name.Attribute, Operator), ('#pop', 'dn-value'))], 'dn-value': [('\\\\[^\\n]', Escape), (',', Punctuation, ('#pop', 'dn')), ('\\+', Operator, ('#pop', 'dn')), ('[^,\\+\\n]+', String), ('\\n ', Whitespace), ('\\n', Whitespace, '#pop')], 'base64-dn': [('([ \\t]*)([^ \\t\\n][^ \\t\\n]*[^\\n])([ \\t]*\\n )', bygroups(Whitespace, Name, Whitespace)), ('([ \\t]*)([^ \\t\\n][^ \\t\\n]*[^\\n])([ \\t]*\\n)', bygroups(Whitespace, Name, Whitespace), '#pop')]}



class LdaprcLexer(RegexLexer):
    """
    Lexer for OpenLDAP configuration files.
    """
    name = 'LDAP configuration file'
    aliases = ['ldapconf', 'ldaprc']
    filenames = ['.ldaprc', 'ldaprc', 'ldap.conf']
    mimetypes = ['text/x-ldapconf']
    url = 'https://www.openldap.org/software//man.cgi?query=ldap.conf&sektion=5&apropos=0&manpath=OpenLDAP+2.4-Release'
    version_added = '2.17'
    _sasl_keywords = 'SASL_(?:MECH|REALM|AUTHCID|AUTHZID|CBINDING)'
    _tls_keywords = 'TLS_(?:CACERT|CACERTDIR|CERT|ECNAME|KEY|CIPHER_SUITE|PROTOCOL_MIN|RANDFILE|CRLFILE)'
    _literal_keywords = f'(?:URI|SOCKET_BIND_ADDRESSES|{_sasl_keywords}|{_tls_keywords})'
    _boolean_keywords = 'GSSAPI_(?:ALLOW_REMOTE_PRINCIPAL|ENCRYPT|SIGN)|REFERRALS|SASL_NOCANON'
    _integer_keywords = 'KEEPALIVE_(?:IDLE|PROBES|INTERVAL)|NETWORK_TIMEOUT|PORT|SIZELIMIT|TIMELIMIT|TIMEOUT'
    _secprops = 'none|noanonymous|noplain|noactive|nodict|forwardsec|passcred|(?:minssf|maxssf|maxbufsize)=\\d+'
    flags = re.IGNORECASE | re.MULTILINE
    tokens = {'root': [('#.*', Comment.Single), ('\\s+', Whitespace), (f'({_boolean_keywords})(\\s+)(on|true|yes|off|false|no)$', bygroups(Keyword, Whitespace, Keyword.Constant)), (f'({_integer_keywords})(\\s+)(\\d+)', bygroups(Keyword, Whitespace, Number.Integer)), ('(VERSION)(\\s+)(2|3)', bygroups(Keyword, Whitespace, Number.Integer)), ('(DEREF)(\\s+)(never|searching|finding|always)', bygroups(Keyword, Whitespace, Keyword.Constant)), (f'(SASL_SECPROPS)(\\s+)((?:{_secprops})(?:,{_secprops})*)', bygroups(Keyword, Whitespace, Keyword.Constant)), ('(SASL_CBINDING)(\\s+)(none|tls-unique|tls-endpoint)', bygroups(Keyword, Whitespace, Keyword.Constant)), ('(TLS_REQ(?:CERT|SAN))(\\s+)(allow|demand|hard|never|try)', bygroups(Keyword, Whitespace, Keyword.Constant)), ('(TLS_CRLCHECK)(\\s+)(none|peer|all)', bygroups(Keyword, Whitespace, Keyword.Constant)), ('(BASE|BINDDN)(\\s+)(\\S+)$', bygroups(Keyword, Whitespace, Literal)), ('(HOST)(\\s+)([a-z0-9]+)((?::(\\d+))?)', bygroups(Keyword, Whitespace, Literal, Number.Integer)), (f'({_literal_keywords})(\\s+)(\\S+)$', bygroups(Keyword, Whitespace, Literal))]}



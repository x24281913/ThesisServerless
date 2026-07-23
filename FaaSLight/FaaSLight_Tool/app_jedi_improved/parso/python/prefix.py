import re
from codecs import BOM_UTF8
from typing import Tuple
from parso.python.tokenize import group
unicode_bom = BOM_UTF8.decode('utf-8')


class PrefixPart:
    
    def __init__(self, leaf, typ, value, spacing='', start_pos=None):
        assert start_pos is not None
        self.parent = leaf
        self.type = typ
        self.value = value
        self.spacing = spacing
        self.start_pos: Tuple[(int, int)] = start_pos
    
    @property
    def end_pos(self) -> Tuple[(int, int)]:
        if (self.value.endswith('\n') or self.value.endswith('\r')):
            return (self.start_pos[0] + 1, 0)
        if self.value == unicode_bom:
            return self.start_pos
        return (self.start_pos[0], self.start_pos[1] + len(self.value))
    
    def create_spacing_part(self):
        column = self.start_pos[1] - len(self.spacing)
        return PrefixPart(self.parent, 'spacing', self.spacing, start_pos=(self.start_pos[0], column))
    
    def __repr__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__, self.type, repr(self.value), self.start_pos)
    
    def search_ancestor(self, *node_types):
        node = self.parent
        while node is not None:
            if node.type in node_types:
                return node
            node = node.parent
        return None

_comment = '#[^\\n\\r\\f]*'
_backslash = '\\\\\\r?\\n|\\\\\\r'
_newline = '\\r?\\n|\\r'
_form_feed = '\\f'
_only_spacing = '$'
_spacing = '[ \\t]*'
_bom = unicode_bom
_regex = group(_comment, _backslash, _newline, _form_feed, _only_spacing, _bom, capture=True)
_regex = re.compile(group(_spacing, capture=True) + _regex)
_types = {'#': 'comment', '\\': 'backslash', '\x0c': 'formfeed', '\n': 'newline', '\r': 'newline', unicode_bom: 'bom'}

def split_prefix(leaf, start_pos):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('parso.python.prefix.split_prefix', 'split_prefix(leaf, start_pos)', {'_regex': _regex, '_types': _types, 'PrefixPart': PrefixPart, 'leaf': leaf, 'start_pos': start_pos}, 0)


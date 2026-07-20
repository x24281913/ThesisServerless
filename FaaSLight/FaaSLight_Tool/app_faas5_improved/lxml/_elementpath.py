from __future__ import absolute_import
import re
xpath_tokenizer_re = re.compile('(\'[^\']*\'|"[^"]*"|::|//?|\\.\\.|\\(\\)|[/.*:\\[\\]\\(\\)@=])|((?:\\{[^}]+\\})?[^/\\[\\]\\(\\)@=\\s]+)|\\s+')

def xpath_tokenizer(pattern, namespaces=None):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml._elementpath.xpath_tokenizer', 'xpath_tokenizer(pattern, namespaces=None)', {'xpath_tokenizer_re': xpath_tokenizer_re, 'pattern': pattern, 'namespaces': namespaces}, 0)

def prepare_child(next, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.prepare_child', 'prepare_child(next, token)', {'next': next, 'token': token}, 1)

def prepare_star(next, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.prepare_star', 'prepare_star(next, token)', {'next': next, 'token': token}, 1)

def prepare_self(next, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.prepare_self', 'prepare_self(next, token)', {'next': next, 'token': token}, 1)

def prepare_descendant(next, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.prepare_descendant', 'prepare_descendant(next, token)', {'next': next, 'token': token}, 1)

def prepare_parent(next, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.prepare_parent', 'prepare_parent(next, token)', {'next': next, 'token': token}, 1)

def prepare_predicate(next, token):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.prepare_predicate', 'prepare_predicate(next, token)', {'re': re, 'next': next, 'token': token}, 1)
ops = {'': prepare_child, '*': prepare_star, '.': prepare_self, '..': prepare_parent, '//': prepare_descendant, '[': prepare_predicate}
_cache = {}

def _build_path_iterator(path, namespaces):
    """compile selector pattern"""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath._build_path_iterator', '_build_path_iterator(path, namespaces)', {'_cache': _cache, 'xpath_tokenizer': xpath_tokenizer, 'ops': ops, 'path': path, 'namespaces': namespaces}, 1)

def iterfind(elem, path, namespaces=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.iterfind', 'iterfind(elem, path, namespaces=None)', {'_build_path_iterator': _build_path_iterator, 'elem': elem, 'path': path, 'namespaces': namespaces}, 1)

def find(elem, path, namespaces=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.find', 'find(elem, path, namespaces=None)', {'iterfind': iterfind, 'elem': elem, 'path': path, 'namespaces': namespaces}, 1)

def findall(elem, path, namespaces=None):
    return list(iterfind(elem, path, namespaces))

def findtext(elem, path, default=None, namespaces=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml._elementpath.findtext', 'findtext(elem, path, default=None, namespaces=None)', {'elem': elem, 'path': path, 'default': default, 'namespaces': namespaces}, 1)


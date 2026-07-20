from lxml.etree import XPath, ElementBase
from lxml.html import fromstring, XHTML_NAMESPACE
from lxml.html import _forms_xpath, _options_xpath, _nons, _transform_result
from lxml.html import defs
import copy
try:
    basestring
except NameError:
    basestring = str
__all__ = ['FormNotFound', 'fill_form', 'fill_form_html', 'insert_errors', 'insert_errors_html', 'DefaultErrorCreator']


class FormNotFound(LookupError):
    """
    Raised when no form can be found
    """
    

_form_name_xpath = XPath('descendant-or-self::form[name=$name]|descendant-or-self::x:form[name=$name]', namespaces={'x': XHTML_NAMESPACE})
_input_xpath = XPath('|'.join(['descendant-or-self::' + _tag for _tag in ('input', 'select', 'textarea', 'x:input', 'x:select', 'x:textarea')]), namespaces={'x': XHTML_NAMESPACE})
_label_for_xpath = XPath('//label[@for=$for_id]|//x:label[@for=$for_id]', namespaces={'x': XHTML_NAMESPACE})
_name_xpath = XPath('descendant-or-self::*[@name=$name]')

def fill_form(el, values, form_id=None, form_index=None):
    el = _find_form(el, form_id=form_id, form_index=form_index)
    _fill_form(el, values)

def fill_form_html(html, values, form_id=None, form_index=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.formfill.fill_form_html', 'fill_form_html(html, values, form_id=None, form_index=None)', {'basestring': basestring, 'fromstring': fromstring, 'copy': copy, 'fill_form': fill_form, '_transform_result': _transform_result, 'html': html, 'values': values, 'form_id': form_id, 'form_index': form_index}, 1)

def _fill_form(el, values):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._fill_form', '_fill_form(el, values)', {'_input_xpath': _input_xpath, '_takes_multiple': _takes_multiple, '_fill_multiple': _fill_multiple, '_fill_single': _fill_single, 'el': el, 'values': values}, 0)

def _takes_multiple(input):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.formfill._takes_multiple', '_takes_multiple(input)', {'_nons': _nons, 'input': input}, 1)

def _fill_multiple(input, value):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._fill_multiple', '_fill_multiple(input, value)', {'basestring': basestring, '_check': _check, '_nons': _nons, '_options_xpath': _options_xpath, '_select': _select, 'input': input, 'value': value}, 0)

def _check(el, check):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._check', '_check(el, check)', {'el': el, 'check': check}, 0)

def _select(el, select):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._select', '_select(el, select)', {'el': el, 'select': select}, 0)

def _fill_single(input, value):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._fill_single', '_fill_single(input, value)', {'_nons': _nons, 'input': input, 'value': value}, 0)

def _find_form(el, form_id=None, form_index=None):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.formfill._find_form', '_find_form(el, form_id=None, form_index=None)', {'_forms_xpath': _forms_xpath, 'FormNotFound': FormNotFound, '_form_name_xpath': _form_name_xpath, '_find_form_ids': _find_form_ids, 'el': el, 'form_id': form_id, 'form_index': form_index}, 1)

def _find_form_ids(el):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.formfill._find_form_ids', '_find_form_ids(el)', {'_forms_xpath': _forms_xpath, 'el': el}, 1)


class DefaultErrorCreator(object):
    insert_before = True
    block_inside = True
    error_container_tag = 'div'
    error_message_class = 'error-message'
    error_block_class = 'error-block'
    default_message = 'Invalid'
    
    def __init__(self, **kw):
        for (name, value) in kw.items():
            if not hasattr(self, name):
                raise TypeError('Unexpected keyword argument: %s' % name)
            setattr(self, name, value)
    
    def __call__(self, el, is_block, message):
        error_el = el.makeelement(self.error_container_tag)
        if self.error_message_class:
            error_el.set('class', self.error_message_class)
        if (is_block and self.error_block_class):
            error_el.set('class', error_el.get('class', '') + ' ' + self.error_block_class)
        if (message is None or message == ''):
            message = self.default_message
        if isinstance(message, ElementBase):
            error_el.append(message)
        else:
            assert isinstance(message, basestring), 'Bad message; should be a string or element: %r' % message
            error_el.text = (message or self.default_message)
        if (is_block and self.block_inside):
            if self.insert_before:
                error_el.tail = el.text
                el.text = None
                el.insert(0, error_el)
            else:
                el.append(error_el)
        else:
            parent = el.getparent()
            pos = parent.index(el)
            if self.insert_before:
                parent.insert(pos, error_el)
            else:
                error_el.tail = el.tail
                el.tail = None
                parent.insert(pos + 1, error_el)

default_error_creator = DefaultErrorCreator()

def insert_errors(el, errors, form_id=None, form_index=None, error_class='error', error_creator=default_error_creator):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill.insert_errors', "insert_errors(el, errors, form_id=None, form_index=None, error_class='error', error_creator=default_error_creator)", {'_find_form': _find_form, '_find_elements_for_name': _find_elements_for_name, 'basestring': basestring, 'ElementBase': ElementBase, '_insert_error': _insert_error, 'el': el, 'errors': errors, 'form_id': form_id, 'form_index': form_index, 'error_class': error_class, 'error_creator': error_creator, 'default_error_creator': default_error_creator}, 0)

def insert_errors_html(html, values, **kw):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.formfill.insert_errors_html', 'insert_errors_html(html, values, **kw)', {'basestring': basestring, 'fromstring': fromstring, 'copy': copy, 'insert_errors': insert_errors, '_transform_result': _transform_result, 'html': html, 'values': values, 'kw': kw}, 1)

def _insert_error(el, error, error_class, error_creator):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._insert_error', '_insert_error(el, error, error_class, error_creator)', {'_nons': _nons, 'defs': defs, '_add_class': _add_class, '_label_for_xpath': _label_for_xpath, 'el': el, 'error': error, 'error_class': error_class, 'error_creator': error_creator}, 0)

def _add_class(el, class_name):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.formfill._add_class', '_add_class(el, class_name)', {'el': el, 'class_name': class_name}, 0)

def _find_elements_for_name(form, name, error):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.formfill._find_elements_for_name', '_find_elements_for_name(form, name, error)', {'_name_xpath': _name_xpath, 'form': form, 'name': name, 'error': error}, 1)


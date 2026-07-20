"""A cleanup tool for HTML.

Removes unwanted tags and content.  See the `Cleaner` class for
details.
"""

from __future__ import absolute_import
import copy
import re
import sys
try:
    from urlparse import urlsplit
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import urlsplit, unquote_plus
from lxml import etree
from lxml.html import defs
from lxml.html import fromstring, XHTML_NAMESPACE
from lxml.html import xhtml_to_html, _transform_result
try:
    unichr
except NameError:
    unichr = chr
try:
    unicode
except NameError:
    unicode = str
try:
    basestring
except NameError:
    basestring = (str, bytes)
__all__ = ['clean_html', 'clean', 'Cleaner', 'autolink', 'autolink_html', 'word_break', 'word_break_html']
_replace_css_javascript = re.compile('expression\\s*\\(.*?\\)', re.S | re.I).sub
_replace_css_import = re.compile('@\\s*import', re.I).sub
_looks_like_tag_content = re.compile('</?[a-zA-Z]+|\\son[a-zA-Z]+\\s*=', *((re.ASCII, ) if sys.version_info[0] >= 3 else ())).search
_find_image_dataurls = re.compile('data:image/(.+);base64,', re.I).findall
_possibly_malicious_schemes = re.compile('(javascript|jscript|livescript|vbscript|data|about|mocha):', re.I).findall
_is_unsafe_image_type = re.compile('(xml|svg)', re.I).search

def _has_javascript_scheme(s):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean._has_javascript_scheme', '_has_javascript_scheme(s)', {'_find_image_dataurls': _find_image_dataurls, '_is_unsafe_image_type': _is_unsafe_image_type, '_possibly_malicious_schemes': _possibly_malicious_schemes, 's': s}, 1)
_substitute_whitespace = re.compile('[\\s\\x00-\\x08\\x0B\\x0C\\x0E-\\x19]+').sub
_conditional_comment_re = re.compile('\\[if[\\s\\n\\r]+.*?][\\s\\n\\r]*>', re.I | re.S)
_find_styled_elements = etree.XPath('descendant-or-self::*[@style]')
_find_external_links = etree.XPath("descendant-or-self::a  [normalize-space(@href) and substring(normalize-space(@href),1,1) != '#'] |descendant-or-self::x:a[normalize-space(@href) and substring(normalize-space(@href),1,1) != '#']", namespaces={'x': XHTML_NAMESPACE})


class Cleaner(object):
    """
    Instances cleans the document of each of the possible offending
    elements.  The cleaning is controlled by attributes; you can
    override attributes in a subclass, or set them in the constructor.

    ``scripts``:
        Removes any ``<script>`` tags.

    ``javascript``:
        Removes any Javascript, like an ``onclick`` attribute. Also removes stylesheets
        as they could contain Javascript.

    ``comments``:
        Removes any comments.

    ``style``:
        Removes any style tags.

    ``inline_style``
        Removes any style attributes.  Defaults to the value of the ``style`` option.

    ``links``:
        Removes any ``<link>`` tags

    ``meta``:
        Removes any ``<meta>`` tags

    ``page_structure``:
        Structural parts of a page: ``<head>``, ``<html>``, ``<title>``.

    ``processing_instructions``:
        Removes any processing instructions.

    ``embedded``:
        Removes any embedded objects (flash, iframes)

    ``frames``:
        Removes any frame-related tags

    ``forms``:
        Removes any form tags

    ``annoying_tags``:
        Tags that aren't *wrong*, but are annoying.  ``<blink>`` and ``<marquee>``

    ``remove_tags``:
        A list of tags to remove.  Only the tags will be removed,
        their content will get pulled up into the parent tag.

    ``kill_tags``:
        A list of tags to kill.  Killing also removes the tag's content,
        i.e. the whole subtree, not just the tag itself.

    ``allow_tags``:
        A list of tags to include (default include all).

    ``remove_unknown_tags``:
        Remove any tags that aren't standard parts of HTML.

    ``safe_attrs_only``:
        If true, only include 'safe' attributes (specifically the list
        from the feedparser HTML sanitisation web site).

    ``safe_attrs``:
        A set of attribute names to override the default list of attributes
        considered 'safe' (when safe_attrs_only=True).

    ``add_nofollow``:
        If true, then any <a> tags will have ``rel="nofollow"`` added to them.

    ``host_whitelist``:
        A list or set of hosts that you can use for embedded content
        (for content like ``<object>``, ``<link rel="stylesheet">``, etc).
        You can also implement/override the method
        ``allow_embedded_url(el, url)`` or ``allow_element(el)`` to
        implement more complex rules for what can be embedded.
        Anything that passes this test will be shown, regardless of
        the value of (for instance) ``embedded``.

        Note that this parameter might not work as intended if you do not
        make the links absolute before doing the cleaning.

        Note that you may also need to set ``whitelist_tags``.

    ``whitelist_tags``:
        A set of tags that can be included with ``host_whitelist``.
        The default is ``iframe`` and ``embed``; you may wish to
        include other tags like ``script``, or you may want to
        implement ``allow_embedded_url`` for more control.  Set to None to
        include all tags.

    This modifies the document *in place*.
    """
    scripts = True
    javascript = True
    comments = True
    style = False
    inline_style = None
    links = True
    meta = True
    page_structure = True
    processing_instructions = True
    embedded = True
    frames = True
    forms = True
    annoying_tags = True
    remove_tags = None
    allow_tags = None
    kill_tags = None
    remove_unknown_tags = True
    safe_attrs_only = True
    safe_attrs = defs.safe_attrs
    add_nofollow = False
    host_whitelist = ()
    whitelist_tags = {'iframe', 'embed'}
    
    def __init__(self, **kw):
        not_an_attribute = object()
        for (name, value) in kw.items():
            default = getattr(self, name, not_an_attribute)
            if (default is not None and default is not True and default is not False and not isinstance(default, (frozenset, set, tuple, list))):
                raise TypeError('Unknown parameter: %s=%r' % (name, value))
            setattr(self, name, value)
        if (self.inline_style is None and 'inline_style' not in kw):
            self.inline_style = self.style
        if kw.get('allow_tags'):
            if kw.get('remove_unknown_tags'):
                raise ValueError('It does not make sense to pass in both allow_tags and remove_unknown_tags')
            self.remove_unknown_tags = False
    _tag_link_attrs = dict(script='src', link='href', applet=['code', 'object'], iframe='src', embed='src', layer='src', a='href')
    
    def __call__(self, doc):
        """
        Cleans the document.
        """
        try:
            getroot = doc.getroot
        except AttributeError:
            pass
        else:
            doc = getroot()
        xhtml_to_html(doc)
        for el in doc.iter('image'):
            el.tag = 'img'
        if not self.comments:
            self.kill_conditional_comments(doc)
        kill_tags = set((self.kill_tags or ()))
        remove_tags = set((self.remove_tags or ()))
        allow_tags = set((self.allow_tags or ()))
        if self.scripts:
            kill_tags.add('script')
        if self.safe_attrs_only:
            safe_attrs = set(self.safe_attrs)
            for el in doc.iter(etree.Element):
                attrib = el.attrib
                for aname in attrib.keys():
                    if aname not in safe_attrs:
                        del attrib[aname]
        if self.javascript:
            if not ((self.safe_attrs_only and self.safe_attrs == defs.safe_attrs)):
                for el in doc.iter(etree.Element):
                    attrib = el.attrib
                    for aname in attrib.keys():
                        if aname.startswith('on'):
                            del attrib[aname]
            doc.rewrite_links(self._remove_javascript_link, resolve_base_href=False)
            if not self.inline_style:
                for el in _find_styled_elements(doc):
                    old = el.get('style')
                    new = _replace_css_javascript('', old)
                    new = _replace_css_import('', new)
                    if self._has_sneaky_javascript(new):
                        del el.attrib['style']
                    elif new != old:
                        el.set('style', new)
            if not self.style:
                for el in list(doc.iter('style')):
                    if el.get('type', '').lower().strip() == 'text/javascript':
                        el.drop_tree()
                        continue
                    old = (el.text or '')
                    new = _replace_css_javascript('', old)
                    new = _replace_css_import('', new)
                    if self._has_sneaky_javascript(new):
                        el.text = '/* deleted */'
                    elif new != old:
                        el.text = new
        if self.comments:
            kill_tags.add(etree.Comment)
        if self.processing_instructions:
            kill_tags.add(etree.ProcessingInstruction)
        if self.style:
            kill_tags.add('style')
        if self.inline_style:
            etree.strip_attributes(doc, 'style')
        if self.links:
            kill_tags.add('link')
        elif (self.style or self.javascript):
            for el in list(doc.iter('link')):
                if 'stylesheet' in el.get('rel', '').lower():
                    if not self.allow_element(el):
                        el.drop_tree()
        if self.meta:
            kill_tags.add('meta')
        if self.page_structure:
            remove_tags.update(('head', 'html', 'title'))
        if self.embedded:
            for el in list(doc.iter('param')):
                parent = el.getparent()
                while (parent is not None and parent.tag not in ('applet', 'object')):
                    parent = parent.getparent()
                if parent is None:
                    el.drop_tree()
            kill_tags.update(('applet', ))
            remove_tags.update(('iframe', 'embed', 'layer', 'object', 'param'))
        if self.frames:
            kill_tags.update(defs.frame_tags)
        if self.forms:
            remove_tags.add('form')
            kill_tags.update(('button', 'input', 'select', 'textarea'))
        if self.annoying_tags:
            remove_tags.update(('blink', 'marquee'))
        _remove = []
        _kill = []
        for el in doc.iter():
            if el.tag in kill_tags:
                if self.allow_element(el):
                    continue
                _kill.append(el)
            elif el.tag in remove_tags:
                if self.allow_element(el):
                    continue
                _remove.append(el)
        if (_remove and _remove[0] == doc):
            el = _remove.pop(0)
            el.tag = 'div'
            el.attrib.clear()
        elif (_kill and _kill[0] == doc):
            el = _kill.pop(0)
            if el.tag != 'html':
                el.tag = 'div'
            el.clear()
        _kill.reverse()
        for el in _kill:
            el.drop_tree()
        for el in _remove:
            el.drop_tag()
        if self.remove_unknown_tags:
            if allow_tags:
                raise ValueError('It does not make sense to pass in both allow_tags and remove_unknown_tags')
            allow_tags = set(defs.tags)
        if allow_tags:
            if not self.comments:
                allow_tags.add(etree.Comment)
            if not self.processing_instructions:
                allow_tags.add(etree.ProcessingInstruction)
            bad = []
            for el in doc.iter():
                if el.tag not in allow_tags:
                    bad.append(el)
            if bad:
                if bad[0] is doc:
                    el = bad.pop(0)
                    el.tag = 'div'
                    el.attrib.clear()
                for el in bad:
                    el.drop_tag()
        if self.add_nofollow:
            for el in _find_external_links(doc):
                if not self.allow_follow(el):
                    rel = el.get('rel')
                    if rel:
                        if ('nofollow' in rel and ' nofollow ' in ' %s ' % rel):
                            continue
                        rel = '%s nofollow' % rel
                    else:
                        rel = 'nofollow'
                    el.set('rel', rel)
    
    def allow_follow(self, anchor):
        """
        Override to suppress rel="nofollow" on some anchors.
        """
        return False
    
    def allow_element(self, el):
        """
        Decide whether an element is configured to be accepted or rejected.

        :param el: an element.
        :return: true to accept the element or false to reject/discard it.
        """
        if el.tag not in self._tag_link_attrs:
            return False
        attr = self._tag_link_attrs[el.tag]
        if isinstance(attr, (list, tuple)):
            for one_attr in attr:
                url = el.get(one_attr)
                if not url:
                    return False
                if not self.allow_embedded_url(el, url):
                    return False
            return True
        else:
            url = el.get(attr)
            if not url:
                return False
            return self.allow_embedded_url(el, url)
    
    def allow_embedded_url(self, el, url):
        """
        Decide whether a URL that was found in an element's attributes or text
        if configured to be accepted or rejected.

        :param el: an element.
        :param url: a URL found on the element.
        :return: true to accept the URL and false to reject it.
        """
        if (self.whitelist_tags is not None and el.tag not in self.whitelist_tags):
            return False
        (scheme, netloc, path, query, fragment) = urlsplit(url)
        netloc = netloc.lower().split(':', 1)[0]
        if scheme not in ('http', 'https'):
            return False
        if netloc in self.host_whitelist:
            return True
        return False
    
    def kill_conditional_comments(self, doc):
        """
        IE conditional comments basically embed HTML that the parser
        doesn't normally see.  We can't allow anything like that, so
        we'll kill any comments that could be conditional.
        """
        has_conditional_comment = _conditional_comment_re.search
        self._kill_elements(doc, lambda el: has_conditional_comment(el.text), etree.Comment)
    
    def _kill_elements(self, doc, condition, iterate=None):
        bad = []
        for el in doc.iter(iterate):
            if condition(el):
                bad.append(el)
        for el in bad:
            el.drop_tree()
    
    def _remove_javascript_link(self, link):
        new = _substitute_whitespace('', unquote_plus(link))
        if _has_javascript_scheme(new):
            return ''
        return link
    _substitute_comments = re.compile('/\\*.*?\\*/', re.S).sub
    
    def _has_sneaky_javascript(self, style):
        """
        Depending on the browser, stuff like ``e x p r e s s i o n(...)``
        can get interpreted, or ``expre/* stuff */ssion(...)``.  This
        checks for attempt to do stuff like this.

        Typically the response will be to kill the entire style; if you
        have just a bit of Javascript in the style another rule will catch
        that and remove only the Javascript from the style; this catches
        more sneaky attempts.
        """
        style = self._substitute_comments('', style)
        style = style.replace('\\', '')
        style = _substitute_whitespace('', style)
        style = style.lower()
        if _has_javascript_scheme(style):
            return True
        if 'expression(' in style:
            return True
        if '@import' in style:
            return True
        if '</noscript' in style:
            return True
        if _looks_like_tag_content(style):
            return True
        return False
    
    def clean_html(self, html):
        result_type = type(html)
        if isinstance(html, basestring):
            doc = fromstring(html)
        else:
            doc = copy.deepcopy(html)
        self(doc)
        return _transform_result(result_type, doc)

clean = Cleaner()
clean_html = clean.clean_html
_link_regexes = [re.compile('(?P<body>https?://(?P<host>[a-z0-9._-]+)(?:/[/\\-_.,a-z0-9%&?;=~]*)?(?:\\([/\\-_.,a-z0-9%&?;=~]*\\))?)', re.I), re.compile('mailto:(?P<body>[a-z0-9._-]+@(?P<host>[a-z0-9_.-]+[a-z]))', re.I)]
_avoid_elements = ['textarea', 'pre', 'code', 'head', 'select', 'a']
_avoid_hosts = [re.compile('^localhost', re.I), re.compile('\\bexample\\.(?:com|org|net)$', re.I), re.compile('^127\\.0\\.0\\.1$')]
_avoid_classes = ['nolink']

def autolink(el, link_regexes=_link_regexes, avoid_elements=_avoid_elements, avoid_hosts=_avoid_hosts, avoid_classes=_avoid_classes):
    """
    Turn any URLs into links.

    It will search for links identified by the given regular
    expressions (by default mailto and http(s) links).

    It won't link text in an element in avoid_elements, or an element
    with a class in avoid_classes.  It won't link to anything with a
    host that matches one of the regular expressions in avoid_hosts
    (default localhost and 127.0.0.1).

    If you pass in an element, the element's tail will not be
    substituted, only the contents of the element.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean.autolink', 'autolink(el, link_regexes=_link_regexes, avoid_elements=_avoid_elements, avoid_hosts=_avoid_hosts, avoid_classes=_avoid_classes)', {'autolink': autolink, '_link_text': _link_text, 'el': el, 'link_regexes': link_regexes, 'avoid_elements': avoid_elements, 'avoid_hosts': avoid_hosts, 'avoid_classes': avoid_classes, '_link_regexes': _link_regexes, '_avoid_elements': _avoid_elements, '_avoid_hosts': _avoid_hosts, '_avoid_classes': _avoid_classes}, 1)

def _link_text(text, link_regexes, avoid_hosts, factory):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean._link_text', '_link_text(text, link_regexes, avoid_hosts, factory)', {'text': text, 'link_regexes': link_regexes, 'avoid_hosts': avoid_hosts, 'factory': factory}, 2)

def autolink_html(html, *args, **kw):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean.autolink_html', 'autolink_html(html, *args, **kw)', {'basestring': basestring, 'fromstring': fromstring, 'copy': copy, 'autolink': autolink, '_transform_result': _transform_result, 'html': html, 'args': args, 'kw': kw}, 1)
autolink_html.__doc__ = autolink.__doc__
_avoid_word_break_elements = ['pre', 'textarea', 'code']
_avoid_word_break_classes = ['nobreak']

def word_break(el, max_width=40, avoid_elements=_avoid_word_break_elements, avoid_classes=_avoid_word_break_classes, break_character=unichr(8203)):
    """
    Breaks any long words found in the body of the text (not attributes).

    Doesn't effect any of the tags in avoid_elements, by default
    ``<textarea>`` and ``<pre>``

    Breaks words by inserting &#8203;, which is a unicode character
    for Zero Width Space character.  This generally takes up no space
    in rendering, but does copy as a space, and in monospace contexts
    usually takes up space.

    See http://www.cs.tut.fi/~jkorpela/html/nobr.html for a discussion
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean.word_break', 'word_break(el, max_width=40, avoid_elements=_avoid_word_break_elements, avoid_classes=_avoid_word_break_classes, break_character=unichr(8203))', {'_break_text': _break_text, 'word_break': word_break, 'el': el, 'max_width': max_width, 'avoid_elements': avoid_elements, 'avoid_classes': avoid_classes, 'break_character': break_character, '_avoid_word_break_elements': _avoid_word_break_elements, '_avoid_word_break_classes': _avoid_word_break_classes}, 1)

def word_break_html(html, *args, **kw):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean.word_break_html', 'word_break_html(html, *args, **kw)', {'fromstring': fromstring, 'word_break': word_break, '_transform_result': _transform_result, 'html': html, 'args': args, 'kw': kw}, 1)

def _break_text(text, max_width, break_character):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean._break_text', '_break_text(text, max_width, break_character)', {'_insert_break': _insert_break, 'text': text, 'max_width': max_width, 'break_character': break_character}, 1)
_break_prefer_re = re.compile('[^a-z]', re.I)

def _insert_break(word, width, break_character):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.clean._insert_break', '_insert_break(word, width, break_character)', {'_break_prefer_re': _break_prefer_re, 'word': word, 'width': width, 'break_character': break_character}, 1)


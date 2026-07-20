from __future__ import absolute_import
import difflib
from lxml import etree
from lxml.html import fragment_fromstring
import re
__all__ = ['html_annotate', 'htmldiff']
try:
    from html import escape as html_escape
except ImportError:
    from cgi import escape as html_escape
try:
    _unicode = unicode
except NameError:
    _unicode = str
try:
    basestring
except NameError:
    basestring = str

def default_markup(text, version):
    return '<span title="%s">%s</span>' % (html_escape(_unicode(version), 1), text)

def html_annotate(doclist, markup=default_markup):
    """
    doclist should be ordered from oldest to newest, like::

        >>> version1 = 'Hello World'
        >>> version2 = 'Goodbye World'
        >>> print(html_annotate([(version1, 'version 1'),
        ...                      (version2, 'version 2')]))
        <span title="version 2">Goodbye</span> <span title="version 1">World</span>

    The documents must be *fragments* (str/UTF8 or unicode), not
    complete documents

    The markup argument is a function to markup the spans of words.
    This function is called like markup('Hello', 'version 2'), and
    returns HTML.  The first argument is text and never includes any
    markup.  The default uses a span with a title:

        >>> print(default_markup('Some Text', 'by Joe'))
        <span title="by Joe">Some Text</span>
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.html_annotate', 'html_annotate(doclist, markup=default_markup)', {'tokenize_annotated': tokenize_annotated, 'html_annotate_merge_annotations': html_annotate_merge_annotations, 'compress_tokens': compress_tokens, 'markup_serialize_tokens': markup_serialize_tokens, 'doclist': doclist, 'markup': markup, 'default_markup': default_markup}, 1)

def tokenize_annotated(doc, annotation):
    """Tokenize a document and add an annotation attribute to each token
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.tokenize_annotated', 'tokenize_annotated(doc, annotation)', {'tokenize': tokenize, 'doc': doc, 'annotation': annotation}, 1)

def html_annotate_merge_annotations(tokens_old, tokens_new):
    """Merge the annotations from tokens_old into tokens_new, when the
    tokens in the new document already existed in the old document.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.html_annotate_merge_annotations', 'html_annotate_merge_annotations(tokens_old, tokens_new)', {'InsensitiveSequenceMatcher': InsensitiveSequenceMatcher, 'copy_annotations': copy_annotations, 'tokens_old': tokens_old, 'tokens_new': tokens_new}, 0)

def copy_annotations(src, dest):
    """
    Copy annotations from the tokens listed in src to the tokens in dest
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.copy_annotations', 'copy_annotations(src, dest)', {'src': src, 'dest': dest}, 0)

def compress_tokens(tokens):
    """
    Combine adjacent tokens when there is no HTML between the tokens, 
    and they share an annotation
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.compress_tokens', 'compress_tokens(tokens)', {'compress_merge_back': compress_merge_back, 'tokens': tokens}, 1)

def compress_merge_back(tokens, tok):
    """ Merge tok into the last element of tokens (modifying the list of
    tokens in-place).  """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.compress_merge_back', 'compress_merge_back(tokens, tok)', {'token': token, '_unicode': _unicode, 'tokens': tokens, 'tok': tok}, 0)

def markup_serialize_tokens(tokens, markup_func):
    """
    Serialize the list of tokens into a list of text chunks, calling
    markup_func around text to add annotations.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.markup_serialize_tokens', 'markup_serialize_tokens(tokens, markup_func)', {'tokens': tokens, 'markup_func': markup_func}, 0)

def htmldiff(old_html, new_html):
    """ Do a diff of the old and new document.  The documents are HTML
    *fragments* (str/UTF8 or unicode), they are not complete documents
    (i.e., no <html> tag).

    Returns HTML with <ins> and <del> tags added around the
    appropriate text.  

    Markup is generally ignored, with the markup from new_html
    preserved, and possibly some markup from old_html (though it is
    considered acceptable to lose some of the old markup).  Only the
    words in the HTML are diffed.  The exception is <img> tags, which
    are treated like words, and the href attribute of <a> tags, which
    are noted inside the tag itself when there are changes.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.htmldiff', 'htmldiff(old_html, new_html)', {'tokenize': tokenize, 'htmldiff_tokens': htmldiff_tokens, 'fixup_ins_del_tags': fixup_ins_del_tags, 'old_html': old_html, 'new_html': new_html}, 1)

def htmldiff_tokens(html1_tokens, html2_tokens):
    """ Does a diff on the tokens themselves, returning a list of text
    chunks (not tokens).
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.htmldiff_tokens', 'htmldiff_tokens(html1_tokens, html2_tokens)', {'InsensitiveSequenceMatcher': InsensitiveSequenceMatcher, 'expand_tokens': expand_tokens, 'merge_insert': merge_insert, 'merge_delete': merge_delete, 'cleanup_delete': cleanup_delete, 'html1_tokens': html1_tokens, 'html2_tokens': html2_tokens}, 1)

def expand_tokens(tokens, equal=False):
    """Given a list of tokens, return a generator of the chunks of
    text for the data in the tokens.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.expand_tokens', 'expand_tokens(tokens, equal=False)', {'tokens': tokens, 'equal': equal}, 0)

def merge_insert(ins_chunks, doc):
    """ doc is the already-handled document (as a list of text chunks);
    here we add <ins>ins_chunks</ins> to the end of that.  """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.merge_insert', 'merge_insert(ins_chunks, doc)', {'split_unbalanced': split_unbalanced, 'ins_chunks': ins_chunks, 'doc': doc}, 0)


class DEL_START:
    pass



class DEL_END:
    pass



class NoDeletes(Exception):
    """ Raised when the document no longer contains any pending deletes
    (DEL_START/DEL_END) """
    


def merge_delete(del_chunks, doc):
    """ Adds the text chunks in del_chunks to the document doc (another
    list of text chunks) with marker to show it is a delete.
    cleanup_delete later resolves these markers into <del> tags."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.merge_delete', 'merge_delete(del_chunks, doc)', {'DEL_START': DEL_START, 'DEL_END': DEL_END, 'del_chunks': del_chunks, 'doc': doc}, 0)

def cleanup_delete(chunks):
    """ Cleans up any DEL_START/DEL_END markers in the document, replacing
    them with <del></del>.  To do this while keeping the document
    valid, it may need to drop some tags (either start or end tags).

    It may also move the del into adjacent tags to try to move it to a
    similar location where it was originally located (e.g., moving a
    delete into preceding <div> tag, if the del looks like (DEL_START,
    'Text</div>', DEL_END)"""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.cleanup_delete', 'cleanup_delete(chunks)', {'split_delete': split_delete, 'NoDeletes': NoDeletes, 'split_unbalanced': split_unbalanced, 'locate_unbalanced_start': locate_unbalanced_start, 'locate_unbalanced_end': locate_unbalanced_end, 'chunks': chunks}, 1)

def split_unbalanced(chunks):
    """Return (unbalanced_start, balanced, unbalanced_end), where each is
    a list of text and tag chunks.

    unbalanced_start is a list of all the tags that are opened, but
    not closed in this span.  Similarly, unbalanced_end is a list of
    tags that are closed but were not opened.  Extracting these might
    mean some reordering of the chunks."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.split_unbalanced', 'split_unbalanced(chunks)', {'empty_tags': empty_tags, 'chunks': chunks}, 3)

def split_delete(chunks):
    """ Returns (stuff_before_DEL_START, stuff_inside_DEL_START_END,
    stuff_after_DEL_END).  Returns the first case found (there may be
    more DEL_STARTs in stuff_after_DEL_END).  Raises NoDeletes if
    there's no DEL_START found. """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.split_delete', 'split_delete(chunks)', {'DEL_START': DEL_START, 'NoDeletes': NoDeletes, 'DEL_END': DEL_END, 'chunks': chunks}, 3)

def locate_unbalanced_start(unbalanced_start, pre_delete, post_delete):
    """ pre_delete and post_delete implicitly point to a place in the
    document (where the two were split).  This moves that point (by
    popping items from one and pushing them onto the other).  It moves
    the point to try to find a place where unbalanced_start applies.

    As an example::

        >>> unbalanced_start = ['<div>']
        >>> doc = ['<p>', 'Text', '</p>', '<div>', 'More Text', '</div>']
        >>> pre, post = doc[:3], doc[3:]
        >>> pre, post
        (['<p>', 'Text', '</p>'], ['<div>', 'More Text', '</div>'])
        >>> locate_unbalanced_start(unbalanced_start, pre, post)
        >>> pre, post
        (['<p>', 'Text', '</p>', '<div>'], ['More Text', '</div>'])

    As you can see, we moved the point so that the dangling <div> that
    we found will be effectively replaced by the div in the original
    document.  If this doesn't work out, we just throw away
    unbalanced_start without doing anything.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.locate_unbalanced_start', 'locate_unbalanced_start(unbalanced_start, pre_delete, post_delete)', {'DEL_START': DEL_START, 'unbalanced_start': unbalanced_start, 'pre_delete': pre_delete, 'post_delete': post_delete}, 0)

def locate_unbalanced_end(unbalanced_end, pre_delete, post_delete):
    """ like locate_unbalanced_start, except handling end tags and
    possibly moving the point earlier in the document.  """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff.locate_unbalanced_end', 'locate_unbalanced_end(unbalanced_end, pre_delete, post_delete)', {'DEL_END': DEL_END, 'unbalanced_end': unbalanced_end, 'pre_delete': pre_delete, 'post_delete': post_delete}, 0)


class token(_unicode):
    """ Represents a diffable token, generally a word that is displayed to
    the user.  Opening tags are attached to this token when they are
    adjacent (pre_tags) and closing tags that follow the word
    (post_tags).  Some exceptions occur when there are empty tags
    adjacent to a word, so there may be close tags in pre_tags, or
    open tags in post_tags.

    We also keep track of whether the word was originally followed by
    whitespace, even though we do not want to treat the word as
    equivalent to a similar word that does not have a trailing
    space."""
    hide_when_equal = False
    
    def __new__(cls, text, pre_tags=None, post_tags=None, trailing_whitespace=''):
        obj = _unicode.__new__(cls, text)
        if pre_tags is not None:
            obj.pre_tags = pre_tags
        else:
            obj.pre_tags = []
        if post_tags is not None:
            obj.post_tags = post_tags
        else:
            obj.post_tags = []
        obj.trailing_whitespace = trailing_whitespace
        return obj
    
    def __repr__(self):
        return 'token(%s, %r, %r, %r)' % (_unicode.__repr__(self), self.pre_tags, self.post_tags, self.trailing_whitespace)
    
    def html(self):
        return _unicode(self)



class tag_token(token):
    """ Represents a token that is actually a tag.  Currently this is just
    the <img> tag, which takes up visible space just like a word but
    is only represented in a document by a tag.  """
    
    def __new__(cls, tag, data, html_repr, pre_tags=None, post_tags=None, trailing_whitespace=''):
        obj = token.__new__(cls, '%s: %s' % (type, data), pre_tags=pre_tags, post_tags=post_tags, trailing_whitespace=trailing_whitespace)
        obj.tag = tag
        obj.data = data
        obj.html_repr = html_repr
        return obj
    
    def __repr__(self):
        return 'tag_token(%s, %s, html_repr=%s, post_tags=%r, pre_tags=%r, trailing_whitespace=%r)' % (self.tag, self.data, self.html_repr, self.pre_tags, self.post_tags, self.trailing_whitespace)
    
    def html(self):
        return self.html_repr



class href_token(token):
    """ Represents the href in an anchor tag.  Unlike other words, we only
    show the href when it changes.  """
    hide_when_equal = True
    
    def html(self):
        return ' Link: %s' % self


def tokenize(html, include_hrefs=True):
    """
    Parse the given HTML and returns token objects (words with attached tags).

    This parses only the content of a page; anything in the head is
    ignored, and the <head> and <body> elements are themselves
    optional.  The content is then parsed by lxml, which ensures the
    validity of the resulting parsed document (though lxml may make
    incorrect guesses when the markup is particular bad).

    <ins> and <del> tags are also eliminated from the document, as
    that gets confusing.

    If include_hrefs is true, then the href attribute of <a> tags is
    included as a special kind of diffable token."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.tokenize', 'tokenize(html, include_hrefs=True)', {'etree': etree, 'parse_html': parse_html, 'flatten_el': flatten_el, 'fixup_chunks': fixup_chunks, 'html': html, 'include_hrefs': include_hrefs}, 1)

def parse_html(html, cleanup=True):
    """
    Parses an HTML fragment, returning an lxml element.  Note that the HTML will be
    wrapped in a <div> tag that was not in the original document.

    If cleanup is true, make sure there's no <head> or <body>, and get
    rid of any <ins> and <del> tags.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.parse_html', 'parse_html(html, cleanup=True)', {'cleanup_html': cleanup_html, 'fragment_fromstring': fragment_fromstring, 'html': html, 'cleanup': cleanup}, 1)
_body_re = re.compile('<body.*?>', re.I | re.S)
_end_body_re = re.compile('</body.*?>', re.I | re.S)
_ins_del_re = re.compile('</?(ins|del).*?>', re.I | re.S)

def cleanup_html(html):
    """ This 'cleans' the HTML, meaning that any page structure is removed
    (only the contents of <body> are used, if there is any <body).
    Also <ins> and <del> tags are removed.  """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.cleanup_html', 'cleanup_html(html)', {'_body_re': _body_re, '_end_body_re': _end_body_re, '_ins_del_re': _ins_del_re, 'html': html}, 1)
end_whitespace_re = re.compile('[ \\t\\n\\r]$')

def split_trailing_whitespace(word):
    """
    This function takes a word, such as 'test

' and returns ('test','

')
    """
    stripped_length = len(word.rstrip())
    return (word[0:stripped_length], word[stripped_length:])

def fixup_chunks(chunks):
    """
    This function takes a list of chunks and produces a list of tokens.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.fixup_chunks', 'fixup_chunks(chunks)', {'split_trailing_whitespace': split_trailing_whitespace, 'tag_token': tag_token, 'href_token': href_token, 'is_word': is_word, 'token': token, 'is_start_tag': is_start_tag, 'is_end_tag': is_end_tag, 'chunks': chunks}, 1)
empty_tags = ('param', 'img', 'area', 'br', 'basefont', 'input', 'base', 'meta', 'link', 'col')
block_level_tags = ('address', 'blockquote', 'center', 'dir', 'div', 'dl', 'fieldset', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'isindex', 'menu', 'noframes', 'noscript', 'ol', 'p', 'pre', 'table', 'ul')
block_level_container_tags = ('dd', 'dt', 'frameset', 'li', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr')

def flatten_el(el, include_hrefs, skip_tag=False):
    """ Takes an lxml element el, and generates all the text chunks for
    that tag.  Each start tag is a chunk, each word is a chunk, and each
    end tag is a chunk.

    If skip_tag is true, then the outermost container tag is
    not returned (just its contents)."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.flatten_el', 'flatten_el(el, include_hrefs, skip_tag=False)', {'start_tag': start_tag, 'empty_tags': empty_tags, 'split_words': split_words, 'html_escape': html_escape, 'flatten_el': flatten_el, 'end_tag': end_tag, 'el': el, 'include_hrefs': include_hrefs, 'skip_tag': skip_tag}, 1)
split_words_re = re.compile('\\S+(?:\\s+|$)', re.U)

def split_words(text):
    """ Splits some text into words. Includes trailing whitespace
    on each word when appropriate.  """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.split_words', 'split_words(text)', {'split_words_re': split_words_re, 'text': text}, 1)
start_whitespace_re = re.compile('^[ \\t\\n\\r]')

def start_tag(el):
    """
    The text representation of the start tag for a tag.
    """
    return '<%s%s>' % (el.tag, ''.join([' %s="%s"' % (name, html_escape(value, True)) for (name, value) in el.attrib.items()]))

def end_tag(el):
    """ The text representation of an end tag for a tag.  Includes
    trailing whitespace when appropriate.  """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.end_tag', 'end_tag(el)', {'start_whitespace_re': start_whitespace_re, 'el': el}, 1)

def is_word(tok):
    return not tok.startswith('<')

def is_end_tag(tok):
    return tok.startswith('</')

def is_start_tag(tok):
    return (tok.startswith('<') and not tok.startswith('</'))

def fixup_ins_del_tags(html):
    """ Given an html string, move any <ins> or <del> tags inside of any
    block-level elements, e.g. transform <ins><p>word</p></ins> to
    <p><ins>word</ins></p> """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.fixup_ins_del_tags', 'fixup_ins_del_tags(html)', {'parse_html': parse_html, '_fixup_ins_del_tags': _fixup_ins_del_tags, 'serialize_html_fragment': serialize_html_fragment, 'html': html}, 1)

def serialize_html_fragment(el, skip_outer=False):
    """ Serialize a single lxml element as HTML.  The serialized form
    includes the elements tail.  

    If skip_outer is true, then don't serialize the outermost tag
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff.serialize_html_fragment', 'serialize_html_fragment(el, skip_outer=False)', {'basestring': basestring, 'etree': etree, '_unicode': _unicode, 'el': el, 'skip_outer': skip_outer}, 1)

def _fixup_ins_del_tags(doc):
    """fixup_ins_del_tags that works on an lxml document in-place
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff._fixup_ins_del_tags', '_fixup_ins_del_tags(doc)', {'_contains_block_level_tag': _contains_block_level_tag, '_move_el_inside_block': _move_el_inside_block, 'doc': doc}, 0)

def _contains_block_level_tag(el):
    """True if the element contains any block-level elements, like <p>, <td>, etc.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff._contains_block_level_tag', '_contains_block_level_tag(el)', {'block_level_tags': block_level_tags, 'block_level_container_tags': block_level_container_tags, '_contains_block_level_tag': _contains_block_level_tag, 'el': el}, 1)

def _move_el_inside_block(el, tag):
    """ helper for _fixup_ins_del_tags; actually takes the <ins> etc tags
    and moves them inside any block-level tags.  """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('lxml.html.diff._move_el_inside_block', '_move_el_inside_block(el, tag)', {'_contains_block_level_tag': _contains_block_level_tag, 'etree': etree, '_move_el_inside_block': _move_el_inside_block, 'el': el, 'tag': tag}, 1)

def _merge_element_contents(el):
    """
    Removes an element, but merges its contents into its place, e.g.,
    given <p>Hi <i>there!</i></p>, if you remove the <i> element you get
    <p>Hi there!</p>
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('lxml.html.diff._merge_element_contents', '_merge_element_contents(el)', {'el': el}, 0)


class InsensitiveSequenceMatcher(difflib.SequenceMatcher):
    """
    Acts like SequenceMatcher, but tries not to find very small equal
    blocks amidst large spans of changes
    """
    threshold = 2
    
    def get_matching_blocks(self):
        size = min(len(self.b), len(self.b))
        threshold = min(self.threshold, size / 4)
        actual = difflib.SequenceMatcher.get_matching_blocks(self)
        return [item for item in actual if (item[2] > threshold or not item[2])]

if __name__ == '__main__':
    from lxml.html import _diffcommand
    _diffcommand.main()


"""A Docutils-XML parser.

   Provisional:
     The API is not fixed yet.
     Defined objects may be renamed or changed
     in any Docutils release without prior notice.
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
import re
import xml.etree.ElementTree as ET
from docutils import frontend, nodes, parsers, utils


class Parser(parsers.Parser):
    """A Docutils-XML parser."""
    supported = ('xml', 'docutils-xml')
    'Aliases this parser supports.'
    config_section = 'xml parser'
    config_section_dependencies = ('parsers', )
    settings_default_overrides = {'doctitle_xform': False, 'validate': True}
    
    def parse(self, inputstring, document) -> None:
        """
        Parse `inputstring` and populate `document`, a "document tree".

        Provisional.
        """
        self.setup_parse(inputstring, document)
        node = parse_element(inputstring, document)
        if not isinstance(node, nodes.document):
            document.append(node)
        self.finish_parse()



class Unknown(nodes.Special, nodes.Inline, nodes.Element):
    """An unknown element found by the XML parser."""
    content_model = (((nodes.Element, nodes.Text), '*'), )


def parse_element(inputstring, document=None):
    """
    Parse `inputstring` as "Docutils XML", return `nodes.Element` instance.

    :inputstring: XML source.
    :document: `nodes.document` instance (default: a new dummy instance).
               Provides settings and reporter.
               Populated and returned, if the inputstring's root element
               is <document>.

    Caution:
      The function does not detect invalid XML.

      To check the validity of the returned node,
      you may use its `validate()` method::

        node = parse_element('<tip><hint>text</hint></tip>')
        node.validate()

    Provisional.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.docutils_xml.parse_element', 'parse_element(inputstring, document=None)', {'ET': ET, 'element2node': element2node, 'inputstring': inputstring, 'document': document}, 1)

def element2node(element, document=None, unindent=True):
    """
    Convert an `etree` element and its children to Docutils doctree nodes.

    :element:  `xml.etree` element
    :document: see `parse_element()`
    :unindent: Remove formatting indentation of follow-up text lines?
               Cf. `append_text()`.
               TODO: do we need an "unindent" configuration setting?

    Return a `docutils.nodes.Element` instance.

    Internal.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.docutils_xml.element2node', 'element2node(element, document=None, unindent=True)', {'utils': utils, 'frontend': frontend, 'Parser': Parser, 'nodes': nodes, 'Unknown': Unknown, 'append_text': append_text, 'element2node': element2node, 'element': element, 'document': document, 'unindent': unindent}, 1)

def append_text(node, text, unindent) -> None:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.parsers.docutils_xml.append_text', 'append_text(node, text, unindent)', {'re': re, 'nodes': nodes, 'node': node, 'text': text, 'unindent': unindent}, 1)


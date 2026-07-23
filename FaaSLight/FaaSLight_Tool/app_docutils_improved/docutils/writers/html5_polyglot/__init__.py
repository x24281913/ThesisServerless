"""
Plain HyperText Markup Language document tree Writer.

The output conforms to the `HTML 5` specification.

The cascading style sheet "minimal.css" is required for proper viewing,
the style sheet "plain.css" improves reading experience.
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
from pathlib import Path
from docutils import frontend, nodes
from docutils.writers import _html_base


class Writer(_html_base.Writer):
    supported = ('html5', 'xhtml', 'html')
    'Formats this writer supports.'
    default_stylesheets = ['minimal.css', 'plain.css']
    default_stylesheet_dirs = ['.', str(Path(__file__).parent)]
    default_template = Path(__file__).parent / 'template.txt'
    settings_spec = frontend.filter_settings_spec(_html_base.Writer.settings_spec, template=(f'Template file. (UTF-8 encoded, default: "{default_template}")', ['--template'], {'default': default_template, 'metavar': '<file>'}), stylesheet_path=('Comma separated list of stylesheet paths. Relative paths are expanded if a matching file is found in the --stylesheet-dirs. With --link-stylesheet, the path is rewritten relative to the output HTML file. (default: "%s")' % ','.join(default_stylesheets), ['--stylesheet-path'], {'metavar': '<file[,file,...]>', 'overrides': 'stylesheet', 'validator': frontend.validate_comma_separated_list, 'default': default_stylesheets}), stylesheet_dirs=('Comma-separated list of directories where stylesheets are found. Used by --stylesheet-path when expanding relative path arguments. (default: "%s")' % ','.join(default_stylesheet_dirs), ['--stylesheet-dirs'], {'metavar': '<dir[,dir,...]>', 'validator': frontend.validate_comma_separated_list, 'default': default_stylesheet_dirs}), initial_header_level=('Specify the initial header level. Does not affect document title & subtitle (see --no-doc-title). (default: 2 for "<h2>")', ['--initial-header-level'], {'choices': '1 2 3 4 5 6 auto'.split(), 'default': '2', 'metavar': '<level>'}), no_xml_declaration=('Omit the XML declaration (default).', ['--no-xml-declaration'], {'dest': 'xml_declaration', 'action': 'store_false'}))
    settings_spec = settings_spec + ('HTML5 Writer Options', '', ((frontend.SUPPRESS_HELP, ['--embed-images'], {'action': 'store_true', 'validator': frontend.validate_boolean}), (frontend.SUPPRESS_HELP, ['--link-images'], {'dest': 'embed_images', 'action': 'store_false'}), ('Suggest at which point images should be loaded: "embed", "link" (default), or "lazy".', ['--image-loading'], {'metavar': '<strategy>', 'choices': ('embed', 'link', 'lazy')}), ('Append a self-link to section headings.', ['--section-self-link'], {'default': False, 'action': 'store_true'}), ('Do not append a self-link to section headings. (default)', ['--no-section-self-link'], {'dest': 'section_self_link', 'action': 'store_false'})))
    config_section = 'html5 writer'
    
    def __init__(self) -> None:
        self.parts = {}
        self.translator_class = HTMLTranslator



class HTMLTranslator(_html_base.HTMLTranslator):
    """
    This writer generates `polyglot markup`: HTML5 that is also valid XML.

    Safe subclassing: when overriding, treat ``visit_*`` and ``depart_*``
    methods as a unit to prevent breaks due to internal changes. See the
    docstring of docutils.writers._html_base.HTMLTranslator for details
    and examples.
    """
    documenttag_args = {'tagname': 'main'}
    
    def __init__(self, document) -> None:
        super().__init__(document)
        self.meta.append('<meta name="viewport" content="width=device-width, initial-scale=1" />\n')
    
    def visit_acronym(self, node) -> None:
        self.body.append(self.starttag(node, 'abbr', ''))
    
    def depart_acronym(self, node) -> None:
        self.body.append('</abbr>')
    
    def visit_authors(self, node) -> None:
        self.visit_docinfo_item(node, 'authors', meta=False)
        for subnode in node:
            self.meta.append(f'<meta name="author" content="{self.attval(subnode.astext())}" />\n')
    
    def depart_authors(self, node) -> None:
        self.depart_docinfo_item()
    
    def visit_caption(self, node) -> None:
        if isinstance(node.parent, nodes.figure):
            self.body.append(self.starttag(node, 'figcaption'))
        self.body.append('<p>')
    
    def depart_caption(self, node) -> None:
        self.body.append('</p>\n')
    supported_block_tags = {'ins', 'del'}
    
    def visit_container(self, node) -> None:
        classes = node['classes']
        tags = [cls for cls in classes if cls in self.supported_block_tags]
        if len(tags) == 1:
            node.html5tagname = tags[0]
            classes.remove(tags[0])
        else:
            node.html5tagname = 'div'
        self.body.append(self.starttag(node, node.html5tagname, CLASS='docutils container'))
    
    def depart_container(self, node) -> None:
        self.body.append(f'</{node.html5tagname}>\n')
        del node.html5tagname
    
    def visit_copyright(self, node) -> None:
        self.visit_docinfo_item(node, 'copyright', meta=False)
        self.meta.append(f'<meta name="dcterms.rights" content="{self.attval(node.astext())}" />\n')
    
    def depart_copyright(self, node) -> None:
        self.depart_docinfo_item()
    
    def visit_date(self, node) -> None:
        self.visit_docinfo_item(node, 'date', meta=False)
        self.meta.append(f'<meta name="dcterms.date" content="{self.attval(node.astext())}" />\n')
    
    def depart_date(self, node) -> None:
        self.depart_docinfo_item()
    
    def visit_figure(self, node) -> None:
        atts = {}
        if 'width' in node:
            atts['style'] = f"width: {node['width']}"
        if node.get('align'):
            atts['class'] = f"align-{node['align']}"
        self.body.append(self.starttag(node, 'figure', **atts))
    
    def depart_figure(self, node) -> None:
        if len(node) > 1:
            self.body.append('</figcaption>\n')
        self.body.append('</figure>\n')
    
    def visit_footer(self, node) -> None:
        self.context.append(len(self.body))
    
    def depart_footer(self, node) -> None:
        start = self.context.pop()
        footer = [self.starttag(node, 'footer')]
        footer.extend(self.body[start:])
        footer.append('</footer>\n')
        self.footer.extend(footer)
        self.body_suffix[:0] = footer
        del self.body[start:]
    
    def visit_header(self, node) -> None:
        self.context.append(len(self.body))
    
    def depart_header(self, node) -> None:
        start = self.context.pop()
        header = [self.starttag(node, 'header')]
        header.extend(self.body[start:])
        header.append('</header>\n')
        self.body_prefix.extend(header)
        self.header.extend(header)
        del self.body[start:]
    supported_inline_tags = {'code', 'kbd', 'dfn', 'samp', 'var', 'bdi', 'del', 'ins', 'mark', 'small', 'b', 'i', 'q', 's', 'u'}
    
    def visit_inline(self, node) -> None:
        classes = node['classes']
        node.html5tagname = 'span'
        if ((isinstance(node.parent, nodes.literal_block) and 'code' in node.parent.get('classes')) or (isinstance(node.parent, nodes.literal) and getattr(node.parent, 'html5tagname', None) == 'code')):
            if classes == ['ln']:
                if self.body[-1] == '<code>':
                    del self.body[-1]
                else:
                    self.body.append('</code>')
                node.html5tagname = 'small'
        else:
            tags = [cls for cls in self.supported_inline_tags if cls in classes]
            if len(tags):
                node.html5tagname = tags[0]
                classes.remove(node.html5tagname)
        self.body.append(self.starttag(node, node.html5tagname, ''))
    
    def depart_inline(self, node) -> None:
        self.body.append(f'</{node.html5tagname}>')
        if (node.html5tagname == 'small' and node.get('classes') == ['ln'] and isinstance(node.parent, nodes.literal_block)):
            self.body.append(f'<code data-lineno="{node.astext()}">')
        del node.html5tagname
    
    def visit_legend(self, node) -> None:
        if not isinstance(node.previous_sibling(), nodes.caption):
            self.body.append('<figcaption>\n')
        self.body.append(self.starttag(node, 'div', CLASS='legend'))
    
    def depart_legend(self, node) -> None:
        self.body.append('</div>\n')
    
    def visit_literal(self, node):
        classes = node['classes']
        html5tagname = 'span'
        tags = [cls for cls in self.supported_inline_tags if cls in classes]
        if len(tags):
            html5tagname = tags[0]
            classes.remove(html5tagname)
        if html5tagname == 'code':
            node.html5tagname = html5tagname
            self.body.append(self.starttag(node, html5tagname, ''))
            return
        self.body.append(self.starttag(node, html5tagname, '', CLASS='docutils literal'))
        text = node.astext()
        if not isinstance(node.parent, nodes.literal_block):
            text = text.replace('\n', ' ')
        for token in self.words_and_spaces.findall(text):
            if (token.strip() and self.in_word_wrap_point.search(token)):
                self.body.append(f'<span class="pre">{self.encode(token)}</span>')
            else:
                self.body.append(self.encode(token))
        self.body.append(f'</{html5tagname}>')
        raise nodes.SkipNode
    
    def depart_literal(self, node) -> None:
        self.depart_inline(node)
    
    def visit_meta(self, node) -> None:
        if node.hasattr('lang'):
            node['xml:lang'] = node['lang']
        self.meta.append(self.emptytag(node, 'meta', **node.non_default_attributes()))
    
    def depart_meta(self, node) -> None:
        pass
    
    def visit_organization(self, node) -> None:
        self.visit_docinfo_item(node, 'organization', meta=False)
    
    def depart_organization(self, node) -> None:
        self.depart_docinfo_item()
    
    def visit_section(self, node) -> None:
        self.section_level += 1
        self.body.append(self.starttag(node, 'section'))
    
    def depart_section(self, node) -> None:
        self.section_level -= 1
        self.body.append('</section>\n')
    
    def visit_sidebar(self, node) -> None:
        self.body.append(self.starttag(node, 'aside', CLASS='sidebar'))
        self.in_sidebar = True
    
    def depart_sidebar(self, node) -> None:
        self.body.append('</aside>\n')
        self.in_sidebar = False
    
    def visit_topic(self, node) -> None:
        atts = {'classes': ['topic']}
        if 'contents' in node['classes']:
            node.html5tagname = 'nav'
            del atts['classes']
            if isinstance(node.parent, nodes.document):
                atts['role'] = 'doc-toc'
                self.body_prefix[0] = '</head>\n<body class="with-toc">\n'
        elif 'abstract' in node['classes']:
            node.html5tagname = 'div'
            atts['role'] = 'doc-abstract'
        elif 'dedication' in node['classes']:
            node.html5tagname = 'div'
            atts['role'] = 'doc-dedication'
        else:
            node.html5tagname = 'aside'
        self.body.append(self.starttag(node, node.html5tagname, **atts))
    
    def depart_topic(self, node) -> None:
        self.body.append(f'</{node.html5tagname}>\n')
        del node.html5tagname
    
    def section_title_tags(self, node):
        (start_tag, close_tag) = super().section_title_tags(node)
        ids = node.parent['ids']
        if (ids and getattr(self.settings, 'section_self_link', None) and not isinstance(node.parent, nodes.document)):
            self_link = f'<a class="self-link" title="link to this section" href="#{ids[-1]}"></a>'
            close_tag = close_tag.replace('</h', self_link + '</h')
        return (start_tag, close_tag)



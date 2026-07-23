"""
XeLaTeX document tree Writer.

A variant of Docutils' standard 'latex2e' writer producing LaTeX output
suited for processing with the Unicode-aware TeX engines
LuaTeX and XeTeX.
"""

from __future__ import annotations
__docformat__ = 'reStructuredText'
from docutils import frontend
from docutils.writers import latex2e
from docutils.writers.latex2e import PreambleCmds


class Writer(latex2e.Writer):
    """A writer for Unicode-aware LaTeX variants (XeTeX, LuaTeX)"""
    supported = ('latex', 'tex', 'xetex', 'xelatex', 'luatex', 'lualatex')
    'Formats this writer supports.'
    default_template = 'xelatex.tex'
    default_preamble = '% Linux Libertine (free, wide coverage, not only for Linux)\n\\setmainfont{Linux Libertine O}\n\\setsansfont{Linux Biolinum O}\n\\setmonofont[HyphenChar=None,Scale=MatchLowercase]{DejaVu Sans Mono}'
    config_section = 'xetex writer'
    config_section_dependencies = ('writers', 'latex writers')
    settings_spec = frontend.filter_settings_spec(latex2e.Writer.settings_spec, 'font_encoding', template=('Template file. Default: "%s".' % default_template, ['--template'], {'default': default_template, 'metavar': '<file>'}), latex_preamble=('Customization by LaTeX code in the preamble. Default: select "Linux Libertine" fonts.', ['--latex-preamble'], {'metavar': '<preamble>', 'default': default_preamble}))
    
    def __init__(self) -> None:
        latex2e.Writer.__init__(self)
        self.settings_defaults.update({'fontencoding': ''})
        self.translator_class = XeLaTeXTranslator



class Babel(latex2e.Babel):
    """Language specifics for XeTeX.

    Use `polyglossia` instead of `babel` and adapt settings.
    """
    language_codes = latex2e.Babel.language_codes.copy()
    language_codes.update({'cop': 'coptic', 'de': 'german', 'de-1901': 'ogerman', 'dv': 'divehi', 'dsb': 'lsorbian', 'el-polyton': 'polygreek', 'fa': 'farsi', 'grc': 'ancientgreek', 'ko': 'korean', 'hsb': 'usorbian', 'sh-Cyrl': 'serbian', 'sh-Latn': 'croatian', 'sq': 'albanian', 'sr': 'serbian', 'th': 'thai', 'vi': 'vietnamese'})
    language_codes = {k.lower(): v for (k, v) in language_codes.items()}
    for key in ('af', 'de-AT', 'de-AT-1901', 'en-CA', 'en-GB', 'en-NZ', 'en-US', 'fr-CA', 'grc-ibycus', 'sr-Latn'):
        del language_codes[key.lower()]
    warn_msg = 'Language "%s" not supported by LaTeX (polyglossia)'
    
    def __init__(self, language_code, reporter) -> None:
        self.language_code = language_code
        self.reporter = reporter
        self.language = self.language_name(language_code)
        self.otherlanguages = {}
        self.warn_msg = 'Language "%s" not supported by Polyglossia.'
        self.quote_index = 0
        self.quotes = ('"', '"')
        self.literal_double_quote = '"'
    
    def __call__(self):
        setup = ['\\usepackage{polyglossia}', '\\setdefaultlanguage{%s}' % self.language]
        if self.otherlanguages:
            setup.append('\\setotherlanguages{%s}' % ','.join(sorted(self.otherlanguages.keys())))
        return '\n'.join(setup)



class XeLaTeXTranslator(latex2e.LaTeXTranslator):
    """
    Generate code for LaTeX using Unicode fonts (XeLaTex or LuaLaTeX).

    See the docstring of docutils.writers._html_base.HTMLTranslator for
    notes on and examples of safe subclassing.
    """
    
    def __init__(self, document) -> None:
        self.is_xetex = True
        latex2e.LaTeXTranslator.__init__(self, document, Babel)
        if self.latex_encoding == 'utf8':
            self.requirements.pop('_inputenc', None)
        else:
            self.requirements['_inputenc'] = '\\XeTeXinputencoding %s ' % self.latex_encoding
    
    def to_latex_length(self, length_str: str, node=None) -> str:
        """Convert "measure" `length_str` to LaTeX length specification.

        XeTeX does not know the length unit px.
        Use ``\pdfpxdimen``, the macro holding the value of 1 px in pdfTeX.
        This way, configuring works the same for pdftex and xetex.
        """
        length_str = super().to_latex_length(length_str, node)
        if length_str.endswith('px'):
            if not self.fallback_stylesheet:
                self.fallbacks['_providelength'] = PreambleCmds.providelength
            self.fallbacks['px'] = '\n\\DUprovidelength{\\pdfpxdimen}{1bp}'
            return length_str.replace('px', '\\pdfpxdimen')
        return length_str



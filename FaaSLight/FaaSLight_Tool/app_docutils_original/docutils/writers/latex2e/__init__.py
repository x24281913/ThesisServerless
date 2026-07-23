"""LaTeX2e document tree Writer."""

from __future__ import annotations
__docformat__ = 'reStructuredText'
import re
import string
import warnings
from pathlib import Path
from docutils import frontend, nodes, languages, writers, utils
from docutils.transforms import references, writer_aux
from docutils.utils._roman_numerals import RomanNumeral
from docutils.utils.math import pick_math_environment, unichar2tex
LATEX_WRITER_DIR = Path(__file__).parent


class Writer(writers.Writer):
    supported = ('latex', 'latex2e')
    'Formats this writer supports.'
    default_template = 'default.tex'
    default_template_path = LATEX_WRITER_DIR
    default_preamble = '% PDF Standard Fonts\n\\usepackage{mathptmx} % Times\n\\usepackage[scaled=.90]{helvet}\n\\usepackage{courier}'
    table_style_values = ['booktabs', 'borderless', 'colwidths-auto', 'nolines', 'standard']
    settings_spec = ('LaTeX-Specific Options', None, (('Specify LaTeX documentclass.  Default: "article".', ['--documentclass'], {'metavar': '<documentclass>', 'default': 'article'}), ('Specify document options.  Multiple options can be given, separated by commas.  Default: "a4paper".', ['--documentoptions'], {'metavar': '<options>', 'default': 'a4paper'}), ('Format for footnote references: one of "superscript" or "brackets".  Default: "superscript".', ['--footnote-references'], {'choices': ['superscript', 'brackets'], 'default': 'superscript', 'metavar': '<format>', 'overrides': 'trim_footnote_reference_space'}), ('Use \\cite command for citations. (future default)', ['--use-latex-citations'], {'default': None, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Use figure floats for citations (might get mixed with real figures). (provisional default)', ['--figure-citations'], {'dest': 'use_latex_citations', 'action': 'store_false', 'validator': frontend.validate_boolean}), ('Format for block quote attributions: one of "dash" (em-dash prefix), "parentheses"/"parens", or "none".  Default: "dash".', ['--attribution'], {'choices': ['dash', 'parentheses', 'parens', 'none'], 'default': 'dash', 'metavar': '<format>'}), ('Specify LaTeX packages/stylesheets. A style is referenced with "\\usepackage" if extension is ".sty" or omitted and with "\\input" else.  Overrides previous --stylesheet and --stylesheet-path settings.', ['--stylesheet'], {'default': '', 'metavar': '<file[,file,...]>', 'overrides': 'stylesheet_path', 'validator': frontend.validate_comma_separated_list}), ('Comma separated list of LaTeX packages/stylesheets. Relative paths are expanded if a matching file is found in the --stylesheet-dirs. With --link-stylesheet, the path is rewritten relative to the output *.tex file. ', ['--stylesheet-path'], {'metavar': '<file[,file,...]>', 'overrides': 'stylesheet', 'validator': frontend.validate_comma_separated_list}), ('Link to the stylesheet(s) in the output file. (default)', ['--link-stylesheet'], {'dest': 'embed_stylesheet', 'action': 'store_false'}), ('Embed the stylesheet(s) in the output file. Stylesheets must be accessible during processing. ', ['--embed-stylesheet'], {'default': False, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Comma-separated list of directories where stylesheets are found. Used by --stylesheet-path when expanding relative path arguments. Default: ".".', ['--stylesheet-dirs'], {'metavar': '<dir[,dir,...]>', 'validator': frontend.validate_comma_separated_list, 'default': ['.']}), ('Customization by LaTeX code in the preamble. Default: select PDF standard fonts (Times, Helvetica, Courier).', ['--latex-preamble'], {'metavar': '<preamble>', 'default': default_preamble}), ('Specify the template file. Default: "%s".' % default_template, ['--template'], {'default': default_template, 'metavar': '<file>'}), ('Table of contents by LaTeX. (default)', ['--use-latex-toc'], {'default': True, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Table of contents by Docutils (without page numbers).', ['--use-docutils-toc'], {'dest': 'use_latex_toc', 'action': 'store_false', 'validator': frontend.validate_boolean}), ('Add parts on top of the section hierarchy.', ['--use-part-section'], {'default': False, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Attach author and date to the document info table. (default)', ['--use-docutils-docinfo'], {'dest': 'use_latex_docinfo', 'action': 'store_false', 'validator': frontend.validate_boolean}), ('Attach author and date to the document title.', ['--use-latex-docinfo'], {'default': False, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Typeset abstract as topic. (default)', ['--topic-abstract'], {'dest': 'use_latex_abstract', 'action': 'store_false', 'validator': frontend.validate_boolean}), ("Use LaTeX abstract environment for the document's abstract.", ['--use-latex-abstract'], {'default': False, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Color of any hyperlinks embedded in text. Default: "blue" (use "false" to disable).', ['--hyperlink-color'], {'metavar': '<color>', 'default': 'blue'}), ('Additional options to the "hyperref" package.', ['--hyperref-options'], {'metavar': '<options>', 'default': ''}), ('Enable compound enumerators for nested enumerated lists (e.g. "1.2.a.ii").', ['--compound-enumerators'], {'default': False, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Disable compound enumerators for nested enumerated lists. (default)', ['--no-compound-enumerators'], {'action': 'store_false', 'dest': 'compound_enumerators'}), ('Enable section ("." subsection ...) prefixes for compound enumerators.  This has no effect without --compound-enumerators.', ['--section-prefix-for-enumerators'], {'default': None, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Disable section prefixes for compound enumerators. (default)', ['--no-section-prefix-for-enumerators'], {'action': 'store_false', 'dest': 'section_prefix_for_enumerators'}), ('Set the separator between section number and enumerator for compound enumerated lists.  Default: "-".', ['--section-enumerator-separator'], {'default': '-', 'metavar': '<char>'}), ('When possible, use the specified environment for literal-blocks. Default: "" (fall back to "alltt").', ['--literal-block-env'], {'metavar': '<environment>', 'default': ''}), (frontend.SUPPRESS_HELP, ['--use-verbatim-when-possible'], {'action': 'store_true', 'validator': frontend.validate_boolean}), ('Table style. "standard" with horizontal and vertical lines, "booktabs" (LaTeX booktabs style) only horizontal lines above and below the table and below the header, or "borderless". Default: "standard"', ['--table-style'], {'default': ['standard'], 'metavar': '<format>', 'action': 'append', 'validator': frontend.validate_comma_separated_list, 'choices': table_style_values}), ('LaTeX graphicx package option. Default: "".', ['--graphicx-option'], {'metavar': '<option>', 'default': ''}), ('LaTeX font encoding. Possible values are "", "T1" (default), "OT1", "LGR,T1" or any other combination of options to the `fontenc` package. ', ['--font-encoding'], {'metavar': '<encoding>', 'default': 'T1'}), ('Per default the latex-writer puts the reference title into hyperreferences. Specify "ref" or "pageref" to get the section number or the page number.', ['--reference-label'], {'metavar': '<command name>', 'default': ''}), ('Specify style and database(s) for bibtex, for example "--use-bibtex=unsrt,mydb1,mydb2". Provisional!', ['--use-bibtex'], {'default': '', 'metavar': '<style,bibfile[,bibfile,...]>', 'validator': frontend.validate_comma_separated_list}), ('Use legacy functions with class value list for \\DUtitle and \\DUadmonition.', ['--legacy-class-functions'], {'default': False, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Use \\DUrole and "DUclass" wrappers for class values. Place admonition content in an environment. (default)', ['--new-class-functions'], {'dest': 'legacy_class_functions', 'action': 'store_false', 'validator': frontend.validate_boolean}), ('Use legacy algorithm to determine table column widths. (provisional default)', ['--legacy-column-widths'], {'default': None, 'action': 'store_true', 'validator': frontend.validate_boolean}), ('Use new algorithm to determine table column widths. (future default)', ['--new-column-widths'], {'dest': 'legacy_column_widths', 'action': 'store_false', 'validator': frontend.validate_boolean}), ('Footnotes with numbers/symbols by Docutils. (default)', ['--docutils-footnotes'], {'dest': 'latex_footnotes', 'action': 'store_false', 'validator': frontend.validate_boolean}), ('Footnotes with numbers by LaTeX.', ['--latex-footnotes'], {'action': 'store_true', 'default': False, 'validator': frontend.validate_boolean})))
    relative_path_settings = ('template', )
    settings_defaults = {}
    config_section = 'latex2e writer'
    config_section_dependencies = ('writers', 'latex writers')
    head_parts = ('head_prefix', 'requirements', 'latex_preamble', 'stylesheet', 'fallbacks', 'pdfsetup', 'titledata')
    visitor_attributes = head_parts + ('title', 'subtitle', 'body_pre_docinfo', 'docinfo', 'dedication', 'abstract', 'body')
    output = None
    'Final translated form of `document`.'
    
    def __init__(self) -> None:
        writers.Writer.__init__(self)
        self.translator_class = LaTeXTranslator
    
    def get_transforms(self):
        return super().get_transforms() + [writer_aux.Admonitions, references.CitationReferences]
    
    def translate(self) -> None:
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        for part in self.visitor_attributes:
            setattr(self, part, getattr(visitor, part))
        self.assemble_parts()
        self.output = string.Template(self.parts['template']).substitute(self.parts)
    
    def assemble_parts(self) -> None:
        """Assemble the `self.parts` dictionary of output fragments."""
        super().assemble_parts()
        for part in self.visitor_attributes:
            if part in self.parts:
                continue
            lines = getattr(self, part)
            if part in self.head_parts:
                if lines:
                    lines.append('')
                self.parts[part] = '\n'.join(lines)
            else:
                self.parts[part] = ''.join(lines)
        templatepath = Path(self.document.settings.template)
        if not templatepath.exists():
            templatepath = self.default_template_path / templatepath.name
        self.parts['template'] = templatepath.read_text(encoding='utf-8')



class Babel:
    """Language specifics for LaTeX."""
    language_codes = {'af': 'afrikaans', 'ar': 'arabic', 'bg': 'bulgarian', 'br': 'breton', 'ca': 'catalan', 'cs': 'czech', 'cy': 'welsh', 'da': 'danish', 'de': 'ngerman', 'de-1901': 'german', 'de-AT': 'naustrian', 'de-AT-1901': 'austrian', 'dsb': 'lowersorbian', 'el': 'greek', 'el-polyton': 'polutonikogreek', 'en': 'english', 'en-AU': 'australian', 'en-CA': 'canadian', 'en-GB': 'british', 'en-NZ': 'newzealand', 'en-US': 'american', 'eo': 'esperanto', 'es': 'spanish', 'et': 'estonian', 'eu': 'basque', 'fi': 'finnish', 'fr': 'french', 'fr-CA': 'canadien', 'ga': 'irish', 'grc-ibycus': 'ibycus', 'gl': 'galician', 'he': 'hebrew', 'hr': 'croatian', 'hsb': 'uppersorbian', 'hu': 'magyar', 'ia': 'interlingua', 'id': 'bahasai', 'is': 'icelandic', 'it': 'italian', 'ja': 'japanese', 'kk': 'kazakh', 'la': 'latin', 'lt': 'lithuanian', 'lv': 'latvian', 'mn': 'mongolian', 'ms': 'bahasam', 'nb': 'norsk', 'nl': 'dutch', 'nn': 'nynorsk', 'no': 'norsk', 'pl': 'polish', 'pt': 'portuges', 'pt-BR': 'brazil', 'ro': 'romanian', 'ru': 'russian', 'se': 'samin', 'sh-Cyrl': 'serbianc', 'sh-Latn': 'serbian', 'sk': 'slovak', 'sl': 'slovene', 'sq': 'albanian', 'sr': 'serbianc', 'sr-Latn': 'serbian', 'sv': 'swedish', 'tr': 'turkish', 'uk': 'ukrainian', 'vi': 'vietnam'}
    language_codes = {k.lower(): v for (k, v) in language_codes.items()}
    warn_msg = 'Language "%s" not supported by LaTeX (babel)'
    active_chars = {'galician': '.<>', 'spanish': '.<>'}
    
    def __init__(self, language_code, reporter=None) -> None:
        self.reporter = reporter
        self.language = self.language_name(language_code)
        self.otherlanguages = {}
    
    def __call__(self):
        """Return the babel call with correct options and settings"""
        languages = sorted(self.otherlanguages.keys())
        if languages:
            languages.append(f"main={(self.language or 'english')}")
        else:
            languages.append((self.language or 'english'))
        self.setup = ['\\usepackage[%s]{babel}' % ','.join(languages)]
        shorthands = []
        for c in ''.join((self.active_chars.get(lng, '') for lng in languages)):
            if c not in shorthands:
                shorthands.append(c)
        if shorthands:
            self.setup.append('\\AtBeginDocument{\\shorthandoff{%s}}' % ''.join(shorthands))
        if 'galician' in languages:
            self.setup.append('\\deactivatetilden % restore ~ in Galician')
        if 'estonian' in languages:
            self.setup.extend(['\\makeatletter', '  \\addto\\extrasestonian{\\bbl@deactivate{~}}', '\\makeatother'])
        if 'basque' in languages:
            self.setup.extend(['\\makeatletter', '  \\addto\\extrasbasque{\\bbl@deactivate{~}}', '\\makeatother'])
        if (languages[-1] == 'main=english' and 'french' in self.otherlanguages.keys()):
            self.setup += ['% Prevent side-effects if French hyphenation patterns are not loaded:', '\\frenchbsetup{StandardLayout}', '\\AtBeginDocument{\\selectlanguage{%s}\\noextrasfrench}' % self.language]
        return '\n'.join(self.setup)
    
    def language_name(self, language_code):
        """Return TeX language name for `language_code`"""
        for tag in utils.normalize_language_tag(language_code):
            try:
                return self.language_codes[tag]
            except KeyError:
                pass
        if self.reporter is not None:
            self.reporter.warning(self.warn_msg % language_code)
        return ''
    
    def get_language(self):
        return self.language



class SortableDict(dict):
    """Dictionary with additional sorting methods

    Deprecated. Will be removed in Docutils 0.24.
    """
    
    def __init__(self, *args, **kwargs):
        warnings.warn('`writers.latex2e.SortableDict` is obsolete and will be removed in Docutils 0.24.', DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
    
    def sortedkeys(self):
        """Return sorted list of keys"""
        return sorted(self.keys())
    
    def sortedvalues(self):
        """Return list of values sorted by keys"""
        return [self[key] for key in self.sortedkeys()]



class PreambleCmds:
    """Building blocks for the latex preamble."""
    

PreambleCmds.ch = '\n\\ifdefined\\DUchdimen  % lengh unit "ch": width of a zero char\n\\else\n  \\newlength{\\DUchdimen}\n  \\AtBeginDocument{\\settowidth\\DUchdimen{0}}  % set after font setup,\n  % update with font changes (requires LaTeX > 2021-06-01, see lthooks-doc.pdf)\n  \\AddToHook{cmd/selectfont/after}{\\settowidth\\DUchdimen{0}}\n\\fi'
PreambleCmds.color = '\\usepackage{color}'
PreambleCmds.float = '\\usepackage{float} % extended float configuration\n\\floatplacement{figure}{H} % place figures here definitely'
PreambleCmds.linking = '%% hyperlinks:\n\\ifdefined\\hypersetup\n\\else\n  \\usepackage[%s]{hyperref}\n  \\usepackage{bookmark}\n  \\urlstyle{same} %% normal text font (alternatives: tt, rm, sf)\n\\fi'
PreambleCmds.minitoc = '%% local table of contents\n\\usepackage{minitoc}'
PreambleCmds.table = '\\usepackage{longtable,ltcaption,array}\n\\setlength{\\extrarowheight}{2pt}\n\\newlength{\\DUtablewidth} % internal use in tables'
PreambleCmds.table_columnwidth = '\\newcommand{\\DUcolumnwidth}[1]{\\dimexpr#1\\DUtablewidth-2\\tabcolsep\\relax}'
PreambleCmds.textcomp = '\\usepackage{textcomp} % text symbol macros'
PreambleCmds.abstract_legacy = '\n% abstract title\n\\providecommand*{\\DUtitleabstract}[1]{\\centerline{\\textbf{#1}}}'
PreambleCmds.admonition_legacy = '\n% admonition (specially marked topic)\n\\providecommand{\\DUadmonition}[2][class-arg]{%\n  % try \\DUadmonition#1{#2}:\n  \\ifcsname DUadmonition#1\\endcsname%\n    \\csname DUadmonition#1\\endcsname{#2}%\n  \\else\n    \\begin{center}\n      \\fbox{\\parbox{0.9\\linewidth}{#2}}\n    \\end{center}\n  \\fi\n}'
PreambleCmds.error_legacy = '\n% error admonition title\n\\providecommand*{\\DUtitleerror}[1]{\\DUtitle{\\color{red}#1}}'
PreambleCmds.title_legacy = '\n% title for topics, admonitions, unsupported section levels, and sidebar\n\\providecommand*{\\DUtitle}[2][class-arg]{%\n  % call \\DUtitle#1{#2} if it exists:\n  \\ifcsname DUtitle#1\\endcsname%\n    \\csname DUtitle#1\\endcsname{#2}%\n  \\else\n    \\smallskip\\noindent\\textbf{#2}\\smallskip%\n  \\fi\n}'
PreambleCmds.toc_list = '\n\\providecommand*{\\DUCLASScontents}{%\n  \\renewenvironment{itemize}%\n    {\\begin{list}{}{\\setlength{\\partopsep}{0pt}\n                    \\setlength{\\parsep}{0pt}}\n                   }%\n    {\\end{list}}%\n}'
PreambleCmds.ttem = '\n% character width in monospaced font\n\\newlength{\\ttemwidth}\n\\settowidth{\\ttemwidth}{\\ttfamily M}'

def _read_block(fp):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.writers.latex2e.__init__._read_block', '_read_block(fp)', {'fp': fp}, 1)
with open(LATEX_WRITER_DIR / 'docutils.sty', encoding='utf-8') as fp:
    for line in fp:
        line = line.strip('% \n')
        if not line.endswith('::'):
            continue
        block_name = line.rstrip(':')
        if not block_name:
            continue
        definitions = _read_block(fp)
        if block_name in ('color', 'float', 'table', 'textcomp'):
            definitions = definitions.strip()
        setattr(PreambleCmds, block_name, definitions)


class CharMaps:
    """LaTeX representations for active and Unicode characters."""
    alltt = {ord('\\'): '\\textbackslash{}', ord('{'): '\\{', ord('}'): '\\}'}
    special = {ord('#'): '\\#', ord('$'): '\\$', ord('%'): '\\%', ord('&'): '\\&', ord('~'): '\\textasciitilde{}', ord('_'): '\\_', ord('^'): '\\textasciicircum{}', ord('"'): '\\textquotedbl{}', ord('['): '{[}', ord(']'): '{]}', 173: '\\-'}
    unsupported_unicode = {8192: '\\enskip', 8193: '\\quad', 8194: '\\enskip', 8195: '\\quad', 8200: '\\,', 8203: '\\hspace{0pt}', 8239: '\\,', 8209: '\\hbox{-}', 8491: '\\AA', 8660: '\\ensuremath{\\Leftrightarrow}', 8800: '\\ensuremath{\\neq}', 8801: '\\ensuremath{\\equiv}', 8804: '\\ensuremath{\\le}', 8805: '\\ensuremath{\\ge}', 9824: '\\ensuremath{\\spadesuit}', 9827: '\\ensuremath{\\clubsuit}', 64256: 'ff', 64257: 'fi', 64258: 'fl', 64259: 'ffi', 64260: 'ffl'}
    utf8_supported_unicode = {160: '~', 171: '\\guillemotleft{}', 187: '\\guillemotright{}', 8204: '\\textcompwordmark{}', 8211: '\\textendash{}', 8212: '\\textemdash{}', 8216: '\\textquoteleft{}', 8217: '\\textquoteright{}', 8218: '\\quotesinglbase{}', 8220: '\\textquotedblleft{}', 8221: '\\textquotedblright{}', 8222: '\\quotedblbase{}', 8240: '\\textperthousand{}', 8241: '\\textpertenthousand{}', 8249: '\\guilsinglleft{}', 8250: '\\guilsinglright{}', 9251: '\\textvisiblespace{}', 8224: '\\dag{}', 8225: '\\ddag{}', 8230: '\\dots{}', 8482: '\\texttrademark{}'}
    textcomp = {162: '\\textcent{}', 164: '\\textcurrency{}', 165: '\\textyen{}', 166: '\\textbrokenbar{}', 167: '\\textsection{}', 168: '\\textasciidieresis{}', 169: '\\textcopyright{}', 170: '\\textordfeminine{}', 172: '\\textlnot{}', 174: '\\textregistered{}', 175: '\\textasciimacron{}', 176: '\\textdegree{}', 177: '\\textpm{}', 178: '\\texttwosuperior{}', 179: '\\textthreesuperior{}', 180: '\\textasciiacute{}', 181: '\\textmu{}', 182: '\\textparagraph{}', 185: '\\textonesuperior{}', 186: '\\textordmasculine{}', 188: '\\textonequarter{}', 189: '\\textonehalf{}', 190: '\\textthreequarters{}', 215: '\\texttimes{}', 247: '\\textdiv{}', 402: '\\textflorin{}', 697: '\\textasciiacute{}', 698: '\\textacutedbl{}', 8214: '\\textbardbl{}', 8226: '\\textbullet{}', 8242: '\\textasciiacute{}', 8243: '\\textacutedbl{}', 8245: '\\textasciigrave{}', 8246: '\\textgravedbl{}', 8251: '\\textreferencemark{}', 8253: '\\textinterrobang{}', 8260: '\\textfractionsolidus{}', 8261: '\\textlquill{}', 8262: '\\textrquill{}', 8274: '\\textdiscount{}', 8353: '\\textcolonmonetary{}', 8355: '\\textfrenchfranc{}', 8356: '\\textlira{}', 8358: '\\textnaira{}', 8361: '\\textwon{}', 8363: '\\textdong{}', 8364: '\\texteuro{}', 8369: '\\textpeso{}', 8370: '\\textguarani{}', 8451: '\\textcelsius{}', 8470: '\\textnumero{}', 8471: '\\textcircledP{}', 8478: '\\textrecipe{}', 8480: '\\textservicemark{}', 8482: '\\texttrademark{}', 8486: '\\textohm{}', 8487: '\\textmho{}', 8494: '\\textestimated{}', 8592: '\\textleftarrow{}', 8593: '\\textuparrow{}', 8594: '\\textrightarrow{}', 8595: '\\textdownarrow{}', 8722: '\\textminus{}', 8727: '\\textasteriskcentered{}', 8730: '\\textsurd{}', 9250: '\\textblank{}', 9702: '\\textopenbullet{}', 9711: '\\textbigcircle{}', 9834: '\\textmusicalnote{}', 9901: '\\textmarried{}', 9902: '\\textdivorced{}', 10216: '\\textlangle{}', 10217: '\\textrangle{}'}
    pifont = {9829: '\\ding{170}', 9830: '\\ding{169}', 10003: '\\ding{51}', 10007: '\\ding{55}'}



class DocumentClass:
    """Details of a LaTeX document class."""
    
    def __init__(self, document_class, with_part=False) -> None:
        self.document_class = document_class
        self._with_part = with_part
        self.sections = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph']
        if (self.document_class.endswith('book') or self.document_class.endswith('report') or self.document_class in ('ctexrep', 'memoir', 'mwbk', 'mwrep', 'scrreprt')):
            self.sections.insert(0, 'chapter')
        if self._with_part:
            self.sections.insert(0, 'part')
    
    def section(self, level):
        """Return the LaTeX section name for section `level`.

        The name depends on the specific document class.
        Level is 1,2,3..., as level 0 is the title.
        """
        if level <= len(self.sections):
            return self.sections[level - 1]
        return 'DUtitle'
    
    def latex_section_depth(self, depth: int) -> int:
        """
        Return LaTeX equivalent of Docutils section level `depth`.

        Given the value of the ``:depth:`` option of the "contents" or
        "sectnum" directive, return the corresponding value for the
        LaTeX ``tocdepth`` or ``secnumdepth`` counters.

        LaTeX section depth values:
          :-1|0: part (optional, 0 with "article"-like document classes)
          :0:    chapter (missing in "article"-like document classes)
          :1:    section
          :2:    subsection
          :3:    subsubsection
          :4:    paragraph
          :5:    subparagraph
        """
        depth = min(depth, len(self.sections))
        if 'chapter' in self.sections:
            depth -= 1
        if self.sections[0] == 'part':
            depth -= 1
        return depth



class Table:
    """Manage a table while traversing.

    Table style might be

    :standard:   horizontal and vertical lines
    :booktabs:   only horizontal lines (requires "booktabs" LaTeX package)
    :borderless: no borders around table cells
    :nolines:    alias for borderless

    :colwidths-auto:  column widths determined by LaTeX
    """
    
    def __init__(self, translator, latex_type) -> None:
        self._translator = translator
        self._latex_type = latex_type
        self.legacy_column_widths = False
        self.close()
        self._colwidths = []
        self._rowspan = []
        self._in_thead = 0
    
    def open(self) -> None:
        self._open = True
        self._col_specs = []
        self.caption = []
        self._attrs = {}
        self._in_head = False
    
    def close(self) -> None:
        self._open = False
        self._col_specs = None
        self.caption = []
        self._attrs = {}
        self.stubs = []
        self.colwidths_auto = False
    
    def is_open(self):
        return self._open
    
    def set_table_style(self, node, settings) -> None:
        self.legacy_column_widths = settings.legacy_column_widths
        if 'align' in node:
            self.set('align', node['align'])
        borders = [cls.replace('nolines', 'borderless') for cls in ['standard'] + settings.table_style + node['classes'] if cls in ('standard', 'booktabs', 'borderless', 'nolines')]
        self.borders = borders[-1]
        self.colwidths_auto = ((('colwidths-auto' in node['classes'] or 'colwidths-auto' in settings.table_style)) and 'colwidths-given' not in node['classes'] and 'width' not in node)
    
    def get_latex_type(self):
        if (self._latex_type == 'longtable' and not self.caption):
            return 'longtable*'
        return self._latex_type
    
    def set(self, attr, value) -> None:
        self._attrs[attr] = value
    
    def get(self, attr):
        if attr in self._attrs:
            return self._attrs[attr]
        return None
    
    def get_vertical_bar(self) -> str:
        if self.borders == 'standard':
            return '|'
        return ''
    
    def get_opening(self, width='\\linewidth'):
        opening = []
        nr_of_cols = len(self._col_specs)
        align_map = {'left': '[l]', 'center': '[c]', 'right': '[r]', None: ''}
        align = align_map.get(self.get('align'))
        latex_type = self.get_latex_type()
        if (align and not latex_type.startswith('longtable')):
            opening.append('\\noindent\\makebox[\\linewidth]%s{%%' % align)
            align = ''
        if not self.colwidths_auto:
            if (self.borders == 'standard' and not self.legacy_column_widths):
                opening.append('\\setlength{\\DUtablewidth}{\\dimexpr%s-%i\\arrayrulewidth\\relax}%%' % (width, nr_of_cols + 1))
            else:
                opening.append('\\setlength{\\DUtablewidth}{%s}%%' % width)
        opening.append('\\begin{%s}%s' % (latex_type, align))
        return '\n'.join(opening)
    
    def get_closing(self):
        closing = []
        if self.borders == 'booktabs':
            closing.append('\\bottomrule')
        closing.append('\\end{%s}' % self.get_latex_type())
        if (self.get('align') and not self.get_latex_type().startswith('longtable')):
            closing.append('}')
        return '\n'.join(closing)
    
    def visit_colspec(self, node) -> None:
        self._col_specs.append(node)
        self.stubs.append(node.attributes.get('stub'))
    
    def get_colspecs(self, node):
        """Return column specification for longtable.
        """
        bar = self.get_vertical_bar()
        self._rowspan = [0] * len(self._col_specs)
        if self.colwidths_auto:
            self._colwidths = []
            latex_colspecs = ['l'] * len(self._col_specs)
        elif self.legacy_column_widths:
            width = 80
            factor = 0.93
            total_width = sum((node.propwidth() + 1 for node in self._col_specs))
            if total_width > width:
                factor *= width / total_width
            self._colwidths = [factor * (node.propwidth() + 1) / width + 0.005 for node in self._col_specs]
            latex_colspecs = ['p{%.3f\\DUtablewidth}' % colwidth for colwidth in self._colwidths]
        else:
            norm_length = 40
            if 'colwidths-given' not in node.parent.parent['classes']:
                allowance = 1
            else:
                allowance = 0
            self._colwidths = [(node.propwidth() + allowance) / norm_length for node in self._col_specs]
            total_width = sum(self._colwidths)
            if (total_width > 1 or 'width' in node.parent.parent.attributes):
                self._colwidths = [colwidth / total_width for colwidth in self._colwidths]
            latex_colspecs = ['p{\\DUcolumnwidth{%.3f}}' % colwidth for colwidth in self._colwidths]
        return bar + bar.join(latex_colspecs) + bar
    
    def get_column_width(self) -> str:
        """Return columnwidth for current cell (not multicell)."""
        try:
            if self.legacy_column_widths:
                return '%.2f\\DUtablewidth' % self._colwidths[self._cell_in_row]
            return '\\DUcolumnwidth{%.2f}' % self._colwidths[self._cell_in_row]
        except IndexError:
            return '*'
    
    def get_multicolumn_width(self, start, len_) -> str:
        """Return sum of columnwidths for multicell."""
        try:
            multicol_width = sum((self._colwidths[start + co] for co in range(len_)))
            if self.legacy_column_widths:
                return 'p{%.2f\\DUtablewidth}' % multicol_width
            return 'p{\\DUcolumnwidth{%.3f}}' % multicol_width
        except IndexError:
            return 'l'
    
    def need_recurse(self):
        if self._latex_type == 'longtable':
            return 1 == self._translator.thead_depth()
        return 0
    
    def visit_thead(self):
        self._in_thead += 1
        if self.borders == 'standard':
            return ['\\hline\n']
        elif self.borders == 'booktabs':
            return ['\\toprule\n']
        return []
    
    def depart_thead(self):
        a = []
        if self.borders == 'booktabs':
            a.append('\\midrule\n')
        if self._latex_type == 'longtable':
            if 1 == self._translator.thead_depth():
                a.append('\\endfirsthead\n')
            else:
                n_c = len(self._col_specs)
                a.append('\\endhead\n')
                t_width = sum((node.propwidth() + 2 for node in self._col_specs))
                if (t_width > 30 or (t_width > 12 and not self.colwidths_auto)):
                    a.append('\\multicolumn{%d}{%s}' % (n_c, self.get_multicolumn_width(0, n_c)) + '{\\raggedleft\\ldots continued on next page}\\\\' + '\n')
                a.append('\\endfoot\n\\endlastfoot\n')
        self._in_thead -= 1
        return a
    
    def visit_row(self) -> None:
        self._cell_in_row = 0
    
    def depart_row(self):
        res = [' \\\\\n']
        self._cell_in_row = None
        for i in range(len(self._rowspan)):
            if self._rowspan[i] > 0:
                self._rowspan[i] -= 1
        if self.borders == 'standard':
            rowspans = [i + 1 for i in range(len(self._rowspan)) if self._rowspan[i] <= 0]
            if len(rowspans) == len(self._rowspan):
                res.append('\\hline\n')
            else:
                cline = ''
                rowspans.reverse()
                while True:
                    try:
                        c_start = rowspans.pop()
                    except IndexError:
                        break
                    cline += '\\cline{%d-%d}\n' % (c_start, c_start)
                res.append(cline)
        return res
    
    def set_rowspan(self, cell, value) -> None:
        try:
            self._rowspan[cell] = value
        except IndexError:
            pass
    
    def get_rowspan(self, cell):
        try:
            return self._rowspan[cell]
        except IndexError:
            return 0
    
    def get_entry_number(self):
        return self._cell_in_row
    
    def visit_entry(self) -> None:
        self._cell_in_row += 1
    
    def is_stub_column(self):
        if len(self.stubs) >= self._cell_in_row:
            return self.stubs[self._cell_in_row]
        return False



class LaTeXTranslator(writers.DoctreeTranslator):
    """
    Generate code for 8-bit LaTeX from a Docutils document tree.

    See the docstring of docutils.writers._html_base.HTMLTranslator for
    notes on and examples of safe subclassing.
    """
    is_xetex = False
    compound_enumerators = False
    section_prefix_for_enumerators = False
    section_enumerator_separator = '-'
    has_latex_toc = False
    section_level = 0
    inside_citation_reference_label = False
    verbatim = False
    insert_non_breaking_blanks = False
    insert_newline = False
    literal = False
    alltt = False
    TITLEDATA_NODES = (nodes.address, nodes.author, nodes.authors, nodes.contact, nodes.date, nodes.organization)
    
    def __init__(self, document, babel_class=Babel) -> None:
        super().__init__(document)
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error
        self.refids = set()
        for node in document.findall(nodes.reference):
            if 'refid' in node:
                self.refids.add(node['refid'])
        settings = self.settings
        if (settings.use_latex_citations is None and not settings.use_bibtex):
            settings.use_latex_citations = False
            warnings.warn('The default for the setting "use_latex_citations" will change to "True" in Docutils 1.0.', FutureWarning, stacklevel=7)
        if settings.legacy_column_widths is None:
            settings.legacy_column_widths = True
            warnings.warn('The default for the setting "legacy_column_widths" will change to "False" in Docutils 1.0.)', FutureWarning, stacklevel=7)
        if settings.use_verbatim_when_possible is not None:
            warnings.warn('The configuration setting "use_verbatim_when_possible" will be removed in Docutils 2.0. Use "literal_block_env: verbatim".', FutureWarning, stacklevel=7)
        self.latex_encoding = self.to_latex_encoding(settings.output_encoding)
        self.use_latex_toc = settings.use_latex_toc
        self.use_latex_docinfo = settings.use_latex_docinfo
        self.use_latex_citations = settings.use_latex_citations
        self.reference_label = settings.reference_label
        self.hyperlink_color = settings.hyperlink_color
        self.compound_enumerators = settings.compound_enumerators
        self.font_encoding = getattr(settings, 'font_encoding', '')
        self.section_prefix_for_enumerators = settings.section_prefix_for_enumerators
        self.section_enumerator_separator = settings.section_enumerator_separator.replace('_', '\\_')
        self.literal_block_env = ''
        self.literal_block_options = ''
        if settings.literal_block_env:
            (_none, self.literal_block_env, self.literal_block_options, _none) = re.split('(\\w+)(.*)', settings.literal_block_env)
        elif settings.use_verbatim_when_possible:
            self.literal_block_env = 'verbatim'
        if settings.use_bibtex:
            self.use_latex_citations = True
        self.bibtex = settings.use_bibtex
        self.language_module = languages.get_language(settings.language_code, document.reporter)
        self.babel = babel_class(settings.language_code, document.reporter)
        self.author_separator = self.language_module.author_separators[0]
        d_options = [settings.documentoptions]
        if self.babel.language not in ('english', ''):
            d_options.append(self.babel.language)
        self.documentoptions = ','.join(filter(None, d_options))
        self.d_class = DocumentClass(settings.documentclass, settings.use_part_section)
        if settings.graphicx_option == '':
            self.graphicx_package = '\\usepackage{graphicx}'
        else:
            self.graphicx_package = '\\usepackage[%s]{graphicx}' % settings.graphicx_option
        self.latex_footnotes = settings.latex_footnotes
        self.head_prefix = [f'\\documentclass[{self.documentoptions}]{{{settings.documentclass}}}']
        self.requirements = {}
        self.latex_preamble = [settings.latex_preamble]
        self.fallbacks = {}
        self.pdfsetup = []
        self.title = []
        self.subtitle = []
        self.titledata = []
        self.body_pre_docinfo = []
        self.docinfo = []
        self.dedication = []
        self.abstract = []
        self.body = []
        self.context = []
        'Heterogeneous stack.\n\n        Used by visit_* and depart_* functions in conjunction with the tree\n        traversal. Make sure that the pops correspond to the pushes.'
        self.title_labels = []
        self.subtitle_labels = []
        self.author_stack = [['']]
        self.date = []
        self.pdfauthor = []
        self.pdfinfo = []
        if settings.language_code != 'en':
            self.pdfinfo.append('  pdflang={%s},' % settings.language_code)
        self._section_number = [0]
        self._enumeration_counters = []
        self._max_enumeration_counters = 0
        self._bibitems = []
        self.table_stack = []
        self.active_table = Table(self, 'longtable')
        self.out = self.body
        self.out_stack = []
        self.footnote_queue = []
        self.processed_footnotes = set()
        if self.latex_encoding not in ('ascii', 'unicode', 'utf8'):
            self.requirements['_inputenc'] = '\\usepackage[%s]{inputenc}' % self.latex_encoding
        if not self.is_xetex:
            if self.font_encoding:
                self.requirements['_fontenc'] = '\\usepackage[%s]{fontenc}' % self.font_encoding
            for enc in self.font_encoding.split(','):
                enc = enc.strip()
                if enc == 'OT1':
                    self.requirements['_textquotedblOT1'] = '\\DeclareTextSymbol{\\textquotedbl}{OT1}{`\\"}'
                elif enc not in ('T1', 'T2A', 'T2B', 'T2C', 'T4', 'T5'):
                    self.requirements['_textquotedbl'] = '\\DeclareTextSymbolDefault{\\textquotedbl}{T1}'
        if (not settings.documentclass.startswith('scr') and (('DIV' in self.documentoptions or 'BCOR' in self.documentoptions))):
            self.requirements['typearea'] = '\\usepackage{typearea}'
        stylesheet_list = utils.get_stylesheet_list(settings)
        self.fallback_stylesheet = 'docutils' in stylesheet_list
        if self.fallback_stylesheet:
            stylesheet_list.remove('docutils')
            if settings.legacy_class_functions:
                self.fallback_stylesheet = False
            else:
                self.fallbacks['_docutils.sty'] = '\\usepackage{docutils}[2026-05-06]'
        self.stylesheet = [self.stylesheet_call(path) for path in stylesheet_list]
        self.hyperref_options = []
        if not self.latex_footnotes:
            self.hyperref_options = ['hyperfootnotes=false']
        if self.hyperlink_color.lower() not in ('0', 'off', 'no', 'false', ''):
            self.hyperref_options.append(f'colorlinks=true,linkcolor={self.hyperlink_color},urlcolor={self.hyperlink_color}')
        if settings.hyperref_options:
            self.hyperref_options.append(settings.hyperref_options)
        self.hyperref_options = ',\n              '.join(self.hyperref_options)
    
    def stylesheet_call(self, path):
        """Return code to reference or embed stylesheet file `path`."""
        path = Path(path)
        is_package = path.suffix in ('.sty', '')
        if self.settings.embed_stylesheet:
            if is_package:
                path = path.with_suffix('.sty')
            try:
                content = path.read_text(encoding='utf-8')
            except OSError as err:
                msg = f'Cannot embed stylesheet:\n {err}'.replace('\\\\', '/')
                self.document.reporter.error(msg)
                return '% ' + msg.replace('\n', '\n% ')
            else:
                self.settings.record_dependencies.add(path.as_posix())
            if is_package:
                content = f'\\makeatletter\n{content}\n\\makeatother'
            return f'% embedded stylesheet: {path.as_posix()}\n{content}'
        if is_package:
            path = path.parent / path.stem
            cmd = '\\usepackage{%s}'
        else:
            cmd = '\\input{%s}'
        if self.settings.stylesheet_path:
            return cmd % utils.relative_path(self.settings.output_path, path)
        return cmd % path.as_posix()
    
    def to_latex_encoding(self, docutils_encoding):
        """Translate docutils encoding name into LaTeX's.

        Default method is remove "-" and "_" chars from docutils_encoding.
        """
        tr = {'iso-8859-1': 'latin1', 'iso-8859-2': 'latin2', 'iso-8859-3': 'latin3', 'iso-8859-4': 'latin4', 'iso-8859-5': 'iso88595', 'iso-8859-9': 'latin5', 'iso-8859-15': 'latin9', 'mac_cyrillic': 'maccyr', 'windows-1251': 'cp1251', 'koi8-r': 'koi8-r', 'koi8-u': 'koi8-u', 'windows-1250': 'cp1250', 'windows-1252': 'cp1252', 'us-ascii': 'ascii'}
        encoding = docutils_encoding.lower()
        encoding = encoding.split(':')[0]
        if encoding in tr:
            return tr[encoding]
        return encoding.replace('_', '').replace('-', '')
    
    def language_label(self, docutil_label):
        return self.language_module.labels[docutil_label]
    
    def encode(self, text):
        """Return text with 'problematic' characters escaped.

        * Escape the special printing characters ``# $ % & ~ _ ^ \ { }``,
          square brackets ``[ ]``, double quotes and (in OT1) ``< | >``.
        * Translate non-supported Unicode characters.
        * Separate ``-`` (and more in literal text) to prevent input ligatures.
        """
        if self.verbatim:
            return text
        table = CharMaps.alltt.copy()
        if not self.alltt:
            table.update(CharMaps.special)
        if (self.inside_citation_reference_label and not self.alltt):
            del table[ord('_')]
        if (self.font_encoding in ['OT1', ''] and not self.is_xetex):
            if self.literal:
                table[ord('_')] = '\\underline{~}'
                self.requirements['graphicx'] = self.graphicx_package
                table[ord('\\')] = '\\reflectbox{/}'
            else:
                table[ord('|')] = '\\textbar{}'
                table[ord('<')] = '\\textless{}'
                table[ord('>')] = '\\textgreater{}'
        if self.insert_non_breaking_blanks:
            table[ord(' ')] = '~'
            table[ord('\t')] = '~' * self.settings.tab_width
        if not self.is_xetex:
            if not self.latex_encoding.startswith('utf8'):
                table.update(CharMaps.unsupported_unicode)
                table.update(CharMaps.utf8_supported_unicode)
                table.update(CharMaps.textcomp)
            table.update(CharMaps.pifont)
            for ch in text:
                cp = ord(ch)
                if (cp in CharMaps.textcomp and not self.fallback_stylesheet):
                    self.requirements['textcomp'] = PreambleCmds.textcomp
                elif cp in CharMaps.pifont:
                    self.requirements['pifont'] = '\\usepackage{pifont}'
                elif (self.latex_encoding == 'utf8' and cp in CharMaps.unsupported_unicode):
                    self.requirements['_inputenc' + str(cp)] = '\\DeclareUnicodeCharacter{%04X}{%s}' % (cp, CharMaps.unsupported_unicode[cp])
        text = text.translate(table)
        if not self.is_xetex:
            separate_chars = '-'
            if self.literal:
                separate_chars += ',`\'"<>'
            for char in separate_chars * 2:
                text = text.replace(char + char, char + '{}' + char)
        if self.insert_newline:
            lines = text.split('\n')
            for (i, line) in enumerate(lines[:-1]):
                if not line.lstrip():
                    lines[i] += '~'
            text = ('\\\\' + '\n').join(lines)
        if (self.literal and not self.insert_non_breaking_blanks):
            text = text.replace('  ', ' ~')
        return text
    
    def attval(self, text, whitespace=re.compile('[\n\r\t\x0b\x0c]')):
        """Cleanse, encode, and return attribute value text."""
        return self.encode(whitespace.sub(' ', text))
    
    def is_inline(self, node):
        """Check whether a node represents an inline or block-level element"""
        return isinstance(node.parent, nodes.TextElement)
    
    def append_hypertargets(self, node) -> None:
        """Append hypertargets for all ids of `node`"""
        self.out.append('%\n'.join(('\\raisebox{1em}{\\hypertarget{%s}{}}' % id for id in node['ids'])))
    
    def ids_to_labels(self, node, set_anchor=True, protect=False, newline=False, pre_nl=False) -> list[str]:
        """Return label definitions for IDs of `node`.

        Make labels for all IDs that are either explicit or referenced in
        the document (i.e. not for section headings that are not referenced).

        If `set_anchor` is True, an anchor is set with \phantomsection.
        If `protect` is True, the \label cmd is made robust.
        If `newline` is True, a newline is added if there are labels.
        If `pre_nl` is True, a newline is prepended if there are labels.

        Provisional.
        """
        explicit_IDs = set((self.document.nameids[name] for name in node['names'] if self.document.nametypes[name]))
        prefix = ('\\protect' if protect else '')
        labels = [f'{prefix}\\label{{{ID}}}' for ID in node['ids'] if ID in explicit_IDs.union(self.refids)]
        if labels:
            if set_anchor:
                labels.insert(0, '\\phantomsection')
            if newline:
                labels.append('\n')
            if pre_nl:
                labels.insert(0, '\n')
        return labels
    
    def set_align_from_classes(self, node) -> None:
        """Convert ``align-*`` class arguments into alignment args."""
        align = [cls for cls in node['classes'] if cls.startswith('align-')]
        if align:
            node['align'] = align[-1].removeprefix('align-')
            node['classes'] = [cls for cls in node['classes'] if not cls.startswith('align-')]
    
    def insert_align_declaration(self, node, default=None) -> None:
        align = node.get('align', default)
        if align == 'left':
            self.out.append('\\raggedright\n')
        elif align == 'center':
            self.out.append('\\centering\n')
        elif align == 'right':
            self.out.append('\\raggedleft\n')
    
    def provide_fallback(self, feature, key=None) -> None:
        if key is None:
            key = feature
        if self.fallback_stylesheet:
            return
        self.fallbacks[key] = getattr(PreambleCmds, feature)
    
    def duclass_open(self, node) -> None:
        """Open a group and insert declarations for class values."""
        if not isinstance(node.parent, nodes.compound):
            self.out.append('\n')
        for cls in node['classes']:
            if cls.startswith('language-'):
                language = self.babel.language_name(cls[9:])
                if language:
                    self.babel.otherlanguages[language] = True
                    self.out.append('\\begin{selectlanguage}{%s}\n' % language)
            elif (isinstance(node, nodes.table) and cls in Writer.table_style_values + ['colwidths-given']):
                pass
            else:
                self.provide_fallback('duclass', 'DUclass')
                self.out.append('\\begin{DUclass}{%s}\n' % cls)
    
    def duclass_close(self, node) -> None:
        """Close a group of class declarations."""
        for cls in reversed(node['classes']):
            if cls.startswith('language-'):
                language = self.babel.language_name(cls[9:])
                if language:
                    self.out.append('\\end{selectlanguage}\n')
            elif (isinstance(node, nodes.table) and cls in Writer.table_style_values + ['colwidths-given']):
                pass
            else:
                self.provide_fallback('duclass', 'DUclass')
                self.out.append('\\end{DUclass}\n')
    
    def push_output_collector(self, new_out: list) -> None:
        self.out_stack.append(self.out)
        self.out = new_out
    
    def pop_output_collector(self) -> list:
        old_out = self.out
        self.out = self.out_stack.pop()
        return old_out
    
    def term_postfix(self, node):
        """
        Return LaTeX code required between term or field name and content.

        In a LaTeX "description" environment (used for definition
        lists and non-docinfo field lists), a ``\leavevmode``
        between an item's label and content ensures the correct
        placement of certain block constructs.
        """
        for child in node:
            if not isinstance(child, (nodes.Invisible, nodes.footnote, nodes.citation)):
                break
        else:
            return ''
        if isinstance(child, (nodes.container, nodes.compound)):
            return self.term_postfix(child)
        if isinstance(child, nodes.image):
            return '\\leavevmode\n'
        if not isinstance(child, (nodes.paragraph, nodes.math_block)):
            return '\\leavevmode'
        return ''
    
    def visit_Text(self, node) -> None:
        self.out.append(self.encode(node.astext()))
    
    def depart_Text(self, node) -> None:
        pass
    
    def visit_abbreviation(self, node) -> None:
        node['classes'].insert(0, 'abbreviation')
        self.visit_inline(node)
    
    def depart_abbreviation(self, node) -> None:
        self.depart_inline(node)
    
    def visit_acronym(self, node) -> None:
        node['classes'].insert(0, 'acronym')
        self.visit_inline(node)
    
    def depart_acronym(self, node) -> None:
        self.depart_inline(node)
    
    def visit_address(self, node) -> None:
        self.insert_newline = True
        self.visit_docinfo_item(node)
    
    def depart_address(self, node) -> None:
        self.depart_docinfo_item(node)
        self.insert_newline = False
    
    def visit_admonition(self, node) -> None:
        node['classes'] = [cls for cls in node['classes'] if cls != 'admonition']
        if self.settings.legacy_class_functions:
            self.fallbacks['admonition'] = PreambleCmds.admonition_legacy
            if 'error' in node['classes']:
                self.fallbacks['error'] = PreambleCmds.error_legacy
            self.out.append('\n\\DUadmonition[%s]{' % ','.join(node['classes']))
            return
        self.provide_fallback('admonition')
        if 'error' in node['classes']:
            self.provide_fallback('error')
        if not isinstance(node, nodes.system_message):
            self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append('\\begin{DUadmonition}')
    
    def depart_admonition(self, node) -> None:
        if self.settings.legacy_class_functions:
            self.out.append('}\n')
            return
        self.out.append('\\end{DUadmonition}\n')
        self.duclass_close(node)
    
    def visit_author(self, node) -> None:
        self.pdfauthor.append(self.attval(node.astext()))
        if isinstance(node.parent, nodes.authors):
            self.push_output_collector([])
        else:
            self.visit_docinfo_item(node)
    
    def depart_author(self, node) -> None:
        if isinstance(node.parent, nodes.authors):
            author_name = self.pop_output_collector()
            self.out.append(''.join(author_name))
        else:
            self.depart_docinfo_item(node)
    
    def visit_authors(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_authors(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_block_quote(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append('\\begin{quote}')
    
    def depart_block_quote(self, node) -> None:
        self.out.append('\\end{quote}\n')
        self.duclass_close(node)
    
    def visit_bullet_list(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append('\\begin{itemize}')
    
    def depart_bullet_list(self, node) -> None:
        self.out.append('\\end{itemize}\n')
        self.duclass_close(node)
    
    def visit_superscript(self, node) -> None:
        self.out.append('\\textsuperscript{')
        self.visit_inline(node)
    
    def depart_superscript(self, node) -> None:
        self.depart_inline(node)
        self.out.append('}')
    
    def visit_subscript(self, node) -> None:
        self.out.append('\\textsubscript{')
        self.visit_inline(node)
    
    def depart_subscript(self, node) -> None:
        self.depart_inline(node)
        self.out.append('}')
    
    def visit_caption(self, node) -> None:
        self.out.append('\\caption{')
        self.visit_inline(node)
    
    def depart_caption(self, node) -> None:
        self.depart_inline(node)
        self.out.append('}\n')
    
    def visit_title_reference(self, node) -> None:
        self.provide_fallback('titlereference')
        self.out.append('\\DUroletitlereference{')
        self.visit_inline(node)
    
    def depart_title_reference(self, node) -> None:
        self.depart_inline(node)
        self.out.append('}')
    
    def visit_citation(self, node) -> None:
        if self.use_latex_citations:
            self.push_output_collector([])
        else:
            self.out.append('\\begin{figure}[b]')
            self.append_hypertargets(node)
    
    def depart_citation(self, node) -> None:
        if self.use_latex_citations:
            label = self.out[0]
            text = ''.join(self.out[1:])
            self._bibitems.append([label, text])
            self.pop_output_collector()
        else:
            self.out.append('\\end{figure}\n')
    
    def visit_citation_reference(self, node) -> None:
        if self.bibtex:
            self._bibitems.append([node.astext()])
        if self.use_latex_citations:
            if not self.inside_citation_reference_label:
                self.out.append('\\cite{')
                self.inside_citation_reference_label = True
            else:
                assert self.out[-1] in (' ', '\n'), 'unexpected non-whitespace while in reference label'
                del self.out[-1]
        else:
            href = ''
            if 'refid' in node:
                href = node['refid']
            elif 'refname' in node:
                href = self.document.nameids[node['refname']]
            self.out.append('\\hyperlink{%s}{[' % href)
    
    def depart_citation_reference(self, node) -> None:
        if self.use_latex_citations:
            followup_citation = False
            sibling = node.next_node(descend=False, siblings=True)
            if (isinstance(sibling, nodes.Text) and sibling.astext() in (' ', '\n')):
                sibling2 = sibling.next_node(descend=False, siblings=True)
                if isinstance(sibling2, nodes.citation_reference):
                    followup_citation = True
            if followup_citation:
                self.out.append(',')
            else:
                self.out.append('}')
                self.inside_citation_reference_label = False
        else:
            self.out.append(']}')
    
    def visit_classifier(self, node) -> None:
        self.out.append('(\\textbf{')
    
    def depart_classifier(self, node) -> None:
        self.out.append('})')
        if node.next_node(nodes.term, descend=False, siblings=True):
            self.out.append('\n')
    
    def visit_colspec(self, node) -> None:
        self.active_table.visit_colspec(node)
    
    def depart_colspec(self, node) -> None:
        pass
    
    def visit_comment(self, node):
        if not isinstance(node.parent, nodes.compound):
            self.out.append('\n')
        self.out.append('%% %s\n' % node.astext().replace('\n', '\n% '))
        raise nodes.SkipNode
    
    def depart_comment(self, node) -> None:
        pass
    
    def visit_compound(self, node) -> None:
        if isinstance(node.parent, nodes.compound):
            self.out.append('\n')
        self.out += self.ids_to_labels(node, pre_nl=True)
        node['classes'].insert(0, 'compound')
        self.duclass_open(node)
    
    def depart_compound(self, node) -> None:
        self.duclass_close(node)
    
    def visit_contact(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_contact(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_container(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
    
    def depart_container(self, node) -> None:
        self.duclass_close(node)
    
    def visit_copyright(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_copyright(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_date(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_date(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_decoration(self, node) -> None:
        pass
    
    def depart_decoration(self, node) -> None:
        pass
    
    def visit_definition(self, node) -> None:
        pass
    
    def depart_definition(self, node) -> None:
        pass
    
    def visit_definition_list(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append('\\begin{description}\n')
    
    def depart_definition_list(self, node) -> None:
        self.out.append('\\end{description}\n')
        self.duclass_close(node)
    
    def visit_definition_list_item(self, node) -> None:
        self.out += self.ids_to_labels(node, newline=True)
    
    def depart_definition_list_item(self, node) -> None:
        if node.next_node(descend=False, siblings=True) is not None:
            self.out.append('\n')
    
    def visit_description(self, node) -> None:
        self.out.append(' ')
    
    def depart_description(self, node) -> None:
        pass
    
    def visit_docinfo(self, node) -> None:
        self.push_output_collector(self.docinfo)
    
    def depart_docinfo(self, node) -> None:
        self.pop_output_collector()
        if self.docinfo:
            self.requirements['tabularx'] = '\\usepackage{tabularx}'
            self.provide_fallback('providelength', '_providelength')
            self.provide_fallback('docinfo')
            self.docinfo.insert(0, '\n% Docinfo\n\\begin{center}\n\\begin{tabularx}{\\DUdocinfowidth}{lX}\n')
            self.docinfo.append('\\end{tabularx}\n\\end{center}\n')
    
    def visit_docinfo_item(self, node, name=None) -> None:
        if name is not None:
            warnings.warn('visit_docinfo_item(): argument "name" is obsolete and will be removed in Docutils 0.24', DeprecationWarning, stacklevel=2)
        if (self.use_latex_docinfo and isinstance(node, self.TITLEDATA_NODES)):
            self.push_output_collector([])
        else:
            label = self.language_label(node.tagname)
            self.out.append('\\textbf{%s}: &' % label)
            if isinstance(node, nodes.address):
                self.out.append(' {\\raggedright\n')
            elif len(label) + len(node.astext()) > 64:
                self.out.append('\n  ')
            else:
                self.out.append(' ')
            if isinstance(node, nodes.authors):
                self.push_output_collector([])
    
    def depart_docinfo_item(self, node) -> None:
        if (self.use_latex_docinfo and isinstance(node, self.TITLEDATA_NODES)):
            if isinstance(node, nodes.authors):
                s = ' \\and '
                for nn in node.findall(include_self=False, descend=False, siblings=True):
                    if isinstance(nn, (nodes.author, nodes.authors)):
                        break
                    if isinstance(nn, (nodes.address, nodes.contact, nodes.organization)):
                        s = ' \\quad '
            else:
                s = ''
            text = s.join(self.pop_output_collector())
            if isinstance(node, nodes.date):
                self.date.append(text)
            elif isinstance(node, (nodes.author, nodes.authors)):
                if self.author_stack[-1][0]:
                    self.author_stack.append([text])
                else:
                    self.author_stack[-1][0] = text
            else:
                self.author_stack[-1].append(text)
        else:
            if isinstance(node, nodes.address):
                self.out.append('}')
            elif isinstance(node, nodes.authors):
                author_names = self.pop_output_collector()
                for sep in reversed(self.language_module.author_separators):
                    if not any((sep in name for name in author_names)):
                        break
                self.out.append((sep + ' ').join(author_names))
            self.out.append(' \\\\\n')
    
    def visit_doctest_block(self, node) -> None:
        self.visit_literal_block(node)
    
    def depart_doctest_block(self, node) -> None:
        self.depart_literal_block(node)
    
    def visit_document(self, node) -> None:
        if (self.use_latex_docinfo or isinstance(node.next_node(), nodes.title)):
            protect = self.settings.documentclass == 'memoir'
            self.title_labels += self.ids_to_labels(node, set_anchor=False, protect=protect)
    
    def depart_document(self, node) -> None:
        if (self.babel.otherlanguages or self.babel.language not in ('', 'english')):
            self.requirements['babel'] = self.babel()
        self.pdfsetup.append(PreambleCmds.linking % self.hyperref_options)
        if self.document.get('title', ''):
            self.pdfinfo.insert(0, '  pdftitle={%s},' % self.encode(self.document.get('title', '')))
        if self.pdfauthor:
            authors = (self.author_separator + ' ').join(self.pdfauthor)
            self.pdfinfo.append('  pdfauthor={%s}' % authors)
        if self.pdfinfo:
            self.pdfsetup += ['\\hypersetup{'] + self.pdfinfo + ['}']
        if (self.title or self.date or self.author_stack != [['']]):
            self.make_title()
        if self._bibitems:
            self.append_bibliogaphy()
        if ('minitoc' in self.requirements and not self.has_latex_toc):
            self.out.append('\n\\faketableofcontents % for local ToCs\n')
        self.requirements = [self.requirements[key] for key in sorted(self.requirements.keys())]
        self.fallbacks = [self.fallbacks[key] for key in sorted(self.fallbacks.keys())]
    
    def make_title(self) -> None:
        title_arg = [''.join(self.title)]
        if self.title:
            title_arg += self.title_labels
        if self.subtitle:
            title_arg += ['\\\\', '\\DUdocumentsubtitle{%s}' % ''.join(self.subtitle)] + self.subtitle_labels
        self.titledata.append('\\title{%s}' % '%\n  '.join(title_arg))
        authors = ['\\\\\n'.join(filter(None, author_entry)) for author_entry in self.author_stack]
        self.titledata.append('\\author{%s}' % ' \\and\n'.join(authors))
        self.titledata.append('\\date{%s}' % ', '.join(self.date))
        self.body_pre_docinfo.append('\\maketitle\n')
    
    def append_bibliogaphy(self) -> None:
        if self.bibtex:
            self.out.append('\n\\bibliographystyle{%s}\n' % self.bibtex[0])
            self.out.append('\\bibliography{%s}\n' % ','.join(self.bibtex[1:]))
        elif self.use_latex_citations:
            widest_label = ''
            for bibitem in self._bibitems:
                if len(widest_label) < len(bibitem[0]):
                    widest_label = bibitem[0]
            self.out.append('\n\\begin{thebibliography}{%s}\n' % widest_label)
            for bibitem in self._bibitems:
                cite_key = bibitem[0].replace('\\_', '_')
                self.out.append('\\bibitem[%s]{%s}{%s}\n' % (bibitem[0], cite_key, bibitem[1]))
            self.out.append('\\end{thebibliography}\n')
    
    def visit_emphasis(self, node) -> None:
        self.out.append('\\emph{')
        self.visit_inline(node)
    
    def depart_emphasis(self, node) -> None:
        self.depart_inline(node)
        self.out.append('}')
    
    def insert_additional_table_colum_delimiters(self) -> None:
        while self.active_table.get_rowspan(self.active_table.get_entry_number()):
            self.out.append(' & ')
            self.active_table.visit_entry()
    
    def visit_entry(self, node):
        if self.active_table.get_entry_number() == 0:
            self.insert_additional_table_colum_delimiters()
        else:
            self.out.append(' & ')
        if ('morerows' in node and 'morecols' in node):
            raise NotImplementedError('Cells that span multiple rows *and* columns currently not supported by the LaTeX writer')
        if 'morerows' in node:
            self.requirements['multirow'] = '\\usepackage{multirow}'
            mrows = node['morerows'] + 1
            self.active_table.set_rowspan(self.active_table.get_entry_number(), mrows)
            self.out.append('\\multirow{%d}{%s}{' % (mrows, self.active_table.get_column_width()))
            self.context.append('}')
        elif 'morecols' in node:
            if self.active_table.get_entry_number() == 0:
                bar1 = self.active_table.get_vertical_bar()
            else:
                bar1 = ''
            mcols = node['morecols'] + 1
            self.out.append('\\multicolumn{%d}{%s%s%s}{' % (mcols, bar1, self.active_table.get_multicolumn_width(self.active_table.get_entry_number(), mcols), self.active_table.get_vertical_bar()))
            self.context.append('}')
        else:
            self.context.append('')
        if (len(node) and ((isinstance(node.parent.parent, nodes.thead) or self.active_table.is_stub_column()))):
            self.out.append('\\textbf{')
            self.context.append('}')
        else:
            self.context.append('')
        if (not self.active_table.colwidths_auto and self.out[-1].endswith('{') and node.astext()):
            self.out.append('%')
        self.active_table.visit_entry()
    
    def depart_entry(self, node) -> None:
        self.out.append(self.context.pop())
        self.out.append(self.context.pop())
        self.insert_additional_table_colum_delimiters()
    
    def visit_row(self, node) -> None:
        self.active_table.visit_row()
    
    def depart_row(self, node) -> None:
        self.out.extend(self.active_table.depart_row())
    
    def visit_enumerated_list(self, node) -> None:
        types = {'': '', 'arabic': 'arabic', 'loweralpha': 'alph', 'upperalpha': 'Alph', 'lowerroman': 'roman', 'upperroman': 'Roman'}
        default_labels = [('', 'arabic', '.'), ('(', 'alph', ')'), ('', 'roman', '.'), ('', 'Alph', '.')]
        prefix = ''
        if self.compound_enumerators:
            if (self.section_prefix_for_enumerators and self.section_level and not self._enumeration_counters):
                prefix = '.'.join((str(n) for n in self._section_number[:self.section_level])) + self.section_enumerator_separator
            if self._enumeration_counters:
                prefix += self._enumeration_counters[-1]
        prefix += node.get('prefix', '')
        enumtype = types[node.get('enumtype', 'arabic')]
        suffix = node.get('suffix', '.')
        enum_level = len(self._enumeration_counters) + 1
        counter_name = 'enum' + RomanNumeral(enum_level).to_lowercase()
        label = '%s\\%s{%s}%s' % (prefix, enumtype, counter_name, suffix)
        self._enumeration_counters.append(label)
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        if enum_level <= 4:
            self.out.append('\\begin{enumerate}')
            if (prefix, enumtype, suffix) != default_labels[enum_level - 1]:
                self.out.append('\n\\renewcommand{\\label%s}{%s}' % (counter_name, label))
        else:
            self.fallbacks[counter_name] = '\\newcounter{%s}' % counter_name
            self.out.append('\\begin{list}')
            self.out.append('{%s}' % label)
            self.out.append('{\\usecounter{%s}}' % counter_name)
        if 'start' in node:
            self.out.append('\n\\setcounter{%s}{%d}' % (counter_name, node['start'] - 1))
    
    def depart_enumerated_list(self, node) -> None:
        if len(self._enumeration_counters) <= 4:
            self.out.append('\\end{enumerate}\n')
        else:
            self.out.append('\\end{list}\n')
        self.duclass_close(node)
        self._enumeration_counters.pop()
    
    def visit_field(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
    
    def depart_field(self, node) -> None:
        pass
    
    def visit_field_body(self, node) -> None:
        if not isinstance(node.parent.parent, nodes.docinfo):
            self.out.append(self.term_postfix(node))
    
    def depart_field_body(self, node) -> None:
        if self.out is self.docinfo:
            self.out.append('\\\\' + '\n')
    
    def visit_field_list(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        if self.out is not self.docinfo:
            self.provide_fallback('fieldlist')
            self.out.append('\\begin{DUfieldlist}')
    
    def depart_field_list(self, node) -> None:
        if self.out is not self.docinfo:
            self.out.append('\\end{DUfieldlist}\n')
        self.duclass_close(node)
    
    def visit_field_name(self, node) -> None:
        if self.out is self.docinfo:
            self.out.append('\\textbf{')
        else:
            self.out.append('\n\\item[{')
    
    def depart_field_name(self, node) -> None:
        if self.out is self.docinfo:
            self.out.append('}: &')
        else:
            self.out.append(':}]')
    
    def visit_figure(self, node) -> None:
        self.requirements['float'] = PreambleCmds.float
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        alignment = node.attributes.get('align', 'center')
        if alignment != 'center':
            self.out.append('\\begin{figure} %% align = "%s"' % alignment)
        else:
            self.out.append('\\begin{figure}')
    
    def depart_figure(self, node) -> None:
        self.out.append('\\end{figure}\n')
        self.duclass_close(node)
    
    def visit_footer(self, node) -> None:
        self.push_output_collector([])
        self.out.append('\\newcommand{\\DUfooter}{')
    
    def depart_footer(self, node) -> None:
        self.out.append('}')
        self.requirements['~footer'] = ''.join(self.out)
        self.pop_output_collector()
    
    def visit_footnote(self, node) -> None:
        if not self.latex_footnotes:
            try:
                backref = node['backrefs'][0]
            except IndexError:
                backref = ''
            self.provide_fallback('footnotes')
            label = self.encode(node[0].astext())
            if self.settings.footnote_references == 'brackets':
                label = '[%s]' % label
            self.out.append('%%\n\\DUfootnotetext{%s}{%s}{%s}{%%' % (node['ids'][0], backref, label))
        elif not self.footnote_queue:
            raise nodes.SkipNode
    
    def depart_footnote(self, node) -> None:
        if isinstance(node[-1], nodes.Admonition):
            self.out.append('\\smallskip')
        if not self.latex_footnotes:
            self.out.append('}\n')
    
    def visit_footnote_reference(self, node) -> None:
        href = node['refid']
        if not self.latex_footnotes:
            if isinstance(node.parent, nodes.title):
                if isinstance(node.parent.parent, nodes.section):
                    self.out.append('\\texorpdfstring{')
                self.out.append('\\protect')
            if self.settings.footnote_references == 'brackets':
                self.provide_fallback('bracket_footnoterefs')
                cmd = '\\DUbracketfootnotemark'
            else:
                self.provide_fallback('footnotes')
                cmd = '\\DUfootnotemark'
            self.out.append('%s{%s}{%s}{' % (cmd, node['ids'][0], href))
        else:
            target = self.document.ids[href]
            if not isinstance(target, nodes.footnote):
                self.out.append('\\textsuperscript{')
                self.visit_reference(node)
                return
            if href in self.processed_footnotes:
                self.out.append('\\footref{%s}' % href)
                raise nodes.SkipNode
            if self.footnote_queue:
                self.out.append('\\footref{%s}' % href)
                self.footnote_queue.append(href)
                raise nodes.SkipNode
            self.footnote_queue.append(href)
            footnote_cmd = '%\n\\footnote'
            if isinstance(node.parent, nodes.title):
                if isinstance(node.parent.parent, nodes.section):
                    self.out.append('%\n\\texorpdfstring{')
                footnote_cmd = '%\n \\protect\\footnote'
            add_label = (target['names'] and self.document.refnames.get(target['names'][0], []))
            while self.footnote_queue:
                ID = self.footnote_queue[0]
                footnote = self.document.ids[ID]
                self.processed_footnotes.add(ID)
                self.out += [footnote_cmd, '{']
                if add_label:
                    self.out += ['\\label{', ID, '}']
                self.out.append('%')
                self.push_output_collector([])
                footnote.walkabout(self)
                note = ''.join(self.pop_output_collector())
                note = '\n  '.join(note.splitlines())
                self.out.append(note)
                self.out.append('\n}')
                self.footnote_queue.pop(0)
                footnote_cmd = '%\n\\refstepcounter{footnote}\\footnotetext'
                add_label = True
            raise nodes.SkipChildren
    
    def depart_footnote_reference(self, node) -> None:
        if not self.latex_footnotes:
            self.out.append('}')
        elif not isinstance(self.document.ids[node['refid']], nodes.footnote):
            self.depart_reference(node)
            self.out.append('}')
            return
        if (isinstance(node.parent.parent, nodes.section) and isinstance(node.parent, nodes.title)):
            self.out.append('}{}')
    
    def label_delim(self, node, bracket, superscript):
        if isinstance(node.parent, nodes.footnote):
            raise nodes.SkipNode
        else:
            assert isinstance(node.parent, nodes.citation)
            if not self.use_latex_citations:
                self.out.append(bracket)
    
    def visit_label(self, node) -> None:
        """footnote or citation label: in brackets or as superscript"""
        self.label_delim(node, '[', '\\textsuperscript{')
    
    def depart_label(self, node) -> None:
        self.label_delim(node, ']', '}')
    
    def visit_generated(self, node) -> None:
        pass
    
    def depart_generated(self, node) -> None:
        pass
    
    def visit_header(self, node) -> None:
        self.push_output_collector([])
        self.out.append('\\newcommand{\\DUheader}{')
    
    def depart_header(self, node) -> None:
        self.out.append('}')
        self.requirements['~header'] = ''.join(self.out)
        self.pop_output_collector()
    
    def to_latex_length(self, length_str, node=None) -> str:
        """Convert "measure" `length_str` to LaTeX length specification.

        Note: the default length unit will change from "bp"
        (Postscript point) to "px" in Docutils 1.0.
        """
        (value, unit) = nodes.parse_measure(length_str)
        if unit in ('em', 'ex', 'cm', 'mm', 'in', 'pc', 'px', 'bp', 'cc', 'dd', 'sp', 'mu'):
            return length_str
        if unit in ('', 'pt'):
            return f'{value}bp'
        if unit == 'Q':
            return f'{value / 4}mm'
        if unit == '%':
            return f'{value / 100:g}\\linewidth'
        if unit == 'vw':
            return f'{value / 100:g}\\paperwidth'
        if unit == 'vh':
            return f'{value / 100:g}\\paperheight'
        if not hasattr(PreambleCmds, unit):
            self.warn(f'Unit "{unit}" not supported by LaTeX.\n  Define lenght "\\DU{unit}dimen" in preamble, raw LaTeX, or custom stylesheet.', base_node=node)
        elif unit == 'ch':
            self.fallbacks['ch'] = PreambleCmds.ch
        else:
            self.provide_fallback('providelength', '_providelength')
            self.provide_fallback(unit)
        return f'{value}\\DU{unit}dimen'
    
    def visit_image(self, node) -> None:
        self.requirements['graphicx'] = self.graphicx_package
        attrs = node.attributes
        imagepath = self.uri2path(attrs['uri'], output_path='')
        if 'align' not in attrs:
            if (isinstance(node.parent, nodes.figure) or (isinstance(node.parent, nodes.reference) and isinstance(node.parent.parent, nodes.figure))):
                attrs['align'] = 'center'
            self.set_align_from_classes(node)
        pre = []
        post = []
        include_graphics_options = []
        if isinstance(node.parent, nodes.reference):
            pre.append(self.out.pop())
        align_codes = {'bottom': ('', ''), 'middle': ('\\raisebox{-0.5\\height}{', '}'), 'top': ('\\raisebox{-\\height}{', '}'), 'center': ('\\noindent\\makebox[\\linewidth][c]{', '}'), 'left': ('\\noindent{', '\\hfill}'), 'right': ('\\noindent{\\hfill', '}')}
        if 'align' in attrs:
            try:
                align_code = align_codes[attrs['align']]
                pre.append(align_code[0])
                post.append(align_code[1])
            except KeyError:
                pass
        if 'height' in attrs:
            include_graphics_options.append(f"height={self.to_latex_length(attrs['height'], node)}")
        if 'scale' in attrs:
            include_graphics_options.append(f"scale={attrs['scale'] / 100:g}")
        if 'width' in attrs:
            include_graphics_options.append(f"width={self.to_latex_length(attrs['width'], node)}")
        pre.append(''.join(self.ids_to_labels(node, newline=True)))
        if not ((self.is_inline(node) or isinstance(node.parent, nodes.compound))):
            pre.append('\n')
        if not self.is_inline(node):
            post.append('\n')
        pre.reverse()
        self.out.extend(pre)
        if (imagepath.suffix == '.svg' and 'svg' in self.settings.stylesheet):
            cmd = 'includesvg'
        else:
            cmd = 'includegraphics'
        options = ''
        if include_graphics_options:
            options = f"[{','.join(include_graphics_options)}]"
        self.out.append(f'\\{cmd}{options}{{{imagepath.as_posix()}}}')
        self.out.extend(post)
    
    def depart_image(self, node) -> None:
        pass
    
    def visit_inline(self, node) -> None:
        anchor_nodes = (nodes.caption, nodes.subtitle, nodes.title)
        set_anchor = not ((isinstance(node.parent, anchor_nodes) or isinstance(node, anchor_nodes)))
        add_newline = isinstance(node, nodes.paragraph)
        self.out += self.ids_to_labels(node, set_anchor, newline=add_newline)
        for cls in node['classes']:
            if cls.startswith('language-'):
                language = self.babel.language_name(cls[9:])
                if language:
                    self.babel.otherlanguages[language] = True
                    self.out.append('\\foreignlanguage{%s}{' % language)
            else:
                self.provide_fallback('inline')
                if hasattr(PreambleCmds, f'inline role {cls}'):
                    self.provide_fallback(f'inline role {cls}')
                if cls in ('del', 'ins', 'mark', 's', 'u'):
                    self.requirements['soul'] = '\\usepackage{soul}'
                if cls == 'mark':
                    self.requirements['color'] = PreambleCmds.color
                self.out.append('\\DUrole{%s}{' % cls)
    
    def depart_inline(self, node) -> None:
        self.out.append('}' * len(node['classes']))
    
    def visit_legend(self, node) -> None:
        self.provide_fallback('legend')
        self.out.append('\\begin{DUlegend}')
    
    def depart_legend(self, node) -> None:
        self.out.append('\\end{DUlegend}\n')
    
    def visit_line(self, node) -> None:
        self.out.append('\\item[] ')
    
    def depart_line(self, node) -> None:
        self.out.append('\n')
    
    def visit_line_block(self, node) -> None:
        self.provide_fallback('providelength', '_providelength')
        self.provide_fallback('lineblock')
        self.set_align_from_classes(node)
        if isinstance(node.parent, nodes.line_block):
            self.out.append('\\item[]\n\\begin{DUlineblock}{\\DUlineblockindent}\n')
        else:
            self.out += self.ids_to_labels(node, pre_nl=True)
            self.duclass_open(node)
            self.out.append('\\begin{DUlineblock}{0em}\n')
            self.insert_align_declaration(node)
    
    def depart_line_block(self, node) -> None:
        self.out.append('\\end{DUlineblock}\n')
        self.duclass_close(node)
    
    def visit_list_item(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.out.append('\n\\item ')
    
    def depart_list_item(self, node) -> None:
        pass
    
    def visit_literal(self, node) -> None:
        self.literal = True
        if ('code' in node['classes'] and self.settings.syntax_highlight != 'none'):
            self.requirements['color'] = PreambleCmds.color
            self.provide_fallback('highlight_rules', 'code')
        self.out.append('\\texttt{')
        self.visit_inline(node)
    
    def depart_literal(self, node) -> None:
        self.literal = False
        self.depart_inline(node)
        self.out.append('}')
    
    def is_plaintext(self, node):
        """Check whether `node` contains only text"""
        return (len(node) == 1 and isinstance(node[0], nodes.Text))
    
    def visit_literal_block(self, node) -> None:
        """Render a literal block.

        Corresponding rST elements: literal block, parsed-literal, code.
        """
        packages = {'lstlisting': '\\usepackage{listings}\n\\lstset{xleftmargin=\\leftmargin}', 'listing': '\\usepackage{moreverb}', 'Verbatim': '\\usepackage{fancyvrb}', 'verbatimtab': '\\usepackage{moreverb}'}
        literal_env = self.literal_block_env
        _plaintext = self.is_plaintext(node)
        _in_table = self.active_table.is_open()
        _autowidth_table = (_in_table and self.active_table.colwidths_auto)
        _no_env_nodes = (nodes.footnote, nodes.sidebar)
        if self.settings.legacy_class_functions:
            _no_env_nodes += (nodes.admonition, nodes.system_message)
        _use_env = (_plaintext and not isinstance(node.parent, _no_env_nodes))
        _use_listings = (literal_env == 'lstlisting' and _use_env)
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        if (not _plaintext and 'code' in node['classes'] and self.settings.syntax_highlight != 'none'):
            self.requirements['color'] = PreambleCmds.color
            self.provide_fallback('highlight_rules', 'code')
        if (_in_table and _use_env and not _autowidth_table):
            self.fallbacks['ttem'] = PreambleCmds.ttem
            self.out.append('\\begin{minipage}{%d\\ttemwidth}\n' % max((len(line) for line in node.astext().split('\n'))))
            self.context.append('\n\\end{minipage}\n')
        elif (not _in_table and not _use_listings):
            self.out.append('\\begin{quote}\n')
            self.context.append('\n\\end{quote}\n')
        else:
            self.context.append('\n')
        if (literal_env and _use_env and ((not _autowidth_table or _use_listings))):
            try:
                self.requirements['literal_block'] = packages[literal_env]
            except KeyError:
                pass
            self.verbatim = True
            if (_in_table and _use_listings):
                self.out.append('\\lstset{xleftmargin=0pt}\n')
            self.out.append('\\begin{%s}%s\n' % (literal_env, self.literal_block_options))
            self.context.append('\n\\end{%s}' % literal_env)
        elif (_use_env and not _autowidth_table):
            self.alltt = True
            self.requirements['alltt'] = '\\usepackage{alltt}'
            self.out.append('\\begin{alltt}\n')
            self.context.append('\n\\end{alltt}')
        else:
            self.literal = True
            self.insert_newline = True
            self.insert_non_breaking_blanks = True
            self.out.append('\\ttfamily\\raggedright\n')
            self.context.append('')
    
    def depart_literal_block(self, node) -> None:
        self.insert_non_breaking_blanks = False
        self.insert_newline = False
        self.literal = False
        self.verbatim = False
        self.alltt = False
        self.out.append(self.context.pop())
        self.out.append(self.context.pop())
        self.duclass_close(node)
    
    def visit_meta(self, node) -> None:
        if ('name' not in node or 'content' not in node):
            raise nodes.SkipNode
        name = node['name']
        content = self.encode(node['content'])
        if name in ('author', 'keywords', 'producer', 'subject', 'title'):
            self.pdfinfo.append('  pdf%s={%s},' % (name, content))
        elif name == 'creator':
            self.pdfinfo.append('  addtopdfcreator={%s},' % content)
        else:
            self.pdfinfo.append('  pdfinfo={%s={%s}},' % (name, content))
    
    def depart_meta(self, node) -> None:
        pass
    
    def visit_math(self, node, math_env='$') -> None:
        """
        Provisional: the `math_env` argument will be dropped in Docutils 2.0.
        """
        self.requirements['amsmath'] = '\\usepackage{amsmath}'
        self.visit_inline(node)
        math_code = node.astext().translate(unichar2tex.uni2tex_table)
        if self.alltt:
            self.out += ['\\(', math_code, '\\)']
        else:
            self.out += ['$', math_code, '$']
        self.depart_inline(node)
        raise nodes.SkipNode
    
    def depart_math(self, node) -> None:
        pass
    
    def visit_math_block(self, node) -> None:
        self.requirements['amsmath'] = '\\usepackage{amsmath}'
        math_env = pick_math_environment(node.astext())
        self.out.append('%\n')
        if (node['ids'] and math_env.endswith('*')):
            self.out.append('\\phantomsection\n')
        for cls in node['classes']:
            self.provide_fallback('inline')
            self.out.append(f'\\DUrole{{{cls}}}{{%\n')
        self.out += [f'\\begin{{{math_env}}}\n', node.astext().translate(unichar2tex.uni2tex_table), '\n', *self.ids_to_labels(node, set_anchor=False, newline=True), f'\\end{{{math_env}}}']
        if node['classes']:
            self.out.append('\n' + '}' * len(node['classes']))
        raise nodes.SkipNode
    
    def depart_math_block(self, node) -> None:
        pass
    
    def visit_option(self, node) -> None:
        if self.context[-1]:
            self.out.append(', ')
    
    def depart_option(self, node) -> None:
        self.context[-1] += 1
    
    def visit_option_argument(self, node) -> None:
        """Append the delimiter between an option and its argument to body."""
        self.out.append(node.get('delimiter', ' '))
    
    def depart_option_argument(self, node) -> None:
        pass
    
    def visit_option_group(self, node) -> None:
        self.out.append('\\item[')
        self.context.append(0)
    
    def depart_option_group(self, node) -> None:
        self.context.pop()
        self.out.append('] ')
    
    def visit_option_list(self, node) -> None:
        self.provide_fallback('providelength', '_providelength')
        self.provide_fallback('optionlist')
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append('\\begin{DUoptionlist}\n')
    
    def depart_option_list(self, node) -> None:
        self.out.append('\\end{DUoptionlist}\n')
        self.duclass_close(node)
    
    def visit_option_list_item(self, node) -> None:
        self.out += self.ids_to_labels(node, newline=True)
    
    def depart_option_list_item(self, node) -> None:
        pass
    
    def visit_option_string(self, node) -> None:
        pass
    
    def depart_option_string(self, node) -> None:
        pass
    
    def visit_organization(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_organization(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_paragraph(self, node) -> None:
        index = node.parent.index(node)
        if (index == 0 and isinstance(node.parent, (nodes.list_item, nodes.description, nodes.compound, nodes.container))):
            pass
        elif (index > 0 and isinstance(node.parent, nodes.compound) and not isinstance(node.parent[index - 1], (nodes.paragraph, nodes.compound))):
            pass
        elif self.active_table.colwidths_auto:
            if index == 1:
                self.warn('LaTeX merges paragraphs in tables with auto-sized columns!', base_node=node)
            if index > 0:
                self.out.append('\n')
        else:
            self.out.append('\n')
        self.visit_inline(node)
    
    def depart_paragraph(self, node) -> None:
        self.depart_inline(node)
        if not self.active_table.colwidths_auto:
            self.out.append('\n')
    
    def visit_problematic(self, node) -> None:
        self.requirements['color'] = PreambleCmds.color
        self.out.append('%\n')
        self.append_hypertargets(node)
        self.out.append('\\hyperlink{%s}{\\textbf{\\color{red}' % node['refid'])
    
    def depart_problematic(self, node) -> None:
        self.out.append('}}')
    
    def visit_raw(self, node):
        if 'latex' not in node.get('format', '').split():
            raise nodes.SkipNode
        if not ((self.is_inline(node) or isinstance(node.parent, nodes.compound))):
            self.out.append('\n')
        self.visit_inline(node)
        self.verbatim = True
    
    def depart_raw(self, node) -> None:
        self.verbatim = False
        self.depart_inline(node)
        if not self.is_inline(node):
            self.out.append('\n')
    
    def has_unbalanced_braces(self, string):
        """Test whether there are unmatched '{' or '}' characters."""
        level = 0
        for ch in string:
            if ch == '{':
                level += 1
            if ch == '}':
                level -= 1
            if level < 0:
                return True
        return level != 0
    
    def visit_reference(self, node):
        special_chars = {ord('#'): '\\#', ord('%'): '\\%', ord('\\'): '\\\\'}
        if not self.is_inline(node):
            self.out.append('\n')
        if 'refuri' in node:
            href = str(node['refuri']).translate(special_chars)
            if ('^^' in href or self.has_unbalanced_braces(href)):
                self.error(f'External link "{href}" not supported by LaTeX.\n (Must not contain "^^" or unbalanced braces.)')
            if node['refuri'] == node.astext():
                self.out.append('\\url{%s}' % href)
                raise nodes.SkipNode
            self.out.append('\\href{%s}{' % href)
            return
        if 'refid' in node:
            href = node['refid']
        elif 'refname' in node:
            href = self.document.nameids[node['refname']]
        else:
            raise AssertionError('Unknown reference.')
        if self.reference_label:
            self.out.append('\\%s{%s}' % (self.reference_label, href.replace('#', '')))
            raise nodes.SkipNode
        self.out.append('\\hyperref[%s]{' % href)
    
    def depart_reference(self, node) -> None:
        self.out.append('}')
        if not self.is_inline(node):
            self.out.append('\n')
    
    def visit_revision(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_revision(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_rubric(self, node) -> None:
        self.provide_fallback('rubric')
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append('\\DUrubric{')
    
    def depart_rubric(self, node) -> None:
        self.out.append('}\n')
        self.duclass_close(node)
    
    def visit_section(self, node) -> None:
        self.section_level += 1
        self._section_number.append(0)
        self._section_number[self.section_level - 1] += 1
        if 'sectnum' in self.requirements:
            return
        if self.settings.sectnum_xform:
            sectnum_depth = 0
        else:
            sectnum_depth = getattr(self.settings, 'sectnum_depth', 0)
            if isinstance(sectnum_depth, str):
                sectnum_depth = 0
            sectnum_start = getattr(self.settings, 'sectnum_start', 1)
            if isinstance(sectnum_start, str):
                sectnum_start = 1
            if sectnum_start != 1:
                self.requirements['sectnum_start'] = '\\setcounter{%s}{%d}' % (self.d_class.sections[0], sectnum_start - 1)
        if sectnum_depth is not None:
            self.requirements['sectnum'] = '\\setcounter{secnumdepth}{%d}' % self.d_class.latex_section_depth(sectnum_depth)
    
    def depart_section(self, node) -> None:
        self._section_number.pop()
        self.section_level -= 1
    
    def visit_sidebar(self, node) -> None:
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.requirements['color'] = PreambleCmds.color
        self.provide_fallback('sidebar')
        self.out.append('\\DUsidebar{')
    
    def depart_sidebar(self, node) -> None:
        self.out.append('}\n')
        self.duclass_close(node)
    attribution_formats = {'dash': ('—', ''), 'parentheses': ('(', ')'), 'parens': ('(', ')'), 'none': ('', '')}
    
    def visit_attribution(self, node) -> None:
        (prefix, suffix) = self.attribution_formats[self.settings.attribution]
        self.out.append('\\nopagebreak\n')
        self.out += self.ids_to_labels(node, pre_nl=True)
        self.duclass_open(node)
        self.out.append(f'\\raggedleft {prefix}')
        self.context.append(suffix)
    
    def depart_attribution(self, node) -> None:
        self.out.append(self.context.pop() + '\n')
        self.duclass_close(node)
    
    def visit_status(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_status(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def visit_strong(self, node) -> None:
        self.out.append('\\textbf{')
        self.visit_inline(node)
    
    def depart_strong(self, node) -> None:
        self.depart_inline(node)
        self.out.append('}')
    
    def visit_substitution_definition(self, node):
        raise nodes.SkipNode
    
    def visit_substitution_reference(self, node) -> None:
        self.unimplemented_visit(node)
    
    def visit_subtitle(self, node) -> None:
        if isinstance(node.parent, nodes.document):
            self.push_output_collector(self.subtitle)
            self.provide_fallback('documentsubtitle')
            protect = self.settings.documentclass == 'memoir'
            self.subtitle_labels += self.ids_to_labels(node, set_anchor=False, protect=protect)
        elif isinstance(node.parent, nodes.section):
            self.out.append('\\%s*{' % self.d_class.section(self.section_level + 1))
        else:
            self.provide_fallback('subtitle')
            self.out.append('\n\\DUsubtitle{')
    
    def depart_subtitle(self, node) -> None:
        if isinstance(node.parent, nodes.document):
            self.pop_output_collector()
        else:
            self.out.append('}\n')
    
    def visit_system_message(self, node) -> None:
        self.requirements['color'] = PreambleCmds.color
        self.provide_fallback('title')
        if self.settings.legacy_class_functions:
            self.fallbacks['title'] = PreambleCmds.title_legacy
        node['classes'] = ['system-message']
        self.out.append('\n')
        self.append_hypertargets(node)
        self.visit_admonition(node)
        if self.settings.legacy_class_functions:
            self.out.append('\n\\DUtitle[system-message]{\\color{red}System Message}\n')
        else:
            self.out.append('\n\\DUtitle{\\color{red}System Message}\n')
        try:
            line = f", line~{node['line']}"
        except KeyError:
            line = ''
        self.out.append(f"\n{node['type']}/{node['level']} in \\texttt{{{self.encode(node['source'])}}}{line}\n")
        if len(node['backrefs']) == 1:
            self.out.append(f"\n\\hyperlink{{{node['backrefs'][0]}}}{{")
            self.context.append('}\n')
        else:
            backrefs = [f'\\hyperlink{{{href}}}{{{i + 1}}}\n' for (i, href) in enumerate(node['backrefs'])]
            self.context.append('backrefs: ' + ' '.join(backrefs))
    
    def depart_system_message(self, node) -> None:
        self.out.append(self.context.pop())
        self.depart_admonition(node)
    
    def visit_table(self, node) -> None:
        self.requirements['table'] = PreambleCmds.table
        if not self.settings.legacy_column_widths:
            self.requirements['table1'] = PreambleCmds.table_columnwidth
        if self.active_table.is_open():
            self.table_stack.append(self.active_table)
            self.active_table = Table(self, 'tabular')
        if (self.active_table._latex_type == 'longtable' and isinstance(node.parent, nodes.section) and node.parent.index(node) == 1 and 'paragraph' in self.d_class.section(self.section_level)):
            self.out.append('\\leavevmode')
        self.active_table.open()
        self.active_table.set_table_style(node, self.settings)
        if self.active_table.borders == 'booktabs':
            self.requirements['booktabs'] = '\\usepackage{booktabs}'
        self.push_output_collector([])
    
    def depart_table(self, node) -> None:
        content = self.pop_output_collector()
        try:
            width = self.to_latex_length(node['width'], node)
        except KeyError:
            width = '\\linewidth'
        if not self.active_table.caption:
            set_anchor = len(self.table_stack) != 1
            self.out += self.ids_to_labels(node, set_anchor, pre_nl=True)
        self.duclass_open(node)
        self.out.append(self.active_table.get_opening(width))
        self.out += content
        self.out.append(self.active_table.get_closing() + '\n')
        self.active_table.close()
        if len(self.table_stack) > 0:
            self.active_table = self.table_stack.pop()
        self.duclass_close(node)
    
    def visit_target(self, node) -> None:
        if ('refuri' in node or 'refid' in node or 'refname' in node):
            return
        if self.is_inline(node):
            self.out.append('%')
        self.out.append('\n')
        self.visit_inline(node)
    
    def depart_target(self, node) -> None:
        self.depart_inline(node)
    
    def visit_tbody(self, node) -> None:
        if not self.active_table.get('preamble written'):
            self.visit_thead(node)
            self.depart_thead(None)
    
    def depart_tbody(self, node) -> None:
        pass
    
    def visit_term(self, node) -> None:
        """definition list term"""
        self.out.append('\\item[{')
    
    def depart_term(self, node) -> None:
        self.out.append('}] ')
        next_node = node.next_node(descend=False, siblings=True)
        if isinstance(next_node, nodes.term):
            self.out.append('\n')
        elif not isinstance(next_node, nodes.classifier):
            self.out.append(self.term_postfix(next_node))
    
    def visit_tgroup(self, node) -> None:
        pass
    
    def depart_tgroup(self, node) -> None:
        pass
    _thead_depth = 0
    
    def thead_depth(self):
        return self._thead_depth
    
    def visit_thead(self, node) -> None:
        self._thead_depth += 1
        if 1 == self.thead_depth():
            self.out.append('{%s}\n' % self.active_table.get_colspecs(node))
            self.active_table.set('preamble written', 1)
        if self.active_table.caption:
            if self._thead_depth == 1:
                pre = ['\\caption{']
                post = self.ids_to_labels(node.parent.parent, False) + ['}\\\\']
            else:
                pre = ['\\caption[]{']
                post = [' (... continued)}\\\\']
            self.out.extend(pre + self.active_table.caption + post + ['\n'])
        self.out.extend(self.active_table.visit_thead())
    
    def depart_thead(self, node) -> None:
        if node is not None:
            self.out.extend(self.active_table.depart_thead())
            if self.active_table.need_recurse():
                node.walkabout(self)
        self._thead_depth -= 1
    
    def visit_title(self, node) -> None:
        """Append section and other titles."""
        if isinstance(node.parent, nodes.document):
            self.push_output_collector(self.title)
            self.context.append('')
        elif (isinstance(node.parent, nodes.topic) or isinstance(node.parent, nodes.admonition) or isinstance(node.parent, nodes.sidebar)):
            classes = (node.parent['classes'] or [node.parent.tagname])
            if self.settings.legacy_class_functions:
                self.fallbacks['title'] = PreambleCmds.title_legacy
                self.out.append('\n\\DUtitle[%s]{' % ','.join(classes))
            else:
                self.provide_fallback('title')
                self.out.append('\n\\DUtitle{')
            self.context.append('}\n')
        elif isinstance(node.parent, nodes.table):
            self.push_output_collector(self.active_table.caption)
            self.context.append('')
        else:
            level = self.section_level
            section_name = self.d_class.section(level)
            self.out.append('\n\n')
            if level > len(self.d_class.sections):
                if self.settings.legacy_class_functions:
                    self.fallbacks['title'] = PreambleCmds.title_legacy
                    section_name += '[section%s]' % RomanNumeral(level)
                else:
                    self.provide_fallback('title')
                    self.provide_fallback('duclass', 'DUclass')
                    self.out.append('\\begin{DUclass}{section%s}\n' % RomanNumeral(level))
            if 'system-messages' in node.parent['classes']:
                self.requirements['color'] = PreambleCmds.color
                section_title = self.encode(node.astext())
                self.out.append('\\%s[%s]{\\color{red}' % (section_name, section_title))
            else:
                self.out.append('\\%s{' % section_name)
            labels = self.ids_to_labels(node.parent, set_anchor=False)
            if labels:
                self.context.append('%\n  '.join(('', *labels)) + '%\n}\n')
            else:
                self.context.append('}\n')
            if (level > len(self.d_class.sections) and not self.settings.legacy_class_functions):
                self.context[-1] += '\\end{DUclass}\n'
    
    def depart_title(self, node) -> None:
        self.out.append(self.context.pop())
        if isinstance(node.parent, (nodes.table, nodes.document)):
            self.pop_output_collector()
    
    def visit_contents(self, node):
        """Write the table of contents.

        Called from visit_topic() for "contents" topics.
        """
        if (self.use_latex_toc and 'local' in node['classes']):
            section_name = self.d_class.section(self.section_level)
            minitoc_names = {'part': 'part', 'chapter': 'mini', 'section': 'sect'}
            if 'chapter' in self.d_class.sections:
                del minitoc_names['section']
            try:
                mtc_name = minitoc_names[section_name]
            except KeyError:
                self.warn('Skipping local ToC at "%s" level.\n  Feature not supported with option "use-latex-toc"' % section_name, base_node=node)
                raise nodes.SkipNode
        self.out.append('\n')
        self.out += self.ids_to_labels(node, newline=True)
        if (isinstance(node.next_node(), nodes.title) and 'local' not in node['classes'] and self.settings.documentclass != 'memoir'):
            self.out.append('\\pdfbookmark[%d]{%s}{%s}\n' % (self.section_level + 1, node.next_node().astext(), node.get('ids', ['contents'])[0]))
        if not self.use_latex_toc:
            self.fallbacks['toc-list'] = PreambleCmds.toc_list
            self.duclass_open(node)
            return
        try:
            details = node.next_node(nodes.pending).details
        except AttributeError:
            self.warn('Setting "use_latex_toc" is True but "contents" details are missing. Directive option values may be lost.')
            details = {}
        depth = details.get('depth', 0)
        maxdepth = len(self.d_class.sections)
        if isinstance(node.next_node(), nodes.title):
            title = self.encode(node[0].astext())
        else:
            title = ''
        if 'local' in node['classes']:
            self.requirements['minitoc'] = PreambleCmds.minitoc
            self.requirements['minitoc-' + mtc_name] = '\\do%stoc' % mtc_name
            self.requirements['minitoc-%s-depth' % mtc_name] = '\\mtcsetdepth{%stoc}{%d}' % (mtc_name, maxdepth)
            offset = {'sect': 1, 'mini': 0, 'part': 0}
            if 'chapter' in self.d_class.sections:
                offset['part'] = -1
            if depth:
                self.out.append('\\setcounter{%stocdepth}{%d}' % (mtc_name, depth + offset[mtc_name]))
            self.out.append('\\mtcsettitle{%stoc}{%s}\n' % (mtc_name, title))
            self.out.append('\\%stoc\n' % mtc_name)
        else:
            if depth:
                self.out.append('\\setcounter{tocdepth}{%d}\n' % self.d_class.latex_section_depth(depth))
            if title != 'Contents':
                self.out.append('\\renewcommand{\\contentsname}{%s}\n' % title)
            self.out.append('\\tableofcontents\n')
            self.has_latex_toc = True
        raise nodes.SkipNode
    
    def visit_topic(self, node) -> None:
        if 'contents' in node['classes']:
            self.visit_contents(node)
        elif ('abstract' in node['classes'] and self.settings.use_latex_abstract):
            self.push_output_collector(self.abstract)
            self.out.append('\\begin{abstract}')
            if isinstance(node.next_node(), nodes.title):
                node.pop(0)
        else:
            if 'abstract' in node['classes']:
                self.provide_fallback('abstract')
                if self.settings.legacy_class_functions:
                    self.fallbacks['abstract'] = PreambleCmds.abstract_legacy
                self.push_output_collector(self.abstract)
            elif 'dedication' in node['classes']:
                self.provide_fallback('dedication')
                self.push_output_collector(self.dedication)
            else:
                node['classes'].insert(0, 'topic')
            self.visit_block_quote(node)
    
    def depart_topic(self, node) -> None:
        if ('abstract' in node['classes'] and self.settings.use_latex_abstract):
            self.out.append('\\end{abstract}\n')
        elif 'contents' in node['classes']:
            self.duclass_close(node)
        else:
            self.depart_block_quote(node)
        if ('abstract' in node['classes'] or 'dedication' in node['classes']):
            self.pop_output_collector()
    
    def visit_transition(self, node) -> None:
        self.provide_fallback('transition')
        self.out.append('\n%' + '_' * 75 + '\n')
        self.out.append('\\DUtransition\n')
    
    def depart_transition(self, node) -> None:
        pass
    
    def visit_version(self, node) -> None:
        self.visit_docinfo_item(node)
    
    def depart_version(self, node) -> None:
        self.depart_docinfo_item(node)
    
    def unimplemented_visit(self, node):
        raise NotImplementedError('visiting unimplemented node type: %s' % node.__class__.__name__)



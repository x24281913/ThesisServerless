"""
    pygments.filters
    ~~~~~~~~~~~~~~~~

    Module containing filter lookup functions and default
    filters.

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
from pygments.token import String, Comment, Keyword, Name, Error, Whitespace, string_to_tokentype
from pygments.filter import Filter
from pygments.util import get_list_opt, get_int_opt, get_bool_opt, get_choice_opt, ClassNotFound, OptionError
from pygments.plugin import find_plugin_filters

def find_filter_class(filtername):
    """Lookup a filter by name. Return None if not found."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.filters.__init__.find_filter_class', 'find_filter_class(filtername)', {'FILTERS': FILTERS, 'find_plugin_filters': find_plugin_filters, 'filtername': filtername}, 1)

def get_filter_by_name(filtername, **options):
    """Return an instantiated filter.

    Options are passed to the filter initializer if wanted.
    Raise a ClassNotFound if not found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.filters.__init__.get_filter_by_name', 'get_filter_by_name(filtername, **options)', {'find_filter_class': find_filter_class, 'ClassNotFound': ClassNotFound, 'filtername': filtername, 'options': options}, 1)

def get_all_filters():
    """Return a generator of all filter names."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.filters.__init__.get_all_filters', 'get_all_filters()', {'FILTERS': FILTERS, 'find_plugin_filters': find_plugin_filters}, 0)

def _replace_special(ttype, value, regex, specialttype, replacefunc=lambda x: x):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('pygments.filters.__init__._replace_special', '_replace_special(ttype, value, regex, specialttype, replacefunc=lambda x: x)', {'ttype': ttype, 'value': value, 'regex': regex, 'specialttype': specialttype, 'replacefunc': replacefunc}, 0)


class CodeTagFilter(Filter):
    """Highlight special code tags in comments and docstrings.

    Options accepted:

    `codetags` : list of strings
       A list of strings that are flagged as code tags.  The default is to
       highlight ``XXX``, ``TODO``, ``FIXME``, ``BUG`` and ``NOTE``.

    .. versionchanged:: 2.13
       Now recognizes ``FIXME`` by default.
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        tags = get_list_opt(options, 'codetags', ['XXX', 'TODO', 'FIXME', 'BUG', 'NOTE'])
        self.tag_re = re.compile('\\b({})\\b'.format('|'.join([re.escape(tag) for tag in tags if tag])))
    
    def filter(self, lexer, stream):
        regex = self.tag_re
        for (ttype, value) in stream:
            if (ttype in String.Doc or (ttype in Comment and ttype not in Comment.Preproc)):
                yield from _replace_special(ttype, value, regex, Comment.Special)
            else:
                yield (ttype, value)



class SymbolFilter(Filter):
    """Convert mathematical symbols into Unicode characters.

    Examples are ``\<longrightarrow>`` in Isabelle or
    ``\longrightarrow`` in LaTeX.

    This is mostly useful for HTML or console output when you want to
    approximate the source rendering you'd see in an IDE.

    Options accepted:

    `lang` : string
       The symbol language. Must be one of ``'isabelle'`` or
       ``'latex'``.  The default is ``'isabelle'``.
    """
    latex_symbols = {'\\alpha': 'α', '\\beta': 'β', '\\gamma': 'γ', '\\delta': 'δ', '\\varepsilon': 'ε', '\\zeta': 'ζ', '\\eta': 'η', '\\vartheta': 'θ', '\\iota': 'ι', '\\kappa': 'κ', '\\lambda': 'λ', '\\mu': 'μ', '\\nu': 'ν', '\\xi': 'ξ', '\\pi': 'π', '\\varrho': 'ρ', '\\sigma': 'σ', '\\tau': 'τ', '\\upsilon': 'υ', '\\varphi': 'φ', '\\chi': 'χ', '\\psi': 'ψ', '\\omega': 'ω', '\\Gamma': 'Γ', '\\Delta': 'Δ', '\\Theta': 'Θ', '\\Lambda': 'Λ', '\\Xi': 'Ξ', '\\Pi': 'Π', '\\Sigma': 'Σ', '\\Upsilon': 'Υ', '\\Phi': 'Φ', '\\Psi': 'Ψ', '\\Omega': 'Ω', '\\leftarrow': '←', '\\longleftarrow': '⟵', '\\rightarrow': '→', '\\longrightarrow': '⟶', '\\Leftarrow': '⇐', '\\Longleftarrow': '⟸', '\\Rightarrow': '⇒', '\\Longrightarrow': '⟹', '\\leftrightarrow': '↔', '\\longleftrightarrow': '⟷', '\\Leftrightarrow': '⇔', '\\Longleftrightarrow': '⟺', '\\mapsto': '↦', '\\longmapsto': '⟼', '\\relbar': '─', '\\Relbar': '═', '\\hookleftarrow': '↩', '\\hookrightarrow': '↪', '\\leftharpoondown': '↽', '\\rightharpoondown': '⇁', '\\leftharpoonup': '↼', '\\rightharpoonup': '⇀', '\\rightleftharpoons': '⇌', '\\leadsto': '↝', '\\downharpoonleft': '⇃', '\\downharpoonright': '⇂', '\\upharpoonleft': '↿', '\\upharpoonright': '↾', '\\restriction': '↾', '\\uparrow': '↑', '\\Uparrow': '⇑', '\\downarrow': '↓', '\\Downarrow': '⇓', '\\updownarrow': '↕', '\\Updownarrow': '⇕', '\\langle': '⟨', '\\rangle': '⟩', '\\lceil': '⌈', '\\rceil': '⌉', '\\lfloor': '⌊', '\\rfloor': '⌋', '\\flqq': '«', '\\frqq': '»', '\\bot': '⊥', '\\top': '⊤', '\\wedge': '∧', '\\bigwedge': '⋀', '\\vee': '∨', '\\bigvee': '⋁', '\\forall': '∀', '\\exists': '∃', '\\nexists': '∄', '\\neg': '¬', '\\Box': '□', '\\Diamond': '◇', '\\vdash': '⊢', '\\models': '⊨', '\\dashv': '⊣', '\\surd': '√', '\\le': '≤', '\\ge': '≥', '\\ll': '≪', '\\gg': '≫', '\\lesssim': '≲', '\\gtrsim': '≳', '\\lessapprox': '⪅', '\\gtrapprox': '⪆', '\\in': '∈', '\\notin': '∉', '\\subset': '⊂', '\\supset': '⊃', '\\subseteq': '⊆', '\\supseteq': '⊇', '\\sqsubset': '⊏', '\\sqsupset': '⊐', '\\sqsubseteq': '⊑', '\\sqsupseteq': '⊒', '\\cap': '∩', '\\bigcap': '⋂', '\\cup': '∪', '\\bigcup': '⋃', '\\sqcup': '⊔', '\\bigsqcup': '⨆', '\\sqcap': '⊓', '\\Bigsqcap': '⨅', '\\setminus': '∖', '\\propto': '∝', '\\uplus': '⊎', '\\bigplus': '⨄', '\\sim': '∼', '\\doteq': '≐', '\\simeq': '≃', '\\approx': '≈', '\\asymp': '≍', '\\cong': '≅', '\\equiv': '≡', '\\Join': '⋈', '\\bowtie': '⨝', '\\prec': '≺', '\\succ': '≻', '\\preceq': '≼', '\\succeq': '≽', '\\parallel': '∥', '\\mid': '¦', '\\pm': '±', '\\mp': '∓', '\\times': '×', '\\div': '÷', '\\cdot': '⋅', '\\star': '⋆', '\\circ': '∘', '\\dagger': '†', '\\ddagger': '‡', '\\lhd': '⊲', '\\rhd': '⊳', '\\unlhd': '⊴', '\\unrhd': '⊵', '\\triangleleft': '◃', '\\triangleright': '▹', '\\triangle': '△', '\\triangleq': '≜', '\\oplus': '⊕', '\\bigoplus': '⨁', '\\otimes': '⊗', '\\bigotimes': '⨂', '\\odot': '⊙', '\\bigodot': '⨀', '\\ominus': '⊖', '\\oslash': '⊘', '\\dots': '…', '\\cdots': '⋯', '\\sum': '∑', '\\prod': '∏', '\\coprod': '∐', '\\infty': '∞', '\\int': '∫', '\\oint': '∮', '\\clubsuit': '♣', '\\diamondsuit': '♢', '\\heartsuit': '♡', '\\spadesuit': '♠', '\\aleph': 'ℵ', '\\emptyset': '∅', '\\nabla': '∇', '\\partial': '∂', '\\flat': '♭', '\\natural': '♮', '\\sharp': '♯', '\\angle': '∠', '\\copyright': '©', '\\textregistered': '®', '\\textonequarter': '¼', '\\textonehalf': '½', '\\textthreequarters': '¾', '\\textordfeminine': 'ª', '\\textordmasculine': 'º', '\\euro': '€', '\\pounds': '£', '\\yen': '¥', '\\textcent': '¢', '\\textcurrency': '¤', '\\textdegree': '°'}
    isabelle_symbols = {'\\<zero>': '𝟬', '\\<one>': '𝟭', '\\<two>': '𝟮', '\\<three>': '𝟯', '\\<four>': '𝟰', '\\<five>': '𝟱', '\\<six>': '𝟲', '\\<seven>': '𝟳', '\\<eight>': '𝟴', '\\<nine>': '𝟵', '\\<A>': '𝒜', '\\<B>': 'ℬ', '\\<C>': '𝒞', '\\<D>': '𝒟', '\\<E>': 'ℰ', '\\<F>': 'ℱ', '\\<G>': '𝒢', '\\<H>': 'ℋ', '\\<I>': 'ℐ', '\\<J>': '𝒥', '\\<K>': '𝒦', '\\<L>': 'ℒ', '\\<M>': 'ℳ', '\\<N>': '𝒩', '\\<O>': '𝒪', '\\<P>': '𝒫', '\\<Q>': '𝒬', '\\<R>': 'ℛ', '\\<S>': '𝒮', '\\<T>': '𝒯', '\\<U>': '𝒰', '\\<V>': '𝒱', '\\<W>': '𝒲', '\\<X>': '𝒳', '\\<Y>': '𝒴', '\\<Z>': '𝒵', '\\<a>': '𝖺', '\\<b>': '𝖻', '\\<c>': '𝖼', '\\<d>': '𝖽', '\\<e>': '𝖾', '\\<f>': '𝖿', '\\<g>': '𝗀', '\\<h>': '𝗁', '\\<i>': '𝗂', '\\<j>': '𝗃', '\\<k>': '𝗄', '\\<l>': '𝗅', '\\<m>': '𝗆', '\\<n>': '𝗇', '\\<o>': '𝗈', '\\<p>': '𝗉', '\\<q>': '𝗊', '\\<r>': '𝗋', '\\<s>': '𝗌', '\\<t>': '𝗍', '\\<u>': '𝗎', '\\<v>': '𝗏', '\\<w>': '𝗐', '\\<x>': '𝗑', '\\<y>': '𝗒', '\\<z>': '𝗓', '\\<AA>': '𝔄', '\\<BB>': '𝔅', '\\<CC>': 'ℭ', '\\<DD>': '𝔇', '\\<EE>': '𝔈', '\\<FF>': '𝔉', '\\<GG>': '𝔊', '\\<HH>': 'ℌ', '\\<II>': 'ℑ', '\\<JJ>': '𝔍', '\\<KK>': '𝔎', '\\<LL>': '𝔏', '\\<MM>': '𝔐', '\\<NN>': '𝔑', '\\<OO>': '𝔒', '\\<PP>': '𝔓', '\\<QQ>': '𝔔', '\\<RR>': 'ℜ', '\\<SS>': '𝔖', '\\<TT>': '𝔗', '\\<UU>': '𝔘', '\\<VV>': '𝔙', '\\<WW>': '𝔚', '\\<XX>': '𝔛', '\\<YY>': '𝔜', '\\<ZZ>': 'ℨ', '\\<aa>': '𝔞', '\\<bb>': '𝔟', '\\<cc>': '𝔠', '\\<dd>': '𝔡', '\\<ee>': '𝔢', '\\<ff>': '𝔣', '\\<gg>': '𝔤', '\\<hh>': '𝔥', '\\<ii>': '𝔦', '\\<jj>': '𝔧', '\\<kk>': '𝔨', '\\<ll>': '𝔩', '\\<mm>': '𝔪', '\\<nn>': '𝔫', '\\<oo>': '𝔬', '\\<pp>': '𝔭', '\\<qq>': '𝔮', '\\<rr>': '𝔯', '\\<ss>': '𝔰', '\\<tt>': '𝔱', '\\<uu>': '𝔲', '\\<vv>': '𝔳', '\\<ww>': '𝔴', '\\<xx>': '𝔵', '\\<yy>': '𝔶', '\\<zz>': '𝔷', '\\<alpha>': 'α', '\\<beta>': 'β', '\\<gamma>': 'γ', '\\<delta>': 'δ', '\\<epsilon>': 'ε', '\\<zeta>': 'ζ', '\\<eta>': 'η', '\\<theta>': 'θ', '\\<iota>': 'ι', '\\<kappa>': 'κ', '\\<lambda>': 'λ', '\\<mu>': 'μ', '\\<nu>': 'ν', '\\<xi>': 'ξ', '\\<pi>': 'π', '\\<rho>': 'ρ', '\\<sigma>': 'σ', '\\<tau>': 'τ', '\\<upsilon>': 'υ', '\\<phi>': 'φ', '\\<chi>': 'χ', '\\<psi>': 'ψ', '\\<omega>': 'ω', '\\<Gamma>': 'Γ', '\\<Delta>': 'Δ', '\\<Theta>': 'Θ', '\\<Lambda>': 'Λ', '\\<Xi>': 'Ξ', '\\<Pi>': 'Π', '\\<Sigma>': 'Σ', '\\<Upsilon>': 'Υ', '\\<Phi>': 'Φ', '\\<Psi>': 'Ψ', '\\<Omega>': 'Ω', '\\<bool>': '𝔹', '\\<complex>': 'ℂ', '\\<nat>': 'ℕ', '\\<rat>': 'ℚ', '\\<real>': 'ℝ', '\\<int>': 'ℤ', '\\<leftarrow>': '←', '\\<longleftarrow>': '⟵', '\\<rightarrow>': '→', '\\<longrightarrow>': '⟶', '\\<Leftarrow>': '⇐', '\\<Longleftarrow>': '⟸', '\\<Rightarrow>': '⇒', '\\<Longrightarrow>': '⟹', '\\<leftrightarrow>': '↔', '\\<longleftrightarrow>': '⟷', '\\<Leftrightarrow>': '⇔', '\\<Longleftrightarrow>': '⟺', '\\<mapsto>': '↦', '\\<longmapsto>': '⟼', '\\<midarrow>': '─', '\\<Midarrow>': '═', '\\<hookleftarrow>': '↩', '\\<hookrightarrow>': '↪', '\\<leftharpoondown>': '↽', '\\<rightharpoondown>': '⇁', '\\<leftharpoonup>': '↼', '\\<rightharpoonup>': '⇀', '\\<rightleftharpoons>': '⇌', '\\<leadsto>': '↝', '\\<downharpoonleft>': '⇃', '\\<downharpoonright>': '⇂', '\\<upharpoonleft>': '↿', '\\<upharpoonright>': '↾', '\\<restriction>': '↾', '\\<Colon>': '∷', '\\<up>': '↑', '\\<Up>': '⇑', '\\<down>': '↓', '\\<Down>': '⇓', '\\<updown>': '↕', '\\<Updown>': '⇕', '\\<langle>': '⟨', '\\<rangle>': '⟩', '\\<lceil>': '⌈', '\\<rceil>': '⌉', '\\<lfloor>': '⌊', '\\<rfloor>': '⌋', '\\<lparr>': '⦇', '\\<rparr>': '⦈', '\\<lbrakk>': '⟦', '\\<rbrakk>': '⟧', '\\<lbrace>': '⦃', '\\<rbrace>': '⦄', '\\<guillemotleft>': '«', '\\<guillemotright>': '»', '\\<bottom>': '⊥', '\\<top>': '⊤', '\\<and>': '∧', '\\<And>': '⋀', '\\<or>': '∨', '\\<Or>': '⋁', '\\<forall>': '∀', '\\<exists>': '∃', '\\<nexists>': '∄', '\\<not>': '¬', '\\<box>': '□', '\\<diamond>': '◇', '\\<turnstile>': '⊢', '\\<Turnstile>': '⊨', '\\<tturnstile>': '⊩', '\\<TTurnstile>': '⊫', '\\<stileturn>': '⊣', '\\<surd>': '√', '\\<le>': '≤', '\\<ge>': '≥', '\\<lless>': '≪', '\\<ggreater>': '≫', '\\<lesssim>': '≲', '\\<greatersim>': '≳', '\\<lessapprox>': '⪅', '\\<greaterapprox>': '⪆', '\\<in>': '∈', '\\<notin>': '∉', '\\<subset>': '⊂', '\\<supset>': '⊃', '\\<subseteq>': '⊆', '\\<supseteq>': '⊇', '\\<sqsubset>': '⊏', '\\<sqsupset>': '⊐', '\\<sqsubseteq>': '⊑', '\\<sqsupseteq>': '⊒', '\\<inter>': '∩', '\\<Inter>': '⋂', '\\<union>': '∪', '\\<Union>': '⋃', '\\<squnion>': '⊔', '\\<Squnion>': '⨆', '\\<sqinter>': '⊓', '\\<Sqinter>': '⨅', '\\<setminus>': '∖', '\\<propto>': '∝', '\\<uplus>': '⊎', '\\<Uplus>': '⨄', '\\<noteq>': '≠', '\\<sim>': '∼', '\\<doteq>': '≐', '\\<simeq>': '≃', '\\<approx>': '≈', '\\<asymp>': '≍', '\\<cong>': '≅', '\\<smile>': '⌣', '\\<equiv>': '≡', '\\<frown>': '⌢', '\\<Join>': '⋈', '\\<bowtie>': '⨝', '\\<prec>': '≺', '\\<succ>': '≻', '\\<preceq>': '≼', '\\<succeq>': '≽', '\\<parallel>': '∥', '\\<bar>': '¦', '\\<plusminus>': '±', '\\<minusplus>': '∓', '\\<times>': '×', '\\<div>': '÷', '\\<cdot>': '⋅', '\\<star>': '⋆', '\\<bullet>': '∙', '\\<circ>': '∘', '\\<dagger>': '†', '\\<ddagger>': '‡', '\\<lhd>': '⊲', '\\<rhd>': '⊳', '\\<unlhd>': '⊴', '\\<unrhd>': '⊵', '\\<triangleleft>': '◃', '\\<triangleright>': '▹', '\\<triangle>': '△', '\\<triangleq>': '≜', '\\<oplus>': '⊕', '\\<Oplus>': '⨁', '\\<otimes>': '⊗', '\\<Otimes>': '⨂', '\\<odot>': '⊙', '\\<Odot>': '⨀', '\\<ominus>': '⊖', '\\<oslash>': '⊘', '\\<dots>': '…', '\\<cdots>': '⋯', '\\<Sum>': '∑', '\\<Prod>': '∏', '\\<Coprod>': '∐', '\\<infinity>': '∞', '\\<integral>': '∫', '\\<ointegral>': '∮', '\\<clubsuit>': '♣', '\\<diamondsuit>': '♢', '\\<heartsuit>': '♡', '\\<spadesuit>': '♠', '\\<aleph>': 'ℵ', '\\<emptyset>': '∅', '\\<nabla>': '∇', '\\<partial>': '∂', '\\<flat>': '♭', '\\<natural>': '♮', '\\<sharp>': '♯', '\\<angle>': '∠', '\\<copyright>': '©', '\\<registered>': '®', '\\<hyphen>': '\xad', '\\<inverse>': '¯', '\\<onequarter>': '¼', '\\<onehalf>': '½', '\\<threequarters>': '¾', '\\<ordfeminine>': 'ª', '\\<ordmasculine>': 'º', '\\<section>': '§', '\\<paragraph>': '¶', '\\<exclamdown>': '¡', '\\<questiondown>': '¿', '\\<euro>': '€', '\\<pounds>': '£', '\\<yen>': '¥', '\\<cent>': '¢', '\\<currency>': '¤', '\\<degree>': '°', '\\<amalg>': '⨿', '\\<mho>': '℧', '\\<lozenge>': '◊', '\\<wp>': '℘', '\\<wrong>': '≀', '\\<struct>': '⋄', '\\<acute>': '´', '\\<index>': 'ı', '\\<dieresis>': '¨', '\\<cedilla>': '¸', '\\<hungarumlaut>': '˝', '\\<some>': 'ϵ', '\\<newline>': '⏎', '\\<open>': '‹', '\\<close>': '›', '\\<here>': '⌂', '\\<^sub>': '⇩', '\\<^sup>': '⇧', '\\<^bold>': '❙', '\\<^bsub>': '⇘', '\\<^esub>': '⇙', '\\<^bsup>': '⇗', '\\<^esup>': '⇖'}
    lang_map = {'isabelle': isabelle_symbols, 'latex': latex_symbols}
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        lang = get_choice_opt(options, 'lang', ['isabelle', 'latex'], 'isabelle')
        self.symbols = self.lang_map[lang]
    
    def filter(self, lexer, stream):
        for (ttype, value) in stream:
            if value in self.symbols:
                yield (ttype, self.symbols[value])
            else:
                yield (ttype, value)



class KeywordCaseFilter(Filter):
    """Convert keywords to lowercase or uppercase or capitalize them.

    This means first letter uppercase, rest lowercase.

    This can be useful e.g. if you highlight Pascal code and want to adapt the
    code to your styleguide.

    Options accepted:

    `case` : string
       The casing to convert keywords to. Must be one of ``'lower'``,
       ``'upper'`` or ``'capitalize'``.  The default is ``'lower'``.
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        case = get_choice_opt(options, 'case', ['lower', 'upper', 'capitalize'], 'lower')
        self.convert = getattr(str, case)
    
    def filter(self, lexer, stream):
        for (ttype, value) in stream:
            if ttype in Keyword:
                yield (ttype, self.convert(value))
            else:
                yield (ttype, value)



class NameHighlightFilter(Filter):
    """Highlight a normal Name (and Name.*) token with a different token type.

    Example::

        filter = NameHighlightFilter(
            names=['foo', 'bar', 'baz'],
            tokentype=Name.Function,
        )

    This would highlight the names "foo", "bar" and "baz"
    as functions. `Name.Function` is the default token type.

    Options accepted:

    `names` : list of strings
      A list of names that should be given the different token type.
      There is no default.
    `tokentype` : TokenType or string
      A token type or a string containing a token type name that is
      used for highlighting the strings in `names`.  The default is
      `Name.Function`.
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        self.names = set(get_list_opt(options, 'names', []))
        tokentype = options.get('tokentype')
        if tokentype:
            self.tokentype = string_to_tokentype(tokentype)
        else:
            self.tokentype = Name.Function
    
    def filter(self, lexer, stream):
        for (ttype, value) in stream:
            if (ttype in Name and value in self.names):
                yield (self.tokentype, value)
            else:
                yield (ttype, value)



class ErrorToken(Exception):
    pass



class RaiseOnErrorTokenFilter(Filter):
    """Raise an exception when the lexer generates an error token.

    Options accepted:

    `excclass` : Exception class
      The exception class to raise.
      The default is `pygments.filters.ErrorToken`.

    .. versionadded:: 0.8
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        self.exception = options.get('excclass', ErrorToken)
        try:
            if not issubclass(self.exception, Exception):
                raise TypeError
        except TypeError:
            raise OptionError('excclass option is not an exception class')
    
    def filter(self, lexer, stream):
        for (ttype, value) in stream:
            if ttype is Error:
                raise self.exception(value)
            yield (ttype, value)



class VisibleWhitespaceFilter(Filter):
    """Convert tabs, newlines and/or spaces to visible characters.

    Options accepted:

    `spaces` : string or bool
      If this is a one-character string, spaces will be replaces by this string.
      If it is another true value, spaces will be replaced by ``·`` (unicode
      MIDDLE DOT).  If it is a false value, spaces will not be replaced.  The
      default is ``False``.
    `tabs` : string or bool
      The same as for `spaces`, but the default replacement character is ``»``
      (unicode RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK).  The default value
      is ``False``.  Note: this will not work if the `tabsize` option for the
      lexer is nonzero, as tabs will already have been expanded then.
    `tabsize` : int
      If tabs are to be replaced by this filter (see the `tabs` option), this
      is the total number of characters that a tab should be expanded to.
      The default is ``8``.
    `newlines` : string or bool
      The same as for `spaces`, but the default replacement character is ``¶``
      (unicode PILCROW SIGN).  The default value is ``False``.
    `wstokentype` : bool
      If true, give whitespace the special `Whitespace` token type.  This allows
      styling the visible whitespace differently (e.g. greyed out), but it can
      disrupt background colors.  The default is ``True``.

    .. versionadded:: 0.8
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        for (name, default) in [('spaces', '·'), ('tabs', '»'), ('newlines', '¶')]:
            opt = options.get(name, False)
            if (isinstance(opt, str) and len(opt) == 1):
                setattr(self, name, opt)
            else:
                setattr(self, name, ((opt and default) or ''))
        tabsize = get_int_opt(options, 'tabsize', 8)
        if self.tabs:
            self.tabs += ' ' * (tabsize - 1)
        if self.newlines:
            self.newlines += '\n'
        self.wstt = get_bool_opt(options, 'wstokentype', True)
    
    def filter(self, lexer, stream):
        if self.wstt:
            spaces = (self.spaces or ' ')
            tabs = (self.tabs or '\t')
            newlines = (self.newlines or '\n')
            regex = re.compile('\\s')
            
            def replacefunc(wschar):
                if wschar == ' ':
                    return spaces
                elif wschar == '\t':
                    return tabs
                elif wschar == '\n':
                    return newlines
                return wschar
            for (ttype, value) in stream:
                yield from _replace_special(ttype, value, regex, Whitespace, replacefunc)
        else:
            (spaces, tabs, newlines) = (self.spaces, self.tabs, self.newlines)
            for (ttype, value) in stream:
                if spaces:
                    value = value.replace(' ', spaces)
                if tabs:
                    value = value.replace('\t', tabs)
                if newlines:
                    value = value.replace('\n', newlines)
                yield (ttype, value)



class GobbleFilter(Filter):
    """Gobble source code lines (eats initial characters).

    This filter drops the first ``n`` characters off every line of code.  This
    may be useful when the source code fed to the lexer is indented by a fixed
    amount of space that isn't desired in the output.

    Options accepted:

    `n` : int
       The number of characters to gobble.

    .. versionadded:: 1.2
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
        self.n = get_int_opt(options, 'n', 0)
    
    def gobble(self, value, left):
        if left < len(value):
            return (value[left:], 0)
        else:
            return ('', left - len(value))
    
    def filter(self, lexer, stream):
        n = self.n
        left = n
        for (ttype, value) in stream:
            parts = value.split('\n')
            (parts[0], left) = self.gobble(parts[0], left)
            for i in range(1, len(parts)):
                (parts[i], left) = self.gobble(parts[i], n)
            value = '\n'.join(parts)
            if value != '':
                yield (ttype, value)



class TokenMergeFilter(Filter):
    """Merge consecutive tokens with the same token type in the output stream.

    .. versionadded:: 1.2
    """
    
    def __init__(self, **options):
        Filter.__init__(self, **options)
    
    def filter(self, lexer, stream):
        current_type = None
        current_value = None
        for (ttype, value) in stream:
            if ttype is current_type:
                current_value += value
            else:
                if current_type is not None:
                    yield (current_type, current_value)
                current_type = ttype
                current_value = value
        if current_type is not None:
            yield (current_type, current_value)

FILTERS = {'codetagify': CodeTagFilter, 'keywordcase': KeywordCaseFilter, 'highlight': NameHighlightFilter, 'raiseonerror': RaiseOnErrorTokenFilter, 'whitespace': VisibleWhitespaceFilter, 'gobble': GobbleFilter, 'tokenmerge': TokenMergeFilter, 'symbols': SymbolFilter}


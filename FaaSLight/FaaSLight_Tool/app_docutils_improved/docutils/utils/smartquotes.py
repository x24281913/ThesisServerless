"""
=========================
Smart Quotes for Docutils
=========================

Synopsis
========

"SmartyPants" is a free web publishing plug-in for Movable Type, Blosxom, and
BBEdit that easily translates plain ASCII punctuation characters into "smart"
typographic punctuation characters.

``smartquotes.py`` is an adaption of "SmartyPants" to Docutils_.

* Using Unicode instead of HTML entities for typographic punctuation
  characters, it works for any output format that supports Unicode.
* Supports `language specific quote characters`__.

__ https://en.wikipedia.org/wiki/Non-English_usage_of_quotation_marks


Authors
=======

`John Gruber`_ did all of the hard work of writing this software in Perl for
`Movable Type`_ and almost all of this useful documentation.  `Chad Miller`_
ported it to Python to use with Pyblosxom_.
Adapted to Docutils_ by Günter Milde.

Additional Credits
==================

Portions of the SmartyPants original work are based on Brad Choate's nifty
MTRegex plug-in.  `Brad Choate`_ also contributed a few bits of source code to
this plug-in.  Brad Choate is a fine hacker indeed.

`Jeremy Hedley`_ and `Charles Wiltgen`_ deserve mention for exemplary beta
testing of the original SmartyPants.

`Rael Dornfest`_ ported SmartyPants to Blosxom.

.. _Brad Choate: http://bradchoate.com/
.. _Jeremy Hedley: http://antipixel.com/
.. _Charles Wiltgen: http://playbacktime.com/
.. _Rael Dornfest: http://raelity.org/


Copyright and License
=====================

SmartyPants_ license (3-Clause BSD license):

  Copyright (c) 2003 John Gruber (http://daringfireball.net/)
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are
  met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  * Neither the name "SmartyPants" nor the names of its contributors
    may be used to endorse or promote products derived from this
    software without specific prior written permission.

  This software is provided by the copyright holders and contributors
  "as is" and any express or implied warranties, including, but not
  limited to, the implied warranties of merchantability and fitness for
  a particular purpose are disclaimed. In no event shall the copyright
  owner or contributors be liable for any direct, indirect, incidental,
  special, exemplary, or consequential damages (including, but not
  limited to, procurement of substitute goods or services; loss of use,
  data, or profits; or business interruption) however caused and on any
  theory of liability, whether in contract, strict liability, or tort
  (including negligence or otherwise) arising in any way out of the use
  of this software, even if advised of the possibility of such damage.

smartypants.py license (2-Clause BSD license):

  smartypants.py is a derivative work of SmartyPants.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are
  met:

  * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

  This software is provided by the copyright holders and contributors
  "as is" and any express or implied warranties, including, but not
  limited to, the implied warranties of merchantability and fitness for
  a particular purpose are disclaimed. In no event shall the copyright
  owner or contributors be liable for any direct, indirect, incidental,
  special, exemplary, or consequential damages (including, but not
  limited to, procurement of substitute goods or services; loss of use,
  data, or profits; or business interruption) however caused and on any
  theory of liability, whether in contract, strict liability, or tort
  (including negligence or otherwise) arising in any way out of the use
  of this software, even if advised of the possibility of such damage.

.. _John Gruber: http://daringfireball.net/
.. _Chad Miller: http://web.chad.org/

.. _Pyblosxom: http://pyblosxom.bluesock.org/
.. _SmartyPants: http://daringfireball.net/projects/smartypants/
.. _Movable Type: http://www.movabletype.org/
.. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause
.. _Docutils: https://docutils.sourceforge.io/

Description
===========

SmartyPants can perform the following transformations:

- Straight quotes ( " and ' ) into "curly" quote characters
- Backticks-style quotes (\`\`like this'') into "curly" quote characters
- Dashes (``--`` and ``---``) into en- and em-dash entities
- Three consecutive dots (``...`` or ``. . .``) into an ellipsis ``…``.

This means you can write, edit, and save your posts using plain old
ASCII straight quotes, plain dashes, and plain dots, but your published
posts (and final HTML output) will appear with smart quotes, em-dashes,
and proper ellipses.

Backslash Escapes
=================

If you need to use literal straight quotes (or plain hyphens and periods),
`smartquotes` accepts the following backslash escape sequences to force
ASCII-punctuation. Mind, that you need two backslashes in "docstrings", as
Python expands them, too.

========  =========
Escape    Character
========  =========
``\``    \
``\"``   \"
``\'``   \'
``\.``   \.
``\-``   \-
``\```   \`
========  =========

This is useful, for example, when you want to use straight quotes as
foot and inch marks: 6\'2\" tall; a 17\" iMac.


Caveats
=======

Why You Might Not Want to Use Smart Quotes in Your Weblog
---------------------------------------------------------

For one thing, you might not care.

Most normal, mentally stable individuals do not take notice of proper
typographic punctuation. Many design and typography nerds, however, break
out in a nasty rash when they encounter, say, a restaurant sign that uses
a straight apostrophe to spell "Joe's".

If you're the sort of person who just doesn't care, you might well want to
continue not caring. Using straight quotes -- and sticking to the 7-bit
ASCII character set in general -- is certainly a simpler way to live.

Even if you *do* care about accurate typography, you still might want to
think twice before educating the quote characters in your weblog. One side
effect of publishing curly quote characters is that it makes your
weblog a bit harder for others to quote from using copy-and-paste. What
happens is that when someone copies text from your blog, the copied text
contains the 8-bit curly quote characters (as well as the 8-bit characters
for em-dashes and ellipses, if you use these options). These characters
are not standard across different text encoding methods, which is why they
need to be encoded as characters.

People copying text from your weblog, however, may not notice that you're
using curly quotes, and they'll go ahead and paste the unencoded 8-bit
characters copied from their browser into an email message or their own
weblog. When pasted as raw "smart quotes", these characters are likely to
get mangled beyond recognition.

That said, my own opinion is that any decent text editor or email client
makes it easy to stupefy smart quote characters into their 7-bit
equivalents, and I don't consider it my problem if you're using an
indecent text editor or email client.


Algorithmic Shortcomings
------------------------

One situation in which quotes will get curled the wrong way is when
apostrophes are used at the start of leading contractions. For example::

  'Twas the night before Christmas.

In the case above, SmartyPants will turn the apostrophe into an opening
secondary quote, when in fact it should be the `RIGHT SINGLE QUOTATION MARK`
character which is also "the preferred character to use for apostrophe"
(Unicode). I don't think this problem can be solved in the general case --
every word processor I've tried gets this wrong as well. In such cases, it's
best to inset the `RIGHT SINGLE QUOTATION MARK` (’) by hand.

In English, the same character is used for apostrophe and  closing secondary
quote (both plain and "smart" ones). For other locales (French, Italean,
Swiss, ...) "smart" secondary closing quotes differ from the curly apostrophe.

   .. class:: language-fr

   Il dit : "C'est 'super' !"

If the apostrophe is used at the end of a word, it cannot be distinguished
from a secondary quote by the algorithm. Therefore, a text like::

   .. class:: language-de-CH

   "Er sagt: 'Ich fass' es nicht.'"

will get a single closing guillemet instead of an apostrophe.

This can be prevented by use use of the `RIGHT SINGLE QUOTATION MARK` in
the source::

   -  "Er sagt: 'Ich fass' es nicht.'"
   +  "Er sagt: 'Ich fass’ es nicht.'"


Version History
===============

1.10    2023-11-18
        - Pre-compile regexps once, not with every call of `educateQuotes()`
          (patch #206 by Chris Sewell). Simplify regexps.

1.9     2022-03-04
        - Code cleanup. Require Python 3.

1.8.1   2017-10-25
        - Use open quote after Unicode whitespace, ZWSP, and ZWNJ.
        - Code cleanup.

1.8:    2017-04-24
        - Command line front-end.

1.7.1:  2017-03-19
        - Update and extend language-dependent quotes.
        - Differentiate apostrophe from single quote.

1.7:    2012-11-19
        - Internationalization: language-dependent quotes.

1.6.1:  2012-11-06
        - Refactor code, code cleanup,
        - `educate_tokens()` generator as interface for Docutils.

1.6:    2010-08-26
        - Adaption to Docutils:
          - Use Unicode instead of HTML entities,
          - Remove code special to pyblosxom.

1.5_1.6: Fri, 27 Jul 2007 07:06:40 -0400
        - Fixed bug where blocks of precious unalterable text was instead
          interpreted.  Thanks to Le Roux and Dirk van Oosterbosch.

1.5_1.5: Sat, 13 Aug 2005 15:50:24 -0400
        - Fix bogus magical quotation when there is no hint that the
          user wants it, e.g., in "21st century".  Thanks to Nathan Hamblen.
        - Be smarter about quotes before terminating numbers in an en-dash'ed
          range.

1.5_1.4: Thu, 10 Feb 2005 20:24:36 -0500
        - Fix a date-processing bug, as reported by jacob childress.
        - Begin a test-suite for ensuring correct output.
        - Removed import of "string", since I didn't really need it.
          (This was my first every Python program.  Sue me!)

1.5_1.3: Wed, 15 Sep 2004 18:25:58 -0400
        - Abort processing if the flavour is in forbidden-list.  Default of
          [ "rss" ]   (Idea of Wolfgang SCHNERRING.)
        - Remove stray virgules from en-dashes.  Patch by Wolfgang SCHNERRING.

1.5_1.2: Mon, 24 May 2004 08:14:54 -0400
        - Some single quotes weren't replaced properly.  Diff-tesuji played
          by Benjamin GEIGER.

1.5_1.1: Sun, 14 Mar 2004 14:38:28 -0500
        - Support upcoming pyblosxom 0.9 plugin verification feature.

1.5_1.0: Tue, 09 Mar 2004 08:08:35 -0500
        - Initial release
"""

from __future__ import annotations
import re
import sys
options = '\nOptions\n=======\n\nNumeric values are the easiest way to configure SmartyPants\' behavior:\n\n:0:     Suppress all transformations. (Do nothing.)\n\n:1:     Performs default SmartyPants transformations: quotes (including\n        \\`\\`backticks\'\' -style), em-dashes, and ellipses. "``--``" (dash dash)\n        is used to signify an em-dash; there is no support for en-dashes\n\n:2:     Same as smarty_pants="1", except that it uses the old-school typewriter\n        shorthand for dashes:  "``--``" (dash dash) for en-dashes, "``---``"\n        (dash dash dash)\n        for em-dashes.\n\n:3:     Same as smarty_pants="2", but inverts the shorthand for dashes:\n        "``--``" (dash dash) for em-dashes, and "``---``" (dash dash dash) for\n        en-dashes.\n\n:-1:    Stupefy mode. Reverses the SmartyPants transformation process, turning\n        the characters produced by SmartyPants into their ASCII equivalents.\n        E.g. the LEFT DOUBLE QUOTATION MARK (“) is turned into a simple\n        double-quote (\\"), "—" is turned into two dashes, etc.\n\n\nThe following single-character attribute values can be combined to toggle\nindividual transformations from within the smarty_pants attribute. For\nexample, ``"1"`` is equivalent to ``"qBde"``.\n\n:q:     Educates normal quote characters: (") and (\').\n\n:b:     Educates \\`\\`backticks\'\' -style double quotes.\n\n:B:     Educates \\`\\`backticks\'\' -style double quotes and \\`single\' quotes.\n\n:d:     Educates em-dashes.\n\n:D:     Educates em-dashes and en-dashes, using old-school typewriter\n        shorthand: (dash dash) for en-dashes, (dash dash dash) for em-dashes.\n\n:i:     Educates em-dashes and en-dashes, using inverted old-school typewriter\n        shorthand: (dash dash) for em-dashes, (dash dash dash) for en-dashes.\n\n:e:     Educates ellipses.\n\n:w:     Translates any instance of ``&quot;`` into a normal double-quote\n        character. This should be of no interest to most people, but\n        of particular interest to anyone who writes their posts using\n        Dreamweaver, as Dreamweaver inexplicably uses this entity to represent\n        a literal double-quote character. SmartyPants only educates normal\n        quotes, not entities (because ordinarily, entities are used for\n        the explicit purpose of representing the specific character they\n        represent). The "w" option must be used in conjunction with one (or\n        both) of the other quote options ("q" or "b"). Thus, if you wish to\n        apply all SmartyPants transformations (quotes, en- and em-dashes, and\n        ellipses) and also translate ``&quot;`` entities into regular quotes\n        so SmartyPants can educate them, you should pass the following to the\n        smarty_pants attribute:\n'


class smartchars:
    """Smart quotes and dashes"""
    endash = '–'
    emdash = '—'
    ellipsis = '…'
    apostrophe = '’'
    quotes = {'af': '“”‘’', 'af-x-altquot': '„”‚’', 'bg': '„“‚‘', 'ca': '«»“”', 'ca-x-altquot': '“”‘’', 'cs': '„“‚‘', 'cs-x-altquot': '»«›‹', 'da': '»«›‹', 'da-x-altquot': '„“‚‘', 'de': '„“‚‘', 'de-x-altquot': '»«›‹', 'de-ch': '«»‹›', 'el': '«»“”', 'en': '“”‘’', 'en-uk-x-altquot': '‘’“”', 'eo': '“”‘’', 'es': '«»“”', 'es-x-altquot': '“”‘’', 'et': '„“‚‘', 'et-x-altquot': '«»‹›', 'eu': '«»‹›', 'fi': '””’’', 'fi-x-altquot': '»»››', 'fr': ('«\xa0', '\xa0»', '“', '”'), 'fr-x-altquot': ('«\u202f', '\u202f»', '“', '”'), 'fr-ch': '«»‹›', 'fr-ch-x-altquot': ('«\u202f', '\u202f»', '‹\u202f', '\u202f›'), 'gl': '«»“”', 'he': '”“»«', 'he-x-altquot': '„”‚’', 'hr': '„”‘’', 'hr-x-altquot': '»«›‹', 'hsb': '„“‚‘', 'hsb-x-altquot': '»«›‹', 'hu': '„”«»', 'is': '„“‚‘', 'it': '«»“”', 'it-ch': '«»‹›', 'it-x-altquot': '“”‘’', 'ja': '「」『』', 'ko': '“”‘’', 'lt': '„“‚‘', 'lv': '„“‚‘', 'mk': '„“‚‘', 'nl': '“”‘’', 'nl-x-altquot': '„”‚’', 'nb': '«»’’', 'nn': '«»’’', 'nn-x-altquot': '«»‘’', 'no': '«»’’', 'no-x-altquot': '«»‘’', 'pl': '„”«»', 'pl-x-altquot': '«»‚’', 'pt': '«»“”', 'pt-br': '“”‘’', 'ro': '„”«»', 'ru': '«»„“', 'sh': '„”‚’', 'sh-x-altquot': '»«›‹', 'sk': '„“‚‘', 'sk-x-altquot': '»«›‹', 'sl': '„“‚‘', 'sl-x-altquot': '»«›‹', 'sq': '«»‹›', 'sq-x-altquot': '“„‘‚', 'sr': '„”’’', 'sr-x-altquot': '»«›‹', 'sv': '””’’', 'sv-x-altquot': '»»››', 'tr': '“”‘’', 'tr-x-altquot': '«»‹›', 'uk': '«»„“', 'uk-x-altquot': '„“‚‘', 'zh-cn': '“”‘’', 'zh-tw': '「」『』'}
    
    def __init__(self, language='en') -> None:
        self.language = language
        try:
            (self.opquote, self.cpquote, self.osquote, self.csquote) = self.quotes[language.lower()]
        except KeyError:
            (self.opquote, self.cpquote, self.osquote, self.csquote) = '""\'\''



class RegularExpressions:
    _CH_CLASSES = {'open': '[([{]', 'close': '[^\\s]', 'punct': '[-!"  #\\$\\%\'()*+,.\\/:;<=>?\\@\\[\\\\\\]\\^_`{|}~]', 'dash': '[-–—]', 'sep': '[\\s\u200b\u200c]'}
    START_SINGLE = re.compile("^'(?=%s\\\\B)" % _CH_CLASSES['punct'])
    START_DOUBLE = re.compile('^"(?=%s\\\\B)' % _CH_CLASSES['punct'])
    ADJACENT_1 = re.compile('"\'(?=\\w)')
    ADJACENT_2 = re.compile('\'"(?=\\w)')
    OPEN_SINGLE = re.compile("(%(open)s|%(dash)s)'(?=%(punct)s? )" % _CH_CLASSES)
    OPEN_DOUBLE = re.compile('(%(open)s|%(dash)s)"(?=%(punct)s? )' % _CH_CLASSES)
    DECADE = re.compile("'(?=\\d{2}s)")
    APOSTROPHE = re.compile("(?<=(\\w|\\d))'(?=\\w)")
    OPENING_SECONDARY = re.compile("\n                    (# ?<=  # look behind fails: requires fixed-width pattern\n                        %(sep)s     |  # a whitespace char, or\n                        %(open)s    |  # opening brace, or\n                        %(dash)s       # em/en-dash\n                    )\n                    '                  # the quote\n                    (?=\\w|%(punct)s)  # word character or punctuation\n                    " % _CH_CLASSES, re.VERBOSE)
    CLOSING_SECONDARY = re.compile("(?<!\\s)'")
    OPENING_PRIMARY = re.compile('\n                    (\n                        %(sep)s     |  # a whitespace char, or\n                        %(open)s    |  # zero width separating char, or\n                        %(dash)s       # em/en-dash\n                    )\n                    "                 # the quote, followed by\n                    (?=\\w|%(punct)s) # a word character or punctuation\n                    ' % _CH_CLASSES, re.VERBOSE)
    CLOSING_PRIMARY = re.compile('\n                    (\n                    (?<!\\s)" | # no whitespace before\n                    "(?=\\s)    # whitespace behind\n                    )\n                    ', re.VERBOSE)

regexes = RegularExpressions()
default_smartypants_attr = '1'

def smartyPants(text, attr=default_smartypants_attr, language='en'):
    """Main function for "traditional" use."""
    return ''.join((t for t in educate_tokens(tokenize(text), attr, language)))

def educate_tokens(text_tokens, attr=default_smartypants_attr, language='en'):
    """Return iterator that "educates" the items of `text_tokens`."""
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educate_tokens', "educate_tokens(text_tokens, attr=default_smartypants_attr, language='en')", {'processEscapes': processEscapes, 'educateDashes': educateDashes, 'educateDashesOldSchool': educateDashesOldSchool, 'educateDashesOldSchoolInverted': educateDashesOldSchoolInverted, 'educateEllipses': educateEllipses, 'educateBackticks': educateBackticks, 'educateSingleBackticks': educateSingleBackticks, 'educateQuotes': educateQuotes, 'stupefyEntities': stupefyEntities, 'text_tokens': text_tokens, 'attr': attr, 'language': language, 'default_smartypants_attr': default_smartypants_attr}, 0)

def educateQuotes(text, language='en'):
    """
    Parameter:  - text string (unicode or bytes).
                - language (`BCP 47` language tag.)
    Returns:    The `text`, with "educated" curly quote characters.

    Example input:  "Isn't this fun?"
    Example output: “Isn’t this fun?“
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateQuotes', "educateQuotes(text, language='en')", {'smartchars': smartchars, 're': re, 'regexes': regexes, 'text': text, 'language': language}, 1)

def educateBackticks(text, language='en'):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with ``backticks'' -style double quotes
                translated into HTML curly quote entities.
    Example input:  ``Isn't this fun?''
    Example output: “Isn't this fun?“
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateBackticks', "educateBackticks(text, language='en')", {'smartchars': smartchars, 'text': text, 'language': language}, 1)

def educateSingleBackticks(text, language='en'):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with `backticks' -style single quotes
                translated into HTML curly quote entities.

    Example input:  `Isn't this fun?'
    Example output: ‘Isn’t this fun?’
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateSingleBackticks', "educateSingleBackticks(text, language='en')", {'smartchars': smartchars, 'text': text, 'language': language}, 1)

def educateDashes(text):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "--" translated to
                an em-dash character.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateDashes', 'educateDashes(text)', {'smartchars': smartchars, 'text': text}, 1)

def educateDashesOldSchool(text):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "--" translated to
                an en-dash character, and each "---" translated to
                an em-dash character.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateDashesOldSchool', 'educateDashesOldSchool(text)', {'smartchars': smartchars, 'text': text}, 1)

def educateDashesOldSchoolInverted(text):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "--" translated to
                an em-dash character, and each "---" translated to
                an en-dash character. Two reasons why: First, unlike the
                en- and em-dash syntax supported by
                EducateDashesOldSchool(), it's compatible with existing
                entries written before SmartyPants 1.1, back when "--" was
                only used for em-dashes.  Second, em-dashes are more
                common than en-dashes, and so it sort of makes sense that
                the shortcut should be shorter to type. (Thanks to Aaron
                Swartz for the idea.)
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateDashesOldSchoolInverted', 'educateDashesOldSchoolInverted(text)', {'smartchars': smartchars, 'text': text}, 1)

def educateEllipses(text):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each instance of "..." translated to
                an ellipsis character.

    Example input:  Huh...?
    Example output: Huh…?
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.educateEllipses', 'educateEllipses(text)', {'smartchars': smartchars, 'text': text}, 1)

def stupefyEntities(text, language='en'):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with each SmartyPants character translated to
                its ASCII counterpart.

    Example input:  “Hello — world.”
    Example output: "Hello -- world."
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.stupefyEntities', "stupefyEntities(text, language='en')", {'smartchars': smartchars, 'text': text, 'language': language}, 1)

def processEscapes(text, restore=False):
    """
    Parameter:  String (unicode or bytes).
    Returns:    The `text`, with after processing the following backslash
                escape sequences. This is useful if you want to force a "dumb"
                quote or other character to appear.

                Escape  Value
                ------  -----
                \      &#92;
                "      &#34;
                '      &#39;
                \.      &#46;
                \-      &#45;
                \`      &#96;
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('docutils.utils.smartquotes.processEscapes', 'processEscapes(text, restore=False)', {'text': text, 'restore': restore}, 1)

def tokenize(text):
    """
    Parameter:  String containing HTML markup.
    Returns:    An iterator that yields the tokens comprising the input
                string. Each token is either a tag (possibly with nested,
                tags contained therein, such as <a href="<MTFoo>">, or a
                run of text between tags. Each yielded element is a
                two-element tuple; the first is either 'tag' or 'text';
                the second is the actual value.

    Based on the _tokenize() subroutine from Brad Choate's MTRegex plugin.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('docutils.utils.smartquotes.tokenize', 'tokenize(text)', {'re': re, 'text': text}, 0)
if __name__ == '__main__':
    import itertools
    import locale
    try:
        locale.setlocale(locale.LC_ALL, '')
        defaultlanguage = locale.getlocale()[0]
    except:
        defaultlanguage = 'en'
    defaultlanguage = defaultlanguage.lower().replace('-', '_')
    defaultlanguage = re.sub('_([a-zA-Z0-9])_', '_\\1-', defaultlanguage)
    _subtags = list(defaultlanguage.split('_'))
    _basetag = _subtags.pop(0)
    for n in range(len(_subtags), 0, -1):
        for tags in itertools.combinations(_subtags, n):
            _tag = '-'.join((_basetag, *tags))
            if _tag in smartchars.quotes:
                defaultlanguage = _tag
                break
        else:
            if _basetag in smartchars.quotes:
                defaultlanguage = _basetag
            else:
                defaultlanguage = 'en'
    import argparse
    parser = argparse.ArgumentParser(description='Filter <input> making ASCII punctuation "smart".')
    parser.add_argument('-a', '--action', default='1', help='what to do with the input (see --actionhelp)')
    parser.add_argument('-e', '--encoding', default='utf-8', help='text encoding')
    parser.add_argument('-l', '--language', default=defaultlanguage, help=f'text language (BCP47 tag), Default: {defaultlanguage}')
    parser.add_argument('-q', '--alternative-quotes', action='store_true', help='use alternative quote style')
    parser.add_argument('--doc', action='store_true', help='print documentation')
    parser.add_argument('--actionhelp', action='store_true', help='list available actions')
    parser.add_argument('--stylehelp', action='store_true', help='list available quote styles')
    parser.add_argument('--test', action='store_true', help='perform short self-test')
    args = parser.parse_args()
    if args.doc:
        print(__doc__)
    elif args.actionhelp:
        print(options)
    elif args.stylehelp:
        print()
        print('Available styles (primary open/close, secondary open/close)')
        print('language tag   quotes')
        print('============   ======')
        for key in sorted(smartchars.quotes.keys()):
            print('%-14s %s' % (key, smartchars.quotes[key]))
    elif args.test:
        import unittest
        
        
        class TestSmartypantsAllAttributes(unittest.TestCase):
            
            def test_dates(self) -> None:
                self.assertEqual(smartyPants("1440-80's"), '1440-80’s')
                self.assertEqual(smartyPants("1440-'80s"), '1440-’80s')
                self.assertEqual(smartyPants("1440---'80s"), '1440–’80s')
                self.assertEqual(smartyPants("1960's"), '1960’s')
                self.assertEqual(smartyPants("one two '60s"), 'one two ’60s')
                self.assertEqual(smartyPants("'60s"), '’60s')
            
            def test_educated_quotes(self) -> None:
                self.assertEqual(smartyPants('"Isn\'t this fun?"'), '“Isn’t this fun?”')
            
            def test_html_tags(self) -> None:
                text = '<a src="foo">more</a>'
                self.assertEqual(smartyPants(text), text)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSmartypantsAllAttributes)
        unittest.TextTestRunner().run(suite)
    else:
        if args.alternative_quotes:
            if '-x-altquot' in args.language:
                args.language = args.language.replace('-x-altquot', '')
            else:
                args.language += '-x-altquot'
        text = sys.stdin.read()
        print(smartyPants(text, attr=args.action, language=args.language))


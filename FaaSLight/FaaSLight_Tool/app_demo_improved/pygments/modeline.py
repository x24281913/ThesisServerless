"""
    pygments.modeline
    ~~~~~~~~~~~~~~~~~

    A simple modeline parser (based on pymodeline).

    :copyright: Copyright 2006-present by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re
__all__ = ['get_filetype_from_buffer']
modeline_re = re.compile('\n    (?: vi | vim | ex ) (?: [<=>]? \\d* )? :\n    .* (?: ft | filetype | syn | syntax ) = ( [^:\\s]+ )\n', re.VERBOSE)

def get_filetype_from_line(l):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.modeline.get_filetype_from_line', 'get_filetype_from_line(l)', {'modeline_re': modeline_re, 'l': l}, 1)

def get_filetype_from_buffer(buf, max_lines=5):
    """
    Scan the buffer for modelines and return filetype if one is found.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('pygments.modeline.get_filetype_from_buffer', 'get_filetype_from_buffer(buf, max_lines=5)', {'get_filetype_from_line': get_filetype_from_line, 'buf': buf, 'max_lines': max_lines}, 1)


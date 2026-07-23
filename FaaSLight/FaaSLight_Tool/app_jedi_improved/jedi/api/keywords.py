import pydoc
from contextlib import suppress
from typing import Dict, Optional
from jedi.inference.names import AbstractArbitraryName
try:
    from pydoc_data import topics
    pydoc_topics: Optional[Dict[(str, str)]] = topics.topics
except ImportError:
    pydoc_topics = None


class KeywordName(AbstractArbitraryName):
    api_type = 'keyword'
    
    def py__doc__(self):
        return imitate_pydoc(self.string_name)


def imitate_pydoc(string):
    """
    It's not possible to get the pydoc's without starting the annoying pager
    stuff.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.keywords.imitate_pydoc', 'imitate_pydoc(string)', {'pydoc_topics': pydoc_topics, 'pydoc': pydoc, 'suppress': suppress, 'string': string}, 1)


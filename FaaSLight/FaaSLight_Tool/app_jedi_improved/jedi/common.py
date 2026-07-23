from contextlib import contextmanager

@contextmanager
def monkeypatch(obj, attribute_name, new_value):
    """
    Like pytest's monkeypatch, but as a value manager.
    """
    old_value = getattr(obj, attribute_name)
    try:
        setattr(obj, attribute_name, new_value)
        yield
    finally:
        setattr(obj, attribute_name, old_value)

def indent_block(text, indention='    '):
    """This function indents a text block with a default of four spaces."""
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.common.indent_block', "indent_block(text, indention='    ')", {'text': text, 'indention': indention}, 1)


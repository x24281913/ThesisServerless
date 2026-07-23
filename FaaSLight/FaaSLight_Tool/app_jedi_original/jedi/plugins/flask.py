
def import_module(callback):
    """
    Handle "magic" Flask extension imports:
    ``flask.ext.foo`` is really ``flask_foo`` or ``flaskext.foo``.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.plugins.flask.import_module', 'import_module(callback)', {'callback': callback}, 1)


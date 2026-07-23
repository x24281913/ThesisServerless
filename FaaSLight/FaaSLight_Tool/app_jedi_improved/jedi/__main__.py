import sys
from os.path import join, dirname, abspath, isdir

def _start_linter():
    """
    This is a pre-alpha API. You're not supposed to use it at all, except for
    testing. It will very likely change.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.__main__._start_linter', '_start_linter()', {'sys': sys, 'isdir': isdir}, 0)

def _complete():
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.__main__._complete', '_complete()', {'sys': sys}, 0)
if (len(sys.argv) == 2 and sys.argv[1] == 'repl'):
    print(join(dirname(abspath(__file__)), 'api', 'replstartup.py'))
elif (len(sys.argv) > 1 and sys.argv[1] == '_linter'):
    _start_linter()
elif (len(sys.argv) > 1 and sys.argv[1] == '_complete'):
    _complete()
else:
    print('Command not implemented: %s' % sys.argv[1])


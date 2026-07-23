"""
This module contains variables with global |jedi| settings. To change the
behavior of |jedi|, change the variables defined in :mod:`jedi.settings`.

Plugins should expose an interface so that the user can adjust the
configuration.


Example usage::

    from jedi import settings
    settings.case_insensitive_completion = True


Completion output
~~~~~~~~~~~~~~~~~

.. autodata:: case_insensitive_completion
.. autodata:: add_bracket_after_function


Filesystem cache
~~~~~~~~~~~~~~~~

.. autodata:: cache_directory


Parser
~~~~~~

.. autodata:: fast_parser


Dynamic stuff
~~~~~~~~~~~~~

.. autodata:: dynamic_array_additions
.. autodata:: dynamic_params
.. autodata:: dynamic_params_for_other_modules
.. autodata:: auto_import_modules


Caching
~~~~~~~

.. autodata:: call_signatures_validity


"""

import os
import platform
case_insensitive_completion = True
'\nCompletions are by default case insensitive.\n'
add_bracket_after_function = False
'\nAdds an opening bracket after a function for completions.\n'
if platform.system().lower() == 'windows':
    _cache_directory = os.path.join((os.getenv('LOCALAPPDATA') or os.path.expanduser('~')), 'Jedi', 'Jedi')
elif platform.system().lower() == 'darwin':
    _cache_directory = os.path.join('~', 'Library', 'Caches', 'Jedi')
else:
    _cache_directory = os.path.join((os.getenv('XDG_CACHE_HOME') or '~/.cache'), 'jedi')
cache_directory = os.path.expanduser(_cache_directory)
'\nThe path where the cache is stored.\n\nOn Linux, this defaults to ``~/.cache/jedi/``, on OS X to\n``~/Library/Caches/Jedi/`` and on Windows to ``%LOCALAPPDATA%\\Jedi\\Jedi\\``.\nOn Linux, if the environment variable ``$XDG_CACHE_HOME`` is set,\n``$XDG_CACHE_HOME/jedi`` is used instead of the default one.\n'
fast_parser = True
"\nUses Parso's diff parser. If it is enabled, this might cause issues, please\nread the warning on :class:`.Script`. This feature makes it possible to only\nparse the parts again that have changed, while reusing the rest of the syntax\ntree.\n"
_cropped_file_size = int(10000000.0)
"\nJedi gets extremely slow if the file size exceed a few thousand lines.\nTo avoid getting stuck completely Jedi crops the file at some point.\n\nOne megabyte of typical Python code equals about 20'000 lines of code.\n"
dynamic_array_additions = True
'\ncheck for `append`, etc. on arrays: [], {}, () as well as list/set calls.\n'
dynamic_params = True
'\nA dynamic param completion, finds the callees of the function, which define\nthe params of a function.\n'
dynamic_params_for_other_modules = True
'\nDo the same for other modules.\n'
dynamic_flow_information = True
'\nCheck for `isinstance` and other information to infer a type.\n'
auto_import_modules = ['gi']
'\nModules that will not be analyzed but imported, if they contain Python code.\nThis improves autocompletion for libraries that use ``setattr`` or\n``globals()`` modifications a lot.\n'
allow_unsafe_interpreter_executions = True
'\nControls whether descriptors are evaluated when using an Interpreter. This is\nsomething you might want to control when using Jedi from a Repl (e.g. IPython)\n\nGenerally this setting allows Jedi to execute __getitem__ and descriptors like\n`property`.\n'
call_signatures_validity = 3.0
'\nFinding function calls might be slow (0.1-0.5s). This is not acceptible for\nnormal writing. Therefore cache it for a short time.\n'


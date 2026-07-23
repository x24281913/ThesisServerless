import os
import sys
from importlib.abc import MetaPathFinder
from importlib.machinery import PathFinder
del sys.path[0]

def _get_paths():
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.__main__._get_paths', '_get_paths()', {'os': os, '__file__': __file__, 'sys': sys}, 1)


class _ExactImporter(MetaPathFinder):
    
    def __init__(self, path_dct):
        self._path_dct = path_dct
    
    def find_spec(self, fullname, path=None, target=None):
        if (path is None and fullname in self._path_dct):
            p = self._path_dct[fullname]
            spec = PathFinder.find_spec(fullname, path=[p], target=target)
            return spec
        return None

sys.meta_path.insert(0, _ExactImporter(_get_paths()))
from jedi.inference.compiled import subprocess
sys.meta_path.pop(0)
host_sys_version = [int(x) for x in sys.argv[2].split('.')]
subprocess.Listener().listen()


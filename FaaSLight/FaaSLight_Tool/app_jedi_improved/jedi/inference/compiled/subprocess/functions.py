import sys
import os
import inspect
import importlib
from pathlib import Path
from zipfile import ZipFile
from zipimport import zipimporter, ZipImportError
from importlib.machinery import all_suffixes
from jedi.inference.compiled import access
from jedi import debug
from jedi import parser_utils
from jedi.file_io import KnownContentFileIO, ZipFileIO

def get_sys_path():
    return sys.path

def load_module(inference_state, **kwargs):
    return access.load_module(inference_state, **kwargs)

def get_compiled_method_return(inference_state, id, attribute, *args, **kwargs):
    handle = inference_state.compiled_subprocess.get_access_handle(id)
    return getattr(handle.access, attribute)(*args, **kwargs)

def create_simple_object(inference_state, obj):
    return access.create_access_path(inference_state, obj)

def get_module_info(inference_state, sys_path=None, full_name=None, **kwargs):
    """
    Returns Tuple[Union[NamespaceInfo, FileIO, None], Optional[bool]]
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions.get_module_info', 'get_module_info(inference_state, sys_path=None, full_name=None, **kwargs)', {'sys': sys, '_find_module': _find_module, 'inference_state': inference_state, 'sys_path': sys_path, 'full_name': full_name, 'kwargs': kwargs}, 1)

def get_builtin_module_names(inference_state):
    return sys.builtin_module_names

def _test_raise_error(inference_state, exception_type):
    """
    Raise an error to simulate certain problems for unit tests.
    """
    raise exception_type

def _test_print(inference_state, stderr=None, stdout=None):
    """
    Force some prints in the subprocesses. This exists for unit tests.
    """
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._test_print', '_test_print(inference_state, stderr=None, stdout=None)', {'sys': sys, 'inference_state': inference_state, 'stderr': stderr, 'stdout': stdout}, 0)

def _get_init_path(directory_path):
    """
    The __init__ file can be searched in a directory. If found return it, else
    None.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._get_init_path', '_get_init_path(directory_path)', {'all_suffixes': all_suffixes, 'os': os, 'directory_path': directory_path}, 1)

def safe_literal_eval(inference_state, value):
    return parser_utils.safe_literal_eval(value)

def iter_module_names(*args, **kwargs):
    return list(_iter_module_names(*args, **kwargs))

def _iter_module_names(inference_state, paths):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._iter_module_names', '_iter_module_names(inference_state, paths)', {'os': os, 'zipimporter': zipimporter, '_zip_list_subdirectory': _zip_list_subdirectory, 'ZipImportError': ZipImportError, 'debug': debug, 'inspect': inspect, 'inference_state': inference_state, 'paths': paths}, 0)

def _find_module(string, path=None, full_name=None, is_global_search=True):
    """
    Provides information about a module.

    This function isolates the differences in importing libraries introduced with
    python 3.3 on; it gets a module name and optionally a path. It will return a
    tuple containin an open file for the module (if not builtin), the filename
    or the name of the module if it is a builtin one and a boolean indicating
    if the module is contained in a package.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._find_module', '_find_module(string, path=None, full_name=None, is_global_search=True)', {'sys': sys, 'importlib': importlib, 'ImplicitNSInfo': ImplicitNSInfo, '_find_module_py33': _find_module_py33, 'string': string, 'path': path, 'full_name': full_name, 'is_global_search': is_global_search}, 2)

def _find_module_py33(string, path=None, loader=None, full_name=None, is_global_search=True):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._find_module_py33', '_find_module_py33(string, path=None, loader=None, full_name=None, is_global_search=True)', {'importlib': importlib, '_from_loader': _from_loader, 'string': string, 'path': path, 'loader': loader, 'full_name': full_name, 'is_global_search': is_global_search}, 1)

def _from_loader(loader, string):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._from_loader', '_from_loader(loader, string)', {'importlib': importlib, '_get_source': _get_source, 'zipimporter': zipimporter, 'ZipFileIO': ZipFileIO, 'Path': Path, 'KnownContentFileIO': KnownContentFileIO, 'loader': loader, 'string': string}, 2)

def _get_source(loader, fullname):
    """
    This method is here as a replacement for SourceLoader.get_source. That
    method returns unicode, but we prefer bytes.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._get_source', '_get_source(loader, fullname)', {'loader': loader, 'fullname': fullname}, 1)

def _zip_list_subdirectory(zip_path, zip_subdir_path):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.compiled.subprocess.functions._zip_list_subdirectory', '_zip_list_subdirectory(zip_path, zip_subdir_path)', {'ZipFile': ZipFile, 'Path': Path, 'zip_path': zip_path, 'zip_subdir_path': zip_subdir_path}, 0)


class ImplicitNSInfo:
    """Stores information returned from an implicit namespace spec"""
    
    def __init__(self, name, paths):
        self.name = name
        self.paths = paths



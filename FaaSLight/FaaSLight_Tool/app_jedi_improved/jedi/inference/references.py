import os
import re
from parso import python_bytes_to_unicode
from jedi.debug import dbg
from jedi.file_io import KnownContentFileIO, FolderIO
from jedi.inference.names import SubModuleName
from jedi.inference.imports import load_module_from_path
from jedi.inference.filters import ParserTreeFilter
from jedi.inference.gradual.conversion import convert_names
_IGNORE_FOLDERS = ('.tox', '.venv', '.mypy_cache', 'venv', '__pycache__')
_OPENED_FILE_LIMIT = 2000
"\nStats from a 2016 Lenovo Notebook running Linux:\nWith os.walk, it takes about 10s to scan 11'000 files (without filesystem\ncaching). Once cached it only takes 5s. So it is expected that reading all\nthose files might take a few seconds, but not a lot more.\n"
_PARSED_FILE_LIMIT = 30
'\nFor now we keep the amount of parsed files really low, since parsing might take\neasily 100ms for bigger files.\n'

def _resolve_names(definition_names, avoid_names=()):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.references._resolve_names', '_resolve_names(definition_names, avoid_names=())', {'SubModuleName': SubModuleName, '_resolve_names': _resolve_names, 'definition_names': definition_names, 'avoid_names': avoid_names}, 0)

def _dictionarize(names):
    return dict((((n if n.tree_name is None else n.tree_name), n) for n in names))

def _find_defining_names(module_context, tree_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references._find_defining_names', '_find_defining_names(module_context, tree_name)', {'_find_names': _find_names, 'convert_names': convert_names, '_find_global_variables': _find_global_variables, '_add_names_in_same_context': _add_names_in_same_context, '_resolve_names': _resolve_names, 'module_context': module_context, 'tree_name': tree_name}, 1)

def _find_names(module_context, tree_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references._find_names', '_find_names(module_context, tree_name)', {'_resolve_names': _resolve_names, 'module_context': module_context, 'tree_name': tree_name}, 1)

def _add_names_in_same_context(context, string_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references._add_names_in_same_context', '_add_names_in_same_context(context, string_name)', {'ParserTreeFilter': ParserTreeFilter, 'context': context, 'string_name': string_name}, 1)

def _find_global_variables(names, search_name):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.references._find_global_variables', '_find_global_variables(names, search_name)', {'_add_names_in_same_context': _add_names_in_same_context, 'names': names, 'search_name': search_name}, 0)

def find_references(module_context, tree_name, only_in_module=False):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references.find_references', 'find_references(module_context, tree_name, only_in_module=False)', {'_find_defining_names': _find_defining_names, '_dictionarize': _dictionarize, 'get_module_contexts_containing_name': get_module_contexts_containing_name, '_find_names': _find_names, 'module_context': module_context, 'tree_name': tree_name, 'only_in_module': only_in_module}, 1)

def _check_fs(inference_state, file_io, regex):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references._check_fs', '_check_fs(inference_state, file_io, regex)', {'python_bytes_to_unicode': python_bytes_to_unicode, 'KnownContentFileIO': KnownContentFileIO, 'load_module_from_path': load_module_from_path, 'inference_state': inference_state, 'file_io': file_io, 'regex': regex}, 1)

def gitignored_paths(folder_io, file_io):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references.gitignored_paths', 'gitignored_paths(folder_io, file_io)', {'os': os, 'folder_io': folder_io, 'file_io': file_io}, 2)

def expand_relative_ignore_paths(folder_io, relative_paths):
    curr_path = folder_io.path
    return {os.path.join(curr_path, p[1]) for p in relative_paths if curr_path.startswith(p[0])}

def recurse_find_python_folders_and_files(folder_io, except_paths=()):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.references.recurse_find_python_folders_and_files', 'recurse_find_python_folders_and_files(folder_io, except_paths=())', {'gitignored_paths': gitignored_paths, 'expand_relative_ignore_paths': expand_relative_ignore_paths, '_IGNORE_FOLDERS': _IGNORE_FOLDERS, 'folder_io': folder_io, 'except_paths': except_paths}, 0)

def recurse_find_python_files(folder_io, except_paths=()):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.references.recurse_find_python_files', 'recurse_find_python_files(folder_io, except_paths=())', {'recurse_find_python_folders_and_files': recurse_find_python_folders_and_files, 'folder_io': folder_io, 'except_paths': except_paths}, 0)

def _find_python_files_in_sys_path(inference_state, module_contexts):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.references._find_python_files_in_sys_path', '_find_python_files_in_sys_path(inference_state, module_contexts)', {'recurse_find_python_files': recurse_find_python_files, 'inference_state': inference_state, 'module_contexts': module_contexts}, 0)

def _find_project_modules(inference_state, module_contexts):
    except_ = [m.py__file__() for m in module_contexts]
    yield from recurse_find_python_files(FolderIO(inference_state.project.path), except_)

def get_module_contexts_containing_name(inference_state, module_contexts, name, limit_reduction=1):
    """
    Search a name in the directories of modules.

    :param limit_reduction: Divides the limits on opening/parsing files by this
        factor.
    """
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.inference.references.get_module_contexts_containing_name', 'get_module_contexts_containing_name(inference_state, module_contexts, name, limit_reduction=1)', {'_find_project_modules': _find_project_modules, 'search_in_file_ios': search_in_file_ios, 'inference_state': inference_state, 'module_contexts': module_contexts, 'name': name, 'limit_reduction': limit_reduction}, 1)

def search_in_file_ios(inference_state, file_io_iterator, name, limit_reduction=1, complete=False):
    import custom_funtemplate
    custom_funtemplate.rewrite_template('jedi.inference.references.search_in_file_ios', 'search_in_file_ios(inference_state, file_io_iterator, name, limit_reduction=1, complete=False)', {'_PARSED_FILE_LIMIT': _PARSED_FILE_LIMIT, '_OPENED_FILE_LIMIT': _OPENED_FILE_LIMIT, 're': re, '_check_fs': _check_fs, 'dbg': dbg, 'inference_state': inference_state, 'file_io_iterator': file_io_iterator, 'name': name, 'limit_reduction': limit_reduction, 'complete': complete}, 0)


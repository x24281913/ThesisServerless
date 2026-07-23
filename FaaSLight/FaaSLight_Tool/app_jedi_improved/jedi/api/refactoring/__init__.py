import difflib
from pathlib import Path
from typing import Dict, Iterable, Tuple
from parso import split_lines
from jedi.api.exceptions import RefactoringError
from jedi.inference.value.namespace import ImplicitNSName
EXPRESSION_PARTS = 'or_test and_test not_test comparison expr xor_expr and_expr shift_expr arith_expr term factor power atom_expr'.split()


class ChangedFile:
    
    def __init__(self, inference_state, from_path, to_path, module_node, node_to_str_map):
        self._inference_state = inference_state
        self._from_path = from_path
        self._to_path = to_path
        self._module_node = module_node
        self._node_to_str_map = node_to_str_map
    
    def get_diff(self):
        old_lines = split_lines(self._module_node.get_code(), keepends=True)
        new_lines = split_lines(self.get_new_code(), keepends=True)
        if old_lines[-1] != '':
            old_lines[-1] += '\n'
        if new_lines[-1] != '':
            new_lines[-1] += '\n'
        project_path = self._inference_state.project.path
        if self._from_path is None:
            from_p = ''
        else:
            try:
                from_p = self._from_path.relative_to(project_path)
            except ValueError:
                from_p = self._from_path
        if self._to_path is None:
            to_p = ''
        else:
            try:
                to_p = self._to_path.relative_to(project_path)
            except ValueError:
                to_p = self._to_path
        diff = difflib.unified_diff(old_lines, new_lines, fromfile=str(from_p), tofile=str(to_p))
        return ''.join(diff).rstrip(' ')
    
    def get_new_code(self):
        return self._inference_state.grammar.refactor(self._module_node, self._node_to_str_map)
    
    def apply(self):
        if self._from_path is None:
            raise RefactoringError('Cannot apply a refactoring on a Script with path=None')
        with open(self._from_path, 'w', newline='') as f:
            f.write(self.get_new_code())
    
    def __repr__(self):
        return '<%s: %s>' % (self.__class__.__name__, self._from_path)



class Refactoring:
    
    def __init__(self, inference_state, file_to_node_changes, renames=()):
        self._inference_state = inference_state
        self._renames = renames
        self._file_to_node_changes = file_to_node_changes
    
    def get_changed_files(self) -> Dict[(Path, ChangedFile)]:
        
        def calculate_to_path(p):
            if p is None:
                return p
            p = str(p)
            for (from_, to) in renames:
                if p.startswith(str(from_)):
                    p = str(to) + p[len(str(from_)):]
            return Path(p)
        renames = self.get_renames()
        return {path: ChangedFile(self._inference_state, from_path=path, to_path=calculate_to_path(path), module_node=next(iter(map_)).get_root_node(), node_to_str_map=map_) for (path, map_) in sorted(self._file_to_node_changes.items(), key=lambda x: (x[0] or Path('')))}
    
    def get_renames(self) -> Iterable[Tuple[(Path, Path)]]:
        """
        Files can be renamed in a refactoring.
        """
        return sorted(self._renames)
    
    def get_diff(self):
        text = ''
        project_path = self._inference_state.project.path
        for (from_, to) in self.get_renames():
            text += 'rename from %s\nrename to %s\n' % (_try_relative_to(from_, project_path), _try_relative_to(to, project_path))
        return text + ''.join((f.get_diff() for f in self.get_changed_files().values()))
    
    def apply(self):
        """
        Applies the whole refactoring to the files, which includes renames.
        """
        for f in self.get_changed_files().values():
            f.apply()
        for (old, new) in self.get_renames():
            old.rename(new)


def _calculate_rename(path, new_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.__init__._calculate_rename', '_calculate_rename(path, new_name)', {'path': path, 'new_name': new_name}, 2)

def rename(inference_state, definitions, new_name):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.__init__.rename', 'rename(inference_state, definitions, new_name)', {'RefactoringError': RefactoringError, 'Path': Path, '_calculate_rename': _calculate_rename, 'ImplicitNSName': ImplicitNSName, 'Refactoring': Refactoring, 'inference_state': inference_state, 'definitions': definitions, 'new_name': new_name}, 1)

def inline(inference_state, names):
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.__init__.inline', 'inline(inference_state, names)', {'RefactoringError': RefactoringError, 'EXPRESSION_PARTS': EXPRESSION_PARTS, '_remove_indent_of_prefix': _remove_indent_of_prefix, 'Refactoring': Refactoring, 'inference_state': inference_state, 'names': names}, 1)

def _remove_indent_of_prefix(prefix):
    """
    Removes the last indentation of a prefix, e.g. " 
 
 " becomes " 
 
".
    """
    return ''.join(split_lines(prefix, keepends=True)[:-1])

def _try_relative_to(path: Path, base: Path) -> Path:
    import custom_funtemplate
    return custom_funtemplate.rewrite_template('jedi.api.refactoring.__init__._try_relative_to', '_try_relative_to(path, base)', {'path': path, 'base': base}, 1)


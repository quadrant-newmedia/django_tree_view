'''
module_tree.py

Implements ModuleTree -> a class which walks a python package, creating an easy-to-traverse tree structure.
'''

from importlib import import_module
from pathlib import Path

class ConfigurationError(Exception):
    pass

class ModuleNode:
    '''
        Represents a node in a module tree.

        self.module is the imported python module
        self.submodules is a dictionary of ModuleNodes representing submodules of this one
    '''
    def __init__(self, module_name, module_path):
        self.module = import_module(module_name)
        self.submodules = {
            subdir.name: ModuleNode(f'{module_name}.{subdir.name}', subdir)
            # Note - pretty well any directory name can be imported dynamically with import_module, but directories containing '.' cannot, because a.b is treated as a/b by the import system
            # Also exclude any directory beginning with '__' -> mainly to exclude __pycache__ directory
            for subdir in module_path.iterdir() 
            if subdir.is_dir() and not '.' in subdir.name and not subdir.name.startswith('__')
        }

def _get_valid_module_directory_path(module):
    try :
        f = module.__file__
    except AttributeError :
        return
    if f is None :
        return
    p = Path(f)
    if p.name != '__init__.py' :
        return
    return p.parent

class ModuleTree(ModuleNode):
    def __init__(self, module_name):
        # Note - if import error occurs, that should be pretty self-explanatory to the user - no custom message needed
        module = import_module(module_name)
        p = _get_valid_module_directory_path(module)
        if not p :
            raise ConfigurationError('The root of a module tree must be a python package containing an __init__.py file')
        return super().__init__(module_name, p)
'''
module_tree.py

Implements ModuleTree -> a class which walks a python package, creating an easy-to-traverse tree structure.
'''
from importlib import import_module
from os import path
from pathlib import Path

class ConfigurationError(Exception):
    pass

class ViewTreeNode:
    '''
        Represents a node (directory) in a view tree.

        self.view_tree_path
            the path of this directory, relative to the root of the view tree
        self.module
            the view_tree_node.py module
            will be None if this module does not have a view_tree_node.py file
        self.subtrees
            a dictionary of ViewTreeNodes representing subtrees of this one
    '''
    def __init__(self, view_tree_path, package_name, package_path):
        self.view_tree_path = view_tree_path

        import_name = package_name +'.view_tree_node'
        try :
            self.module = import_module(import_name)
        except ModuleNotFoundError as e :
            if e.name != import_name :
                raise e
            self.module = None

        self.subtrees = {
            subdir.name: ViewTreeNode(
                path.join(view_tree_path, subdir.name), 
                f'{package_name}.{subdir.name}', 
                subdir,
            )
            # Note - pretty well any directory name can be imported dynamically with import_module, but directories containing '.' cannot, because a.b is treated as a/b by the import system
            # Also exclude any directory beginning with '__' -> mainly to exclude __pycache__ directory
            for subdir in package_path.iterdir() 
            if subdir.is_dir() and not '.' in subdir.name and not subdir.name.startswith('__')
        }

def _get_valid_package_directory(module):
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

class ViewTree(ViewTreeNode):
    def __init__(self, package_name):
        # Note - if import error occurs, that should be pretty self-explanatory to the user - no custom message needed
        module = import_module(package_name)
        p = _get_valid_package_directory(module)
        if not p :
            raise ConfigurationError('The root of a module tree must be a python package containing an __init__.py file')
        return super().__init__('', package_name, p)
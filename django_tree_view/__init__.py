from django_dynamic_path import DynamicPath

from .path_resolver import PathResolver
from .view import view

def make_tree_view(root_module_name="view_tree"):
    '''
        Return an object suitable for use in django's urlpatterns.

        root_module_name should be the dotted python path to a python package containing your "view tree"
    '''
    return DynamicPath(
        PathResolver(root_module_name),
        tree_view,
    )
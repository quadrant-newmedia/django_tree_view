from django.urls.exceptions import Resolver404

from django_dynamic_path import DynamicPath
from django_early_return import EarlyReturn

from .path_resolver import PathResolver
from .view import view, preprocess

def make_tree_view(root_module_name="view_tree"):
    '''
        Return an object suitable for use in django's urlpatterns.

        root_module_name should be the dotted python path to a python package containing your "view tree"
    '''
    return DynamicPath(
        PathResolver(root_module_name),
        view,
    )


from django.test.client import RequestFactory
from django.urls import resolve
class NotATreeViewPath(Exception):
    pass
def is_get_allowed(path, user):
    '''
        Test whether the given user can currently access the given path.
        Raise NotATreeViewPath if the path does not resolve to a tree view.
        Return False if the preprocessing step of the view would raise an EarlyReturn exception.

        The main purpose of this is so that you don't have to reproduce permission checks/published checks when deciding whether or not to provide a link to a given a page. Just ask that page whether it can currently respond.
    '''
    request = RequestFactory().get(path)
    request.user = user
    try :
        resolver_match = resolve(path)
    except Resolver404 :
        raise NotATreeViewPath()

    if resolver_match.func != view :
        raise NotATreeViewPath()

    try :
        preprocess(request, resolver_match.args)
    except EarlyReturn :
        return False

    return True
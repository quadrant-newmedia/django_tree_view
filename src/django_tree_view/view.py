import functools
import os

from django import http
from django_early_return import EarlyReturn
from django.views.decorators.csrf import csrf_exempt

import django_referer_csrf

http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

def preprocess(request, handlers):
    branch_data = {}
    for node, arg in handlers :
        try :
            p = getattr(node.module, 'preprocess')
        except AttributeError :
            # Modules don't have to implement preprocess()
            continue

        # Not all modules capture an arg from the url
        args = [arg] if arg is not None else []

        r = p(request, *args, **branch_data)
        # preprocess can return a dictionary to be merged into the "branch data"
        if r :
            branch_data.update(r)

    return branch_data

'''
    Note - we mark the view as csrf_exempt, and then provide our own CSRF protection.
    This is so that users can turn CSRF protection off for particular endpoints.
'''
@csrf_exempt
def view(request, *handlers):
    method = request.method.lower()
    handler_node = handlers[-1][0]
    handler_module = handler_node.module

    # Apply CSRF protection, unless the handler module has set CSRF_EXEMPT=True 
    if not getattr(handler_module, 'CSRF_EXEMPT', False) :
        if not django_referer_csrf.is_valid(request) :
            return http.HttpResponseForbidden('CSRF check failed.')

    if method not in http_method_names :
        return _method_not_allowed(request, handler_module)

    try :
        handler_func = _get_handler_func(handler_module, method)
    except AttributeError :
        if method == 'options' :
            # provide default options implementation
            return _options(request, handler_module)
        return _method_not_allowed(request, handler_module)

    # We recommend storing templates in same directory as the handler module.
    # You'll then want to put the root directory of your tree view in your template DIRS
    # This property enables you to prepend the appropriate path to a template name (relative to the root of your tree view).
    # This will either be empty string (for the root of the view tree) or end in '/'
    request.view_tree_dir = os.path.join(handler_node.view_tree_path, '')

    # Include this, directly, for backward compatibility
    request.view_tree_path = handler_node.view_tree_path

    # Run all preprocess functions
    '''
        Note - we expect you to perform any required authentication in your preprocess functions.
        If authentication fails, we recommend raising a django_early_return.EarlyReturn exception.
        That way you can use our is_get_allowed(path, user) helper method to determine if a given user is currently allowed to access a given path.
    '''
    branch_data = preprocess(request, handlers)

    # Run the view
    return handler_func(request, **branch_data)

    # TODO:
    # Should we allow modules to implement a postprocess(response, request), which runs in reverse order? This could be used, for example, to set response headers for an entire branch

'''
    Add a special "test_page_visibility" property to the view
    This is to support django_page_visibility (which is not yet published)

    This function should raise an exception if the user is not currently allowed to view the page.
    Note that our implemenation of this requires users to all of their permission checks inside preprocess() functions.
'''
def test_page_visibility(request, *handlers):
    preprocess(request, handlers)
    return True
view.test_page_visibility = test_page_visibility

def _get_handler_func(handler_module, method):
    '''Get final handler function, or raise raise AttributeError'''
    try :
        return getattr(handler_module, method)
    except AttributeError :
        pass

    if method == 'head' :
        return getattr(handler_module, 'get')

    raise AttributeError()

def _method_not_allowed(request, handler_module):
    return http.HttpResponseNotAllowed(_allowed_methods(handler_module))
def _options(request, handler_module):
    response = http.HttpResponse()
    response['Allow'] = ', '.join(_allowed_methods(handler_module))
    response['Content-Length'] = '0'
    return response
def _allowed_methods(handler_module):
    methods = [m for m in http_method_names if hasattr(handler_module, m)]
    if 'options' not in methods :
        methods.append('options')
    return methods
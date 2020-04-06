import functools
import os

from django import http
from django.views.decorators.csrf import csrf_exempt

import django_referer_csrf

http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

def preprocess(request, handlers):
    branch_data = {}
    for module, arg in handlers :
        try :
            p = getattr(module, 'preprocess')
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
    handler_module = handlers[-1][0]

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

    # Preprocessors or the view function itself may want to know the entire handler list
    request.tree_view_handler_list = handlers
    # We recommend storing templates in same directory as the handler module.
    # You'll then want to put the root directory of your tree view in your template DIRS
    # This function enables you to prepend the appropriate path to a template name (relative to the root of your tree view).
    request.relative_template_name = functools.partial(_relative_template_name, handlers)

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

def _relative_template_name(handler_list, template_path='template.html'):
    root = handler_list[0][0].__name__
    final = handler_list[-1][0].__name__
    diff = final[len(root)+1:]
    return os.path.join(diff.replace('.', os.path.sep), template_path)

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
# Django Tree View

Organize your view code and templates and in a directory structure, and automatically generate urls for them.

## Terminology

"Tree View" refers the actual view function we've created, which processes a request according to code you write inside your "view tree".

## Installation

1. `pip install django_tree_view`
2. In your urls.py file, add in a call to `make_tree_view`, passing in the python package name (dotted python path) of your view tree:
    ```python
    from django_tree_view import make_tree_view

    urlpatterns = [
        make_tree_view('my_view_tree'),
    ]
    ```

    Note: we're not using django's path() here, and we didn't specify a url regex. make_tree_view() returns an object which dynamically resolves urls, matching them whenever there is a corresponding directory (with a `view_tree_node.py` module) inside of your view tree.

    Note: you can use `include('some_path/', [make_tree_view()])` if you want a url prefix.

3. Optionally, add the full path to your view tree to the `DIRS` option of your `DjangoTemplates` backend:
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'my_view_tree')],
            ...
        },
    ]
    ```

    This will allow you to place page-specific templates inside the same directory which holds the view code for that url.

## CSRF Protection
Our view uses Django's `csrf_exempt` decorator, and selectively applies its own CSRF protection.

Any view tree node can opt-out of CSRF protection by setting `CSRF_EXEMPT=True` at the module level.

The CSRF protection we use is not Django's default CSRF protection. We use utilities from django_referer_csrf. You may want to check out the documentation for django_referer_csrf, and use their middleware in place of Django's, but this is *not* required.

## Organizing Your View Tree

TODO

## TODO

When DEBUG and reloading, reload empty modules (not sure, but this might already be done).

### "Single View Tree" approach
Our path resolver no longer matches when the "path directory" contains no `view_tree_node.py` file. 

I think we should change how view trees are "installed". The user should define one global `VIEW_TREE_ROOT`. You can "install" reusable apps in your view tree by symlinking to them from your view tree.

This makes things easier to understand for the end user. They don't need understand `make_tree_view()`. You have a single directory containing your view tree. Period.

The challenge: if an app is distributed on pypi, symlinking to it (in a way that can be copied between server environments), is not trivial.


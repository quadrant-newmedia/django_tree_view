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

## Organizing Your View Tree

TODO

## TODO

When DEBUG and reloading, reload empty modules
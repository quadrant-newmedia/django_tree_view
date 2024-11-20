## 4.3.0
Explicit Django 5 support

### 4.1.2
Minor readme changes

### 4.1.1

Add support for Django 3.1, 3.2

## 4.1.0

Add support for date capturing via `date__` directories.

# 4.0.0

Segments ending in __ are reserved for capturing nodes. This ensures that `string__` and `path__` nodes may receive 'int__', 'string__', or 'path__' as arguments.

# 3.0.0

PathResolver does not match if terminal leaf node package does not contain `view_tree_node.py` (this was intended in 2.0.0, but not implemented properly).

`ViewTreeNode` no longer swallows `ImportError`s raised within view tree modules. 

Added `encode_path` and `decode_path` utility functions.

### 2.1.3

Fixed `request.view_tree_dir` and `request.view_tree_path`: both were absolute, and are supposed to be relative to root of view tree

## 2.1.0

Added `request.view_tree_dir`.

# 2.0.0

Handler modules are now imported from view_tree_node.py, rather than __init__.py. 

This is much more explicit, and is a better approach if your view tree contains other code. In particular, you may want to add some of your view tree packages to `INSTALLED_APPS`, and include `models.py`, static files, etc.

`request.relative_template_name()` was replaced with `request.view_tree_path`.

# 1.0.0

Breaking changes:
- dropped is_get_allowed(), replaced with support for django_page_visibility

# 0.1.0

Added is_get_allowed() helper utility

# 0.0.1

Fixed bug when reloading module tree in DEBUG mode

# 0.0.0
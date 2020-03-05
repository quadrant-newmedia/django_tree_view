from django_tree_view import make_tree_view

urlpatterns = [
    make_tree_view('django_tree_view.tests.view_tree'),
]
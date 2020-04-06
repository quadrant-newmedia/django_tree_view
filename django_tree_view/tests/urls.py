from django.urls import path
from django.views.generic import TemplateView

from django_tree_view import make_tree_view

urlpatterns = [
    make_tree_view('django_tree_view.tests.view_tree'),
    path('template_view', TemplateView.as_view(template_name='fake')),
]
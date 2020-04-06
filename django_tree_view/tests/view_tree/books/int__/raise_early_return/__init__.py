from django_early_return import EarlyReturn
from django import http

def preprocess(request, **kwargs):
    raise EarlyReturn(http.HttpResponseForbidden())
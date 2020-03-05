from django import http

CSRF_EXEMPT = True

def post(request, **kwargs):
    return http.HttpResponse()
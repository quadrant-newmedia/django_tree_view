from django import http

def get(request):
    return http.HttpResponse('This is bar!')
from django import http

def preprocess(request, book_id, **kwargs):
    return dict(book_id=book_id)

def get(request, root, book_id):
    return http.HttpResponse(f'root:{root}:book_id:{book_id}')

def post(request, root, book_id):
    return http.HttpResponse()
from django.template.response import TemplateResponse

def get(request, **kwargs):
    return TemplateResponse(request, request.view_tree_path+'/template.html', {})
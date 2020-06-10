from django.template.response import TemplateResponse

def get(request, **kwargs):
    return TemplateResponse(request, request.relative_template_name('sub_dir/a.html'), {})
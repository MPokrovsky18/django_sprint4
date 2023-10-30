from django.views.generic import TemplateView
from django.shortcuts import render


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Get page with 404 error."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """Get page with 403csrf error."""
    return render(request, 'pages/403csrf.html', status=403)


def server_error(request):
    """Get page with 500 error."""
    return render(request, 'pages/500.html', status=500)

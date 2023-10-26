from django.shortcuts import render


def about(request):
    """Retern info about project."""
    return render(request, 'pages/about.html')


def rules(request):
    """Retern rules of project."""
    return render(request, 'pages/rules.html')

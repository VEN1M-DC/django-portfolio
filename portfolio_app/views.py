from django.shortcuts import render, get_object_or_404
from .models import Portfolio, Project

def portfolio_list(request):
    portfolios = Portfolio.objects.filter(is_active=True).select_related("student")
    return render(request, "portfolio_app/list.html", {"portfolios": portfolios})


def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio.objects.select_related("student").prefetch_related("projects"), pk=pk, is_active=True)
    return render(request, "portfolio_app/detail.html", {"portfolio": portfolio})


def project_detail(request, pk):
    project = get_object_or_404(Project.objects.select_related("portfolio__student"), pk=pk, portfolio__is_active=True)
    return render(request, "portfolio_app/project.html", {"project": project})

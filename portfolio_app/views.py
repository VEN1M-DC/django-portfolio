from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from .models import Portfolio, Project

def portfolio_list(request):
    portfolios = Portfolio.objects.filter(is_active=True).select_related("student")
    return render(request, "portfolio_app/list.html", {"portfolios": portfolios})


class PortfolioDetailView(DetailView):
    """Show one public portfolio selected by the URL's primary key."""

    model = Portfolio
    template_name = "portfolio_app/portfolio_detail.html"
    context_object_name = "portfolio"

    def get_queryset(self):
        # Preserve the application's existing privacy rule for inactive portfolios.
        return (
            super().get_queryset()
            .filter(is_active=True)
            .select_related("student")
            .prefetch_related("projects")
        )


def project_detail(request, pk):
    project = get_object_or_404(Project.objects.select_related("portfolio__student"), pk=pk, portfolio__is_active=True)
    return render(request, "portfolio_app/project.html", {"project": project})

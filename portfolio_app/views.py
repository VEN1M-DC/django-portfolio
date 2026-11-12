from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import Student, Portfolio, Project

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


class StudentAccessMixin(PermissionRequiredMixin):
    # Student records are managed by authorized accounts, not anonymous visitors.
    login_url = reverse_lazy("admin:login")


class StudentListView(StudentAccessMixin, ListView):
    permission_required = "portfolio_app.view_student"
    model = Student
    template_name = "portfolio_app/student_list.html"
    context_object_name = "students"
    ordering = ["name", "pk"]


class StudentDetailView(StudentAccessMixin, DetailView):
    permission_required = "portfolio_app.view_student"
    model = Student
    template_name = "portfolio_app/student_detail.html"
    context_object_name = "student"


class StudentCreateView(StudentAccessMixin, CreateView):
    permission_required = ("portfolio_app.add_student", "portfolio_app.view_student")
    model = Student
    fields = ["name", "email", "major"]
    template_name = "portfolio_app/student_form.html"

    def get_success_url(self):
        return reverse("student-detail", kwargs={"pk": self.object.pk})


class StudentUpdateView(StudentAccessMixin, UpdateView):
    permission_required = ("portfolio_app.change_student", "portfolio_app.view_student")
    model = Student
    fields = ["name", "email", "major"]
    template_name = "portfolio_app/student_form.html"

    def get_success_url(self):
        return reverse("student-detail", kwargs={"pk": self.object.pk})


class StudentDeleteView(StudentAccessMixin, DeleteView):
    permission_required = ("portfolio_app.delete_student", "portfolio_app.view_student")
    model = Student
    template_name = "portfolio_app/student_confirm_delete.html"
    success_url = reverse_lazy("student-list")


class PortfolioCreateView(StudentAccessMixin, CreateView):
    permission_required = ("portfolio_app.add_portfolio", "portfolio_app.view_student")
    model = Portfolio
    fields = ["student", "title", "contact_email", "is_active", "about"]
    template_name = "portfolio_app/portfolio_form.html"

    def get_initial(self):
        initial = super().get_initial()
        student_id = self.request.GET.get("student")
        if student_id and student_id.isdecimal():
            student = get_object_or_404(Student, pk=student_id)
            initial.update(student=student, contact_email=student.email)
        return initial

    def get_success_url(self):
        # Inactive portfolios remain private; their student page is still usable.
        if self.object.is_active:
            return self.object.get_absolute_url()
        return reverse("student-detail", kwargs={"pk": self.object.student_id})


class ProjectCreateView(StudentAccessMixin, CreateView):
    permission_required = ("portfolio_app.add_project", "portfolio_app.view_student")
    model = Project
    fields = ["portfolio", "title", "description"]
    template_name = "portfolio_app/project_form.html"

    def get_initial(self):
        initial = super().get_initial()
        portfolio_id = self.request.GET.get("portfolio")
        if portfolio_id and portfolio_id.isdecimal():
            initial["portfolio"] = get_object_or_404(Portfolio, pk=portfolio_id)
        return initial

    def get_success_url(self):
        if self.object.portfolio.is_active:
            return self.object.portfolio.get_absolute_url()
        return reverse("student-detail", kwargs={"pk": self.object.portfolio.student_id})

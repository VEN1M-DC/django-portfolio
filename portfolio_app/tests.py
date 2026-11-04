from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Student, Portfolio, Project
from django.db import IntegrityError, transaction


class PortfolioDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.portfolios = []
        for name in ("Jordan", "Taylor", "Empty"):
            student = Student.objects.create(name=name, email=f"{name.lower()}@example.com")
            cls.portfolios.append(Portfolio.objects.create(
                student=student, title=f"{name} portfolio",
                about=f"About {name}", contact_email=student.email,
            ))
        cls.first, cls.second, cls.empty = cls.portfolios
        cls.description = "A complete project description " + "detail " * 40 + "END OF DESCRIPTION"
        cls.first_project = Project.objects.create(
            portfolio=cls.first, title="Jordan project", description=cls.description,
        )
        cls.second_project = Project.objects.create(
            portfolio=cls.second, title="Taylor project", description="Taylor project description",
        )

    def test_different_primary_keys_display_correct_portfolio_fields(self):
        for portfolio in self.portfolios:
            with self.subTest(pk=portfolio.pk):
                response = self.client.get(portfolio.get_absolute_url())
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "portfolio_app/portfolio_detail.html")
                self.assertEqual(response.context["portfolio"], portfolio)
                for value in (portfolio.title, portfolio.about, portfolio.contact_email, "Status:</strong> Active"):
                    self.assertContains(response, value)

    def test_only_related_projects_and_full_descriptions_are_shown(self):
        first = self.client.get(self.first.get_absolute_url())
        second = self.client.get(self.second.get_absolute_url())
        self.assertContains(first, self.first_project.title)
        self.assertContains(first, self.description)
        self.assertNotContains(first, self.second_project.title)
        self.assertContains(second, self.second_project.title)
        self.assertContains(second, self.second_project.description)
        self.assertNotContains(second, self.first_project.title)

    def test_portfolio_without_projects_shows_helpful_message(self):
        response = self.client.get(self.empty.get_absolute_url())
        self.assertContains(response, "No projects have been added yet.")
        self.assertNotContains(response, self.first_project.title)
        self.assertNotContains(response, self.second_project.title)

    def test_nonexistent_portfolio_returns_404(self):
        missing_pk = max(portfolio.pk for portfolio in self.portfolios) + 100
        self.assertEqual(self.client.get(reverse("portfolio-detail", kwargs={"pk": missing_pk})).status_code, 404)

    def test_home_and_detail_navigation(self):
        home = self.client.get(reverse("portfolio-list"))
        for portfolio in self.portfolios:
            with self.subTest(pk=portfolio.pk):
                self.assertContains(home, f'href="{portfolio.get_absolute_url()}"')
                detail = self.client.get(portfolio.get_absolute_url())
                self.assertContains(detail, f'<a href="{reverse("portfolio-list")}">Back to all portfolios</a>', html=True)

class StudentTests(TestCase):
    def test_student_persistence_and_major_query(self):
        student = Student.objects.create(name="Example Student", email="example@example.com", major="CSCI-BS")
        student.refresh_from_db()
        self.assertIsNotNone(student.pk)
        self.assertEqual(str(student), "Example Student")
        self.assertEqual(Student.objects.filter(major="CSCI-BS").get(), student)
        self.assertEqual(Student.objects.filter(major="CPEN-BS").count(), 0)

    def test_admin_requires_login_and_can_add_student(self):
        url = reverse("admin:portfolio_app_student_add")
        self.assertEqual(self.client.get(url).status_code, 302)
        admin = get_user_model().objects.create_superuser("testadmin", "admin@example.com", "test-only-password")
        self.client.force_login(admin)
        response = self.client.post(url, {"name": "Admin Example", "email": "example@example.com", "major": "CSCI-BS", "_save": "Save"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(name="Admin Example").exists())


class RelationshipTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name="Fixture", email="fixture@example.com", major="CSCI-BS")
        self.portfolio = Portfolio.objects.create(student=self.student, title="Fixture portfolio", contact_email="fixture@example.com")
        self.project = Project.objects.create(portfolio=self.portfolio, title="First project", description="Example description")

    def test_one_portfolio_per_student(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Portfolio.objects.create(student=self.student, title="Duplicate", contact_email="duplicate@example.com")

    def test_multiple_projects_and_relationship_queries(self):
        Project.objects.create(portfolio=self.portfolio, title="Second", description="Another example")
        self.assertEqual(self.student.portfolio, self.portfolio)
        self.assertEqual(self.portfolio.projects.count(), 2)
        self.assertEqual(Portfolio.objects.filter(student__major="CSCI-BS").get(), self.portfolio)
        self.assertEqual(Project.objects.filter(portfolio__student__major="CSCI-BS").count(), 2)

    def test_student_deletion_cascades(self):
        self.student.delete()
        self.assertFalse(Portfolio.objects.exists())
        self.assertFalse(Project.objects.exists())

    def test_portfolio_deletion_preserves_student(self):
        self.portfolio.delete()
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())
        self.assertFalse(Project.objects.exists())

    def test_public_pages_and_inactive_visibility(self):
        for url in [reverse("portfolio-list"), self.portfolio.get_absolute_url(), self.project.get_absolute_url()]:
            self.assertEqual(self.client.get(url).status_code, 200)
        self.portfolio.is_active = False
        self.portfolio.save()
        self.assertEqual(self.client.get(self.portfolio.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get(self.project.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse("portfolio-list")), "Fixture portfolio")

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Student, Portfolio, Project
from django.db import IntegrityError, transaction

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

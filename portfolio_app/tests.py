from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Student

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

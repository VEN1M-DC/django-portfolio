from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Portfolio, Project, Student


class StudentPortfolioWorkflowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = get_user_model().objects.create_superuser(
            "workflow-admin", "admin@example.com", "test-only-password"
        )
        cls.student = Student.objects.create(name="Morgan Chen", email="morgan@example.com")
        cls.other = Student.objects.create(name="Alex Rivera", email="alex@example.com")

    def setUp(self):
        self.client.force_login(self.admin)

    def portfolio_data(self, selected_student=None, **changes):
        data = {"student": (selected_student or self.student).pk, "title": "Course portfolio",
                "contact_email": "morgan@example.com", "is_active": "on", "about": "Course projects"}
        data.update(changes)
        return data

    def test_create_two_students_redirects_to_each_new_primary_key(self):
        for name in ("Jordan Park", "Taylor Reed"):
            response = self.client.post(reverse("student-create"),
                                        {"name": name, "email": "example@example.com", "major": "CSCI-BS"})
            student = Student.objects.get(name=name)
            self.assertRedirects(response, reverse("student-detail", kwargs={"pk": student.pk}))
            self.assertContains(self.client.get(response.url), name)

    def test_invalid_student_fields_do_not_create_records(self):
        for changes, field in (({"email": "not-an-email"}, "email"), ({"name": ""}, "name"),
                               ({"major": "INVALID"}, "major"), ({"name": "x" * 201}, "name")):
            with self.subTest(field=field, changes=changes):
                data = {"name": "Invalid record", "email": "test@example.com", "major": ""}
                data.update(changes)
                count = Student.objects.count()
                response = self.client.post(reverse("student-create"), data)
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context["form"].errors)
                self.assertEqual(Student.objects.count(), count)

    def test_student_list_and_detail_navigation(self):
        response = self.client.get(reverse("student-list"))
        for student in (self.student, self.other):
            self.assertContains(response, reverse("student-detail", kwargs={"pk": student.pk}))
        detail = self.client.get(reverse("student-detail", kwargs={"pk": self.student.pk}))
        self.assertContains(detail, self.student.email)
        self.assertContains(detail, "Back to Students")

    def test_empty_student_list(self):
        Student.objects.all().delete()
        self.assertContains(self.client.get(reverse("student-list")), "No students found.")

    def test_update_displays_existing_values_and_saves_selected_student(self):
        url = reverse("student-update", kwargs={"pk": self.student.pk})
        self.assertContains(self.client.get(url), self.student.name)
        response = self.client.post(url, {"name": "Morgan Updated", "email": "updated@example.com", "major": "CSCI-BA"})
        self.assertRedirects(response, reverse("student-detail", kwargs={"pk": self.student.pk}))
        self.student.refresh_from_db()
        self.other.refresh_from_db()
        self.assertEqual(self.student.name, "Morgan Updated")
        self.assertEqual(self.other.name, "Alex Rivera")

    def test_invalid_update_preserves_original_data(self):
        response = self.client.post(reverse("student-update", kwargs={"pk": self.student.pk}),
                                    {"name": "Changed", "email": "invalid", "major": ""})
        self.assertIn("email", response.context["form"].errors)
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Morgan Chen")

    def test_delete_get_only_confirms_and_post_cascades(self):
        portfolio = Portfolio.objects.create(student=self.student, title="Delete fixture", contact_email=self.student.email)
        project = Project.objects.create(portfolio=portfolio, title="Delete project", description="Fixture")
        url = reverse("student-delete", kwargs={"pk": self.student.pk})
        response = self.client.get(url)
        self.assertContains(response, "Confirm delete")
        self.assertContains(response, reverse("student-detail", kwargs={"pk": self.student.pk}))
        self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())
        self.assertRedirects(self.client.post(url), reverse("student-list"))
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
        self.assertFalse(Portfolio.objects.filter(pk=portfolio.pk).exists())
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())
        self.assertTrue(Student.objects.filter(pk=self.other.pk).exists())

    def test_missing_student_routes_return_404(self):
        for name in ("student-detail", "student-update", "student-delete"):
            with self.subTest(route=name):
                self.assertEqual(self.client.get(reverse(name, kwargs={"pk": 999999})).status_code, 404)

    def test_create_portfolio_link_only_without_existing_portfolio(self):
        url = reverse("student-detail", kwargs={"pk": self.student.pk})
        self.assertContains(self.client.get(url), "Create Portfolio")
        Portfolio.objects.create(student=self.student, title="Existing", contact_email=self.student.email)
        self.assertNotContains(self.client.get(url), "Create Portfolio")

    def test_portfolio_form_has_existing_student_selection_and_initial_value(self):
        response = self.client.get(reverse("portfolio-create"), {"student": self.student.pk})
        form = response.context["form"]
        self.assertEqual(form.initial["student"], self.student)
        self.assertEqual(form.initial["contact_email"], self.student.email)
        self.assertEqual(set(form.fields["student"].queryset), {self.student, self.other})

    def test_valid_portfolio_uses_selected_student(self):
        response = self.client.post(reverse("portfolio-create"), self.portfolio_data(self.other))
        portfolio = Portfolio.objects.get(student=self.other)
        self.assertRedirects(response, portfolio.get_absolute_url())
        self.assertFalse(Portfolio.objects.filter(student=self.student).exists())

    def test_invalid_portfolio_is_not_saved(self):
        for changes, field in (({"contact_email": "bad"}, "contact_email"), ({"title": ""}, "title"),
                               ({"student": 999999}, "student")):
            with self.subTest(field=field):
                response = self.client.post(reverse("portfolio-create"), self.portfolio_data(**changes))
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context["form"].errors)
                self.assertFalse(Portfolio.objects.exists())

    def test_duplicate_portfolio_rejected_without_changing_original(self):
        self.client.post(reverse("portfolio-create"), self.portfolio_data())
        response = self.client.post(reverse("portfolio-create"), self.portfolio_data(title="Duplicate"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("student", response.context["form"].errors)
        self.assertEqual(Portfolio.objects.filter(student=self.student).count(), 1)
        self.assertEqual(Portfolio.objects.get(student=self.student).title, "Course portfolio")

    def test_inactive_portfolio_redirects_to_student_and_stays_private(self):
        data = self.portfolio_data()
        data.pop("is_active")
        response = self.client.post(reverse("portfolio-create"), data)
        portfolio = Portfolio.objects.get(student=self.student)
        self.assertRedirects(response, reverse("student-detail", kwargs={"pk": self.student.pk}))
        self.client.logout()
        self.assertEqual(self.client.get(portfolio.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse("portfolio-list")), portfolio.title)

    def test_two_projects_can_belong_to_one_portfolio(self):
        portfolio = Portfolio.objects.create(student=self.student, title="Projects", contact_email=self.student.email)
        form = self.client.get(reverse("project-create"), {"portfolio": portfolio.pk}).context["form"]
        self.assertEqual(form.initial["portfolio"], portfolio)
        for title in ("First project", "Second project"):
            response = self.client.post(reverse("project-create"),
                                        {"portfolio": portfolio.pk, "title": title, "description": "Full project description"})
            self.assertRedirects(response, portfolio.get_absolute_url())
            self.assertContains(self.client.get(response.url), title)
        self.assertEqual(portfolio.projects.count(), 2)

    def test_invalid_project_does_not_save(self):
        portfolio = Portfolio.objects.create(student=self.student, title="Projects", contact_email=self.student.email)
        response = self.client.post(reverse("project-create"), {"portfolio": portfolio.pk, "title": "", "description": ""})
        self.assertIn("title", response.context["form"].errors)
        self.assertIn("description", response.context["form"].errors)
        self.assertFalse(Project.objects.exists())

    def test_project_for_inactive_portfolio_redirects_to_student(self):
        portfolio = Portfolio.objects.create(student=self.student, title="Private", contact_email=self.student.email, is_active=False)
        response = self.client.post(reverse("project-create"),
                                    {"portfolio": portfolio.pk, "title": "Private project", "description": "Not public"})
        self.assertRedirects(response, reverse("student-detail", kwargs={"pk": self.student.pk}))
        self.assertEqual(self.client.get(portfolio.projects.get().get_absolute_url()).status_code, 404)

    def test_anonymous_cannot_read_student_directory_or_modify_data(self):
        self.client.logout()
        urls = [reverse(name) for name in ("student-list", "student-create", "portfolio-create", "project-create")]
        urls += [reverse(name, kwargs={"pk": self.student.pk}) for name in ("student-detail", "student-update", "student-delete")]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 302)
                self.assertEqual(self.client.post(url, {}).status_code, 302)
        self.assertEqual(Student.objects.count(), 2)

    def test_signed_in_user_without_permissions_is_forbidden(self):
        user = get_user_model().objects.create_user("visitor", password="test-only-password")
        self.client.force_login(user)
        for name in ("student-list", "student-create", "portfolio-create", "project-create"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 403)
        for name in ("student-update", "student-delete"):
            self.assertEqual(self.client.post(reverse(name, kwargs={"pk": self.student.pk}), {}).status_code, 403)
        self.assertEqual(Student.objects.count(), 2)

    def test_post_requires_csrf_token(self):
        browser = Client(enforce_csrf_checks=True)
        browser.force_login(self.admin)
        url = reverse("student-create")
        self.assertEqual(browser.post(url, {"name": "Blocked"}).status_code, 403)
        self.assertContains(browser.get(url), "csrfmiddlewaretoken")
        token = browser.cookies["csrftoken"].value
        response = browser.post(url, {"name": "Allowed", "email": "allowed@example.com", "major": "", "csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(name="Allowed").exists())

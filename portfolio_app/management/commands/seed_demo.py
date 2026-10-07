from django.core.management.base import BaseCommand
from django.db import transaction
from portfolio_app.models import Student, Portfolio, Project


class Command(BaseCommand):
    help = "Add fictional portfolio examples without overwriting existing content."

    @transaction.atomic
    def handle(self, *args, **options):
        examples = [
            ("Jordan Rivera", "jordan.rivera@example.com", "CSCI-BS", [
                ("Accessible Portfolio", "A fictional example of a responsive website using semantic HTML and keyboard-friendly navigation."),
                ("Student Database", "A fictional Django exercise connecting Python models, migrations, and SQLite queries."),
            ]),
            ("Taylor Morgan", "taylor.morgan@example.com", "CPEN-BS", [
                ("Sensor Prototype", "A fictional project exploring how sensor measurements can be collected and displayed."),
                ("Project Tracker", "A fictional application organizing tasks and recording progress through small iterations."),
            ]),
        ]
        for name, email, major, projects in examples:
            student, _ = Student.objects.get_or_create(email=email, defaults={"name": name, "major": major})
            portfolio, _ = Portfolio.objects.get_or_create(student=student, defaults={
                "title": f"{name}'s Portfolio", "contact_email": email,
                "about": "Fictional course example demonstrating student information and related projects.",
            })
            for title, description in projects:
                Project.objects.get_or_create(portfolio=portfolio, title=title, defaults={"description": description})
        self.stdout.write(self.style.SUCCESS("Fictional examples ready; existing content preserved."))

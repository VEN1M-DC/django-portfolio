# Portfolio relationship verification

Verified October 7, 2026 using Python 3.14.7 and Django 6.1.1.

Implemented Student → Portfolio as OneToOneField, Portfolio → Project as ForeignKey, CASCADE deletion, admin registration, and detail URLs. Project has the required title and description from the course UML. The original Student lab schema is preserved; its email uses Django's default maximum length and its major remains optional, differing from the later diagram's labels.

Migration 0002_portfolio_project applied successfully. SQLite inspection confirmed:

| Table | Columns |
| --- | --- |
| portfolio_app_student | id, name, email, major |
| portfolio_app_portfolio | id, title, contact_email, is_active, about, student_id |
| portfolio_app_project | id, title, description, portfolio_id |

Local example counts: 2 Students, 2 Portfolios, 4 Projects. Each portfolio contains two fictional projects. Student IDs 1 and 2 remain Jordan Rivera and Taylor Morgan. Example content uses example.com addresses. `python manage.py seed_demo` recreates examples in a new clone without replacing existing content.

`Portfolio.objects.filter(student__major="CSCI-BS")` returns Jordan Rivera's Portfolio. The generated SQL joins portfolio_app_portfolio to portfolio_app_student on student_id and filters the major. Reverse access is student.portfolio and portfolio.projects.all().

Seven automated tests passed. They cover Student persistence, admin Student creation, duplicate Portfolio rejection by the database, multiple Projects and relationship filters, Student deletion cascading to Portfolio and Project, Portfolio deletion preserving Student, and public page visibility for inactive content. Destructive checks run in Django's temporary test database.

The root URL lists active portfolios. Portfolio and Project detail pages return stored content; inactive portfolio content is hidden. Local URLs work only on the server's computer. No public Django hosting has been provisioned.

The implementation was developed on codex/model_setup. The database and private admin credentials are excluded from Git. This record reports technical checks, not personal classroom reflection or screenshots of a student's SQLite Viewer session.

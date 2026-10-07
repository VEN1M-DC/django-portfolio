# Django portfolio

Course project with the Student model and Django admin.

## Windows setup

Use Python 3.14 (this project was verified with 3.14.7).

```powershell
py -m venv djvenv
.\djvenv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py test
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/ to view active portfolios and their projects. Open http://127.0.0.1:8000/admin/ to manage Students, Portfolios, and Projects. Create an admin account locally; no password belongs in Git.

Each Student can have zero or one Portfolio. Each Portfolio belongs to one Student and can have many Projects. Deleting a Student cascades to its Portfolio and Projects; deleting a Portfolio preserves its Student. Inactive portfolios and their project pages return 404 to public visitors.

`seed_demo` adds fictional Jordan Rivera and Taylor Morgan portfolios and two projects each. It is safe to rerun and preserves existing content. The source UML calls for Project.title, a required description, and get_absolute_url; those are implemented. Student retains the initial lab's optional major and default email field rather than retroactively changing that lab's schema to the diagram's stricter labels.

The lab defines name, email, and major. Django generates an id primary key. `makemigrations` records model changes; `migrate` applies schema changes; saving an admin form creates a row.

```python
from portfolio_app.models import Student
Student.objects.all()
Student.objects.count()
Student.objects.filter(major="CSCI-BS")
Student.objects.first()
```

Keep djvenv, db.sqlite3, and .private out of Git. Each clone recreates its database and admin account locally. GitHub Pages can serve the documentation but cannot run this Django application.

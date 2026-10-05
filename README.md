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
python manage.py runserver
```

Open http://127.0.0.1:8000/admin/ and log in. Select Students to add records. The root URL retains Django's default installation page.

The lab defines name, email, and major. Django generates an id primary key. `makemigrations` records model changes; `migrate` applies schema changes; saving an admin form creates a row.

```python
from portfolio_app.models import Student
Student.objects.all()
Student.objects.count()
Student.objects.filter(major="CSCI-BS")
Student.objects.first()
```

Keep djvenv, db.sqlite3, and .private out of Git. Each clone recreates its database and admin account locally. GitHub Pages can serve the documentation but cannot run this Django application.

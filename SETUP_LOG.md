# Django portfolio setup record

This school project follows the assignment in `Documents/`. This log records commands, reported results, and checkpoint status. It is not an automatically captured terminal transcript. Commands below were reported by the student unless explicitly described as assistant actions.

## 1. Python verification — complete

```powershell
py --version
python3 --version
```

Both commands returned `Python 3.14.7` in the student's PowerShell window. An earlier assistant sandbox check returned 3.14.6; the student's development environment version is 3.14.7.

## 2. Local repository — complete

Working directory: `C:\Users\VEN1M\OneDrive\Desktop\django-portfolio`.

The assistant initialized Git and configured `origin` as `https://github.com/VEN1M-DC/django-portfolio.git`.

The student initially ran `mkdir django-portfolio`, `cd django-portfolio`, and `git init` under `C:\Windows\System32`. That created a separate accidental repository. The student then switched to the correct project:

```powershell
cd C:\Users\VEN1M\OneDrive\Desktop\django-portfolio
py --version
```

The System32 repository is not used for this assignment. No cleanup has been performed.

The assistant added `.gitignore` to exclude the virtual environment, Python caches, OS/editor artifacts, local environment secrets, and the generated SQLite database. Project source, dependency versions, assignment documents, and this log belong in Git.

## 3. Virtual environment — complete

```powershell
py -m venv djvenv
```

The environment was created in the project folder.

## 4. Activation — complete

```powershell
.\djvenv\Scripts\Activate.ps1
```

The prompt displayed `(djvenv)`. The student also ran:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\djvenv\Scripts\Activate.ps1
python --version
```

The execution-policy confirmation was answered `y`. This setting applies only to that PowerShell process. Activation had already succeeded, so this workaround was unnecessary in this session. Python inside the active environment reported `3.14.7`.

## 5. Compatibility — complete

- Python: **3.14.7**
- Planned Django series: **6.1**
- Compatible: **YES**
- Source checked by assistant: https://docs.djangoproject.com/en/6.1/faq/install/#what-python-version-can-i-use-with-django

The official table lists Python 3.14 as supported by Django 6.1.

## 6. Django installation — complete

```powershell
python -m pip install django
python -m django --version
```

Installation reported success with `asgiref-3.12.1`, `django-6.1.1`, `sqlparse-0.6.0`, and `tzdata-2026.4`. Django's version command returned **6.1.1**.

The assistant independently ran the virtual environment's `python -m pip freeze` and saved its exact package versions in `requirements.txt`:

```text
asgiref==3.12.1
Django==6.1.1
sqlparse==0.6.0
tzdata==2026.4
```

## 7. Django project creation — complete

The student ran these commands in the active virtual environment:

```powershell
django-admin startproject django_project .
dir
```

The command completed without an error. The assistant verified `manage.py` and the generated `django_project` package containing `__init__.py`, `settings.py`, `urls.py`, `asgi.py`, and `wsgi.py`. `manage.py` references `django_project.settings`. The generated files have been left unchanged, as the assignment requests.

The trailing dot creates the project in the current repository directory. `manage.py` runs Django management commands; `settings.py` holds project configuration; `urls.py` maps URLs; `asgi.py` and `wsgi.py` are server entry points; `__init__.py` marks the Python package.

Server startup and browser verification were subsequently completed in step 8 below.

## 8. Development server and browser verification — complete

The student ran `python manage.py runserver` in the active environment. The supplied output reports zero system-check issues, Django 6.1.1, and a running development server at http://127.0.0.1:8000/ on September 17, 2026, at 08:17:38.

The complete supplied startup output is saved in [Documents/server-startup-output.txt](Documents/server-startup-output.txt). It includes a warning about 18 unapplied migrations for admin, auth, contenttypes, and sessions, plus the standard development-server warning. No migrations have been reported as applied.

The student's screenshot visibly confirms the default Django success page at the local server address. A copy of the original screenshot is saved as [Documents/django-browser-success.png](Documents/django-browser-success.png). The original Desktop file was preserved. The screenshot shows the browser only; the assignment's screenshot showing both the running terminal and browser is still pending.

The student also supplied request logs: GET / returned HTTP 200 at 08:18:42, confirming a successful homepage response; GET /favicon.ico returned HTTP 404 at 08:18:43 because no tab icon was available. These lines are preserved in the server output file. The missing icon does not prevent the default success page from working. The development-server warning is expected for this local assignment.

The student supplied a separate terminal screenshot, saved as [Documents/django-terminal-success.png](Documents/django-terminal-success.png). It visibly shows the active virtual environment, Django 6.1.1, project creation command, successful system check, development server address, and HTTP 200 homepage request. The original Desktop image was preserved. Browser and terminal evidence are now both saved as separate screenshots; a single screenshot showing both windows together remains pending for the assignment's requested format.

The student subsequently supplied the combined screenshot [Documents/django-server-success.png](Documents/django-server-success.png), showing the browser success page and the running PowerShell server side by side. The system check, server address, Django version, and successful homepage request are visible. This completes the screenshot checkpoint. Earlier notes about the combined screenshot being pending describe the previous state; the original Desktop screenshots remain preserved.

## Remaining assignment checkpoints

- [x] Step 7: Generate `django_project` in this directory and examine the generated files.
- [x] Step 8: Start the development server and verify the default success page.
- [x] Capture a screenshot showing the running terminal server and browser success page; save it in the repository for submission.
- [ ] Step 9: Commit the working Django project, push to GitHub, and verify the remote files exclude `djvenv`.
- [ ] Step 10: Stop the server, deactivate, reactivate, restart, and verify the page again.

These checkpoints remain pending until actually performed. Git records saved files and commits, not terminal history automatically. Update this log as the student completes each step.






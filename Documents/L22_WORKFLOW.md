# Student and portfolio workflow

Verified November 12, 2026 against the course's updated Django views slides,
parts 1–4, including portfolio creation starting on slide 56.

## What works

- List students and open the selected student's detail page.
- Create a student and redirect using `self.object.pk`, not a fixed ID.
- Update existing name, email, and major values.
- Confirm deletion with POST; GET only displays the confirmation.
- Create a portfolio for an existing student selected in the form.
- Hide Create Portfolio after that student has a portfolio.
- Reject invalid fields and a second portfolio for the same student.
- Add several projects to the selected portfolio.
- Keep inactive portfolio and project pages private.

## Request flow

1. GET `/students/create/` displays a generated model form.
2. POST validates name, email, and major. Invalid input redisplays errors.
3. A valid form inserts Student; `get_success_url()` redirects to its detail URL.
4. The detail template checks `student.portfolio`. Without one, it offers Create Portfolio.
5. GET `/portfolios/create/?student=<id>` preselects that student and contact email.
   The Student relationship remains selectable, as required by the exercise.
6. POST validates the selected student and portfolio fields, including one-to-one uniqueness.
7. A valid active portfolio redirects to its public detail page. An inactive portfolio
   redirects to the authorized student detail page instead of an unavailable public page.
8. Add Project opens a generated form with the portfolio preselected. Saving adds a
   related Project and returns to the appropriate portfolio or student page.

## Routes and files

| Named route | Path | View |
|---|---|---|
| student-list | /students/ | StudentListView |
| student-detail | /students/&lt;pk&gt;/ | StudentDetailView |
| student-create | /students/create/ | StudentCreateView |
| student-update | /students/&lt;pk&gt;/update/ | StudentUpdateView |
| student-delete | /students/&lt;pk&gt;/delete/ | StudentDeleteView |
| portfolio-create | /portfolios/create/ | PortfolioCreateView |
| project-create | /projects/create/ | ProjectCreateView |

Implementation: `portfolio_app/views.py`, `django_project/urls.py`, and the
`portfolio_app/templates/portfolio_app/` templates. No schema changes are required.
Existing Student, Portfolio, and Project relationships supply the forms' choices.

## Validation and access

Django validates required fields, maximum lengths, email syntax, major choices,
existing related-record IDs, and Portfolio.student uniqueness. Email syntax
validation does not prove that an address exists or require the MSU Denver domain.

All modifying forms use CSRF tokens and check model permissions. Anonymous
requests redirect to the admin login; authenticated accounts lacking required
permissions receive 403. The Student directory also requires view_student to avoid
exposing student email records. A Student is a course data record, not an auth User.

Student deletion cascades through Portfolio to Project because both relationships
use on_delete=CASCADE. The confirmation page explains this before the POST.

## Verification

On November 12, 2026:

```powershell
.\djvenv\Scripts\python.exe manage.py check
.\djvenv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\djvenv\Scripts\python.exe manage.py test portfolio_app --verbosity 2
```

- System check: no issues.
- Migration check: no changes detected.
- 32 automated tests passed: 20 new workflow tests plus 12 existing tests.
- Tests use an isolated database; existing local students, portfolios, and projects
  were not deleted or replaced.

The new tests exercise two distinct student redirects, invalid input, selected
record updates, delete confirmation/cascade, conditional links, duplicate portfolios,
multiple projects, inactive visibility, permissions, and CSRF enforcement.

During verification, a test helper used `student` both for an object argument and
for a deliberately invalid submitted ID. Renaming the object argument to
`selected_student` let the invalid-ID test reach form validation. The final test run passed.

## Course process notes

This is an implementation and test record. It does not document a group meeting,
an instructor check-in, or a handwritten plan. The lecture asks for those activities
in addition to working code. The accompanying Word document contains the technical
plan and test cases for review; it is not evidence that those class activities occurred.

Source: [Django Views, URLs, and Templates Introduction](https://docs.google.com/presentation/d/17gbQS5HHmfZsT0YFp1c6Wr7atBjMPxsjGKAUPu0zxTo/edit).

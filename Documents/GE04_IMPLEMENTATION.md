# GE04 implementation and verification

Verified locally on 4 November 2026. Repository: https://github.com/VEN1M-DC/django-portfolio

## Audit

Already present: Student, Portfolio and Project models; one-to-one student/portfolio
relationship; one-to-many portfolio/project relationship; migrations and admin
registration; home page; named detail URL and model get_absolute_url; project pages;
empty-project message; seven model/admin/public-page tests.

Completed for GE04:

| Requirement | Implementation |
| --- | --- |
| Generic Portfolio DetailView | PortfolioDetailView in portfolio_app/views.py |
| Primary-key routing | portfolios/<int:pk>/ calls PortfolioDetailView.as_view() |
| Required template | portfolio_app/templates/portfolio_app/portfolio_detail.html |
| Title, about, email and active status | Detail template displays all four |
| Related project titles and descriptions | portfolio.projects.all; descriptions are no longer truncated |
| No-project message | Template for/empty branch |
| Home-to-detail navigation | Existing named portfolio-detail URL via get_absolute_url |
| Return navigation | Explicit Back to all portfolios link using portfolio-list |
| Missing ID | Generic DetailView returns 404 |

Inactive portfolios still return 404 to public visitors. The Active status is
visible on published detail pages; inactive records remain manageable in Admin.
The pre-existing individual Project pages were retained, although GE04 does not
require them. No forms, schema changes, new repository or deployment were needed.

## Verification

Run these commands from the repository root on Windows:

```powershell
.\djvenv\Scripts\python.exe manage.py check
.\djvenv\Scripts\python.exe manage.py test -v 2
.\djvenv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Observed: system check found no issues; all 12 tests passed; no migration changes.
Tests use a separate temporary database and do not alter the development records.

The five new tests cover distinct primary keys and all displayed fields, project
isolation and full descriptions, an empty portfolio, missing-ID 404, and two-way
home/detail navigation. Existing tests also verify inactive records are hidden,
admin access, persistence, one-to-one constraints and cascade behavior.

## Local demonstration records

The existing development database had three students, two portfolios and four
projects. A portfolio was added for the existing John Smith classroom record
using the ORM, without changing any Student or Project records. This is fictional
demonstration content and uses john.smith@example.com as the contact address.
The development database is ignored by Git, so these local IDs are not guaranteed
in another clone. Use Django Admin to create/update your own test records as the
assignment requests.

- Home: http://127.0.0.1:8000/
- With projects: http://127.0.0.1:8000/portfolios/1/
- Another portfolio: http://127.0.0.1:8000/portfolios/2/
- Without projects: http://127.0.0.1:8000/portfolios/3/
- Missing record example: http://127.0.0.1:8000/portfolios/999999/
- Admin: http://127.0.0.1:8000/admin/

These links require the local Django development server. GitHub Pages cannot run
the Django server or its database.

## Individual technical summary preparation

The assignment calls for approximately 3–4 pages, screenshots, relevant code,
explanation of primary-key retrieval, relationships, routing/templates, and
expected versus actual test results. Its instructions require the student's own
understanding and prohibit AI-generated summary prose. The accompanying Word
working draft therefore contains evidence and writing prompts, not a completed
student-authored submission. Review the code, perform the Admin steps, write your
explanations, and follow the course's assistance-disclosure requirements.

Do not represent automated testing or assisted implementation as personal class
experience. No teammate work or feedback has been invented.

Assignment: https://docs.google.com/document/d/1Fy8AWwg6cZwwd7HKqIwVADcYfzK1ZC_-b88P9CuQ1CI/edit

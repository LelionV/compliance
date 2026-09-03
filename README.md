# TODOMU — OSH Compliance Platform (Django, multi-tenant)

A Django rebuild of the reference dashboard: an auditing organization (you) manages
OSH/DOSHS compliance for many client companies. Platform admins can switch between
companies from a dropdown; each client company can only ever see its own data.

## How multi-tenancy works

- `apps/organizations/models.py` — `Organization` (client company) and `Site` (branch).
- `apps/accounts/models.py` — custom `User` with `role`:
  - `platform_admin` — your auditors. Not tied to one organization; picks the
    "active" one from the topbar dropdown (or "All sites").
  - `org_admin` / `org_staff` — a client company's own users. Locked to their
    `user.organization` — this is enforced server-side in
    `apps/core/middleware.py::OrganizationMiddleware`, which **ignores** any
    session-based org selection for non-platform-admin users. They cannot see
    or switch to another company no matter what they send in a request.
- `apps/core/mixins.py::OrgRequiredMixin` — every list/create/update/delete view
  for every compliance module inherits this. It:
  - Filters `get_queryset()` to `organization=request.organization`
  - Strips the `organization` field out of any form (can't be spoofed via POST)
  - Scopes any FK dropdown (e.g. "source incident" on a CAPA) to the same org
  - Redirects to `/select-org/` if a platform admin hasn't picked a company yet

## Modules included

Matches the reference sidebar: Safety dashboard, Compliance calendar, Risk
assessments, Job safety analyses, Toolbox talks, Incident reporting,
Inspections, PPE issuance, Fire equipment, Training matrix, First aiders &
marshals, OSH committee, CAPA tracker, DOSHS reports.

Each module has full CRUD (list / add / edit / delete), generated via a shared
factory in `apps/core/generic.py` so every module gets the same org-scoping
and UI for free — you don't need to hand-roll views per module.

## Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo      
python manage.py runserver
```

Visit http://127.0.0.1:8000/

### Demo logins (created by `seed_demo`)

| Role | Username | Password | Sees |
|---|---|---|---|
| Platform admin (auditor) | `auditor` | `admin12345` | All companies, can switch via topbar dropdown |
| Client (Tafari Millers Ltd) | `tafari_hse` | `client12345` | Only Tafari Millers' own data — no switcher shown |

Also creates a second company, **Coastal Logistics Ltd**, with no data yet, so
you can see the admin switch into an empty portal.

Django admin is at `/admin/` (log in as `auditor`) for bulk data management,
adding new client organizations, managing users, etc.

## Project layout

```
config/                 settings, root urls
apps/
  accounts/              custom User model, roles
  organizations/          Organization, Site, ComplianceItem + seed_demo command
  core/                    tenant middleware, mixins, generic CRUD factory, templatetags
  dashboard/               Safety Command Centre view + org switcher
  incidents/ risk/ inspections/ ppe/ fire/ training/ capa/ doshs/
                           one compliance module each (models + generated views/urls)
templates/
  base.html                sidebar/topbar shell
  dashboard/home.html      the KPI + chart dashboard
  core/generic_*.html      shared list/form/delete templates for every module
  registration/login.html
static/css/app.css         styling matching the reference screenshot
```

## Extending

To add a brand-new module (say, "Vehicle Safety Checks"):

1. Create the app, add a model with an `organization = ForeignKey(Organization, ...)` field.
2. In `views.py`:
   ```python
   from apps.core.generic import build_crud_views
   from .models import VehicleCheck
   ListView, CreateView, UpdateView, DeleteView = build_crud_views(
       model=VehicleCheck, fields=[...], url_namespace="vehicle_checks", page_title="Vehicle Check",
   )
   ```
3. Standard `urls.py` with `list/add/<pk>/edit/<pk>/delete` names, wire into `config/urls.py`.
4. Add a sidebar link in `templates/base.html`.

That's it — org-scoping, form filtering, and the generic templates all apply automatically.

## Newly added functionality (round 2)

- **Notifications** (`apps/notifications`) — a bell dropdown in the topbar,
  polled every 60s. Auto-fires on new incidents, new/overdue CAPAs, and DOSHS
  report generation, scoped strictly to the active organization. Mark-as-read
  and mark-all-read endpoints included.
- **Audit trail** (`apps/core/models.py::AuditLogEntry`) — append-only log of
  every create/update/delete on Incident, RiskAssessment, Inspection,
  CorrectiveAction, DOSHSReport, StatutoryDeadline, FireEquipment, and
  ComplianceItem. Captures the acting user via a thread-local
  (`apps/core/current_user.py`) so signals — which don't get the request —
  can still attribute changes correctly. Browsable (read-only) at
  `/admin/core/auditlogentry/`.
- **Real DOSHS pack PDF generation** (`apps/doshs/pdf.py`, uses ReportLab) —
  the "Generate DOSHS pack" button on the dashboard now produces an actual
  multi-section PDF (compliance summary, open incidents, open CAPAs, fire
  equipment service status, risk assessments due, statutory deadlines),
  attaches it to a new `DOSHSReport`, and offers it for download.
- **Compliance calendar** (`/doshs-reports/calendar/`) — statutory deadlines
  grouped by month, replacing the earlier placeholder link to the DOSHS list.
- **CSV export** — every module's list view now has an "Export CSV" button
  (`?export=csv`), still fully org-scoped.
- **Compliance-by-site chart** — added to the dashboard next to the incident
  trend chart, matching the reference screenshot's bar chart.
- **Self-service team management** (`apps/accounts`) — an `org_admin` (the
  client's own HSE officer) can now add/edit their own team's `org_staff`
  users from inside the portal at `/accounts/team/`, without ever touching
  Django admin. New users are force-scoped to the admin's own organization
  server-side — the form has no way to submit a different one. Platform
  admins are explicitly excluded from this view (they manage cross-org users
  via `/admin/` instead), verified to return 403 if attempted.

All of the above were tested end-to-end via Django's test client: notification
counts, real PDF byte output (multi-KB, all 6 sections), CSV content,
audit log actor attribution, and the org-admin-only access boundary on team
management.


## Newly added functionality (round 3)

- **Company (organization) management in-app** — platform admins no longer
  need Django admin to onboard a new client. `/companies/` gives a full
  list/add/edit/delete UI (`apps/organizations/views.py`), including logo
  upload and inline site/branch management on the edit page. The "select a
  company" landing page also links here.
- **Fixed placeholder sidebar links** — Job Safety Analyses and Toolbox Talks
  previously pointed at the Risk Assessments list; First Aiders/Marshals and
  OSH Committee previously pointed at the Training Records list. Each now has
  its own real CRUD (`/job-safety-analyses/`, `/toolbox-talks/`,
  `/first-aiders/`, `/osh-committee/`).
- **Password reset & change** — full "forgot password" email flow (uses
  Django's console/dummy backend by default — wire up real SMTP via
  `EMAIL_BACKEND` in settings for production) plus an in-app "change
  password" page linked from the topbar.
- **Working global search** — the topbar search bar now actually searches
  incidents, risk assessments, JSAs, toolbox talks, training records, first
  aiders, CAPA items, and DOSHS records/deadlines, all scoped to the active
  organization (`apps/core/search.py`).

All verified end-to-end: company add/edit/site management, JSA/toolbox/first-aider/
committee CRUD, the full password-reset round trip (email → token → new
password → login), search, and a full regression pass confirming tenant
isolation (client users get 403 on `/companies/`) and all round-2 features
(PDF generation, audit log, team management, CSV export) still work.


## Notes / production TODO


- `SECRET_KEY` and `DEBUG=True` in `config/settings.py` are dev-only — set via
  environment variables before deploying.
- Swap SQLite for Postgres in `DATABASES` for production.
- The AI toolbox talk assistant and SMS/email deadline reminders are modeled
  (fields exist: `StatutoryDeadline.notify_email/sms`, `ToolboxTalk.ai_generated`)
  but actual SMTP/SMS/AI calls are left as integration points for you to wire
  up (e.g. Celery + django-anymail for scheduled reminders). DOSHS pack PDF
  generation is fully implemented (see `apps/doshs/pdf.py`, ReportLab-based).
# compliance

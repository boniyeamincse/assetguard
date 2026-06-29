# AssetGuard Software Specification v2.0

## Cybersecurity Asset, Bug & Vulnerability Tracking System

## 1. Project Name

**AssetGuard**

## 2. Project Type

Web-based cybersecurity asset, bug, and vulnerability tracking system.

## 3. Technology Stack

### Backend

* Python 3.12+
* Django 5+
* Django ORM
* Django Template Engine
* Django Authentication System
* Django Admin Panel

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Bootstrap 5 optional

### Database

Development:

* SQLite

Production:

* PostgreSQL or MySQL

Recommended production database:

* PostgreSQL

### Server

Development:

* Django development server

Production:

* Ubuntu Server
* Gunicorn
* Nginx
* PostgreSQL
* Supervisor or systemd

## 4. Project Concept

Every software project or IT system will be treated as an **Asset**.

Each asset can have multiple **Bugs / Vulnerabilities**.

The workflow:

```text
Security Team finds vulnerability
↓
Security Team reports vulnerability in AssetGuard
↓
Vulnerability assigned to Software Team
↓
Software Team fixes vulnerability
↓
Security Team retests
↓
Security Team closes or reopens vulnerability
```

## 5. User Roles

AssetGuard will have the following roles:

```text
Super Admin
Security Team
Software Team
Project Owner
Management Viewer
```

## 6. Role Responsibilities

### 6.1 Super Admin

* Full system access
* Manage users
* Manage teams
* Manage assets
* Manage vulnerabilities
* Manage reports
* View audit logs
* Configure settings

### 6.2 Security Team

* View assets
* Create vulnerability reports
* Upload evidence
* Assign vulnerabilities
* Add comments
* Retest vulnerabilities
* Close vulnerabilities
* Reopen vulnerabilities
* View security reports

### 6.3 Software Team

* View assigned vulnerabilities
* Add comments
* Update fix progress
* Upload fix evidence
* Mark vulnerabilities as fixed
* Send vulnerabilities for retest

### 6.4 Project Owner

* View own project assets
* View vulnerabilities under own assets
* Add comments
* Monitor SLA
* View project-level reports

### 6.5 Management Viewer

* View dashboard
* View reports
* Read-only access
* No create, update, or delete permission

## 7. Django Apps Structure

The project should be developed using modular Django apps.

```text
assetguard/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── dashboard/
│   ├── views.py
│   ├── urls.py
│   └── services.py
│
├── teams/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── assets/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── admin.py
│
├── vulnerabilities/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── services.py
│   └── admin.py
│
├── reports/
│   ├── views.py
│   ├── urls.py
│   └── services.py
│
├── audit/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── includes/
│   │   ├── sidebar.html
│   │   ├── navbar.html
│   │   └── messages.html
│   │
│   ├── accounts/
│   ├── dashboard/
│   ├── teams/
│   ├── assets/
│   ├── vulnerabilities/
│   ├── reports/
│   └── audit/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── images/
│
├── media/
│   └── evidences/
│
├── manage.py
├── requirements.txt
└── README.md
```

## 8. Main Modules

```text
Authentication
Dashboard
User Management
Team Management
Asset / Project Management
Vulnerability / Bug Management
Assignment Management
Comment / Discussion
Evidence / Attachment
Retest Management
Reports
Audit Logs
Settings
```

## 9. Django Models

## 9.1 Custom User Model

App: `accounts`

Use Django custom user model by extending `AbstractUser`.

Model name:

```python
User
```

Fields:

```text
id
username
email
first_name
last_name
role
phone
department
designation
status
created_at
updated_at
```

Roles:

```text
super_admin
security_team
software_team
project_owner
management_viewer
```

Status:

```text
Active
Inactive
```

## 9.2 Team Model

App: `teams`

Model name:

```python
Team
```

Fields:

```text
id
team_name
team_type
description
status
members
created_at
updated_at
```

Team types:

```text
security
software
management
```

## 9.3 Asset Model

App: `assets`

Model name:

```python
Asset
```

Fields:

```text
id
asset_code
asset_name
asset_type
description
business_owner
project_owner
software_team
security_team
technology_stack
production_url
staging_url
repository_url
server_ip
database_name
criticality
status
created_by
created_at
updated_at
```

Asset types:

```text
Web Application
Mobile Application
API
Database
Server
Network Device
Desktop Application
Cloud Service
```

Criticality:

```text
Critical
High
Medium
Low
```

Status:

```text
Active
Inactive
Retired
```

Asset code format:

```text
AST-2026-0001
AST-2026-0002
AST-2026-0003
```

## 9.4 Vulnerability Model

App: `vulnerabilities`

Model name:

```python
Vulnerability
```

Fields:

```text
id
vulnerability_code
asset
title
description
bug_type
severity
priority
cvss_score
affected_url
affected_parameter
steps_to_reproduce
impact
recommendation
reported_by
assigned_to
status
due_date
fixed_at
closed_at
created_at
updated_at
```

Bug types:

```text
SQL Injection
Cross Site Scripting
Broken Access Control
Insecure Direct Object Reference
Authentication Bypass
Sensitive Data Exposure
Weak Password Policy
Missing Rate Limit
Security Misconfiguration
Vulnerable Component
File Upload Vulnerability
Business Logic Flaw
API Security Issue
Server Misconfiguration
Network Security Issue
Other
```

Severity:

```text
Critical
High
Medium
Low
Informational
```

Priority:

```text
Urgent
High
Medium
Low
```

Status:

```text
New
Triaged
Assigned
In Progress
Fixed
Ready for Retest
Retesting
Verified Fixed
Closed
Reopened
Rejected
Risk Accepted
```

Vulnerability code format:

```text
VULN-2026-0001
VULN-2026-0002
VULN-2026-0003
```

## 9.5 Vulnerability Comment Model

Model name:

```python
VulnerabilityComment
```

Fields:

```text
id
vulnerability
user
comment
created_at
```

## 9.6 Vulnerability Evidence Model

Model name:

```python
VulnerabilityEvidence
```

Fields:

```text
id
vulnerability
uploaded_by
file
file_name
file_type
file_size
created_at
```

Allowed file types:

```text
jpg
jpeg
png
gif
pdf
txt
doc
docx
xlsx
csv
```

Maximum file size:

```text
5 MB
```

## 9.7 Vulnerability Status History Model

Model name:

```python
VulnerabilityStatusHistory
```

Fields:

```text
id
vulnerability
old_status
new_status
changed_by
note
created_at
```

## 9.8 Retest Result Model

Model name:

```python
RetestResult
```

Fields:

```text
id
vulnerability
retested_by
result
note
retest_date
created_at
```

Retest result:

```text
Passed
Failed
Partially Fixed
```

## 9.9 Audit Log Model

App: `audit`

Model name:

```python
AuditLog
```

Fields:

```text
id
user
action
module_name
record_id
old_value
new_value
ip_address
user_agent
created_at
```

## 10. URL Structure

## 10.1 Authentication URLs

```text
/accounts/login/
/accounts/logout/
/accounts/profile/
/accounts/change-password/
```

## 10.2 Dashboard URLs

```text
/dashboard/
```

## 10.3 User Management URLs

```text
/accounts/users/
/accounts/users/create/
/accounts/users/<id>/
/accounts/users/<id>/edit/
/accounts/users/<id>/delete/
```

## 10.4 Team URLs

```text
/teams/
/teams/create/
/teams/<id>/
/teams/<id>/edit/
/teams/<id>/delete/
```

## 10.5 Asset URLs

```text
/assets/
/assets/create/
/assets/<id>/
/assets/<id>/edit/
/assets/<id>/delete/
```

## 10.6 Vulnerability URLs

```text
/vulnerabilities/
/vulnerabilities/create/
/vulnerabilities/<id>/
/vulnerabilities/<id>/edit/
/vulnerabilities/<id>/assign/
/vulnerabilities/<id>/update-status/
/vulnerabilities/<id>/retest/
/vulnerabilities/<id>/close/
/vulnerabilities/<id>/reopen/
```

## 10.7 Evidence URLs

```text
/vulnerabilities/<id>/evidence/upload/
/vulnerabilities/evidence/<id>/delete/
```

## 10.8 Comment URLs

```text
/vulnerabilities/<id>/comments/add/
```

## 10.9 Report URLs

```text
/reports/
/reports/assets/
/reports/vulnerabilities/
/reports/teams/
/reports/overdue/
/reports/export/csv/
```

## 10.10 Audit URLs

```text
/audit/logs/
```

## 11. Dashboard Specification

Dashboard cards:

```text
Total Assets
Total Vulnerabilities
Critical Open
High Open
Medium Open
Low Open
Retest Pending
Overdue
Closed
Risk Accepted
```

Dashboard charts:

```text
Vulnerability by Severity
Vulnerability by Status
Top Risky Assets
Monthly Vulnerability Trend
```

Dashboard tables:

```text
Recent 10 Vulnerabilities
Top 5 Risky Assets
Overdue Vulnerabilities
Recently Closed Vulnerabilities
```

## 12. Asset Management Features

Asset module must support:

```text
Create asset
Edit asset
View asset
Delete asset
List assets
Search assets
Filter by asset type
Filter by criticality
Filter by status
View vulnerabilities under asset
Calculate asset risk score
```

Asset view page must show:

```text
Asset details
Total vulnerabilities
Open vulnerabilities
Critical vulnerabilities
Assigned software team
Assigned security team
Related vulnerability list
Risk score
```

## 13. Vulnerability Management Features

Vulnerability module must support:

```text
Create vulnerability
Edit vulnerability
View vulnerability
Assign vulnerability
Update status
Add comments
Upload evidence
Retest vulnerability
Close vulnerability
Reopen vulnerability
Search vulnerabilities
Filter vulnerabilities
View status history
```

Filters:

```text
Asset
Severity
Priority
Status
Assigned User
Reported User
Date Range
```

## 14. Vulnerability Workflow

## 14.1 Normal Workflow

```text
New
↓
Triaged
↓
Assigned
↓
In Progress
↓
Fixed
↓
Ready for Retest
↓
Retesting
↓
Verified Fixed
↓
Closed
```

## 14.2 Failed Retest Workflow

```text
Ready for Retest
↓
Retesting
↓
Reopened
↓
Assigned
↓
In Progress
↓
Fixed
↓
Ready for Retest
```

## 14.3 Risk Accepted Workflow

```text
New / Triaged / Assigned
↓
Risk Accepted
```

## 14.4 Rejected Workflow

```text
New / Triaged
↓
Rejected
```

## 15. SLA Policy

Recommended SLA:

```text
Critical: 24-48 hours
High: 3-7 days
Medium: 15 days
Low: 30 days
Informational: Best effort
```

Overdue condition:

```text
status not in Closed, Verified Fixed, Risk Accepted, Rejected
AND due_date < today
```

## 16. Asset Risk Score

Risk score formula:

```text
Critical Open × 10
High Open × 7
Medium Open × 4
Low Open × 2
Informational Open × 1
```

Risk rating:

```text
0-10 = Low Risk
11-30 = Medium Risk
31-60 = High Risk
61+ = Critical Risk
```

## 17. Permission Matrix

| Module          | Super Admin | Security Team      | Software Team    | Project Owner | Management Viewer |
| --------------- | ----------- | ------------------ | ---------------- | ------------- | ----------------- |
| Dashboard       | Full        | Related            | Assigned         | Own Assets    | Read Only         |
| Users           | Full        | No                 | No               | No            | No                |
| Teams           | Full        | View               | View             | No            | No                |
| Assets          | Full        | View/Create        | View             | Own Assets    | View              |
| Vulnerabilities | Full        | Create/Edit/Retest | Assigned Update  | View/Comment  | View              |
| Comments        | Full        | Add                | Add              | Add           | View              |
| Evidence        | Full        | Upload/Delete Own  | Upload Own       | View          | View              |
| Reports         | Full        | Security Reports   | Assigned Reports | Own Reports   | View              |
| Audit Logs      | Full        | No                 | No               | No            | No                |
| Settings        | Full        | No                 | No               | No            | No                |

## 18. Template Design Specification

Use Django templates.

Base template:

```text
templates/base.html
```

Include files:

```text
templates/includes/sidebar.html
templates/includes/navbar.html
templates/includes/messages.html
```

Theme:

```text
Dark sidebar
White content area
Teal primary color
Red for Critical
Orange for High
Yellow for Medium
Green for Low
Blue for Informational
```

Sidebar menu:

```text
Dashboard

Asset Management
- All Assets
- Create Asset

Vulnerability Management
- All Vulnerabilities
- Report Vulnerability
- Assigned Vulnerabilities
- Retest Pending
- Closed Vulnerabilities

Reports
- Asset Report
- Vulnerability Report
- Team Report
- Overdue Report

Team Management
- All Teams
- Create Team

User Management
- All Users
- Create User

Audit Logs

Settings

Logout
```

## 19. Security Requirements

AssetGuard must apply the following Django security rules:

```text
Use Django authentication
Use login_required decorator
Use role-based permission checks
Use Django CSRF protection
Use Django ORM, avoid raw SQL
Use Django forms for validation
Use server-side validation
Use template auto-escaping
Restrict file upload types
Restrict file upload size
Rename uploaded files
Protect media file access if needed
Use secure password hashing
Use audit logs for important actions
Use session timeout
Do not expose debug errors in production
Set DEBUG=False in production
Configure ALLOWED_HOSTS in production
Use HTTPS in production
```

## 20. Forms Required

Accounts app:

```text
LoginForm
UserCreateForm
UserUpdateForm
PasswordChangeForm
```

Teams app:

```text
TeamForm
TeamMemberForm
```

Assets app:

```text
AssetForm
```

Vulnerabilities app:

```text
VulnerabilityCreateForm
VulnerabilityUpdateForm
VulnerabilityAssignForm
VulnerabilityStatusForm
RetestForm
CommentForm
EvidenceUploadForm
```

Reports app:

```text
ReportFilterForm
```

## 21. Views Required

Use Django class-based views or function-based views. Keep code clean and consistent.

Recommended:

```text
ListView
DetailView
CreateView
UpdateView
DeleteView
```

Custom views for:

```text
Dashboard
Assign vulnerability
Update status
Retest
Close
Reopen
Add comment
Upload evidence
Export CSV
Audit logs
```

## 22. Reports Required

Reports:

```text
Asset-wise vulnerability report
Severity-wise vulnerability report
Status-wise vulnerability report
Software team pending report
Security team reported issue report
Overdue vulnerability report
Closed vulnerability report
Monthly vulnerability trend
Critical open issue report
Risk accepted vulnerability report
```

Report filters:

```text
Date From
Date To
Asset
Severity
Status
Team
Assigned User
Reported User
```

Export options:

```text
Print
CSV Export
```

## 23. Audit Log Events

Track the following events:

```text
Login
Logout
Create user
Update user
Delete user
Create team
Update team
Delete team
Create asset
Update asset
Delete asset
Create vulnerability
Update vulnerability
Assign vulnerability
Update vulnerability status
Retest vulnerability
Close vulnerability
Reopen vulnerability
Upload evidence
Delete evidence
Add comment
Export report
```

## 24. Default Login Accounts

```text
Super Admin
Email: admin@demo.com
Password: 123456

Security Team
Email: security@demo.com
Password: 123456

Software Team
Email: software@demo.com
Password: 123456

Project Owner
Email: owner@demo.com
Password: 123456

Management Viewer
Email: management@demo.com
Password: 123456
```

## 25. Sample Assets

```text
ERP System
Type: Web Application
Criticality: Critical

HRM System
Type: Web Application
Criticality: High

Payroll API
Type: API
Criticality: Critical

Inventory Database
Type: Database
Criticality: High

Customer Portal
Type: Web Application
Criticality: Medium
```

## 26. Sample Vulnerabilities

```text
SQL Injection in Login API
Severity: Critical
Asset: ERP System

Missing Rate Limit in Login Page
Severity: High
Asset: HRM System

Sensitive Data Exposure in Payroll API
Severity: Critical
Asset: Payroll API

Weak Password Policy
Severity: Medium
Asset: Customer Portal

Missing Security Header
Severity: Low
Asset: ERP System
```

## 27. Development Order

```text
1. Create Django project
2. Create apps
3. Configure settings
4. Create custom user model
5. Create database models
6. Run migrations
7. Create seed data
8. Build authentication
9. Build base layout
10. Build dashboard
11. Build user management
12. Build team management
13. Build asset management
14. Build vulnerability management
15. Build comment system
16. Build evidence upload
17. Build retest workflow
18. Build reports
19. Build audit logs
20. UI polish
21. Final testing
22. README documentation
```

## 28. Claude CLI Development Instruction

Use this instruction in Claude CLI:

```text
You are an expert Python Django full-stack developer.

Build a complete cybersecurity asset, bug, and vulnerability tracking system named AssetGuard.

Use:
- Python 3.12+
- Django 5+
- Django ORM
- Django Template Engine
- HTML5
- CSS3
- Vanilla JavaScript
- SQLite for development
- PostgreSQL-ready settings for production

Do not use React, Vue, Angular, or Laravel.

Use modular Django apps:
- accounts
- dashboard
- teams
- assets
- vulnerabilities
- reports
- audit

Implement:
- Custom user model
- Role-based access control
- Asset management
- Vulnerability management
- Assignment workflow
- Retest workflow
- Comment system
- Evidence upload
- Reports
- Audit logs
- Dashboard
- Clean admin panel UI

Security:
- Use Django authentication
- Use CSRF protection
- Use login_required
- Use role-based permission checks
- Use Django ORM
- Validate forms
- Escape output
- Restrict file uploads
- Set DEBUG=False instruction for production

Build module by module.
After each module, test migrations, URLs, templates, and permissions.
Do not remove working code.
Give changed file summary after each module.
```

## 29. Final Acceptance Criteria

The project is complete when:

```text
Django project runs successfully.
Migrations run successfully.
Login works.
Logout works.
Role-based permission works.
Dashboard shows correct data.
Super Admin can manage users.
Super Admin can manage teams.
Assets can be created and viewed.
Asset detail page shows vulnerabilities.
Security Team can report vulnerability.
Vulnerability code auto-generates.
Vulnerability can be assigned to Software Team.
Software Team can update status.
Security Team can retest.
Passed retest closes vulnerability.
Failed retest reopens vulnerability.
Comments work.
Evidence upload works.
Reports work.
CSV export works.
Audit logs work.
No broken URLs.
No missing templates.
README setup guide exists.
```

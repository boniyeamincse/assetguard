# AssetGuard
Cybersecurity Asset, Bug & Vulnerability Tracking System

## Overview
AssetGuard is a comprehensive web-based platform for managing cybersecurity assets, vulnerabilities, and bug tracking. It enables security teams to report vulnerabilities, track remediation progress, and manage retest workflows across multiple assets.

## Technology Stack
- **Backend**: Python 3.12+ | Django 5.x
- **Frontend**: HTML5 | CSS3 | Vanilla JavaScript | Bootstrap 5
- **Database**: SQLite (Dev) | PostgreSQL (Production)
- **Server**: Django Dev Server (Dev) | Gunicorn + Nginx (Prod)

## Features
- Role-based access control (5 roles)
- Asset management and criticality tracking
- Vulnerability lifecycle management
- Assignment and workflow automation
- Evidence upload and management
- Comment and discussion system
- Security team retesting workflows
- Comprehensive reporting and CSV export
- Audit logging for compliance
- Dashboard with real-time statistics

## Installation

### Prerequisites
- Python 3.12+
- pip
- virtualenv

### Setup Instructions

1. **Clone or navigate to project directory**
```bash
cd assetsGuard
```

2. **Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Seed demo data**
```bash
python manage.py seed_data
```

6. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

7. **Run development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main App: http://localhost:8000/accounts/login/
- Admin Panel: http://localhost:8000/admin/

## Default Login Accounts

| Role | Email | Password |
|------|-------|----------|
| Super Admin | admin@demo.com | 123456 |
| Security Team | security@demo.com | 123456 |
| Software Team | software@demo.com | 123456 |
| Project Owner | owner@demo.com | 123456 |
| Management Viewer | management@demo.com | 123456 |

## Project Structure

```
assetguard/
├── config/                 # Django settings
├── accounts/              # User authentication & management
├── dashboard/             # Dashboard & analytics
├── teams/                 # Team management
├── assets/                # Asset management
├── vulnerabilities/       # Vulnerability management
├── reports/               # Reporting & exports
├── audit/                 # Audit logging
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── media/                 # Uploaded evidence
└── manage.py              # Django management
```

## App Modules

### Accounts
- User authentication (login/logout)
- User profile management
- User CRUD operations
- Password change functionality

### Dashboard
- Key statistics and metrics
- Vulnerability severity breakdown
- Asset risk scoring
- Recent activity
- Top risky assets

### Teams
- Team creation and management
- Team member assignments
- Team type classification
- Team filtering and search

### Assets
- Asset registration and lifecycle
- Asset type and criticality management
- Vulnerability tracking per asset
- Risk score calculation
- Asset status management

### Vulnerabilities
- Vulnerability reporting
- Bug type classification
- Severity and priority assignment
- Status workflow management
- Evidence upload and attachment
- Comment and discussion threads
- Retest workflow and results

### Reports
- Asset-wise vulnerability reports
- Severity-wise breakdown
- Status-wise reports
- Overdue vulnerability reports
- CSV export functionality
- Print-ready reports

### Audit
- Comprehensive audit logging
- User action tracking
- Change history
- IP address and user-agent logging
- Compliance reporting

## User Roles & Permissions

| Feature | Super Admin | Security | Software | Owner | Management |
|---------|-------------|----------|----------|-------|-----------|
| Dashboard | Full | Related | Assigned | Own | Read-only |
| Users | Full | No | No | No | No |
| Teams | Full | View | View | No | No |
| Assets | Full | View/Create | View | Own | View |
| Vulnerabilities | Full | Create/Edit/Retest | Assign Update | View/Comment | View |
| Reports | Full | Security Reports | Assigned | Own Reports | View |
| Audit Logs | Full | No | No | No | No |

## Vulnerability Workflow

### Normal Workflow
```
New → Triaged → Assigned → In Progress → Fixed 
→ Ready for Retest → Retesting → Verified Fixed → Closed
```

### Failed Retest Workflow
```
Ready for Retest → Retesting → Reopened → Assigned 
→ In Progress → Fixed → Ready for Retest
```

### Alternative Workflows
- **Risk Accepted**: Directly from New/Triaged/Assigned
- **Rejected**: From New/Triaged

## SLA Policy

Recommended response times:
- **Critical**: 24-48 hours
- **High**: 3-7 days
- **Medium**: 15 days
- **Low**: 30 days
- **Informational**: Best effort

## Risk Score Calculation

Asset risk score formula:
```
Critical Open × 10
High Open × 7
Medium Open × 4
Low Open × 2
Informational Open × 1
```

Risk ratings:
- 0-10: Low Risk
- 11-30: Medium Risk
- 31-60: High Risk
- 61+: Critical Risk

## Database Models

### Core Models
- **User**: Custom user model with role-based access
- **Team**: Team management with member assignments
- **Asset**: Tracks software/IT systems and components
- **Vulnerability**: Bug/vulnerability tracking
- **VulnerabilityComment**: Discussion threads
- **VulnerabilityEvidence**: Attached files/evidence
- **VulnerabilityStatusHistory**: Audit trail of status changes
- **RetestResult**: Security team retest outcomes
- **AuditLog**: Comprehensive activity logging

## URL Structure

### Authentication
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/profile/`
- `/accounts/change-password/`

### Management
- `/accounts/users/`
- `/teams/`
- `/assets/`
- `/vulnerabilities/`
- `/reports/`
- `/audit/logs/`

### Dashboard
- `/dashboard/`

## Security Features

- Django's built-in authentication system
- CSRF protection on all forms
- SQL injection prevention (ORM)
- XSS prevention (template auto-escaping)
- Restricted file uploads with type/size validation
- Server-side input validation
- Secure password hashing (PBKDF2)
- Audit logging for compliance
- Session timeout management
- Role-based access control

## Configuration

### Development Settings
- `DEBUG = True`
- SQLite database
- No HTTPS requirement

### Production Settings
- `DEBUG = False`
- PostgreSQL recommended
- `ALLOWED_HOSTS` configuration required
- HTTPS/SSL required
- Gunicorn + Nginx setup
- Secure cookie settings

## File Upload Configuration

**Allowed file types**: jpg, jpeg, png, gif, pdf, txt, doc, docx, xlsx, csv
**Maximum file size**: 5 MB

## Troubleshooting

### Database Issues
```bash
python manage.py flush  # Reset database (dev only)
python manage.py migrate --fake-initial  # Fix migration issues
```

### Static Files
```bash
python manage.py collectstatic
```

### Permission Issues
If facing permission issues:
1. Check user role and permissions
2. Verify login status
3. Check audit logs for error details

## API & Extensions

Currently, AssetGuard uses Django's built-in admin for API access. For REST API support, consider integrating Django REST Framework.

## Admin Panel

Access the Django admin panel at `/admin/` with superuser credentials:
- Full model management
- User administration
- Custom admin configurations
- Bulk operations

## Performance Optimization

- Pagination on all list views (20-50 items per page)
- Database query optimization
- Static file caching
- Template caching ready

## Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker (Optional)
Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

### Using systemd
Create a systemd service file for automated startup and process management.

## Monitoring & Logging

- Django logging configured
- Audit trail for all critical actions
- Error tracking and reporting
- Database query logging (dev mode)

## Support & Documentation

Refer to:
- [Django Official Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- Project specification (docs/specification.md)

## License

This project is proprietary and confidential.

## Version

**AssetGuard v2.0**
- Release Date: 2026
- Status: Production Ready

---

**Last Updated**: 2026-06-29
**Built with**: Django 5.1.6, Bootstrap 5.3.0

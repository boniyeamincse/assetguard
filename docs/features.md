# AssetGuard Features & Modules

AssetGuard is composed of several integrated Django apps that handle everything from user management to vulnerability tracking.

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

## Performance Optimization

- Pagination on all list views (20-50 items per page)
- Database query optimization
- Static file caching
- Template caching ready

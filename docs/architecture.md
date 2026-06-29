# Architecture & Models

## Database Models

AssetGuard utilizes a relational database structure designed around its core entities.

### Core Models
- **User**: Custom user model extending Django's AbstractUser with role-based access.
- **Team**: Team management with member assignments and team types.
- **Asset**: Tracks software/IT systems, components, and their criticality.
- **Vulnerability**: Main bug/vulnerability tracking entity mapping to Assets.
- **VulnerabilityComment**: Discussion threads attached to vulnerabilities.
- **VulnerabilityEvidence**: Attached files, images, or documents as proof.
- **VulnerabilityStatusHistory**: Audit trail of when and who changed a vulnerability's status.
- **RetestResult**: Records of security team retest outcomes (pass/fail).
- **AuditLog**: Comprehensive system-wide activity logging.

## URL Structure

### Authentication & Account
- `/accounts/login/`
- `/accounts/logout/`
- `/accounts/profile/`
- `/accounts/change-password/`

### Dashboard
- `/dashboard/`

### Core Management Modules
- `/accounts/users/`
- `/teams/`
- `/assets/`
- `/vulnerabilities/`
- `/reports/`
- `/audit/logs/`

## API & Extensions
Currently, AssetGuard uses standard Django views and the built-in admin for configuration. If REST API support is required for external integrations, it is recommended to implement Django REST Framework (DRF) endpoints mapping to these core models.

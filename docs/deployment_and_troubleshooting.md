# Deployment & Troubleshooting

## Configuration Guidelines

### Development Settings
- `DEBUG = True`
- SQLite database is used by default.
- No HTTPS requirement.

### Production Settings
- `DEBUG = False`
- **PostgreSQL** is highly recommended over SQLite for production deployments.
- `ALLOWED_HOSTS` configuration required in `.env`.
- HTTPS/SSL should be enforced (`SECURE_SSL_REDIRECT = True`).
- Gunicorn + Nginx is the recommended web server stack.
- Secure cookie settings (`SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE`).

## Deployment Instructions

### Using Gunicorn
For a standard Linux deployment, you can serve the application using Gunicorn:
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

### Using systemd
For automated startup and process management in production, create a systemd service file pointing to your gunicorn execution path.

### Using Docker (Optional)
If containerized deployment is preferred, you will need to create a `Dockerfile` and `docker-compose.yml` to orchestrate the Django app and a PostgreSQL database container.

## File Upload Configuration
AssetGuard restricts evidence uploads for security purposes.
- **Allowed file types**: jpg, jpeg, png, gif, pdf, txt, doc, docx, xlsx, csv
- **Maximum file size**: 5 MB

## Monitoring & Logging
- Django built-in logging is configured for error tracking.
- The `AuditLog` model maintains a strict trail for all critical actions within the platform.
- Database query logging can be enabled in dev mode to trace performance bottlenecks.

## Troubleshooting

### Database Issues
If you encounter database inconsistencies during development:
```bash
# Reset the entire database (Development ONLY)
python manage.py flush  

# Fix migration history issues
python manage.py migrate --fake-initial  
```

### Static Files Not Loading
Ensure you collect static files in production environments:
```bash
python manage.py collectstatic
```

### Permission/Access Issues
If users cannot access certain features:
1. Check the user's assigned role and cross-reference with the [Workflows & Roles guide](workflows.md).
2. Verify their login status and session timeout.
3. Check the Audit Logs within the application (Super Admin only) for explicit permission denial errors.

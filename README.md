# Restosaurus Backend

### Project Structure

- `restosaurus/` - Root app
- `sandbox_api/` - Sandbox app
- `manage.py` - Django manage script
- `requirements.txt` - Python dependencies

### Packages Used

- [x] djangorestframework (APIs)
- [x] django-cors-headers (CORS)
- [x] django-environ (environment variables)
- [x] psycopg2 (PostgreSQL connection)
- [x] dj-database-url (PostgreSQL connection)

### API Endpoints

| Endpoint | Group | Role | Method | Purpose |
| --- | --- | --- | --- | --- |
| `/` | Entrypoint | No role required | GET | Display a welcome message |
| `/` | Entrypoint | No role required | POST | Echo the request body |

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

| Endpoint | App | Protected | Role | Method | Purpose |
| --- | --- | --- | --- | --- | --- |
| `/` | Entrypoint | ❌ | None | GET | Display a welcome message |
| `/` | Entrypoint | ❌ | None | POST | Echo the request body |
| --- | --- | --- | --- | --- | --- |
| `api/auth/login/` | ❌ | Auth | None | POST | Login a user |
| `api/auth/register/` | ❌ | Auth | None | POST | Register a new user |
| `api/auth/users/` | ✅ | Auth | Admin | GET | List all users |
| `api/auth/token-refresh/` | ✅ | Auth | None | POST | Refresh a token |
| `api/auth/token-blacklist/` | ✅ | Auth | None | POST | Blacklist a token |
| `api/auth/groups/` | ✅ | Auth | Admin | POST | Add a user to a group |
| `api/auth/groups/<int:pk>/` | ✅ | Auth | Admin | DELETE | Remove a user from a group |
| --- | --- | --- | --- | --- | --- |
| `api/menu/items/` | ✅ | Menu | None | GET | List all menu items |
| `api/menu/items/` | ✅ | Menu | None | POST | Create a new menu item |
| `api/menu/items/<int:pk>/` | ✅ | Menu | None | GET | Retrieve a menu item |
| `api/menu/items/<int:pk>/` | ✅ | Menu | None | PUT | Update a menu item |
| `api/menu/items/<int:pk>/` | ✅ | Menu | None | DELETE | Delete a menu item |
| `api/menu/categories/` | ✅ | Menu | None | GET | List all menu categories |
| `api/menu/categories/` | ✅ | Menu | None | POST | Create a new menu category |
| `api/menu/categories/<int:pk>/` | ✅ | Menu | None | GET | Retrieve a menu category |
| `api/menu/categories/<int:pk>/` | ✅ | Menu | None | PUT | Update a menu category |
| `api/menu/categories/<int:pk>/` | ✅ | Menu | None | DELETE | Delete a menu category |

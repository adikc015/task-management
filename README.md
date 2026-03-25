# Task Management API with Frontend

A Flask-based task management system with:

- JWT authentication
- Role-based authorization (`admin`, `manager`, and other roles)
- Task, user, department, and project management APIs
- Swagger/OpenAPI documentation
- A built-in frontend dashboard (`/`) for testing and daily operations

## Tech Stack

- Python 3.10+
- Flask
- Flask-Smorest (OpenAPI + request/response validation)
- Flask-JWT-Extended
- SQLAlchemy
- MySQL + PyMySQL

## Project Structure

```text
task-management/
	app/
		app.py                    # Flask app entrypoint
		config.py                 # Environment-based settings
		authentication/
			permissions.py          # role_required decorator
		database/
			engine.py               # DB engine/session setup + DB auto-create
			init_db.py              # create all tables
		models/                   # SQLAlchemy models
		routes/                   # API blueprints
		schemas/                  # Marshmallow schemas
		static/                   # Frontend CSS/JS
		templates/
			index.html              # Frontend dashboard
	requirements.txt
```

## Features

- Login endpoint that returns JWT access tokens
- Role-protected endpoints:
	- `admin` only: users, departments
	- `admin` + `manager`: projects
	- `admin` + `manager`: task creation
- Task assignment to multiple users
- Frontend dashboard for:
	- Login/logout
	- Task CRUD + assignment
	- User creation/listing
	- Department creation/listing
	- Project creation/listing
- Health endpoint: `/api/v1/health`

## Setup

### 1. Clone and enter project

```bash
git clone <your-repo-url>
cd task-management
```

### 2. Create and activate virtual environment

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env` inside `app/` (same directory as `config.py`).

Example:

```env
API_TITLE=Task Management API
API_VERSION=v1
OPENAPI_VERSION=3.0.3
OPENAPI_URL_PREFIX=/
OPENAPI_SWAGGER_UI_PATH=/swagger-ui
OPENAPI_SWAGGER_UI_URL=https://cdn.jsdelivr.net/npm/swagger-ui-dist/

SECRET_KEY=change-this
JWT_SECRET_KEY=change-this-too

FLASK_DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=5000

# MySQL server (no DB name)
DB_SERVER_URI=mysql+pymysql://root:password@localhost:3306
DB_NAME=task_management

# Optional: override full DB URL directly
# DATABASE_URL=mysql+pymysql://root:password@localhost:3306/task_management

DB_ENGINE_ECHO=false
```

## Database Initialization

From the project root:

```powershell
cd app
python database/init_db.py
```

What this does:

- Creates the database if needed (via `database/engine.py`)
- Creates tables for `User`, `Task`, `Department`, and `Project`

## Run the Application

From the project root:

```powershell
python app/app.py
```

Default server URL:

- `http://127.0.0.1:5000`

Important URLs:

- Frontend dashboard: `http://127.0.0.1:5000/`
- Swagger UI: `http://127.0.0.1:5000/swagger-ui`
- Health check: `http://127.0.0.1:5000/api/v1/health`

## Authentication

### Login

- Method: `POST`
- URL: `/api/v1/auth/login`
- Body:

```json
{
	"email": "admin@example.com",
	"password": "password123"
}
```

Response:

```json
{
	"access_token": "<jwt-token>"
}
```

Use this token in protected API calls:

```http
Authorization: Bearer <jwt-token>
```

## API Overview

### Auth

- `POST /api/v1/auth/login`

### Tasks

- `GET /api/v1/tasks/` (JWT required)
- `POST /api/v1/tasks/` (`manager` or `admin`)
- `PUT /api/v1/tasks/<task_id>`
- `DELETE /api/v1/tasks/<task_id>`
- `POST /api/v1/tasks/<task_id>/assign`

### Users (`admin` only)

- `POST /api/v1/users/`
- `GET /api/v1/users/`

### Departments (`admin` only)

- `POST /api/v1/departments/`
- `GET /api/v1/departments/`

### Projects (`admin` or `manager`)

- `POST /api/v1/projects/`
- `GET /api/v1/projects/`

## Minimal Usage Flow

1. Create a department (`POST /departments/` as `admin`)
2. Create users linked to department (`POST /users/`)
3. Create project linked to department (`POST /projects/`)
4. Create task linked to project (`POST /tasks/`)
5. Assign users to task (`POST /tasks/<id>/assign`)

The frontend dashboard at `/` supports this workflow directly after login.

## Notes and Known Limitations

- Seed data is not included; create an initial admin user manually in MySQL.
- `GET /api/v1/projects/` currently returns departments instead of projects due to route logic in `routes/projects.py`.
- `PUT /api/v1/tasks/<task_id>`, `DELETE /api/v1/tasks/<task_id>`, and `POST /api/v1/tasks/<task_id>/assign` are not currently role-protected.
- Passwords are hashed with Werkzeug when users are created through API.

## Troubleshooting

- `ModuleNotFoundError` when running DB init:
	- Run from `app/` directory: `python database/init_db.py`
- Database connection failure:
	- Verify MySQL is running
	- Verify `.env` `DB_SERVER_URI` / `DATABASE_URL`
- Unauthorized/Forbidden responses:
	- Ensure JWT is sent in `Authorization` header
	- Ensure logged-in user has required role

## Future Improvements

- Add migration tooling (Alembic)
- Add seed script for admin user and sample data
- Add tests for route authorization and schema validation
- Fix `GET /projects` query return type
- Add pagination and filtering for list endpoints

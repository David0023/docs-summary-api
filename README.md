# docs-summary-api

Asynchronous REST API that summarizes uploaded documents using OpenAI's GPT-4o model. Built with FastAPI and PostgreSQL.

## Features

- **User authentication** — Register and login with JWT-based auth (OAuth2 Password Bearer)
- **Job management** — Create, list, view, and delete summarization jobs
- **Document upload** — Attach PDF, TXT, DOC, or DOCX files to jobs (validated via magic bytes)
- **Background summarization** — Trigger async summarization via OpenAI; poll for results
- **File cleanup** — Uploaded files are removed from both local storage and OpenAI after processing

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Auth | JWT (PyJWT) + Argon2 password hashing |
| AI | OpenAI GPT-4o (Chat Completions + Files API) |
| Server | Uvicorn |
| Containerization | Docker + Docker Compose |

## Project Structure

```
backend/
├── main.py              # App entry point, table creation
├── alembic/             # Alembic migrations with versions
├── api/
│   ├── auth.py          # /auth/register, /auth/login
│   └── v1/
│       ├── routers.py   # Aggregates v1 routers
│       ├── jobs.py      # Job CRUD + /run endpoint
│       └── documents.py # Document upload/attach
├── core/
│   ├── config.py        # Settings (pydantic-settings)
│   ├── database.py      # SQLAlchemy engine + session
│   ├── dependencies.py  # get_db(), get_current_user()
│   ├── security.py      # JWT + password hashing
│   └── enums.py         # JobStatus enum
├── models/              # SQLAlchemy ORM models
├── schemas/             # Pydantic request/response schemas
├── services/
│   └── job_process.py   # OpenAI summarization logic
└── utils/
    ├── file.py          # File save/delete helpers
    └── validator.py     # Email validation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd docs-summary-api
```

2. Create a `.env` file with your OpenAI key:

```bash
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY
```

3. Start the services:

```bash
docker compose up --build
```

4. (Optional) Alembic migrations
```bash
docker exec -ti <docker-container-name> alembic revision --autogenerate -m "Initial database"
```

The API will be available at `http://localhost:8000`. Interactive docs (Swagger UI) are at `http://localhost:8000/docs`.

### Running Locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set the required environment variables:

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/postgres_db"
export SECRET_KEY="your-secret-key"
export OPENAI_API_KEY="sk-..."
```

Run the server:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | — | PostgreSQL connection string |
| `SECRET_KEY` | Yes | — | JWT signing secret |
| `OPENAI_API_KEY` | Yes | — | OpenAI API key |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Token expiry in minutes |
| `MAX_FILE_SIZE` | No | `10485760` | Max upload size in bytes (default 10 MB) |

## API Endpoints

### Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login, returns JWT token |

### Jobs (requires Bearer token)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/jobs` | Create a summarization job |
| GET | `/api/v1/jobs` | List all jobs for current user |
| GET | `/api/v1/jobs/{job_id}` | Get job details, status, and result |
| DELETE | `/api/v1/jobs/{job_id}` | Delete a job and its files |
| POST | `/api/v1/jobs/{job_id}/run` | Trigger background summarization |

### Documents (requires Bearer token)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/documents/attach/{job_id}` | Upload and attach a document to a job |

## Usage

1. **Register** a user via `POST /auth/register`
2. **Login** via `POST /auth/login` to get a JWT token
3. **Create a job** via `POST /api/v1/jobs` with a title and description
4. **Upload documents** via `POST /api/v1/documents/attach/{job_id}`
5. **Run the job** via `POST /api/v1/jobs/{job_id}/run`
6. **Poll for results** via `GET /api/v1/jobs/{job_id}` until status is `completed`

## Supported File Types

- PDF (`application/pdf`)
- Plain text (`text/plain`)
- Word documents (`application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`)

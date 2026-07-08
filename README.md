# Portfolio & Alert Management API

## Project Overview

A backend service for a stock market application, built with FastAPI and PostgreSQL. It allows users to register and log in securely, manage a stock portfolio, set price alerts, and maintain a watchlist — all behind JWT-protected endpoints.

## Features Implemented

- **Authentication** — register, login, refresh, and logout using JWT access tokens + refresh tokens
- **Portfolio Management** — add, view, update, and delete stock holdings
- **Alerts** — create price alerts (above/below a target price) for a symbol, view and delete them
- **Watchlist** — add, view, and remove tracked stock symbols
- **Rate limiting** on register/login (5 requests per minute per IP)
- **Interactive API docs** via Swagger UI (`/docs`)
- **Unit tests** covering authentication and portfolio flows

## Technologies Used

- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy (async)** — ORM
- **Alembic** — database migrations
- **python-jose** — JWT encoding/decoding
- **bcrypt / passlib** — password hashing
- **slowapi** — rate limiting
- **pytest / pytest-asyncio / httpx** — testing
- **Docker & Docker Compose** — containerization

## Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```
### 2. Set up environment variables

Copy the example env file and fill in your own values:

```bash
cp .env.example .env
```

See the [Environment Variables](#environment-variables) section below for what each value means.

### 3. Run with Docker

```bash
docker compose up -d --build
```

The API will be available at `http://localhost:8000`.

### 4. Explore the API

Open `http://localhost:8000/docs` for interactive Swagger documentation. Register a user, log in to get an access token, then click **Authorize** and paste the token to call protected endpoints.

### 5. Running tests

Tests run against a separate test database. Create it first:

```bash
docker compose exec db psql -U <your_user> -d <your_db> -c "CREATE DATABASE <your_test_db>;"
```

Then run:

```bash
pytest -v
```

## Environment Variables

| Variable | Description |
|---|---|
| `POSTGRES_USER` | Database username |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_DB` | Database name |
| `DATABASE_URL` | Full async connection string used by the app |
| `JWT_SECRET_KEY` | Secret key used to sign JWT tokens |
| `JWT_EXPIRE_MINUTES` | Access token expiry time, in minutes |
| `TEST_DATABASE_URL` | Connection string for the test database |

A template with placeholder values is provided in `.env.example`.

## Assumptions & Limitations

- Prices (`averagePrice`, `targetPrice`) are stored as floats rather than fixed-point decimals — acceptable for this scope, but not ideal for real financial precision.
- Alerts are stored but not actively evaluated against live prices — there's no background job checking whether an alert's condition has been met.
- Refresh tokens are not rotated on use; the same refresh token remains valid until it expires or is explicitly logged out.
- CORS is currently open to all origins (\`allow_origins=["*"]\`) for ease of local development, not intended for production as-is.
- Rate limiting is in-memory (per process), so it won't be consistent across multiple backend instances without a shared store like Redis.
- Route prefixes use `/auth/...` rather than root-level `/register`, `/login`, etc.

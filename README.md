# Portfolio & Alert Management API

A backend service for a stock market application. Built with FastAPI, PostgreSQL, and JWT authentication.

## Features

- **Authentication** — register, login, refresh, and logout using JWT access tokens + refresh tokens
- **Portfolio Management** — add, view, update, and delete stock holdings
- **Alerts** — set price alerts (above/below a target price) for a symbol
- **Watchlist** — track stock symbols of interest
- **Rate limiting** on register/login (5 requests per minute)

## Tech Stack

- FastAPI
- PostgreSQL + SQLAlchemy (async)
- Alembic for migrations
- JWT (python-jose) + bcrypt for password hashing
- pytest for testing
- Docker & Docker Compose

## Getting Started

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

Required variables:

| Variable | Description |
|---|---|
| `POSTGRES_USER` | Database username |
| `POSTGRES_PASSWORD` | Database password |
| `POSTGRES_DB` | Database name |
| `DATABASE_URL` | Full async connection string for the app |
| `JWT_SECRET_KEY` | Secret used to sign JWT tokens |
| `JWT_EXPIRE_MINUTES` | Access token expiry time |
| `TEST_DATABASE_URL` | Connection string for the test database |

### 3. Run with Docker

```bash
docker compose up -d --build
```

The API will be available at `http://localhost:8000`.

### 4. Explore the API

Open `http://localhost:8000/docs` for interactive Swagger documentation.

## Running Tests

Tests run against a separate test database (`TEST_DATABASE_URL` in `.env`).

Create the test database first:

```bash
docker compose exec db psql -U <your_user> -d <your_db> -c "CREATE DATABASE <your_test_db>;"
```

Then run:

```bash
pytest -v
```

## API Overview

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create a new user |
| POST | `/auth/login` | Log in and receive tokens |
| POST | `/auth/refresh` | Get a new access token |
| POST | `/auth/logout` | Revoke a refresh token |

### Portfolio
| Method | Endpoint | Description |
|---|---|---|
| GET | `/portfolio/` | List all holdings |
| POST | `/portfolio/` | Add a holding |
| PUT | `/portfolio/{id}` | Update a holding |
| DELETE | `/portfolio/{id}` | Remove a holding |

### Alerts
| Method | Endpoint | Description |
|---|---|---|
| GET | `/alerts/` | List all alerts |
| POST | `/alerts/` | Create an alert |
| DELETE | `/alerts/{id}` | Remove an alert |

### Watchlist
| Method | Endpoint | Description |
|---|---|---|
| GET | `/watchlist/` | List watchlist items |
| POST | `/watchlist/` | Add a symbol |
| DELETE | `/watchlist/{id}` | Remove a symbol |

All portfolio, alert, and watchlist endpoints require a valid JWT access token in the `Authorization: Bearer <token>` header.

## Project Structure

```
.
├── auth.py           # Authentication routes
├── portfolio.py       # Portfolio routes
├── alerts.py           # Alert routes
├── watchlist.py         # Watchlist routes
├── models.py            # SQLAlchemy models
├── schemas.py            # Pydantic request/response schemas
├── security.py            # JWT + password hashing
├── database.py              # DB engine/session setup
├── config.py                 # Environment-based settings
├── limiter.py                  # Rate limiting setup
├── main.py                      # FastAPI app entry point
├── alembic/                      # Database migrations
├── test_auth.py                   # Auth tests
├── test_portfolio.py                # Portfolio tests
└── conftest.py                       # Test fixtures
```

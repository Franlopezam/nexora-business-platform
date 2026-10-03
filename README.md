# Nexora

Nexora is a small business management platform built with FastAPI, SQLite and vanilla JavaScript.

## Features

- JWT authentication
- Role-based access control
- Users, customers and products
- Inventory movements
- Sales and automatic stock updates
- Dashboard statistics
- Audit log
- CSV export
- Centralized API errors
- Password hashing
- Basic rate limiting middleware
- Unit/API tests
- Docker and Docker Compose
- SQLite for local development, PostgreSQL-ready configuration
- Automatic database table creation and seed data

## Quick start

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and change the secret key.

### 4. Seed the demo database

```bash
python scripts/seed_database.py
```

### 5. Run the server

```bash
uvicorn app.main:app --app-dir backend --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

### Demo account

- Email: admin@nexora.local
- Password: Admin123!

Change the password before using Nexora outside a local demo.

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest backend/tests -q
```

## Project structure

```text
nexora/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── security/
│   │   ├── services/
│   │   ├── middleware/
│   │   ├── utils/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
├── scripts/
├── docs/
└── .github/workflows/
```

## License

MIT

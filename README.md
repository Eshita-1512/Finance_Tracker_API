# 💰 Finance Tracker API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render)](https://render.com/)

A high-performance backend finance tracking system built with **FastAPI** and **PostgreSQL**. This API allows users to manage transactions, track expenses, and view detailed financial analytics with role-based access control.

---

## 🚀 Features

- **🔐 Secure Authentication**: JWT-based auth with `passlib` (bcrypt) for password hashing.
- **👥 Role-Based Access Control (RBAC)**:
  - `Viewer`: Read-only access to transactions and basic summaries.
  - `Analyst`: View detailed monthly/category analytics and filter transactions.
  - `Admin`: Full CRUD capabilities for transactions and user management.
- **📊 Advanced Analytics**:
  - Real-time balance calculation (Income - Expense).
  - Monthly breakdown of financial activity.
  - Category-wise spending analysis with percentage distribution.
- **🔍 Powerful Filtering**: Filter transactions by type, category, date range, and amount.
- **📄 Pagination**: Efficient data retrieval for large transaction histories.
- **🛠️ Tech Stack**: FastAPI, SQLAlchemy (ORM), Alembic (Migrations), Pydantic v2, Docker & Render.

---

## 🛠️ Installation & Local Setup

### Using Docker (Recommended)
The quickest way to get started is using Docker Compose:

```bash
git clone https://github.com/Eshita-1512/Finance_Tracker_API.git
cd Finance_Tracker_API
docker compose up --build
```

### Manual Setup
1. **Clone the repo**: `git clone <repo_url>`
2. **Create a virtual environment**: `python -m venv venv`
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Set up environment variables**: Create a `.env` file based on `.env.example`.
5. **Run migrations**: `alembic upgrade head`
6. **Start the server**: `uvicorn app.main:app --reload`

---

## 🌐 Deployment (Render)

This project is configured for seamless deployment on **Render** using the provided `render.yaml` and `Dockerfile`.

1. **Connect your GitHub repository** to Render.
2. Render will automatically detect the `render.yaml` file and set up:
   - A **Web Service** for the FastAPI application.
   - A **Managed PostgreSQL** instance.
3. Ensure the `DATABASE_URL` environment variable is correctly linked (handled automatically by `render.yaml`).

---

## 📖 API Documentation

Once the server is running, access the interactive documentation at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Default Test Users

The database is seeded with the following accounts for testing:

| Role    | Email            | Password    |
|---------|------------------|-------------|
| Admin   | `admin@test.com`   | `admin123`    |
| Analyst | `analyst@test.com` | `analyst123`  |
| Viewer  | `viewer@test.com`  | `viewer123`   |

> [!TIP]
> Use the `/auth/login` endpoint to get a JWT token, then use it in the **Authorize** header in Swagger UI.

---

## 📁 Project Structure

```text
.
├── app/
│   ├── routers/       # API Route handlers (auth, admin, transactions, summary)
│   ├── auth.py        # JWT & Security logic
│   ├── database.py    # DB Connection & Session management
│   ├── models.py      # SQLAlchemy Models
│   ├── schemas.py     # Pydantic Schemas
│   └── main.py        # FastAPI Application Entrypoint
├── migrations/        # Alembic database migrations
├── tests/             # Pytest suite
├── Dockerfile         # Container configuration
├── render.yaml        # Render Blueprint configuration
└── requirements.txt   # Python dependencies
```


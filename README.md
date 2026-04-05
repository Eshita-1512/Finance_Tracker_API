# Finance Tracker API

A backend finance tracking system built with FastAPI and PostgreSQL.
Built as part of a backend engineering assignment.

## Tech Stack
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy + Alembic
- JWT authentication (python-jose + passlib)
- pytest for testing
- Docker + docker-compose

## Running the project (quickest way)

```bash
git clone <repo>
cd finance-tracker
docker compose up --build
```

The API will be at http://localhost:8000
Interactive docs at http://localhost:8000/docs

## Test users (created by seed data on startup)

| Role     | Email              | Password    |
|----------|--------------------|-------------|
| admin    | admin@test.com     | admin123    |
| analyst  | analyst@test.com   | analyst123  |
| viewer   | viewer@test.com    | viewer123   |

1. Hit POST /auth/login with any of the above
2. Copy the token from the response
3. Click Authorize in /docs, paste the token
4. All protected endpoints now work

## Roles and permissions

- Viewer: read transactions, basic summary
- Analyst: everything viewer can + filters + monthly/category analytics
- Admin: full CRUD + manage users

## Assumptions I made

- Transactions belong to a user (user_id is set from JWT, not request body)
- "Current balance" means total income minus total expenses across all time
- Roles are assigned at registration (viewer by default), changed by admin
- Amount uses Numeric(12,2) to avoid floating point precision issues with money

## What I'd add with more time

- Pagination cursor-based instead of offset (better for large datasets)
- Soft delete for transactions instead of hard delete
- Transaction categories as a separate table with predefined options
- Rate limiting on auth endpoints
- CSV export for transactions

# Email Campaign Tracker

Email Campaign Tracker is a small FastAPI application for managing email campaigns. It supports user accounts, campaign creation, contact management, email sending, tracking, and basic campaign statistics.

## Features

- User registration and login with JWT authentication
- Create, list, update, and soft-delete campaigns
- Add and list contacts for each campaign
- Send campaign emails in the background
- Track email opens and clicks with tracking tokens
- View campaign stats such as total contacts, sent emails, opens, clicks, and rates

## Tech Stack

- FastAPI
- SQLAlchemy async ORM
- Pydantic
- JWT authentication with python-jose and passlib
- FastAPI Mail
- SQLite for local/test use, with support for a DATABASE_URL-based setup

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Copy the example environment file and update the values:

   ```bash
   copy .env.example .env
   ```
4. Start the server:

   ```bash
   uvicorn app.main:app --reload
   ```

The API docs are available at:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Main Endpoints

- POST /auth/register
- POST /auth/login
- POST /campaigns/
- GET /campaigns/
- GET /campaigns/{campaign_id}
- PATCH /campaigns/{campaign_id}
- DELETE /campaigns/{campaign_id}
- POST /campaigns/{campaign_id}/contacts/
- GET /campaigns/{campaign_id}/contacts/
- POST /campaigns/{campaign_id}/send
- GET /track/open
- GET /track/click
- GET /campaigns/{campaign_id}/stats
- GET /health

## Testing

Run tests with:

```bash
pytest -v
```

The test setup uses an in-memory SQLite database by default.

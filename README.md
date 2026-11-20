# Rangmanch Reviews API

A simple FastAPI application for storing and retrieving theatre play reviews using SQLite and SQLModel.

## Features

- Create, read, update, and delete reviews
- Filter reviews by play name
- Paginate review results
- Calculate the average rating and review count for a play
- Interactive API documentation with Swagger UI

## Requirements

- Python 3.10 or newer

## Local Setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open <http://127.0.0.1:8000> for the welcome endpoint.

Open <http://127.0.0.1:8000/docs> for Swagger UI.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/reviews/` | Create a review |
| `GET` | `/reviews/` | List reviews; supports `play_name`, `skip`, and `limit` |
| `GET` | `/reviews/{review_id}` | Get a review by ID |
| `PATCH` | `/reviews/{review_id}` | Update one or more review fields |
| `DELETE` | `/reviews/{review_id}` | Delete a review |
| `GET` | `/reviews/average-rating/{play_name}` | Get average rating and review count |

## Example Request

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/reviews/" -ContentType "application/json" -Body '{
  "play_name": "Hamlet",
  "reviewer_name": "Asha",
  "rating": 5,
  "comment": "Excellent performance."
}'
```

The SQLite database is stored as `rangmanch.db` and is created automatically at startup.

## GitHub Upload

Before uploading, ensure `.gitignore` is included and do not commit `venv/`, `__pycache__/`, `.env`, or local database files unless database versioning is intentional.

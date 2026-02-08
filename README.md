# Deep Work Session Tracker

Track focused work sessions, log interruptions, and analyze your productivity patterns.

## Quick Start

```bash
# Clone and setup
./setup.sh          # Linux/Mac
setupdev.bat        # Windows

# Run the app
./run.sh            # Linux/Mac
runapplication.bat  # Windows
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite, Alembic
- **Frontend**: React 18, Vite
- **Testing**: pytest

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/sessions/` | Create a new session |
| PATCH | `/sessions/{id}/start` | Start a scheduled session |
| PATCH | `/sessions/{id}/pause` | Pause (requires reason) |
| PATCH | `/sessions/{id}/resume` | Resume from pause |
| PATCH | `/sessions/{id}/complete` | Complete session |
| GET | `/sessions/history` | List all sessions |
| GET | `/sessions/{id}` | Get session details |

## Session State Machine

```
scheduled ──start──> active ──pause──> paused
                       │                  │
                       │              resume
                       │                  │
                       └──complete───>────┴──> [final status]
```

## Final Status Logic

Sessions are automatically classified on completion:

| Condition | Status |
|-----------|--------|
| 4+ pauses during session | `interrupted` |
| Paused but never resumed | `abandoned` |
| Actual time > scheduled + 10% | `overdue` |
| Otherwise | `completed` |

## Development

```bash
# Backend tests
cd backend
source env/bin/activate  # or env\Scripts\activate on Windows
pytest test_sessions.py -v

# Generate Python SDK
npx @openapitools/openapi-generator-cli generate \
  -i http://localhost:8000/openapi.json \
  -g python \
  -o deepwork_sdk
```

## Project Structure

```
├── backend/
│   ├── main.py           # FastAPI routes
│   ├── models.py         # SQLAlchemy ORM
│   ├── schemas.py        # Pydantic models
│   ├── crud.py           # DB operations + status logic
│   ├── database.py       # Engine config
│   ├── alembic/          # Migrations
│   └── test_sessions.py  # Tests
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       └── components/
├── sample_usage.py       # SDK demo
└── setup.sh / run.sh     # Scripts
```

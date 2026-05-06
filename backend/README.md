# Nexus Vault — Backend

FastAPI backend for the Nexus Vault local content saving system.

## Structure
```
backend/
└── app/
    ├── main.py         # Entry point — FastAPI app, middleware, error handlers
    ├── config.py       # All config via .env (Pydantic Settings)
    ├── database.py     # SQLAlchemy engine + session dependency
    ├── models/
    │   └── item.py     # Item database table definition
    ├── schemas/
    │   └── item.py     # Pydantic request/response validation
    ├── routes/
    │   └── items.py    # HTTP endpoints for /api/items
    └── services/
        └── item_service.py  # Business logic (CRUD operations)
```

## Setup

### 1. Activate virtual environment (from project root)
```bash
# Windows
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
# Copy the template
copy .env.example .env
# Edit .env with your PostgreSQL credentials
```

### 4. Run the server (from /backend folder)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info + health |
| GET | `/health` | Health check |
| POST | `/api/items/` | Create new item |
| GET | `/api/items/` | List all items (filterable) |
| GET | `/api/items/{id}` | Get item by UUID |
| PATCH | `/api/items/{id}` | Update item (partial) |
| DELETE | `/api/items/{id}` | Delete item |

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Response Format
All responses follow:
```json
{ "success": true, "data": {...}, "error": null }
```

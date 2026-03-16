# Backend (FastAPI) — AI Packaging Optimizer

## Setup (Windows PowerShell)

From `d:\AI PACKAGING\backend`:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\pip install -r requirements.txt
```

## Run

```bash
.venv\Scripts\python -m uvicorn app.main:app --reload
```

Then open:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/db/health` (after PostgreSQL setup)

## API

### `POST /optimize`

Example request body:

```json
{
  "items": [
    { "sku": "A", "qty": 2, "length": 10, "width": 10, "height": 2, "weight": 0.2 },
    { "sku": "B", "qty": 1, "length": 20, "width": 10, "height": 5, "weight": 0.5 }
  ],
  "box_types": [
    { "code": "S", "inner_length": 20, "inner_width": 15, "inner_height": 6, "max_weight": 0 },
    { "code": "M", "inner_length": 30, "inner_width": 20, "inner_height": 10, "max_weight": 0 }
  ]
}
```

Returns a list of chosen boxes and which items were assigned to each box (v1 uses a simple heuristic).

## PostgreSQL

### 1) Create `.env`

Copy `/.env.example` to `/.env` and edit it:

```bash
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/ai_packaging
```

### 2) Create database

Create a database named `ai_packaging` (using pgAdmin or psql).

### 3) What gets stored

Each `POST /optimize` call is saved into PostgreSQL table `optimization_runs` with:
- `request_json`
- `response_json`

### 4) List recent runs

Open `GET /runs` in Swagger or your browser to see the latest 50 runs.


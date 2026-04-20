# Procurement Agent API (FastAPI)

Production-oriented procurement drift detection service built with FastAPI.

## Architecture

The backend now follows a modular structure:

- `src/api/`: FastAPI app, routers, and route handlers
- `src/services/`: business logic (detection, simulation, ingestion, task orchestration)
- `src/models/`: Pydantic API contracts and task store primitives
- `src/utils/`: settings, database engine, logging, serialization helpers

Legacy paths (`src/api/fastapi_app.py`, `src/agents/*`) are kept as compatibility wrappers.

## Quickstart

1. Create a virtual environment and install dependencies:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment variables:

```bash
cp .env.example .env
```

3. Generate and ingest demo data:

```bash
python data_generator.py
python -c "from src.agents.ingestor import run; run()"
```

4. Start the API:

```bash
uvicorn src.api.main:app --reload --port 8000
```

5. (Optional) Start the frontend:

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

- `GET /api/health`: health/version check
- `GET /api/leaks`: current drift detections
- `POST /api/run-detection`: start async detection task
- `GET /api/run-detection/{task_id}`: poll task status
- `POST /api/simulate-traffic`: append synthetic traffic for demos

## Docker

```bash
docker build -t procurement-agent .
docker run -p 8000:8000 procurement-agent
```

The API is exposed at `http://localhost:8000`.

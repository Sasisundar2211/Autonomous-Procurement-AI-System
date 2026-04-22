# AI Procurement Decision Engine

## Problem
Companies struggle to choose the best vendor due to multiple factors.

## Solution
This system ranks vendors using structured supplier data and generates a short AI explanation for the top recommendation.

## Features
- Vendor ranking
- AI explanation
- CSV input
- Live demo (FastAPI + Streamlit)

## Demo
[Add deployed link]

## Tech
- FastAPI
- Streamlit
- OpenAI
- Pandas

## Project Structure
```text
procurement-ai/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── scoring.py
│   │   └── llm.py
│   ├── models/
│   │   └── schema.py
│   └── utils/
│       └── preprocess.py
├── data/
│   └── sample_vendors.csv
├── streamlit_app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start FastAPI backend
```bash
uvicorn app.main:app --reload
```

### 3. Start Streamlit frontend
```bash
streamlit run streamlit_app.py
```

## Deployment

### Option A: Render (Backend)
Start command:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

### Option B: Streamlit Cloud (Frontend)
- Upload repo
- Select `streamlit_app.py`
- Set backend URL to your Render service URL in the app UI

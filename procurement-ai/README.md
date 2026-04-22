# AI Procurement Intelligence System

## Problem
Companies lose money when vendor selection ignores risk signals like delayed delivery, poor quality, and unstable supplier behavior.

## Solution
This system combines multi-factor vendor scoring, ML-based risk prediction, multi-agent orchestration, and LLM-driven decision narratives to support procurement teams with actionable recommendations.

## New Features
- Risk prediction model (`RandomForestRegressor`) for vendor `risk_score` (0-1)
- Multi-agent pipeline orchestration:
  - Data Agent: input validation and preprocessing
  - Risk Agent: risk model training and prediction
  - Decision Agent: weighted scoring and ranking
  - LLM Agent: business explanation
  - Negotiation Agent: negotiation strategy suggestion
- Negotiation intelligence:
  - Discount recommendation for expensive vendors
  - Delay clause recommendation for slow delivery
  - Performance guarantees for high-risk vendors
- External signals:
  - Currency rate signal (`USD/INR`)
  - Supplier location risk lookup
  - Market pressure signal (lightweight mock)
- Stateful memory:
  - Stores previous decisions in process memory
- Interactive dashboard:
  - Vendor comparison table
  - Risk vs price chart
  - Decision summary with pipeline steps

## Architecture
User Upload CSV -> Data Agent -> Risk Agent -> Decision Agent -> LLM Agent -> Negotiation Agent -> UI Output

## Project Structure
```text
procurement-ai/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── scoring.py
│   │   ├── risk_model.py
│   │   ├── llm.py
│   │   ├── negotiation.py
│   │   ├── external_signals.py
│   │   ├── memory.py
│   │   └── agent_controller.py
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

## Example Output
- Ranked vendors with final score and risk score
- Selected top vendor with explanation
- Negotiation advice (e.g., discount request, delay penalty)
- External signals (currency and location risk)

## Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start backend
```bash
uvicorn app.main:app --reload
```

### 3. Start dashboard
```bash
streamlit run streamlit_app.py
```

## Deployment

### Render (Backend)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 10000
```

### Streamlit Cloud (Frontend)
- Deploy `streamlit_app.py`
- Set backend URL to Render endpoint

## Docker
```bash
docker build -t procurement-intelligence .
docker run -p 10000:10000 procurement-intelligence
```

## Environment Variables
- `OPENAI_API_KEY` for explanation generation
- `OPENAI_MODEL` optional model override (default: `gpt-4o-mini`)
- `LOG_LEVEL` backend log level

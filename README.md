# Trade Opportunities API

A FastAPI service that analyzes market data and provides trade opportunity insights for specific sectors in India. The API accepts a sector name, searches for current market data, analyzes it using an LLM, and returns a structured markdown report.


## Tech Stack

- **Framework**: FastAPI
- **LLM**: Groq API (LLaMA 3.3 70B) — used instead of Gemini due to free tier quota limits
- **Web Search**: DuckDuckGo (ddgs) for real-time market data
- **Authentication**: JWT Bearer Token
- **Rate Limiting**: SlowAPI (5 requests/minute per IP)
- **Storage**: In-memory only (no database)


## Project Structure
```
trade_opportunities_api/
├── app/
│   ├── __init__.py        # Package init
│   ├── main.py            # FastAPI app, endpoints, error handlers
│   ├── auth.py            # JWT token creation and verification
│   ├── search.py          # DuckDuckGo web search + fallback
│   ├── analyzer.py        # Groq LLM analysis and report generation
│   └── config.py          # Environment variables and settings
├── outputs/               # Sample generated reports and screenshots
├── .env                   # API keys (not included in repo)
├── .gitignore
├── requirements.txt
└── README.md
```


## Setup Instructions

### Step 1: Clone the repository
```bash
git clone https://github.com/SaiBhavyaYangoti/trade-opportunities-api.git
cd trade-opportunities-api
```

### Step 2: Make sure Python is installed
```bash
python --version
```
Requires Python 3.10 or above.

### Step 3: Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 4: Install all dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create a `.env` file in the root folder
Create a file named `.env` and add the following:
```
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=any_long_random_string_here
```

- Get a **free** Groq API key at: https://console.groq.com
- `SECRET_KEY` can be any random string (e.g. `tradesecret$india2024xK9`)

### Step 6: Run the server
```bash
uvicorn app.main:app --reload
```

Server will start at: **http://127.0.0.1:8000**


## API Endpoints

### 1. `POST /token` — Get access token

Generate a JWT token using any client ID (minimum 3 characters).
```bash
curl -X POST "http://127.0.0.1:8000/token?client_id=yourname"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```


### 2. `GET /analyze/{sector}` — Get trade opportunity report ⭐ Main Endpoint

Returns a structured markdown report with current trade opportunities for the given sector in India.
```bash
curl -X GET "http://127.0.0.1:8000/analyze/pharmaceuticals" \
  -H "Authorization: Bearer your_token_here"
```

**Supported sectors:**
`pharmaceuticals`, `technology`, `agriculture`, `automobile`, `textiles`, `chemicals`, `electronics`, `energy`, `finance`, `retail`

**Response format (markdown report):**
```
# Trade Opportunity Report: Pharmaceuticals Sector (India)

## Executive Summary
## Current Market Overview
## Export Opportunities
## Import Opportunities
## Key Challenges
## Recommendations
## Data Sources
```

**Error responses:**
- `400` — Invalid sector name
- `401` — Missing or invalid token
- `429` — Rate limit exceeded (5 requests/minute)
- `500` — Internal server error


### 3. `GET /session` — Get session usage info

Returns request count and session start time for the current user.
```bash
curl -X GET "http://127.0.0.1:8000/session" \
  -H "Authorization: Bearer your_token_here"
```

Response:
```json
{
  "client_id": "yourname",
  "requests_made": 3,
  "session_started": "2026-03-04T18:00:00"
}
```


### 4. `GET /health` — Health check
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

Response:
```json
{
  "status": "ok",
  "message": "Trade Opportunities API is running"
}
```


## Interactive API Documentation

Visit **http://127.0.0.1:8000/docs** for full Swagger UI where you can test all endpoints interactively.


## Security Features

- **JWT Authentication** — Every request to `/analyze` requires a valid Bearer token
- **Rate Limiting** — Maximum 5 requests per minute per IP address
- **Input Validation** — Sector names are validated against an allowed list
- **Session Tracking** — Each user session tracks request count and start time
- **Error Handling** — All errors return clean, structured responses
- **Environment Variables** — API keys stored in `.env`, never hardcoded


## Core Workflow

1. Client requests a token via `POST /token`
2. Client calls `GET /analyze/{sector}` with Bearer token
3. API validates token and sector name
4. DuckDuckGo search fetches real-time market data for the sector
5. Groq LLM (LLaMA 3.3 70B) analyzes the data and generates a report
6. Structured markdown report is returned directly


## Quick Test Guide (Step by Step)

### Using Swagger UI at http://127.0.0.1:8000/docs

**Step 1: Get your token**
- Click on `POST /token`
- Click **"Try it out"**
- Enter any name in `client_id` field (minimum 3 characters, e.g. `testuser`)
- Click **"Execute"**
- Copy the `access_token` value from the response

**Step 2: Authorize**
- Click the **"Authorize"** button at the top right of the page
- Paste your copied token in the **Value** field
- Click **"Authorize"** then **"Close"**

**Step 3: Get your market report**
- Click on `GET /analyze/{sector}`
- Click **"Try it out"**
- Enter a sector name (e.g. `technology`, `agriculture`, `pharmaceuticals`)
- Click **"Execute"**
- Scroll down to see your markdown report in the response!


## Notes

- Groq API (LLaMA 3.3 70B) was used as the LLM instead of Gemini due to free tier daily quota exhaustion during development. The assignment allows any model of choice.
- All data is stored in-memory — no database setup required
- The `.env` file is excluded from version control via `.gitignore`

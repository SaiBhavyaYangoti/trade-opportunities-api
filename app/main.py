import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.auth import verify_token, create_token, track_request
from app.search import fetch_market_data
from app.analyzer import analyze_sector
from app.config import RATE_LIMIT, VALID_SECTORS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyzes market data and provides trade opportunity insights for Indian sectors.",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error. Please try again."}
    )

# Auth endpoint
@app.post("/token", summary="Get access token")
def get_token(client_id: str):
    """
    Pass any client_id string to get a JWT token.
    Use this token as Bearer auth for /analyze/{sector}
    """
    if not client_id or len(client_id) < 3:
        raise HTTPException(status_code=400, detail="client_id must be at least 3 characters")
    token = create_token(client_id)
    return {"access_token": token, "token_type": "bearer"}


# Main endpoint
@app.get("/analyze/{sector}", summary="Get trade opportunity report")
@limiter.limit(RATE_LIMIT)
async def analyze(
    request: Request,
    sector: str,
    client_id: str = Depends(verify_token)
):
    """
    Returns a structured markdown report with trade opportunities
    for the given sector in India.

    **Supported sectors:** pharmaceuticals, technology, agriculture,
    automobile, textiles, chemicals, electronics, energy, finance, retail
    """
    sector = sector.lower().strip()

    if sector not in VALID_SECTORS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sector '{sector}'. Supported: {', '.join(VALID_SECTORS)}"
        )

    track_request(client_id)
    logger.info(f"Analyzing sector: {sector} | client: {client_id}")

    raw_data = fetch_market_data(sector)
    report = analyze_sector(sector, raw_data)

    return PlainTextResponse(content=report, media_type="text/markdown")

# Session info
@app.get("/session", summary="Get current session usage")
def session_info(client_id: str = Depends(verify_token)):
    """Returns current session usage stats for the authenticated user."""
    from app.auth import active_sessions
    session = active_sessions.get(client_id, {})
    return {
        "client_id": client_id,
        "requests_made": session.get("requests", 0),
        "session_started": session.get("created_at", "unknown")
    }

# Health check 
@app.get("/health", summary="Health check")
def health():
    return {"status": "ok", "message": "Trade Opportunities API is running"}
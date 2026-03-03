import logging
from groq import Groq
from app.config import GROQ_API_KEY

logger = logging.getLogger(__name__)

client = Groq(api_key=GROQ_API_KEY)

def analyze_sector(sector: str, raw_data: str) -> str:
    prompt = f"""
You are a trade analyst specializing in Indian markets.
Based on the following market data, write a detailed trade opportunity report for the {sector} sector in India.

MARKET DATA:
{raw_data}

Write the report in the following markdown format:

# Trade Opportunity Report: {sector.title()} Sector (India)

## Executive Summary
(2-3 lines summarizing the current state of the sector)

## Current Market Overview
(Key stats, market size, recent trends)

## Export Opportunities
(Top export opportunities with target markets)

## Import Opportunities
(Key imports, gaps in domestic supply)

## Key Challenges
(Regulatory, logistical, or competitive challenges)

## Recommendations
(3-5 actionable recommendations for traders/investors)

## Data Sources
(Mention the search queries used to gather this data)

---
*Report generated for informational purposes. Always verify with official sources.*
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return f"# Analysis Unavailable\n\nCould not generate report for **{sector}** sector.\n\nError: {str(e)}"
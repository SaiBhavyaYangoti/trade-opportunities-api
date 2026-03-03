import logging
from ddgs import DDGS

logger = logging.getLogger(__name__)


def fetch_market_data(sector: str) -> str:
    queries = [
        f"{sector} sector India trade opportunities 2024",
        f"India {sector} export import market trends",
        f"{sector} industry India growth challenges",
    ]

    all_results = []

    with DDGS() as ddgs:
        for query in queries:
            try:
                results = ddgs.text(query, max_results=4)
                for r in results:
                    snippet = f"- {r['title']}: {r['body']}"
                    all_results.append(snippet)
            except Exception as e:
                logger.warning(f"Search failed for query '{query}': {e}")
                continue

    if not all_results:
        return f"No recent data found for {sector} sector."

    # Join all snippets into one block of text
    combined = f"Market data for {sector.upper()} sector in India:\n\n"
    combined += "\n".join(all_results)
    return combined
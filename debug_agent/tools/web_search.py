from duckduckgo_search import DDGS
from typing import List, Dict


def search_web(query: str, max_results: int = 3) -> List[Dict]:
    """
    Perform web search for debugging help.

    Args:
        query (str): Search query
        max_results (int): Number of results

    Returns:
        List[Dict]: Search results
    """

    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "snippet": r.get("body", "")
                })
    
    except Exception:
        pass # Fail silently (non-critical tool)

    return results
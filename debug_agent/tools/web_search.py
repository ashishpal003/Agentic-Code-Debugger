from duckduckgo_search import DDGS

def search_web(query: str, max_results=3):
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "snippet": r["body"]
            })

    return results
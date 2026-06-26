from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str, num_sources: int = 5) -> dict:
    """
    Searches the web using Tavily and returns results with sources.
    """
    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=num_sources,
        include_answer=True,
    )

    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content"),
            "score": r.get("score")
        })

    return {
        "answer": response.get("answer", ""),
        "results": results
    }
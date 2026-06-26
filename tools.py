from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str) -> dict:
    """
    Searches the web using Tavily and returns results with sources.
    """
    response = client.search(
        query=query,
        search_depth="advanced",  # deeper search
        max_results=5,            # get top 5 sources
        include_answer=True,      # get a quick answer too
    )

    results = []
    for r in response.get("results", []):
        results.append({
            "title": r.get("title"),
            "url": r.get("url"),
            "content": r.get("content"),
            "score": r.get("score")  # relevance score from Tavily
        })

    return {
        "answer": response.get("answer", ""),
        "results": results
    }
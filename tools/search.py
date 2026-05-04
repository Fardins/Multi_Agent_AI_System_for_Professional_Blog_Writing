"""
Search tool — Tavily preferred (richer content), DuckDuckGo fallback.
Key fix: snippet content NOT truncated at 500 chars — pass full content to analyst.
"""
import os
from typing import List, Dict, Any

_tavily_key = os.getenv("TAVILY_API_KEY", "")

if _tavily_key:
    from langchain_community.tools.tavily_search import TavilySearchResults
    _search = TavilySearchResults(
        max_results=8,              # was 6
        tavily_api_key=_tavily_key,
        include_answer=True,
        include_raw_content=False,
    )

    def run_search(query: str) -> List[Dict[str, Any]]:
        try:
            results = _search.invoke(query)
        except Exception as e:
            return [{"title": "Search error", "url": "", "source": "", "snippet": str(e), "published_at": ""}]
        out = []
        for r in (results or []):
            url = r.get("url", "")
            out.append({
                "title": r.get("title", ""),
                "url": url,
                "source": url.split("/")[2] if url else "",
                "snippet": r.get("content", ""),   # FULL content, no truncation
                "published_at": r.get("published_date", ""),
            })
        return out

else:
    # DuckDuckGo fallback — use DDGS for richer results
    try:
        from duckduckgo_search import DDGS

        def run_search(query: str) -> List[Dict[str, Any]]:
            try:
                results = []
                with DDGS() as ddgs:
                    for r in ddgs.text(query, max_results=8):
                        url = r.get("href", "")
                        results.append({
                            "title": r.get("title", ""),
                            "url": url,
                            "source": url.split("/")[2] if url else "DuckDuckGo",
                            "snippet": r.get("body", ""),  # full body
                            "published_at": "",
                        })
                return results
            except Exception as e:
                return [{"title": "Search error", "url": "", "source": "", "snippet": str(e), "published_at": ""}]

    except ImportError:
        # Fall back to LangChain DuckDuckGo wrapper
        from langchain_community.tools import DuckDuckGoSearchRun
        _ddg = DuckDuckGoSearchRun()

        def run_search(query: str) -> List[Dict[str, Any]]:
            try:
                raw = _ddg.invoke(query)
            except Exception as e:
                return [{"title": "Search error", "url": "", "source": "", "snippet": str(e), "published_at": ""}]
            # LangChain wrapper returns a single string — still useful
            return [{
                "title": query,
                "url": "",
                "source": "DuckDuckGo",
                "snippet": raw[:3000],   # bigger window than before (was 1500)
                "published_at": "",
            }]
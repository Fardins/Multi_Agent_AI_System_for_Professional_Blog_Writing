from graph.workflow import build_graph

graph = build_graph()
app = graph


def run_agent(topic: str, as_of: str = "") -> dict:
    from datetime import date
    return graph.invoke({
        "topic": topic,
        "as_of": as_of or date.today().isoformat(),
        "recency_days": 7,
        "language": "",
        "needs_research": False,
        "queries": [],
        "evidence": [],
        "research": "",
        "plan": None,
        "outline": "",
        "sections": [],
        "merged_md": "",
        "blog": "",
        "edited_blog": "",
        "image_specs": [],
        "md_with_placeholders": "",
        "seo": "",
        "final": "",
        "mode": "",
        "logs": [],
    })
from langgraph.graph import StateGraph, END
from utils.state import BlogState
from agents.language import detect_language
from agents.planner import planner
from agents.researcher import researcher
from agents.writer import writer
from agents.editor import editor
from agents.seo import seo_agent


def build_graph():
    builder = StateGraph(BlogState)

    builder.add_node("detect_language", detect_language)
    builder.add_node("planner", planner)
    builder.add_node("researcher", researcher)
    builder.add_node("writer", writer)
    builder.add_node("editor", editor)
    builder.add_node("seo", seo_agent)

    builder.set_entry_point("detect_language")

    builder.add_edge("detect_language", "planner")
    builder.add_edge("planner", "researcher")
    builder.add_edge("researcher", "writer")
    builder.add_edge("writer", "editor")
    builder.add_edge("editor", "seo")
    builder.add_edge("seo", END)

    return builder.compile()


graph = build_graph()
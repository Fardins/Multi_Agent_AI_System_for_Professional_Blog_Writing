from typing import TypedDict, List, Dict, Any, Optional


class BlogState(TypedDict):
    # Input
    topic: str
    as_of: str
    recency_days: int

    # Language
    language: str          # "en" | "bn"

    # Research
    needs_research: bool
    queries: List[str]
    evidence: List[Dict[str, Any]]
    research: str          # concatenated text for the writer

    # Planning
    plan: Optional[Dict[str, Any]]
    outline: str

    # Writing pipeline
    sections: List[str]    # individual written sections
    merged_md: str         # sections joined
    blog: str              # raw draft
    edited_blog: str       # after editor pass
    image_specs: List[Dict[str, Any]]
    md_with_placeholders: str

    # Output
    seo: str
    final: str             # final markdown delivered to UI

    # Internal / UI extras
    mode: str
    logs: List[str]
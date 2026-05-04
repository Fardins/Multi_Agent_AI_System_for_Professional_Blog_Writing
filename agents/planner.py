import json
import re
from models.llm import llm_plan


def planner(state: dict) -> dict:
    topic = state["topic"]
    lang = state.get("language", "en")
    as_of = state.get("as_of", "")

    if lang == "bn":
        lang_note = "The blog will be written in Bangla. Metadata (blog_title, audience, tone etc.) should still be in English for the pipeline, but section titles can be in Bangla."
    else:
        lang_note = "Blog will be written in English."

    prompt = f"""You are the editorial director of a top-tier digital publication (think Wired, The Atlantic, HBR). You have 20 years of experience knowing exactly what makes a blog post go viral versus get ignored.

Topic: {topic}
Date: {as_of}
{lang_note}

Your job: create the PERFECT content plan for this topic. Think hard about:
- What unique angle will make readers say "I've never thought about it this way"
- What specific audience pain point or curiosity does this topic tap into
- What's the most surprising or counterintuitive truth about this topic

Return ONLY a valid JSON object, no markdown fences, no extra text:
{{
  "blog_title": "Specific, magnetic title. Use one of: number ('7 Reasons...'), bold claim ('Why X Is Killing Y'), curiosity gap ('The X Nobody Talks About'), or how-to with a twist ('How to X Without Y'). Make it impossible to ignore.",
  "hook_angle": "One sentence: the unexpected or counterintuitive angle that makes this blog different from every other article on this topic",
  "audience": "Ultra-specific audience — job title, situation, pain point (e.g. 'junior Python developers who keep writing slow code without knowing why')",
  "tone": "Precise tone description (e.g. 'authoritative mentor — direct, occasionally witty, never condescending, uses real examples')",
  "blog_kind": "tutorial | opinion | explainer | listicle | news | case-study | deep-dive | narrative",
  "needs_research": true,
  "search_queries": [
    "QUERY 1: most specific factual query about the core claim (include current year)",
    "QUERY 2: statistics and data about this topic",
    "QUERY 3: real-world examples and case studies",
    "QUERY 4: expert analysis or academic research on this topic",
    "QUERY 5: common misconceptions or failures related to this topic",
    "QUERY 6: latest developments, trends, or news about this topic 2024 2025"
  ],
  "tasks": [
    {{
      "id": 1,
      "title": "Hook section title — specific, not 'Introduction'",
      "target_words": 280,
      "requires_research": false,
      "requires_citations": false,
      "requires_code": false,
      "writing_brief": "One sentence: exactly what this section should accomplish and what key idea it establishes"
    }},
    {{
      "id": 2,
      "title": "...",
      "target_words": 450,
      "requires_research": true,
      "requires_citations": true,
      "requires_code": false,
      "writing_brief": "One sentence brief"
    }}
  ]
}}

Task rules:
- Include EXACTLY 7 sections (ids 1-7)
- Section 1 is the hook (~280 words), sections 2-6 are body (~400-500 words each), section 7 is conclusion (~220 words)
- Every section title must be specific and editorial — someone should want to read just that section
- Sections 2-5: requires_research=true, requires_citations=true
- If topic is technical/code-related: at least 2 sections need requires_code=true
- writing_brief is mandatory — it's what the writer uses to stay on track
- search_queries must be SPECIFIC to the exact topic, not generic patterns
- Total target words: 2500-3200
"""

    response = llm_plan.invoke(prompt)
    raw = response.content.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    try:
        plan = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            try:
                plan = json.loads(match.group(0))
            except Exception:
                plan = _fallback_plan(topic)
        else:
            plan = _fallback_plan(topic)

    # Ensure 6 search queries minimum
    queries = plan.get("search_queries", [])
    if len(queries) < 3:
        queries = [topic, f"{topic} statistics data", f"{topic} examples case studies",
                   f"{topic} expert analysis", f"{topic} challenges solutions",
                   f"{topic} latest trends 2025"]
    plan["search_queries"] = queries

    return {
        "plan": plan,
        "outline": json.dumps(plan, indent=2),
        "needs_research": plan.get("needs_research", True),
        "queries": queries,
    }


def _fallback_plan(topic: str) -> dict:
    return {
        "blog_title": f"The Complete Truth About {topic}",
        "hook_angle": f"What most people get wrong about {topic}",
        "audience": "Curious, intelligent readers who want depth",
        "tone": "Authoritative but conversational",
        "blog_kind": "deep-dive",
        "needs_research": True,
        "search_queries": [
            f"{topic} facts statistics 2025",
            f"{topic} research studies data",
            f"{topic} real world examples",
            f"{topic} expert opinion analysis",
            f"{topic} common mistakes problems",
            f"{topic} latest developments trends",
        ],
        "tasks": [
            {"id": 1, "title": f"The {topic} Misconception Nobody Corrects", "target_words": 280,
             "requires_research": False, "requires_citations": False, "requires_code": False,
             "writing_brief": "Hook the reader with a surprising truth about this topic"},
            {"id": 2, "title": "What the Evidence Actually Shows", "target_words": 450,
             "requires_research": True, "requires_citations": True, "requires_code": False,
             "writing_brief": "Present the core data and research findings"},
            {"id": 3, "title": "The Mechanisms Behind It All", "target_words": 480,
             "requires_research": True, "requires_citations": True, "requires_code": False,
             "writing_brief": "Explain the why and how with depth"},
            {"id": 4, "title": "Real-World Cases That Prove the Point", "target_words": 450,
             "requires_research": True, "requires_citations": True, "requires_code": False,
             "writing_brief": "Concrete examples from real organizations or people"},
            {"id": 5, "title": "The Biggest Mistakes People Make", "target_words": 400,
             "requires_research": True, "requires_citations": True, "requires_code": False,
             "writing_brief": "Common pitfalls and how to avoid them"},
            {"id": 6, "title": "A Practical Playbook You Can Use Today", "target_words": 420,
             "requires_research": False, "requires_citations": False, "requires_code": False,
             "writing_brief": "Actionable step-by-step guidance"},
            {"id": 7, "title": "The Path Forward", "target_words": 220,
             "requires_research": False, "requires_citations": False, "requires_code": False,
             "writing_brief": "Inspiring conclusion with a memorable closing line"},
        ],
    }
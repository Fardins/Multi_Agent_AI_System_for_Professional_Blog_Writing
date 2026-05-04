"""
Researcher agent — three-phase approach:
1. Run specific, diversified search queries (up to 10)
2. Synthesize raw evidence into a structured knowledge brief
3. Return both the evidence list (for UI) and the brief (for writer)
"""
from tools.search import run_search
from models.llm import llm_analyst


def researcher(state: dict) -> dict:
    queries = state.get("queries") or [state["topic"]]
    topic = state["topic"]
    lang = state.get("language", "en")
    plan = state.get("plan") or {}
    hook_angle = plan.get("hook_angle", "")

    # ── Phase 1: Run all queries ───────────────────────────────────────────
    expanded = _build_query_set(topic, queries, lang, hook_angle)
    all_evidence = _run_queries(expanded)

    # ── Phase 2: Synthesize into a structured brief ────────────────────────
    research_brief = _synthesize(topic, all_evidence, plan, lang)

    return {
        "evidence": all_evidence,
        "research": research_brief,
    }


def _build_query_set(topic: str, planner_queries: list, lang: str, hook_angle: str) -> list:
    """
    Build the final query set.
    Planner gives 6 topic-specific queries. We add 4 more journalist angles.
    Total: up to 10 searches for deep coverage.
    """
    journalist_extras = [
        f'"{topic}" statistics data numbers facts',
        f"{topic} failure mistake lesson learned",
        f"{topic} future prediction forecast 2025 2026",
        f"{topic} beginner guide explained simply",
    ]
    if lang == "bn":
        journalist_extras.append(f"{topic} বাংলাদেশ তথ্য পরিসংখ্যান")

    seen = set()
    merged = []
    for q in list(planner_queries) + journalist_extras:
        key = q.lower().strip()
        if key and key not in seen:
            seen.add(key)
            merged.append(q)

    return merged[:10]  # hard cap at 10 queries


def _run_queries(queries: list) -> list:
    """Execute searches, deduplicate by URL and snippet fingerprint."""
    all_evidence = []
    seen_urls = set()
    seen_fp = set()

    for q in queries:
        try:
            results = run_search(q)
        except Exception:
            continue

        for r in results:
            url = r.get("url", "").strip()
            snippet = r.get("snippet", "").strip()
            fingerprint = snippet[:100].lower()

            if url and url in seen_urls:
                continue
            if fingerprint and fingerprint in seen_fp:
                continue

            if url:
                seen_urls.add(url)
            if fingerprint:
                seen_fp.add(fingerprint)

            all_evidence.append(r)

    return all_evidence[:20]  # keep top 20 unique sources


def _synthesize(topic: str, evidence: list, plan: dict, lang: str) -> str:
    """
    Use an LLM to transform raw search snippets into a structured,
    writer-ready knowledge brief with extracted facts, quotes, and narratives.
    This is the key quality upgrade — the writer receives distilled knowledge,
    not a pile of raw snippets.
    """
    if not evidence:
        return f"No research evidence found for: {topic}"

    # Format raw evidence for the analyst
    raw_block = ""
    for i, e in enumerate(evidence, 1):
        title = e.get("title", "")
        source = e.get("source", "") or (e.get("url", "").split("/")[2] if e.get("url") else "")
        url = e.get("url", "")
        snippet = e.get("snippet", "")
        pub = e.get("published_at", "")
        raw_block += f"\n[{i}] {title}\nSource: {source}{' | ' + pub if pub else ''}\n"
        if url:
            raw_block += f"URL: {url}\n"
        raw_block += f"{snippet}\n"

    audience = plan.get("audience", "")
    hook_angle = plan.get("hook_angle", "")
    sections = plan.get("tasks", [])
    section_titles = [t.get("title", "") for t in sections]

    if lang == "bn":
        synthesis_prompt = f"""আপনি একজন গবেষণা বিশ্লেষক। নিচের কাঁচা গবেষণা উপাত্ত থেকে একটি কাঠামোবদ্ধ জ্ঞান সারসংক্ষেপ তৈরি করুন।

বিষয়: {topic}
পাঠক: {audience}

গবেষণা উপাত্ত:
{raw_block[:8000]}

নির্দেশনা:
একটি বিস্তারিত, ব্যবহারযোগ্য গবেষণা সংক্ষিপ্তসার তৈরি করুন:

1. **মূল তথ্য ও পরিসংখ্যান** — নির্দিষ্ট সংখ্যা, শতাংশ, তারিখ সহ (উৎস উল্লেখ করুন)
2. **বিশেষজ্ঞ উদ্ধৃতি** — সরাসরি উদ্ধৃতি বা শক্তিশালী মতামত (নাম ও পদ সহ)
3. **বাস্তব উদাহরণ** — নির্দিষ্ট সংস্থা, ব্যক্তি বা ঘটনা
4. **আশ্চর্যজনক বা পাল্টা-প্রত্যাশামূলক তথ্য** — পাঠককে চমকে দেবে এমন কিছু
5. **সাধারণ ভুল ধারণা** — যা স্পষ্টভাবে ভুল বলা হয়েছে
6. **বিভাগ অনুযায়ী গবেষণা** — প্রতিটি বিভাগের জন্য প্রাসঙ্গিক তথ্য:
{chr(10).join(f'   - {t}' for t in section_titles)}

প্রতিটি তথ্যের সাথে উৎস নম্বর [N] এবং URL উল্লেখ করুন।
"""
    else:
        synthesis_prompt = f"""You are a senior research analyst. Your job is to transform raw search results into a structured, actionable knowledge brief for a blog writer.

Topic: {topic}
Audience: {audience}
Blog angle: {hook_angle}

Blog sections to cover:
{chr(10).join(f'  - {t}' for t in section_titles)}

RAW SEARCH RESULTS:
{raw_block[:8000]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR TASK: Extract and organize everything a writer needs. Do NOT summarize vaguely.
Be specific — exact numbers, exact names, exact quotes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Produce a structured research brief with these sections:

## KEY STATISTICS & DATA POINTS
- List every specific number, percentage, date, or measurement found
- Format: "STAT: [exact number] — [context] [Source N](url)"
- Include at least 8-10 stats if available

## EXPERT QUOTES & AUTHORITATIVE STATEMENTS
- Exact quotes or strong paraphrased positions from named experts
- Format: "[Quote or position]" — [Name], [Title], [Organization] [Source N](url)

## REAL-WORLD EXAMPLES & CASE STUDIES
- Specific companies, products, people, events with measurable outcomes
- What happened, what was the result, why it matters

## SURPRISING / COUNTERINTUITIVE FINDINGS
- Facts that challenge common assumptions about this topic
- Information that would make a reader say "I didn't know that"

## COMMON MISCONCEPTIONS OR FAILURES
- What people get wrong, what approaches fail and why

## LATEST DEVELOPMENTS (2024-2025)
- Most recent news, research, or changes in this space

## SECTION-BY-SECTION RESEARCH
For each blog section, list the most relevant evidence:
{chr(10).join(f'### For section: "{t}"{chr(10)}[List 2-3 most relevant facts/quotes/examples from the research]' for t in section_titles)}

━━━━━━━━━━━━━━━━━━━━━━━━━━━
Always cite sources as [Source N](url). If a source has no URL, cite as [Source N].
"""

    response = llm_analyst.invoke(synthesis_prompt)
    return response.content.strip()
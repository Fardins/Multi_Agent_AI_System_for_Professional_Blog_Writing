<div align="center">

<br/>

```
 ██████╗ ██╗      ██████╗  ██████╗      █████╗  ██████╗ ███████╗███╗   ██╗████████╗
 ██╔══██╗██║     ██╔═══██╗██╔════╝     ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝
 ██████╔╝██║     ██║   ██║██║  ███╗    ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║
 ██╔══██╗██║     ██║   ██║██║   ██║    ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║
 ██████╔╝███████╗╚██████╔╝╚██████╔╝    ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║
 ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝
```

### A production-grade multi-agent AI system that researches, writes, edits,<br/>and SEO-optimises professional blog posts — fully automatically.

<br/>

[![Live Demo](https://img.shields.io/badge/%20Live%20Demo-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://your-app-name.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1%2B-00C896?style=for-the-badge)](https://github.com/langchain-ai/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3%2070B-F55036?style=for-the-badge)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

**English** · **বাংলা** · 6 Specialised Agents · 10 Research Sources · 2,500–3,200 Words Per Blog

<br/>

</div>

---

## Table of Contents

1. [What This Project Does](#1-what-this-project-does)
2. [Live Demo](#2-live-demo)
3. [Why It Produces Better Content Than a Single Prompt](#3-why-it-produces-better-content-than-a-single-prompt)
4. [The Full Pipeline — How It Works](#4-the-full-pipeline--how-it-works)
5. [Agent Reference](#5-agent-reference)
   - [Language Detector](#51-language-detector--agentslanguagepy)
   - [Planner](#52-planner--agentsplannerpy)
   - [Researcher](#53-researcher--agentsresearcherpy)
   - [Writer](#54-writer--agentswriterpy)
   - [Editor](#55-editor--agentseditorpy)
   - [SEO Agent](#56-seo-agent--agentsseospy)
6. [Project Structure](#6-project-structure)
7. [Tech Stack](#7-tech-stack)
8. [LLM Configuration](#8-llm-configuration)
9. [State Schema — BlogState](#9-state-schema--blogstate)
10. [Search Backends](#10-search-backends)
11. [Bilingual Support](#11-bilingual-support)
12. [Installation](#12-installation)
13. [Environment Variables](#13-environment-variables)
14. [Running the App](#14-running-the-app)
15. [UI Walkthrough](#15-ui-walkthrough)
    - [Sidebar Controls](#sidebar-controls)
    - [Pipeline Progress](#pipeline-progress)
    - [The Six Output Tabs](#the-six-output-tabs)
    - [Past Blogs Library](#past-blogs-library)
    - [Downloads](#downloads)
16. [Output Format](#16-output-format)
17. [Programmatic Usage](#17-programmatic-usage)
18. [Troubleshooting](#18-troubleshooting)
19. [Roadmap](#19-roadmap)
20. [Contributing](#20-contributing)

---

## 1. What This Project Does

Blog Agent takes a single topic as input — typed in plain English or Bangla — and runs it through a **six-node LangGraph pipeline** where each node is a specialised AI agent with one job. The result is a fully-written, research-backed, SEO-optimised Markdown blog post of 2,500–3,200 words, automatically saved and ready to publish.

**Input:** `"Why Python's GIL is finally being removed — and what it means for you"`

**Output in ~2–3 minutes:**
- A 2,800-word Markdown blog with 7 structured sections
- Up to 20 cited research sources
- Image placeholders at strategic positions
- SEO metadata: meta title, description, slug, keywords, reading time, social snippet
- Auto-saved to `saved_blogs/` with a JSON metadata sidecar
- Downloadable as `.md` or as a `.zip` bundle

The UI is a dark-themed Streamlit application with real-time pipeline progress, six output tabs (Preview, Plan, Evidence, SEO, Images, Logs), and a persistent past-blogs library with load and delete controls.

---

## 2. Live Demo

<div align="center">

### Try it live — no installation needed

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://multiagentaisystemforprofessionalblogwriting.streamlit.app/)

**[Multi_Agent_AI_System_for_Professional_Blog_Writing](https://multiagentaisystemforprofessionalblogwriting.streamlit.app/)**


> See [Running the App](#14-running-the-app) → *Deploy to Streamlit Cloud* for step-by-step instructions.

</div>

| What you can do in the live demo | Notes |
|---|---|
| Enter any topic in **English or Bangla** | Auto-detected — no setting needed |
| Watch the **6-agent pipeline** run in real time | Progress updates step by step |
| Read the generated blog in the **Preview tab** | Fully rendered Markdown |
| Inspect all **research sources** in the Evidence tab | Up to 20 cited sources |
| View the **SEO metadata** with character-length meters | Meta title, description, keywords, slug |
| **Download** as `.md` or `.zip` bundle | Ready to publish on Ghost, Hashnode, Dev.to |

> The live demo uses shared API keys with rate limits. For unlimited use, [run it locally](#12-installation) with your own `GROQ_API_KEY`.
---

## 3. Why It Produces Better Content Than a Single Prompt

Asking an LLM "write me a blog about X" produces mediocre output for one reason: the model tries to research, plan, structure, write, edit, and optimise in a single pass. Quality collapses under that cognitive load.

This project breaks the work into **six specialists**, each focused on exactly one task:

| Problem with a single prompt | How this project solves it |
|---|---|
| Generic structure — same introduction, body, conclusion every time | **Planner** crafts a unique `hook_angle` per topic and generates 7 editorially-specific section titles |
| Shallow research — model relies on training data | **Researcher** runs up to 10 live web searches and passes a synthesised knowledge brief (not raw snippets) to the writer |
| Token budget competition — writing 7 sections in one call means each section is short | **Writer** makes 7 separate LLM calls, one per section — full token budget per section |
| Sections don't connect — each section feels isolated | Writer receives the **tail of the previous section** (600 chars) for natural continuity |
| Vague, padded language | Both writer and editor have explicit before/after examples of forbidden vagueness and a 30-item forbidden-phrase list |
| Weak opening and closing | Editor applies a **7-priority editorial mandate** starting with the hook and ending with the conclusion |

---

## 4. The Full Pipeline — How It Works

```
User enters topic (English or Bangla)
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                  LangGraph StateGraph (BlogState)               │
│                                                                 │
│  ┌──────────────────┐                                           │
│  │ detect_language  │  Scans for Bangla Unicode U+0980–U+09FF  │
│  │   language.py    │  Sets state["language"] = "en" | "bn"    │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐                                           │
│  │    planner       │  Produces: blog_title, hook_angle,        │
│  │   planner.py     │  audience, tone, blog_kind,               │
│  │  [llm_plan 0.2]  │  6 search_queries, 7 section tasks        │
│  │                  │  each with title + writing_brief          │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐  Phase 1: Expands to 10 queries           │
│  │   researcher     │  Phase 2: Runs all searches               │
│  │  researcher.py   │  Phase 3: llm_analyst synthesises         │
│  │ [llm_analyst 0.1]│  raw snippets → structured brief          │
│  │                  │  Returns: evidence list + research brief  │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐  7 individual LLM calls (one per section) │
│  │     writer       │  Each call receives: full research brief, │
│  │    writer.py     │  section writing_brief, tail of previous  │
│  │   [llm 0.65]     │  section, role-specific instructions      │
│  │                  │  Assembles: # Title + 7 ## sections        │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐  7-priority editorial mandate:            │
│  │     editor       │  Hook → Dead weight → Vague→Specific →    │
│  │    editor.py     │  Weak verbs → Rhythm → Conclusion →       │
│  │   [llm 0.65]     │  Blockquotes. Safety: reverts if output   │
│  │                  │  < 60% of original word count             │
│  └────────┬─────────┘                                           │
│           │                                                     │
│           ▼                                                     │
│  ┌──────────────────┐  Generates JSON: meta_title, description, │
│  │   seo_agent      │  keywords, slug, reading_time,            │
│  │     seo.py       │  social_snippet. Appends as HTML          │
│  │ [llm_plan 0.2]   │  comment block to final Markdown          │
│  └────────┬─────────┘                                           │
│           │                                                     │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
   state["final"] = complete Markdown
   Auto-saved to saved_blogs/{slug}_{timestamp}.md
   + saved_blogs/{slug}_{timestamp}.json (metadata sidecar)
```

The graph streams — each node emits its output as it completes. The Streamlit UI updates the progress display and live state JSON panel in real time without waiting for the full pipeline to finish.

---

## 5. Agent Reference

### 5.1 Language Detector — `agents/language.py`

**Model:** None (pure Python)

Scans `state["topic"]` for any character in the Bangla Unicode block (`U+0980–U+09FF`). Sets `state["language"]` to `"bn"` or `"en"`. Every downstream agent reads this flag and switches its entire prompt between English and Bangla, making the full pipeline bilingual.

```python
# The entire detection logic
if re.search(r"[\u0980-\u09FF]", topic):
    language = "bn"   # Bangla detected
else:
    language = "en"   # Default: English
```

**Input state keys:** `topic`
**Output state keys:** `language`

---

### 5.2 Planner — `agents/planner.py`

**Model:** `llm_plan` — LLaMA 3.3 70B, temperature **0.2** (precise structured output)

The editorial brain of the pipeline. Receives the topic and returns a complete JSON content plan. Low temperature is critical here because this output is parsed as JSON — creative drift causes parse failures.

**What it produces:**

| JSON field | Description |
|---|---|
| `blog_title` | Magnetic title using proven formulas: number list, bold claim, curiosity gap, or how-to with a twist |
| `hook_angle` | One sentence — the counterintuitive angle that makes this blog different from every other article on this topic |
| `audience` | Ultra-specific persona with job title, situation, and pain point (e.g. "junior Python devs who keep writing slow code without knowing why") |
| `tone` | Precise descriptor (e.g. "authoritative mentor — direct, occasionally witty, never condescending") |
| `blog_kind` | One of: `tutorial`, `opinion`, `explainer`, `listicle`, `news`, `case-study`, `deep-dive`, `narrative` |
| `needs_research` | Always `true` for most topics |
| `search_queries` | Exactly 6 topic-specific queries (not generic patterns) covering: core claim, statistics, case studies, expert analysis, misconceptions, latest trends |
| `tasks` | Array of exactly 7 section objects, each with `id`, `title`, `target_words`, `requires_research`, `requires_citations`, `requires_code`, and `writing_brief` |

**Fallback behaviour:** If JSON parsing fails, `re.search(r"\{[\s\S]*\}", raw)` attempts to extract a JSON object from any surrounding text. If that also fails, a hardcoded `_fallback_plan()` activates with a sensible 7-section structure.

**Minimum query guarantee:** If the model returns fewer than 3 queries, the planner injects 6 standard topic-based queries before passing to the researcher.

**Input state keys:** `topic`, `language`, `as_of`
**Output state keys:** `plan`, `outline`, `needs_research`, `queries`

---

### 5.3 Researcher — `agents/researcher.py`

**Model:** `llm_analyst` — LLaMA 3.3 70B, temperature **0.1** (fact extraction, no hallucination)

Three-phase process that turns a topic into a writer-ready knowledge brief.

**Phase 1 — Query expansion**

Takes the planner's 6 queries and adds 4 journalist-style angles, deduplicating by lowercased string:

```
Planner queries (6)     +     Journalist extras (4)
─────────────────────         ─────────────────────────────────────
Core claim query              "{topic}" statistics data numbers facts
Statistics query              {topic} failure mistake lesson learned
Case studies query            {topic} future prediction forecast 2025 2026
Expert analysis query         {topic} beginner guide explained simply
Misconceptions query          [+ Bangla query if lang == "bn"]
Latest trends query
```

Hard cap: **10 queries maximum**.

**Phase 2 — Evidence collection**

Runs all queries through the search backend. Deduplicates results by **URL** and by **snippet fingerprint** (first 100 characters lowercased). Keeps up to **20 unique sources**.

**Phase 3 — LLM synthesis**

This is the most important quality step in the entire pipeline. Raw search snippets (up to 8,000 characters) are passed to `llm_analyst` which produces a **structured knowledge brief** organised into these sections:

```
## KEY STATISTICS & DATA POINTS
   Format: "STAT: [exact number] — [context] [Source N](url)"
   Minimum 8-10 stats if available

## EXPERT QUOTES & AUTHORITATIVE STATEMENTS
   Format: "[Quote]" — [Name], [Title], [Organization] [Source N](url)

## REAL-WORLD EXAMPLES & CASE STUDIES
   Specific companies/people/events with measurable outcomes

## SURPRISING / COUNTERINTUITIVE FINDINGS
   Facts that challenge common assumptions

## COMMON MISCONCEPTIONS OR FAILURES
   What people get wrong and why

## LATEST DEVELOPMENTS (2024-2025)
   Most recent changes in this space

## SECTION-BY-SECTION RESEARCH
   ### For section: "Section Title"
   [2-3 most relevant facts/quotes/examples]
   ... (repeated for all 7 sections)
```

The writer receives this structured brief, not raw snippets. This is why blog content is specific and well-cited rather than vague and generic.

**Input state keys:** `queries`, `topic`, `language`, `plan`
**Output state keys:** `evidence` (list of source dicts, shown in UI), `research` (synthesised brief, passed to writer)

---

### 5.4 Writer — `agents/writer.py`

**Model:** `llm` — LLaMA 3.3 70B, temperature **0.65**, max_tokens **8,192**

Writes the blog **one section at a time** — 7 separate LLM calls. Each call has its full token budget available and receives exactly the context it needs.

**Per-section context passed to each call:**

```
Full blog context:   title, topic, hook_angle, audience, tone, blog_kind
Section context:     section title, target_words, writing_brief
Role instruction:    position-specific block (hook / body / conclusion)
Research:            full 6,000-char synthesised brief
Continuity:          tail of previous section (last 600 chars)
Requirements:        citations block (if requires_citations=true)
                     code block (if requires_code=true)
                     image placeholder instruction
Writing rules:       voice, specificity, rhythm, mandatory elements,
                     30 forbidden phrases
```

**Position-specific role instructions:**

- **Section 1 (hook):** Four opening strategy options (stat / micro-story / bold claim / specific question). Forbidden opener list. Ends with a "promise sentence" requirement.
- **Sections 2–6 (body):** Mini-hook → core explanation (WHY and HOW, not just WHAT) → evidence from research → surprising sub-point → transition sentence.
- **Section 7 (conclusion):** Callback to opening → 3–4 bullet takeaways → one concrete action → quotable final line.

**Post-processing:**
- Regex strips any LLM preamble before the `##` heading
- Ensures every section starts with a `## ` heading
- Sections assembled with `---` dividers
- `IMAGE_PLACEHOLDER_*` tags extracted into `image_specs`

**Assembly format:**
```
# Blog Title

## Section 1 Title
[content]

---

## Section 2 Title
[content]

--- ... (×7)
```

**Input state keys:** `topic`, `research`, `language`, `plan`
**Output state keys:** `blog`, `sections`, `merged_md`, `image_specs`, `md_with_placeholders`

---

### 5.5 Editor — `agents/editor.py`

**Model:** `llm` — LLaMA 3.3 70B, temperature **0.65**

Applies a **7-priority editorial mandate** in a single focused pass. Not a grammar check — a real editorial intervention.

| Priority | What it fixes | Example |
|---|---|---|
| **1 — Hook** | Rewrites the opening 3 paragraphs entirely if they don't immediately grab | Replaces a generic setup paragraph with a specific stat or micro-story |
| **2 — Dead weight** | Deletes every sentence removable without losing meaning | Removes "In this section, we will explore..." throat-clearing |
| **3 — Vague → specific** | Every vague quantifier replaced with numbers or names | `"many companies"` → `"74% of surveyed companies"` |
| **4 — Weak verbs** | Passive and weak constructions become strong and active | `"it was found that"` → `"[Researcher] found"` |
| **5 — Rhythm** | Adds short punchy sentences after dense paragraphs | A one-sentence takeaway after a complex technical paragraph |
| **6 — Conclusion** | Rewrites the final sentence until it's quotable | Something a reader would screenshot and share |
| **7 — Blockquotes** | Sharpens every `> **Key insight:**` to the section's single best idea | Replaces a generic observation with the section's most surprising finding |

**Hard constraints enforced:**
- All `IMAGE_PLACEHOLDER_*` tags preserved
- All `##` and `###` headings preserved
- All citation links preserved
- Output must be ≥ 90% of input word count
- No new sections added
- No preamble ("Here is the edited version:")

**Safety revert:** If the edited output is less than 60% of the original word count (indicating the model accidentally truncated), the original blog is returned unchanged.

**Input state keys:** `blog`, `language`, `plan`
**Output state keys:** `edited_blog`

---

### 5.6 SEO Agent — `agents/seo.py`

**Model:** `llm_plan` — LLaMA 3.3 70B, temperature **0.2** (precise JSON)

Generates a complete SEO metadata object and appends it as an HTML comment block to the final Markdown.

**JSON output:**
```json
{
  "meta_title":           "≤60 chars, keyword-rich title for search engines",
  "meta_description":     "≤155 chars, compelling description for search snippets",
  "keywords":             ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "slug":                 "url-friendly-slug",
  "reading_time_minutes": 8,
  "social_snippet":       "One punchy sentence optimised for social sharing"
}
```

**Appended to the Markdown as:**
```html
<!-- SEO Metadata
Meta Title: ...
Meta Description: ...
Keywords: keyword1, keyword2, ...
Slug: /url-friendly-slug
Reading Time: 8 min
Social: ...
-->
```

The SEO block is stripped from the UI preview for a clean reading experience but included in all file downloads. The Streamlit SEO tab shows character-length meters (60-char limit for title, 155-char for description) with pass/fail indicators.

**Input state keys:** `edited_blog`, `blog`, `language`, `plan`
**Output state keys:** `seo`, `final`

---

## 6. Project Structure

```
blog-writing-agent/
│
├── app.py                    # Streamlit UI — all frontend code (~950 lines)
├── main.py                   # Entry point: graph alias + run_agent() helper
├── requirements.txt          # All Python dependencies
├── .env.example              # Copy to .env and fill in your keys
│
├── agents/                   # One file = one agent = one responsibility
│   ├── __init__.py
│   ├── language.py           # Unicode scan → "en" | "bn"
│   ├── planner.py            # Content strategy + 6 search queries + 7 section tasks
│   ├── researcher.py         # 10 web searches + LLM synthesis → knowledge brief
│   ├── writer.py             # 7 individual LLM calls → assembled blog
│   ├── editor.py             # 7-priority editorial pass → polished blog
│   └── seo.py                # SEO metadata JSON → appended to final Markdown
│
├── graph/
│   ├── __init__.py
│   └── workflow.py           # LangGraph StateGraph: nodes + edges + compile()
│
├── models/
│   ├── __init__.py
│   └── llm.py                # 4 ChatGroq instances (different temps per role)
│
├── tools/
│   ├── __init__.py
│   └── search.py             # Tavily (preferred) / DDGS / LangChain DDG fallback
│
├── utils/
│   ├── __init__.py
│   ├── state.py              # BlogState TypedDict — shared state schema
│   └── logger.py             # Simple in-memory logger (no Streamlit dependency)
│
├── saved_blogs/              # Auto-created on first run
│   ├── {slug}_{ts}.md        # Final Markdown for each generated blog
│   └── {slug}_{ts}.json      # Metadata sidecar: title, topic, lang, word count, SEO
│
└── images/                   # Drop real images here to include in bundle downloads
```

---

## 7. Tech Stack

| Component | Technology | Version | Role |
|---|---|---|---|
| **Agent orchestration** | [LangGraph](https://github.com/langchain-ai/langgraph) | ≥ 0.1.0 | State machine, streaming, graph compilation |
| **LLM inference** | [Groq](https://groq.com) | API | Ultra-fast LLaMA 3.3 70B (~400 tok/s) |
| **LLM framework** | [LangChain](https://langchain.com) | ≥ 0.2.0 | LLM wrappers (`ChatGroq`), tool integration |
| **Search (primary)** | [Tavily](https://tavily.com) | API (optional) | Full-content web search, built for AI |
| **Search (fallback 1)** | [duckduckgo-search](https://pypi.org/project/duckduckgo-search/) | ≥ 6.1.0 | Free, returns title + URL + body per result |
| **Search (fallback 2)** | LangChain DDG Wrapper | built-in | Last resort, returns single combined string |
| **UI** | [Streamlit](https://streamlit.io) | ≥ 1.35.0 | Web app, streaming display, session state |
| **Data tables** | [Pandas](https://pandas.pydata.org) | ≥ 2.0.0 | Evidence and plan table rendering |
| **Configuration** | [python-dotenv](https://pypi.org/project/python-dotenv/) | ≥ 1.0.0 | `.env` file loading |
| **Language** | Python | 3.10+ | Runtime |

---

## 8. LLM Configuration

Four distinct `ChatGroq` instances are defined in `models/llm.py`, each tuned precisely for its role:

```python
# Primary writer — creative latitude, consistent enough for long-form prose
llm = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.65,
    max_tokens=8192        # Must be high — writer produces ~500 words per call
)

# Planner + SEO — produces JSON that gets parsed; drift = parse failure
llm_plan = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=2048
)

# Research analyst — extracts facts; any creativity = hallucination risk
llm_analyst = ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=4096
)

# Fast model — reserved for lightweight classification tasks
llm_fast = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=1024
)
```

**Why Groq over OpenAI or Anthropic?**
Groq's LPU hardware runs LLaMA 3.3 70B at approximately 400 tokens/second — roughly 8–10× faster than comparable API providers. The writer agent makes **7 sequential LLM calls per blog**. At a slow provider that would take 4–6 minutes; on Groq it takes under 90 seconds.

**Why four separate temperature settings?**
Using one temperature for all agents is a common mistake. The writer needs creative latitude to produce varied, vivid prose (0.65). The planner must output valid JSON reliably — high temperature causes formatting drift (0.2). The research analyst extracts facts from source material; any creative latitude risks fabricating statistics (0.1).

---

## 9. State Schema — BlogState

The `BlogState` TypedDict in `utils/state.py` is the shared memory that flows through the entire graph. Every agent reads from and writes to a subset of these keys.

```python
class BlogState(TypedDict):

    # ── Input (set by UI, never modified by agents) ────────────────────────
    topic:          str            # Raw user input text
    as_of:          str            # ISO date e.g. "2025-05-03" — context for research
    recency_days:   int            # Research recency window (1–90)

    # ── Set by detect_language ─────────────────────────────────────────────
    language:       str            # "en" | "bn"

    # ── Set by planner ─────────────────────────────────────────────────────
    plan:           Optional[Dict] # Full plan JSON (title, angle, audience, tasks...)
    outline:        str            # JSON string of plan (for logging)
    needs_research: bool           # Always true in practice
    queries:        List[str]      # 6 planner search queries

    # ── Set by researcher ──────────────────────────────────────────────────
    evidence:       List[Dict]     # Up to 20 source dicts {title, url, source, snippet}
    research:       str            # Synthesised knowledge brief (passed to writer)

    # ── Set by writer ──────────────────────────────────────────────────────
    sections:       List[str]      # 7 individually-written section strings
    blog:           str            # Assembled draft: "# Title\n\n## S1\n\n---\n\n## S2..."
    merged_md:      str            # Same as blog (alias)
    md_with_placeholders: str      # Same as blog (before placeholder replacement)
    image_specs:    List[Dict]     # [{section: "name", placeholder: "IMAGE_PLACEHOLDER_name"}]

    # ── Set by editor ──────────────────────────────────────────────────────
    edited_blog:    str            # Blog after editorial pass

    # ── Set by seo_agent ───────────────────────────────────────────────────
    seo:            str            # JSON string of SEO metadata
    final:          str            # edited_blog + SEO comment block → delivered to UI

    # ── Internal / UI ──────────────────────────────────────────────────────
    mode:           str            # Reserved for future routing modes
    logs:           List[str]      # Pipeline log entries
```

---

## 10. Search Backends

`tools/search.py` auto-selects the best available backend at import time, with no manual configuration needed.

### Priority 1 — Tavily *(recommended)*
Activated when `TAVILY_API_KEY` is set in the environment. Returns up to **8 results per query** with full article content (not truncated), published dates, and domain attribution. Purpose-built for AI research workflows.

### Priority 2 — DuckDuckGo Search (DDGS)
Used when Tavily is not configured. Uses the `duckduckgo-search` package's `DDGS` class. Returns up to **8 results per query** with `title`, `href` (URL), and full `body` text. Free, no API key required.

### Priority 3 — LangChain DuckDuckGo Wrapper
Secondary fallback if the `duckduckgo-search` package itself is unavailable. Uses `DuckDuckGoSearchRun` from `langchain-community`, which returns a single concatenated string per query. Functional but produces shorter, less structured content.

**To switch backends:** Set or remove `TAVILY_API_KEY` in `.env`. No code changes needed.

**Deduplication:** Results across all queries are deduplicated by URL (exact match) and by snippet fingerprint (first 100 characters, lowercased). This prevents the same article appearing multiple times across different queries.

---

## 11. Bilingual Support

The pipeline has complete end-to-end bilingual support. Detection is automatic — write your topic in Bangla and everything switches automatically.

| Agent | English behaviour | Bangla behaviour |
|---|---|---|
| **Language** | Sets `"en"` | Sets `"bn"` (Unicode scan) |
| **Planner** | English prompts and JSON | Same JSON schema; `lang_note` instructs model that content will be in Bangla |
| **Researcher** | Standard 10 queries | Adds `{topic} বাংলাদেশ তথ্য পরিসংখ্যান` as extra query; full Bangla synthesis prompt |
| **Writer** | English prompts with English voice/specificity rules | Full Bangla prompts with equivalent Bangla rules |
| **Editor** | English 7-priority mandate | Full Bangla editorial mandate |
| **SEO** | Includes `social_snippet` field | Omits `social_snippet`; Bangla metadata |
| **UI sidebar** | Shows 🇬🇧 flag | Shows 🇧🇩 flag |

**Important:** Detection is based on actual Bangla Unicode characters, not Latin transliteration. `"Bangla te blog likhte chai"` is detected as English. Type or paste actual Bangla script for Bangla mode.

---

## 12. Installation

### Prerequisites

- Python **3.10** or higher
- A [Groq API key](https://console.groq.com) — free account available
- A [Tavily API key](https://tavily.com) — optional, free tier available, strongly recommended

### Step-by-step

```bash
# 1. Clone the repository
git clone https://github.com/your-username/blog-writing-agent.git
cd blog-writing-agent

# 2. Create a virtual environment
python -m venv venv

# Activate — macOS / Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Open .env and add your API keys (see next section)

# 5. Launch
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 13. Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# ── Required ───────────────────────────────────────────────────────────────
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ── Optional but strongly recommended ─────────────────────────────────────
TAVILY_API_KEY=tvly_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

| Variable | Required | Where to get it | Effect if missing |
|---|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | [console.groq.com](https://console.groq.com) → API Keys | App will not start — all 4 LLM instances fail |
| `TAVILY_API_KEY` | ⬜ No | [app.tavily.com](https://app.tavily.com) → API | Falls back to DuckDuckGo automatically |

**Groq free tier** is sufficient for development — it includes generous rate limits for LLaMA 3.3 70B. **Tavily free tier** includes 1,000 searches/month, which covers approximately 100 blog generations.

---

## 14. Running the App

```bash
# Standard run
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8080

# Accessible on local network (e.g. for mobile testing)
streamlit run app.py --server.address 0.0.0.0

# Headless (no browser auto-open)
streamlit run app.py --server.headless true
```

**Programmatic run (no UI):**
```bash
python -c "from main import run_agent; r = run_agent('Your topic here'); print(r['final'])"
```

---

## 15. UI Walkthrough

### Sidebar Controls

| Control | Description |
|---|---|
| **Blog Topic** text area | Enter your topic in English or Bangla. The full topic text feeds directly into the planner's editorial reasoning. |
| **As of** date picker | Sets the date context for research queries. Affects recency phrasing in search (e.g. "2025 data"). Defaults to today. |
| **Recency (days)** number input | Range: 1–90. How recent the research should be. Passed to the planner as context. |
| **Generate Blog** | Starts the pipeline. Disabled while another run is in progress (Streamlit prevents concurrent runs). |

---

### Pipeline Progress

While the pipeline runs, the main area splits into two columns:

**Left — Pipeline Progress:**
Six labelled steps with animated state indicators:
- `○` Pending (not yet reached)
- `⏳` Active (pulsing animated dot, currently running)
- `✓` Done (green, completed)

```
○  Detect Language
✓  Plan Structure
⏳ Research Web      ← currently running
○  Write Blog
○  Edit & Polish
○  Generate SEO
```

**Right — Live State JSON:**
Updates after each node completes, showing:
```json
{
  "language": "en",
  "needs_research": true,
  "queries": ["query 1", "query 2", "query 3"],
  "evidence_sources": 14,
  "plan_sections": 7,
  "blog_words": 2847,
  "edited_words": 2791
}
```

---

### The Six Output Tabs

#### 📝 Preview
The full blog rendered as styled Markdown in a reader view (max-width 820px, dark card background). SEO comment block stripped for clean reading. Two download buttons: `.md` file and `.zip` bundle.

#### 🗺️ Plan
The planner's full content strategy:
- Blog title, audience, tone, type displayed prominently
- Section table with columns: `#`, `Title`, `Words`, `Research ✓`, `Citations ✓`, `Code ✓`, `Tags`
- Expandable "Raw plan JSON" for full details

#### 🔎 Evidence
All research sources rendered as rich cards. Each card shows:
- Source number and title
- Domain name and publication date (if available)
- Clickable URL link
- 350-character snippet preview

Expandable table view shows all sources in a sortable dataframe.

#### 🏷️ SEO
Styled metadata display:
- Field cards for: Meta Title, Meta Description, URL Slug, Reading Time, Social Snippet
- Keyword pills rendered as styled inline tags
- Character-length meters: title (60-char limit) and description (155-char limit) with green ✓ or amber ⚠️ indicators
- Expandable raw JSON

#### 🖼️ Images
Two sections:
1. **Image plan** — lists every `IMAGE_PLACEHOLDER_*` tag found in the blog, showing which section it belongs to and the exact placeholder string to replace
2. **Saved images** — if real image files exist in the `images/` folder, they render in a 3-column grid with individual captions, plus a "Download all images (.zip)" button

#### 🧾 Logs
Terminal-style monospace display showing pipeline events: which node completed, word counts at each stage, and the auto-save path. Clearable with the 🗑️ button.

---

### Past Blogs Library

Every successfully generated blog is **automatically saved** to `saved_blogs/` as two files:

```
saved_blogs/
├── why_python_s_GIL_is_finally_20250503_142217.md     ← full blog Markdown
└── why_python_s_GIL_is_finally_20250503_142217.json   ← metadata sidecar
```

The `.json` sidecar contains:
```json
{
  "title": "Blog title",
  "topic": "Original user input",
  "language": "en",
  "word_count": 2847,
  "saved_at": "20250503_142217",
  "seo": "{...SEO JSON...}",
  "evidence_count": 14
}
```

The sidebar lists up to 30 saved blogs, newest first, each showing:
- Language flag (🇬🇧 English / 🇧🇩 Bangla)
- Truncated blog title (35 chars max)
- Word count

**Load** — Restores the blog into all six output tabs, including the SEO tab populated from the sidecar.
**🗑️** — Permanently deletes both the `.md` and `.json` files, then refreshes.

---

### Downloads

| Button | Location | Contents |
|---|---|---|
| **Download .md** | Preview tab | Full Markdown including the SEO comment block at the bottom |
| **Download Bundle** | Preview tab | `.zip` containing the `.md` file + everything in `images/` under an `images/` subdirectory |
| **Download all images (.zip)** | Images tab | Just the images from the `images/` folder |

The `.md` output is directly compatible with **Ghost**, **Hashnode**, **Dev.to**, **Notion**, **Obsidian**, **Medium** (via import), and any Markdown-aware CMS.

---

## 16. Output Format

A complete generated blog follows this structure:

```markdown
# The Blog Title

## Hook Section Title

[Opening paragraph — specific stat, vivid micro-story, or bold claim]

[2–3 supporting paragraphs with research citations]

> **Key insight:** The sharpest idea of this section in one memorable sentence.

![Descriptive alt text](IMAGE_PLACEHOLDER_hook_section)

---

## Body Section 2 Title

[Mini-hook sentence]

[Core explanation — the WHY and HOW]

[Research-backed paragraphs with inline citations]
> **Striking stat here** — [Source Name](https://url)

**Bold key term** used for emphasis where it genuinely aids scanning.

- Bullet point for first item when 3+ related items exist
- Second item
- Third item

> **Key insight:** ...

![Alt text](IMAGE_PLACEHOLDER_section_2)

---

## ... (sections 3–6) ...

---

## Conclusion Title

[Callback to the opening hook — reference the specific stat/story]

Key takeaways:
- Most important insight from the whole blog
- Second key insight
- Third key insight

[One specific, concrete action the reader can take today]

[Quotable final sentence — something worth sharing.]

---
<!-- SEO Metadata
Meta Title: ≤60 char title
Meta Description: ≤155 char description
Keywords: keyword1, keyword2, keyword3, keyword4, keyword5
Slug: /url-friendly-slug
Reading Time: 8 min
Social: One punchy sentence for social sharing
-->
```

---

## 17. Programmatic Usage

Use `run_agent()` from `main.py` for simple invocations:

```python
from main import run_agent

result = run_agent(
    topic="Why Python's GIL is finally being removed",
    as_of="2025-05-03"
)

# Access outputs
print(result["final"])            # Complete final Markdown (edited + SEO)
print(result["blog"])             # Raw draft before editing
print(result["edited_blog"])      # After editor pass, before SEO append
print(result["plan"])             # Dict: title, angle, audience, tasks...
print(result["evidence"])         # List of source dicts
print(result["seo"])              # JSON string of SEO metadata
print(result["language"])         # "en" or "bn"
print(result["image_specs"])      # List of {section, placeholder} dicts
```

For **full state control**, invoke the graph directly:

```python
from graph.workflow import graph
from datetime import date

output = graph.invoke({
    "topic": "কৃত্রিম বুদ্ধিমত্তার ভবিষ্যৎ",  # Bangla topic
    "as_of": date.today().isoformat(),
    "recency_days": 14,
    # All other keys must be present (set to empty/None defaults)
    "language": "", "needs_research": False, "queries": [],
    "evidence": [], "research": "", "plan": None, "outline": "",
    "sections": [], "merged_md": "", "blog": "", "edited_blog": "",
    "image_specs": [], "md_with_placeholders": "",
    "seo": "", "final": "", "mode": "", "logs": [],
})
```

For **streaming** (receive each node's output as it completes):

```python
from graph.workflow import graph

inputs = {"topic": "...", "as_of": "2025-05-03", ...}  # full state dict

for update in graph.stream(inputs):
    node_name = list(update.keys())[0]      # e.g. "planner"
    node_output = update[node_name]          # dict of keys that node set

    print(f"✓ {node_name} completed")

    if node_name == "planner":
        print(f"  Title: {node_output['plan']['blog_title']}")
    elif node_name == "researcher":
        print(f"  Sources: {len(node_output['evidence'])}")
    elif node_name == "writer":
        words = len(node_output['blog'].split())
        print(f"  Draft words: {words}")
    elif node_name == "seo":
        print(f"  Final blog ready")
        print(node_output['final'])
```

---

## 18. Troubleshooting

**`AuthenticationError` or `GROQ_API_KEY not found`**
Ensure your `.env` file is in the **same directory** where you run `streamlit run app.py` (the project root), and that it contains `GROQ_API_KEY=gsk_...` with no extra spaces. Restart Streamlit after editing `.env`.

**"Graph failed to load" error in the sidebar**
An import error occurred at startup. Check your terminal for the full Python traceback. Common causes: missing dependency (`pip install -r requirements.txt`), virtual environment not activated, or a syntax error from manually editing an agent file.

**Blog generates but content is thin or cuts off mid-section**
The writer's `max_tokens=8192` setting in `models/llm.py` should prevent this. If you've lowered it, restore to 8192. Also check if Groq is returning rate-limit errors in the Logs tab — if so, add a short delay or upgrade your Groq plan.

**DuckDuckGo search errors / rate limiting**
DuckDuckGo aggressively rate-limits automated requests. Solutions in order of preference:
1. Add `TAVILY_API_KEY` to your `.env` — Tavily has no rate-limit issues
2. Reduce the number of queries by lowering the cap in `researcher.py → _build_query_set()` from 10 to 6
3. Add `import time; time.sleep(1)` between queries in `_run_queries()`

**Evidence tab shows 0 sources**
The search backend returned nothing or errored silently. Check the Logs tab for search error messages. This usually means DuckDuckGo rate-limiting (see above) or a network issue. With 0 evidence, the synthesis step produces a minimal brief and the blog quality drops significantly — adding Tavily is the reliable fix.

**Past blogs don't appear in the sidebar**
Blogs save to `saved_blogs/` in the **current working directory** when you run `streamlit run app.py`. Always run from the project root: `cd blog-writing-agent && streamlit run app.py`. Running from a different directory creates the `saved_blogs/` folder there instead.

**Bangla topic generates an English blog**
Your topic must contain actual Bangla Unicode characters (block `U+0980–U+09FF`). Latin transliteration like `"Bangla blog likhte chai"` reads as English. Use a Bangla keyboard input, or copy-paste Bangla text from any source.

**The editor produced a shorter blog than the writer**
The safety revert in `editor.py` catches cases where output drops below 60% of input word count and uses the original instead. If this fires frequently, it may indicate the editor is receiving too long a blog for its context window — check Groq's context limit for LLaMA 3.3 70B and reduce `max_tokens` in `llm` if needed.

**`json.JSONDecodeError` in planner logs**
The planner's LLM returned something that couldn't be parsed as JSON. The fallback plan activates automatically, so the pipeline continues. If this happens repeatedly, check your Groq account — low credit or throttling sometimes causes truncated responses.

---

## 19. Roadmap

| Feature | Description | Status |
|---|---|---|
| **Image generation** | Replace `IMAGE_PLACEHOLDER_*` tags with AI-generated images via Stability AI or DALL-E | Planned |
| **Streaming word output** | Display blog text token-by-token as the writer generates, rather than waiting per section | Planned |
| **Custom voice matching** | Upload sample blog posts; the writer matches tone, vocabulary, and style | Planned |
| **Section regeneration** | Regenerate a single weak section without rerunning the full pipeline | Planned |
| **Fact-check agent** | Seventh agent: verifies key claims against the evidence list and flags unverified assertions | Planned |
| **CMS direct publish** | One-click publish to Ghost, Hashnode, WordPress, or Dev.to via their APIs | Planned |
| **Multi-language expansion** | Add Hindi, Arabic, Spanish, French detection and full prompt sets | Planned |
| **Blog version history** | Keep multiple drafts per topic; visual diff between versions | Planned |
| **Docker image** | Containerised production deployment with environment management | Planned |
| **Batch mode** | Accept a CSV of topics, generate all blogs sequentially, export as zip | Planned |

---

## 20. Contributing

Contributions are welcome — bug fixes, new agents, quality improvements, or documentation updates.

**Getting started:**

```bash
git clone https://github.com/your-username/blog-writing-agent.git
cd blog-writing-agent
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your keys
```

**Guidelines:**

- Each agent file has a single responsibility — keep it that way. If you're adding behaviour that spans two agents, consider a new node.
- Keep the `BlogState` TypedDict updated whenever you add state keys. Every key an agent reads must be initialised in `main.py → run_agent()`.
- Test with at least two topics: one English, one Bangla. Both language paths must work.
- If you change prompt templates in `writer.py` or `planner.py`, run three full generations and compare word count, citation density, and section quality before and after.
- For bug reports: include your Python version, the full terminal traceback, and the topic that triggered the issue.

**Pull request checklist:**
- [ ] All Python files pass `python -m ast` syntax check
- [ ] `BlogState` updated if new state keys added
- [ ] `main.py → run_agent()` initialises any new state keys
- [ ] Both English and Bangla tested end-to-end
- [ ] `requirements.txt` updated if new packages added

---

<div align="center">

<br/>

**Md Atickur Rahman**\
Email: atickft13129@gmail.com\
Contact: 01849647396

<br/>

*Give this repo a ⭐ if it saved you time writing blogs.*

</div>

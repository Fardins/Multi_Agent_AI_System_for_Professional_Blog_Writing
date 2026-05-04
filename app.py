"""
Blog Writing Agent — Streamlit UI
"""
import json
import re
import io
import zipfile
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import streamlit as st

# ── Page config (MUST be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="Blog Writing Agent",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

/* ---- Root palette ---- */
:root {
    --bg: #0d0f14;
    --surface: #13161e;
    --card: #1a1e29;
    --border: #252a38;
    --accent: #f5c542;
    --accent2: #e8734a;
    --text: #e8eaf2;
    --muted: #7a8099;
    --green: #4caf7d;
    --red: #e05c5c;
}

/* ---- Base reset ---- */
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

/* ---- Typography ---- */
h1, h2, h3 { font-family: 'Playfair Display', Georgia, serif !important; }
h1 { font-size: 2.4rem !important; font-weight: 900 !important;
     background: linear-gradient(135deg, var(--accent), var(--accent2));
     -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
h2 { font-size: 1.5rem !important; color: var(--text) !important; }
h3 { font-size: 1.1rem !important; color: var(--accent) !important; }
code, pre { font-family: 'JetBrains Mono', monospace !important; }

/* ---- Sidebar inputs ---- */
[data-testid="stTextArea"] textarea {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(245,197,66,0.15) !important;
}
[data-testid="stDateInput"] input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* ---- Buttons ---- */
[data-testid="stButton"] > button {
    width: 100%;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.2rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0d0f14 !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(245,197,66,0.3) !important;
}
[data-testid="stButton"] > button[kind="secondary"] {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
}

/* ---- Tabs ---- */
[data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--card) !important;
    color: var(--accent) !important;
}

/* ---- Dataframe ---- */
[data-testid="stDataFrame"] {
    background: var(--card) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ---- Status & info boxes ---- */
[data-testid="stAlert"] {
    background: var(--card) !important;
    border-radius: 10px !important;
    border-left: 3px solid var(--accent) !important;
}
[data-testid="stStatusWidget"] {
    background: var(--card) !important;
    border-radius: 10px !important;
}

/* ---- Expander ---- */
[data-testid="stExpander"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ---- Download button ---- */
[data-testid="stDownloadButton"] > button {
    background: var(--card) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: rgba(245,197,66,0.1) !important;
}

/* ---- Radio ---- */
[data-testid="stRadio"] label {
    color: var(--text) !important;
    font-size: 0.85rem !important;
}

/* ---- Markdown preview area ---- */
.blog-preview {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 2.5rem 3rem;
    line-height: 1.9;
    max-width: 820px;
    margin: 0 auto;
}
.blog-preview h1 { font-size: 2rem !important; }
.blog-preview h2 { font-size: 1.4rem !important; margin-top: 2rem !important; }
.blog-preview blockquote {
    border-left: 3px solid var(--accent);
    padding-left: 1rem;
    color: var(--muted);
    font-style: italic;
}

/* ---- Stats row ---- */
.stat-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
    display: block;
}
.stat-label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ---- SEO card ---- */
.seo-field { margin-bottom: 0.8rem; }
.seo-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--muted);
    font-weight: 600;
}
.seo-value {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.5rem 0.8rem;
    font-size: 0.9rem;
    margin-top: 0.25rem;
    word-break: break-all;
}

/* ---- Evidence card ---- */
.ev-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}
.ev-card:hover { border-color: var(--accent); }
.ev-title { font-weight: 600; font-size: 0.95rem; margin-bottom: 0.3rem; }
.ev-source { font-size: 0.78rem; color: var(--accent); margin-bottom: 0.4rem; }
.ev-snippet { font-size: 0.85rem; color: var(--muted); line-height: 1.6; }

/* ---- Log terminal ---- */
.log-terminal {
    background: #080a0f;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #7ec87e;
    line-height: 1.7;
    max-height: 450px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
}

/* ---- Divider ---- */
hr { border-color: var(--border) !important; }

/* ---- Sidebar header text ---- */
.sidebar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent);
    margin-bottom: 0.2rem;
}
.sidebar-sub {
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 1.2rem;
}

/* ---- Pipeline progress ---- */
.pipe-step {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.35rem 0;
    font-size: 0.85rem;
    color: var(--muted);
}
.pipe-step.done { color: var(--green); }
.pipe-step.active { color: var(--accent); font-weight: 600; }
.pipe-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--border);
    flex-shrink: 0;
}
.pipe-step.done .pipe-dot { background: var(--green); }
.pipe-step.active .pipe-dot { background: var(--accent);
    box-shadow: 0 0 6px var(--accent); animation: pulse 1s infinite; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}
</style>
""", unsafe_allow_html=True)

# ── Import graph (inside try so Streamlit can still render on import errors) ──
try:
    from main import app
    GRAPH_LOADED = True
except Exception as e:
    GRAPH_LOADED = False
    GRAPH_ERROR = str(e)


# ── Helpers ────────────────────────────────────────────────────────────────

BLOGS_DIR = Path("saved_blogs")
BLOGS_DIR.mkdir(exist_ok=True)


def list_saved_blogs() -> List[Path]:
    """Return .md files from saved_blogs/ newest first."""
    return sorted(BLOGS_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)


def save_blog(state: dict) -> Path:
    """Persist final blog markdown + metadata JSON. Returns the saved .md path."""
    final_md = state.get("final") or state.get("edited_blog") or state.get("blog") or ""
    if not final_md.strip():
        return None

    plan = state.get("plan") or {}
    blog_title = (
        plan.get("blog_title") if isinstance(plan, dict) else None
    ) or extract_title(final_md, state.get("topic", "blog"))

    slug = safe_slug(blog_title)
    # Add timestamp suffix to avoid collisions between different topics
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = BLOGS_DIR / f"{slug}_{ts}.md"
    md_path.write_text(final_md, encoding="utf-8")

    # Save metadata sidecar
    meta = {
        "title": blog_title,
        "topic": state.get("topic", ""),
        "language": state.get("language", "en"),
        "word_count": word_count(final_md),
        "saved_at": ts,
        "seo": state.get("seo", "{}"),
        "evidence_count": len(state.get("evidence") or []),
    }
    meta_path = md_path.with_suffix(".json")
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return md_path


def load_blog_meta(md_path: Path) -> dict:
    """Load sidecar metadata if available."""
    meta_path = md_path.with_suffix(".json")
    if meta_path.exists():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def read_md(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def safe_slug(text: str) -> str:
    return re.sub(r"[^\w\-]", "_", text).strip("_")[:60]


def word_count(text: str) -> int:
    return len(text.split())


def reading_time(text: str) -> int:
    return max(1, round(word_count(text) / 200))


def bundle_zip(md_text: str, md_filename: str, images_dir: Path) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(md_filename, md_text)
        if images_dir.exists():
            for img in images_dir.iterdir():
                if img.is_file():
                    zf.write(img, f"images/{img.name}")
    buf.seek(0)
    return buf.read()


def extract_seo(out: dict) -> dict:
    raw = out.get("seo", "{}")
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            return {}
    if isinstance(raw, dict):
        return raw
    return {}


def try_stream(inputs: dict):
    """Yield (node_name, state_snapshot) tuples, then ("__final__", full_state)."""
    full_state: Dict[str, Any] = dict(inputs)
    try:
        for update in app.stream(inputs):
            if isinstance(update, dict):
                for node_name, node_output in update.items():
                    if isinstance(node_output, dict):
                        full_state.update(node_output)
                    yield node_name, full_state
        yield "__final__", full_state
    except Exception as e:
        yield "__error__", {"error": str(e)}


def format_log_entry(entry: Any) -> str:
    if isinstance(entry, str):
        return entry
    try:
        return json.dumps(entry, indent=2, default=str)
    except Exception:
        return str(entry)


# ── Session state initialisation ───────────────────────────────────────────
if "last_out" not in st.session_state:
    st.session_state["last_out"] = None
if "run_logs" not in st.session_state:
    st.session_state["run_logs"] = []
if "pipeline_steps" not in st.session_state:
    st.session_state["pipeline_steps"] = []


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Blog Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-sub">Powered by LangGraph + Groq</div>', unsafe_allow_html=True)

    # ---- New blog form ----
    topic = st.text_area(
        "Blog Topic",
        placeholder="e.g. How LLMs are transforming software development in 2025\nor বাংলায় কৃত্রিম বুদ্ধিমত্তার ভবিষ্যৎ",
        height=130,
        key="topic_input",
    )
    col_a, col_b = st.columns(2)
    with col_a:
        as_of = st.date_input("As of", value=date.today(), label_visibility="visible")
    with col_b:
        recency = st.number_input("Recency (days)", min_value=1, max_value=90, value=7)

    run_btn = st.button("Generate Blog", type="primary", use_container_width=True)

    if not GRAPH_LOADED:
        st.error(f"Graph failed to load:\n{GRAPH_ERROR}")

    st.divider()

    # ---- Past blogs ----
    st.markdown("**Past Blogs**")
    past = list_saved_blogs()
    if not past:
        st.caption("No saved blogs yet. Generate your first blog above!")
    else:
        labels = {}
        for p in past[:30]:
            meta = load_blog_meta(p)
            title = meta.get("title") or extract_title(read_md(p), p.stem)
            wc = meta.get("word_count", "")
            wc_str = f" · {wc}w" if wc else ""
            label = f"{title[:35]}{'…' if len(title)>35 else ''}{wc_str}"
            labels[label] = p

        sel = st.radio("", list(labels.keys()), label_visibility="collapsed")

        col_load, col_del = st.columns([3, 1])
        with col_load:
            if st.button("Load", use_container_width=True):
                p = labels[sel]
                txt = read_md(p)
                meta = load_blog_meta(p)
                seo_raw = meta.get("seo", "{}")
                st.session_state["last_out"] = {
                    "plan": {"blog_title": meta.get("title", ""), "tasks": []},
                    "evidence": [],
                    "image_specs": [],
                    "seo": seo_raw,
                    "final": txt,
                    "topic": meta.get("topic", ""),
                    "language": meta.get("language", "en"),
                }
                st.session_state["run_logs"] = [f"Loaded: {p.name}"]
                st.rerun()
        with col_del:
            if st.button("🗑️", use_container_width=True, help="Delete this blog"):
                p = labels[sel]
                p.unlink(missing_ok=True)
                p.with_suffix(".json").unlink(missing_ok=True)
                st.rerun()

    

# ── Main header ────────────────────────────────────────────────────────────
st.markdown("# Blog Writing Agent")
st.markdown('<p style="color:var(--muted); margin-top:-0.8rem; margin-bottom:1.5rem;">Multi-agent pipeline: Language → Plan → Research → Write → Edit → SEO</p>', unsafe_allow_html=True)


# ── RUN ────────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a topic first.")
        st.stop()
    if not GRAPH_LOADED:
        st.error("Cannot run — graph failed to import.")
        st.stop()

    st.session_state["run_logs"] = []
    st.session_state["pipeline_steps"] = []

    PIPELINE_ORDER = ["detect_language", "planner", "researcher", "writer", "editor", "seo"]
    PIPELINE_LABELS = {
        "detect_language": "Detect Language",
        "planner":         "Plan Structure",
        "researcher":      "Research Web",
        "writer":          "Write Blog",
        "editor":          "Edit & Polish",
        "seo":             "Generate SEO",
    }

    inputs = {
        "topic": topic.strip(),
        "as_of": as_of.isoformat(),
        "recency_days": int(recency),
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
    }

    # Progress UI
    progress_col, info_col = st.columns([2, 3])

    with progress_col:
        st.markdown("**Pipeline Progress**")
        step_placeholders = {k: st.empty() for k in PIPELINE_ORDER}

        def render_steps(current: str, done: List[str]):
            for key in PIPELINE_ORDER:
                ph = step_placeholders[key]
                if key in done:
                    cls = "done"; icon = "✓"
                elif key == current:
                    cls = "active"; icon = "⏳"
                else:
                    cls = ""; icon = "○"
                ph.markdown(
                    f'<div class="pipe-step {cls}">'
                    f'<span class="pipe-dot"></span>'
                    f'{icon} {PIPELINE_LABELS[key]}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        render_steps("", [])

    with info_col:
        st.markdown("**Live State**")
        live_json = st.empty()

    status = st.status("Running pipeline…", expanded=True)
    log_lines: List[str] = []
    done_steps: List[str] = []
    final_state: Dict[str, Any] = {}

    for node_name, state in try_stream(inputs):
        if node_name == "__error__":
            st.error(f"Pipeline error: {state.get('error')}")
            log_lines.append(f"ERROR: {state.get('error')}")
            break

        if node_name == "__final__":
            final_state = state
            st.session_state["last_out"] = state
            # ── AUTO-SAVE ──────────────────────────────────────────────────
            try:
                saved_path = save_blog(state)
                if saved_path:
                    status.update(label=f"Blog generated & saved → {saved_path.name}", state="complete", expanded=False)
                    log_lines.append(f"[saved] {saved_path}")
                else:
                    status.update(label="Blog generated!", state="complete", expanded=False)
            except Exception as save_err:
                status.update(label="Blog generated (save failed)", state="complete", expanded=False)
                log_lines.append(f"[save error] {save_err}")
            log_lines.append("[__final__] Pipeline complete")
            break

        done_steps.append(node_name)
        render_steps(node_name, done_steps[:-1])
        status.write(f"➡️  **{PIPELINE_LABELS.get(node_name, node_name)}**")

        # Live summary
        summary = {
            "language": state.get("language"),
            "needs_research": state.get("needs_research"),
            "queries": (state.get("queries") or [])[:3],
            "evidence_sources": len(state.get("evidence") or []),
            "plan_sections": len((state.get("plan") or {}).get("tasks", [])),
            "blog_words": word_count(state.get("blog") or ""),
            "edited_words": word_count(state.get("edited_blog") or ""),
        }
        live_json.json(summary)
        log_lines.append(f"[{node_name}] done — blog words: {summary['blog_words']}")

    st.session_state["run_logs"].extend(log_lines)
    # Render all steps done
    render_steps("", list(PIPELINE_ORDER))


# ── Render output ──────────────────────────────────────────────────────────
out = st.session_state.get("last_out")

if out:
    final_md = out.get("final") or out.get("edited_blog") or out.get("blog") or ""
    plan = out.get("plan") or {}
    evidence = out.get("evidence") or []
    image_specs = out.get("image_specs") or []
    seo_data = extract_seo(out)

    blog_title = (
        plan.get("blog_title")
        or extract_title(final_md, "blog")
        if isinstance(plan, dict) else extract_title(final_md, "blog")
    )
    wc = word_count(final_md)
    rt = reading_time(final_md)

    # ── Stats row ──────────────────────────────────────────────────────────
    s1, s2, s3, s4, s5 = st.columns(5)
    stats = [
        (wc, "Words"),
        (rt, "Min read"),
        (len(evidence), "Sources"),
        (len(image_specs), "Images"),
        (len((plan.get("tasks") or []) if isinstance(plan, dict) else []), "Sections"),
    ]
    for col, (num, label) in zip([s1, s2, s3, s4, s5], stats):
        col.markdown(
            f'<div class="stat-card"><span class="stat-num">{num}</span>'
            f'<span class="stat-label">{label}</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────────────────────────────────────
    tab_preview, tab_plan, tab_evidence, tab_seo, tab_images, tab_logs = st.tabs([
        "📝 Preview", "🗺️ Plan", "🔎 Evidence", "🏷️ SEO", "🖼️ Images", "🧾 Logs"
    ])

    # ─────────────────────────────────────────────────────────────────────
    # TAB: PREVIEW
    # ─────────────────────────────────────────────────────────────────────
    with tab_preview:
        c_left, c_right = st.columns([3, 1])
        with c_left:
            st.markdown("### Blog Preview")

        with c_right:
            md_fn = f"{safe_slug(blog_title)}.md"
            st.download_button(
                "⬇️ Download Blog (MD)",
                data=final_md.encode("utf-8"),
                file_name=md_fn,
                mime="text/markdown",
            )

        # Strip SEO comment block for clean preview
        preview_md = re.sub(r"<!--.*?-->", "", final_md, flags=re.DOTALL).strip()

        st.markdown('<div class="blog-preview">', unsafe_allow_html=True)
        st.markdown(preview_md)
        st.markdown("</div>", unsafe_allow_html=True)

        # Bundle download
        st.markdown("<br>", unsafe_allow_html=True)
        bundle = bundle_zip(final_md, md_fn, Path("images"))
        st.download_button(
            "Download Bundle (Blog + images)",
            data=bundle,
            file_name=f"{safe_slug(blog_title)}_bundle.zip",
            mime="application/zip",
        )

    # ─────────────────────────────────────────────────────────────────────
    # TAB: PLAN
    # ─────────────────────────────────────────────────────────────────────
    with tab_plan:
        if not plan or not isinstance(plan, dict):
            st.info("No plan available (loaded from saved file, or generation didn't produce a plan).")
        else:
            st.markdown(f"### {plan.get('blog_title', 'Untitled')}")
            m1, m2, m3 = st.columns(3)
            m1.markdown(f"**Audience**\n\n{plan.get('audience', '—')}")
            m2.markdown(f"**Tone**\n\n{plan.get('tone', '—')}")
            m3.markdown(f"**Type**\n\n{plan.get('blog_kind', '—')}")

            tasks = plan.get("tasks", [])
            if tasks:
                st.markdown("#### Sections")
                rows = []
                for t in sorted(tasks, key=lambda x: x.get("id", 0)):
                    rows.append({
                        "#": t.get("id"),
                        "Title": t.get("title", ""),
                        "Words": t.get("target_words", ""),
                        "Research": "✓" if t.get("requires_research") else "",
                        "Citations": "✓" if t.get("requires_citations") else "",
                        "Code": "✓" if t.get("requires_code") else "",
                        "Tags": ", ".join(t.get("tags") or []),
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            with st.expander("Raw plan JSON"):
                st.json(plan)

    # ─────────────────────────────────────────────────────────────────────
    # TAB: EVIDENCE
    # ─────────────────────────────────────────────────────────────────────
    with tab_evidence:
        if not evidence:
            st.info("No research evidence for this blog (closed-book mode or no search results).")
        else:
            st.markdown(f"### {len(evidence)} Sources Found")
            for i, e in enumerate(evidence, 1):
                if isinstance(e, str):
                    try:
                        e = json.loads(e)
                    except Exception:
                        st.markdown(
                            f'<div class="ev-card">'
                            f'<div class="ev-title">Source {i}</div>'
                            f'<div class="ev-snippet">{e[:300]}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                        continue

                title_ev = e.get("title", f"Source {i}")
                source = e.get("source", "") or e.get("url", "")
                snippet = e.get("snippet", "")[:350]
                url = e.get("url", "")
                pub = e.get("published_at", "")

                url_html = f'<a href="{url}" target="_blank" style="color:var(--accent);font-size:0.78rem">{url[:60]}…</a>' if url else ""
                pub_html = f'<span style="color:var(--muted);font-size:0.75rem"> · {pub}</span>' if pub else ""

                st.markdown(
                    f'<div class="ev-card">'
                    f'<div class="ev-title">{i}. {title_ev}</div>'
                    f'<div class="ev-source">{source}{pub_html}</div>'
                    f'{url_html}'
                    f'<div class="ev-snippet">{snippet}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            # Also show as table
            with st.expander("View as table"):
                rows = []
                for e in evidence:
                    if isinstance(e, str):
                        rows.append({"Title": e[:80], "Source": "", "URL": ""})
                    elif isinstance(e, dict):
                        rows.append({
                            "Title": e.get("title", "")[:80],
                            "Source": e.get("source", ""),
                            "URL": e.get("url", ""),
                            "Published": e.get("published_at", ""),
                        })
                if rows:
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    # ─────────────────────────────────────────────────────────────────────
    # TAB: SEO
    # ─────────────────────────────────────────────────────────────────────
    with tab_seo:
        if not seo_data:
            st.info("No SEO data available.")
        else:
            st.markdown("### SEO Metadata")

            fields = [
                ("Meta Title", seo_data.get("meta_title", "")),
                ("Meta Description", seo_data.get("meta_description", "")),
                ("URL Slug", f"/{seo_data.get('slug', '')}"),
                ("Reading Time", f"{seo_data.get('reading_time_minutes', rt)} minutes"),
            ]
            if seo_data.get("social_snippet"):
                fields.append(("Social Snippet", seo_data["social_snippet"]))

            for label, value in fields:
                st.markdown(
                    f'<div class="seo-field">'
                    f'<div class="seo-label">{label}</div>'
                    f'<div class="seo-value">{value}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            keywords = seo_data.get("keywords", [])
            if keywords:
                st.markdown('<div class="seo-label">Keywords</div>', unsafe_allow_html=True)
                kw_html = " ".join(
                    f'<span style="background:var(--card);border:1px solid var(--border);'
                    f'border-radius:20px;padding:0.2rem 0.7rem;font-size:0.82rem;margin:0.15rem;'
                    f'display:inline-block;color:var(--accent)">{kw}</span>'
                    for kw in keywords
                )
                st.markdown(kw_html, unsafe_allow_html=True)

            # Character counters
            st.markdown("<br>", unsafe_allow_html=True)
            title_len = len(seo_data.get("meta_title", ""))
            desc_len = len(seo_data.get("meta_description", ""))
            c1, c2 = st.columns(2)
            c1.metric("Title length", f"{title_len}/60 chars",
                      delta="✓ Good" if title_len <= 60 else "Too long",
                      delta_color="normal" if title_len <= 60 else "inverse")
            c2.metric("Description length", f"{desc_len}/155 chars",
                      delta="✓ Good" if desc_len <= 155 else "Too long",
                      delta_color="normal" if desc_len <= 155 else "inverse")

            with st.expander("Raw SEO JSON"):
                st.json(seo_data)

    # ─────────────────────────────────────────────────────────────────────
    # TAB: IMAGES
    # ─────────────────────────────────────────────────────────────────────
    with tab_images:
        images_dir = Path("images")
        if image_specs:
            st.markdown("### Image Plan")
            st.markdown("These placeholders were identified in the blog. Replace them with real images:")
            for spec in image_specs:
                section = spec.get("section", "")
                placeholder = spec.get("placeholder", "")
                st.markdown(
                    f'<div class="ev-card">'
                    f'<div class="ev-title">📷 {section.replace("_", " ").title()}</div>'
                    f'<div class="ev-snippet">Placeholder: <code>{placeholder}</code></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        if images_dir.exists():
            files = [p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}]
            if files:
                st.markdown("### Saved Images")
                cols = st.columns(min(3, len(files)))
                for i, p in enumerate(sorted(files)):
                    with cols[i % 3]:
                        st.image(str(p), caption=p.name, use_container_width=True)

                buf = io.BytesIO()
                with zipfile.ZipFile(buf, "w") as zf:
                    for p in files:
                        zf.write(p, p.name)
                buf.seek(0)
                st.download_button("⬇️ Download all images (.zip)", data=buf.read(),
                                   file_name="blog_images.zip", mime="application/zip")
            else:
                st.info("images/ folder exists but contains no image files.")
        else:
            if not image_specs:
                st.info("No images for this blog. Image placeholders will appear here when the writer includes them.")

    # ─────────────────────────────────────────────────────────────────────
    # TAB: LOGS
    # ─────────────────────────────────────────────────────────────────────
    with tab_logs:
        st.markdown("### Pipeline Logs")
        all_logs = st.session_state.get("run_logs", [])
        if not all_logs:
            st.info("No logs yet. Run the agent to see pipeline activity.")
        else:
            log_text = "\n".join(format_log_entry(l) for l in all_logs[-120:])
            st.markdown(f'<div class="log-terminal">{log_text}</div>', unsafe_allow_html=True)

            if st.button("🗑️ Clear logs"):
                st.session_state["run_logs"] = []
                st.rerun()

else:
    # ── Landing state ──────────────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center; padding:4rem 2rem; max-width:600px; margin:0 auto">
    <div style="font-size:3rem; margin-bottom:1rem">✍️</div>
    <h2 style="color:var(--text); font-family:'Playfair Display',serif">Ready to write</h2>
    <p style="color:var(--muted); line-height:1.8">
        Enter a topic in the sidebar and click <strong style="color:var(--accent)">Generate Blog</strong>.
        The multi-agent pipeline will detect your language, research the web,
        write a structured blog, polish it, and add SEO metadata — all automatically.
    </p>
    <div style="margin-top:2rem; display:flex; justify-content:center; gap:1rem; flex-wrap:wrap">
        <span style="background:var(--card);border:1px solid var(--border);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.82rem">🌐 Supports English & বাংলা</span>
        <span style="background:var(--card);border:1px solid var(--border);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.82rem">🔎 Web Research</span>
        <span style="background:var(--card);border:1px solid var(--border);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.82rem">🏷️ Auto SEO</span>
        <span style="background:var(--card);border:1px solid var(--border);border-radius:20px;padding:0.3rem 0.9rem;font-size:0.82rem">📦 Download Bundle</span>
    </div>
</div>
""", unsafe_allow_html=True)
"""
Editor agent — two-pass quality review:
Pass 1: Line-by-line polish (sentences, transitions, rhythm)
Pass 2: Opening & closing punch (the two most important moments)
"""
from models.llm import llm


def editor(state: dict) -> dict:
    blog = state.get("blog", "")
    lang = state.get("language", "en")
    plan = state.get("plan") or {}
    tone = plan.get("tone", "authoritative yet conversational")
    hook_angle = plan.get("hook_angle", "")
    title = plan.get("blog_title", "")

    if not blog.strip():
        return {"edited_blog": blog}

    # Only edit if blog has substance
    if len(blog.split()) < 100:
        return {"edited_blog": blog}

    if lang == "bn":
        edited = _edit_bangla(blog, tone)
    else:
        edited = _edit_english(blog, tone, hook_angle, title)

    # Safety: revert if edit drastically shortened the blog
    if len(edited.split()) < len(blog.split()) * 0.6:
        edited = blog

    return {"edited_blog": edited}


def _edit_english(blog: str, tone: str, hook_angle: str, title: str) -> str:
    prompt = f"""You are the executive editor of a prestigious publication. You've edited hundreds of viral articles. You have one job: make this blog post undeniably excellent.

Blog title: {title}
Intended angle: {hook_angle}
Target tone: {tone}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR EDITING MANDATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Go through the blog systematically. For each issue you find, fix it in-place.

PRIORITY 1 — THE HOOK (first 3 paragraphs):
If the opening doesn't immediately grab with a specific stat, vivid story, or bold claim — rewrite it entirely.
The reader must be unable to stop reading after the first sentence.

PRIORITY 2 — DEAD WEIGHT:
Find and delete every sentence that could be removed without losing meaning.
Typical dead weight: restatements of the heading, throat-clearing, "let's explore...", "in this section..."

PRIORITY 3 — VAGUE TO SPECIFIC:
Every remaining vague quantifier gets replaced with something from the research context or a precise statement:
  ✗ "many companies" → ✓ "companies like X and Y" or "74% of surveyed companies"
  ✗ "significantly" → ✓ "by 3.4x" or "from 12% to 41%"

PRIORITY 4 — WEAK VERBS:
Replace passive and weak constructions:
  ✗ "it was found that" → ✓ "[Researcher] found"
  ✗ "can be used to" → ✓ "lets you" or "enables"
  ✗ "there are many ways" → ✓ "three approaches stand out"

PRIORITY 5 — RHYTHM:
Every paragraph of 5+ sentences: find the weakest sentence and cut or fold it in.
After every dense paragraph: add a 1-sentence punchy takeaway if missing.

PRIORITY 6 — THE CONCLUSION:
The last 2 paragraphs must close with power.
If the final sentence is weak — rewrite it until it's quotable.
The reader should close this blog thinking "I need to send this to someone."

PRIORITY 7 — BLOCKQUOTES:
Each `> **Key insight:**` line should contain the single sharpest idea in its section.
If any blockquote is generic or weak — sharpen it.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HARD CONSTRAINTS — violations are not acceptable
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✗ Do NOT remove any `IMAGE_PLACEHOLDER_...` tags
✗ Do NOT remove any `## ` or `### ` headings
✗ Do NOT remove any citation links or source references
✗ Do NOT truncate the blog — final version must be at least 90% of the original length
✗ Do NOT add a preamble like "Here is the edited version:"
✗ Do NOT add new sections that weren't in the original
✓ Start directly with `# {title}`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOG TO EDIT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{blog}
"""
    response = llm.invoke(prompt)
    return response.content.strip()


def _edit_bangla(blog: str, tone: str) -> str:
    prompt = f"""আপনি একটি শীর্ষ বাংলা প্রকাশনার সম্পাদক। আপনার কাজ: এই ব্লগটিকে অসাধারণ করে তোলা।

লক্ষ্য স্বর: {tone}

━━━━━━━━━━━━━━━━━━━━━━
সম্পাদনার অগ্রাধিকার
━━━━━━━━━━━━━━━━━━━━━━

অগ্রাধিকার ১ — হুক (প্রথম ৩ অনুচ্ছেদ):
যদি শুরুটা তাৎক্ষণিকভাবে আকৃষ্ট না করে — সম্পূর্ণ পুনর্লিখন করুন।

অগ্রাধিকার ২ — মৃত অংশ সরান:
অর্থ না হারিয়ে মুছে ফেলা যায় এমন প্রতিটি বাক্য খুঁজে মুছুন।

অগ্রাধিকার ৩ — অস্পষ্ট থেকে নির্দিষ্টে:
প্রতিটি অস্পষ্ট পরিমাপক নির্দিষ্ট সংখ্যা বা নামে প্রতিস্থাপন করুন।

অগ্রাধিকার ৪ — দুর্বল ক্রিয়া:
নিষ্ক্রিয় (passive) এবং দুর্বল গঠন সক্রিয় করুন।

অগ্রাধিকার ৫ — ছন্দ:
দীর্ঘ অনুচ্ছেদের পরে ছোট শক্তিশালী বাক্য যোগ করুন।

অগ্রাধিকার ৬ — উপসংহার:
শেষ বাক্যটি উদ্ধৃতিযোগ্য করুন।

━━━━━━━━━━━━━━━━━━━━━━
বাধ্যতামূলক সীমাবদ্ধতা
━━━━━━━━━━━━━━━━━━━━━━
✗ IMAGE_PLACEHOLDER_... ট্যাগ সরাবেন না
✗ ## বা ### হেডিং সরাবেন না
✗ উৎস লিঙ্ক সরাবেন না
✗ ব্লগ ছোট করবেন না (কমপক্ষে মূলের ৯০%)
✗ "এখানে সম্পাদিত সংস্করণ:" জাতীয় প্রিঅ্যাম্বল যোগ করবেন না
✓ সরাসরি # শিরোনাম দিয়ে শুরু করুন

━━━━━━━━━━━━━━━━━━━━━━
সম্পাদনার জন্য ব্লগ:
━━━━━━━━━━━━━━━━━━━━━━
{blog}
"""
    response = llm.invoke(prompt)
    return response.content.strip()
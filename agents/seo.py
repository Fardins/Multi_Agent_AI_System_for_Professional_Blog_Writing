from models.llm import llm
import json
import re


def seo_agent(state: dict) -> dict:
    blog = state.get("edited_blog") or state.get("blog", "")
    lang = state.get("language", "en")
    plan = state.get("plan") or {}
    title = plan.get("blog_title", state.get("topic", ""))

    if not blog.strip():
        return {"seo": "{}", "final": blog}

    if lang == "bn":
        seo_prompt = f"""এই ব্লগের জন্য SEO মেটাডেটা তৈরি করুন (JSON ফরম্যাটে):
শিরোনাম: {title}

শুধুমাত্র JSON ফেরত দিন:
{{
  "meta_title": "SEO শিরোনাম (60 অক্ষর পর্যন্ত)",
  "meta_description": "Meta description (155 অক্ষর পর্যন্ত)",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "slug": "url-slug-here",
  "reading_time_minutes": 5
}}"""
    else:
        seo_prompt = f"""Generate SEO metadata for this blog post. Return ONLY valid JSON:

Blog title: {title}

{{
  "meta_title": "SEO title (max 60 chars)",
  "meta_description": "Meta description (max 155 chars, compelling & keyword-rich)",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "slug": "url-friendly-slug",
  "reading_time_minutes": 5,
  "social_snippet": "One punchy sentence for sharing on social media"
}}"""

    seo_response = llm.invoke(seo_prompt)
    seo_raw = seo_response.content.strip()
    seo_raw = re.sub(r"^```(?:json)?\s*", "", seo_raw)
    seo_raw = re.sub(r"\s*```$", "", seo_raw)

    try:
        seo_data = json.loads(seo_raw)
    except Exception:
        seo_data = {"meta_title": title, "meta_description": "", "keywords": [], "slug": ""}

    # Append SEO block at the bottom of the markdown
    seo_block = _build_seo_block(seo_data, lang)
    final_md = blog.rstrip() + "\n\n---\n" + seo_block

    return {
        "seo": json.dumps(seo_data, ensure_ascii=False, indent=2),
        "final": final_md,
    }


def _build_seo_block(seo: dict, lang: str) -> str:
    if lang == "bn":
        return f"""<!-- SEO Metadata
Meta Title: {seo.get('meta_title', '')}
Meta Description: {seo.get('meta_description', '')}
Keywords: {', '.join(seo.get('keywords', []))}
Slug: {seo.get('slug', '')}
-->"""
    else:
        lines = [
            "<!-- SEO Metadata",
            f"Meta Title: {seo.get('meta_title', '')}",
            f"Meta Description: {seo.get('meta_description', '')}",
            f"Keywords: {', '.join(seo.get('keywords', []))}",
            f"Slug: /{seo.get('slug', '')}",
            f"Reading Time: {seo.get('reading_time_minutes', '?')} min",
        ]
        if seo.get("social_snippet"):
            lines.append(f"Social: {seo['social_snippet']}")
        lines.append("-->")
        return "\n".join(lines)
"""
Writer agent — writes each section individually with full synthesized research context.
Each section gets its own focused prompt so no token budget competition.
"""
import re
from models.llm import llm


def writer(state: dict) -> dict:
    topic = state["topic"]
    research = state.get("research", "")   # this is now the SYNTHESIZED brief
    lang = state.get("language", "en")
    plan = state.get("plan") or {}

    title = plan.get("blog_title", topic)
    audience = plan.get("audience", "curious, intelligent readers")
    tone = plan.get("tone", "authoritative yet conversational")
    blog_kind = plan.get("blog_kind", "deep-dive")
    hook_angle = plan.get("hook_angle", "")
    tasks = plan.get("tasks") or _default_tasks(topic)

    # Write each section individually with its own focused prompt
    written_sections = []
    for i, task in enumerate(tasks):
        is_first = i == 0
        is_last = i == len(tasks) - 1
        prev_section = written_sections[-1] if written_sections else ""

        section_md = _write_section(
            task=task,
            topic=topic,
            title=title,
            audience=audience,
            tone=tone,
            blog_kind=blog_kind,
            hook_angle=hook_angle,
            research=research,
            lang=lang,
            all_tasks=tasks,
            is_first=is_first,
            is_last=is_last,
            prev_section_tail=prev_section[-600:] if prev_section else "",
        )
        written_sections.append(section_md)

    # Assemble full blog
    blog_content = f"# {title}\n\n" + "\n\n---\n\n".join(written_sections)

    # Clean up any LLM preamble before the title
    blog_content = re.sub(r"^[^#\n]{0,400}\n+(?=#)", "", blog_content).strip()

    placeholders = re.findall(r"IMAGE_PLACEHOLDER_(\w+)", blog_content)
    image_specs = [{"section": p, "placeholder": f"IMAGE_PLACEHOLDER_{p}"} for p in placeholders]

    return {
        "blog": blog_content,
        "sections": written_sections,
        "merged_md": blog_content,
        "image_specs": image_specs,
        "md_with_placeholders": blog_content,
    }


def _write_section(task, topic, title, audience, tone, blog_kind, hook_angle,
                   research, lang, all_tasks, is_first, is_last, prev_section_tail):
    section_title = task.get("title", "Section")
    target_words = task.get("target_words", 400)
    needs_citations = task.get("requires_citations", False)
    needs_code = task.get("requires_code", False)
    writing_brief = task.get("writing_brief", "")

    blog_structure = " → ".join(f'"{t["title"]}"' for t in all_tasks)

    if lang == "bn":
        prompt = _bangla_prompt(
            section_title, target_words, topic, title, audience, tone,
            hook_angle, research, is_first, is_last, blog_structure,
            needs_citations, writing_brief, prev_section_tail
        )
    else:
        prompt = _english_prompt(
            section_title, target_words, topic, title, audience, tone,
            blog_kind, hook_angle, research, is_first, is_last, blog_structure,
            needs_citations, needs_code, writing_brief, prev_section_tail
        )

    response = llm.invoke(prompt)
    content = response.content.strip()

    # Strip any LLM preamble before the ## heading
    content = re.sub(r"^(?:[^#\n][^\n]*\n)+(?=##\s)", "", content).strip()
    content = re.sub(r"^(?:Here is|Here's|Below is|Section:|Writing:)[^\n]*\n+", "", content, flags=re.IGNORECASE).strip()

    # Ensure section starts with ## heading
    if not re.match(r"^#{1,3}\s", content):
        content = f"## {section_title}\n\n{content}"

    return content


def _english_prompt(section_title, target_words, topic, title, audience, tone,
                    blog_kind, hook_angle, research, is_first, is_last,
                    blog_structure, needs_citations, needs_code, writing_brief, prev_tail):

    # ── Role instruction based on position ──────────────────────────────
    if is_first:
        role_block = f"""
╔══════════════════════════════════════════╗
║  YOUR ROLE: OPENING SECTION              ║
╚══════════════════════════════════════════╝
This is the most important section. You have ONE chance to hook the reader.
The blog's central angle is: "{hook_angle}"

OPENING STRATEGIES — use the one most powerful for THIS specific topic:
  A) Jaw-dropping specific stat that reframes everything ("In 2024, X happened to Y% of...")
  B) A 3-sentence vivid micro-story that puts the reader inside a real scenario
  C) A direct bold claim that challenges what the reader thinks they know
  D) A question so specific and surprising that the reader cannot look away

After the hook:
- Build context naturally, weave in 1-2 supporting facts from research
- Establish WHY this topic matters to THIS specific audience
- End with a "promise sentence": what the reader will know/be able to do after reading

FORBIDDEN openers: "In today's world", "Have you ever wondered", "Welcome", "In this article", "As technology evolves"
"""
    elif is_last:
        role_block = f"""
╔══════════════════════════════════════════╗
║  YOUR ROLE: CONCLUSION                   ║
╚══════════════════════════════════════════╝
Leave a lasting impression. This section must feel earned and complete.

Structure:
1. Callback — reference something specific from the opening (the stat, story, or claim)
2. Synthesis — bullet list of 3-4 THE most important insights from the whole blog
   (not summaries of sections — the 3-4 ideas the reader should carry with them forever)
3. One specific, concrete action the reader can take TODAY (not "start exploring" — be specific)
4. Closing line — single sentence. Make it quotable. Almost aphoristic.
   Think: something that could be a tweet that 10,000 people would retweet.

FORBIDDEN: "In conclusion", "To summarize", "As we've seen", "I hope this helped", "Happy learning"
"""
    else:
        role_block = f"""
╔══════════════════════════════════════════╗
║  YOUR ROLE: BODY SECTION                 ║
╚══════════════════════════════════════════╝
Section brief: {writing_brief}

This section must deliver GENUINE DEPTH. Go beyond surface-level explanation.

STRUCTURE this section as:
1. Mini-hook (1 sharp sentence that earns the reader's attention for THIS section)
2. Core explanation — the WHY and HOW, not just the WHAT
3. Evidence from research — specific stats, named examples, direct quotes
4. One surprising sub-point that deepens understanding
5. Transition sentence that flows naturally toward the next section

The previous section ended with:
---
{prev_tail}
---
Your opening should feel like a natural continuation, not a fresh start.
"""

    # ── Special requirements ────────────────────────────────────────────
    citation_block = """
CITATIONS (MANDATORY for this section):
- Every factual claim must be attributed: "According to [Source Name](url), X"
- Use at minimum 3 different sources
- For particularly striking stats, give them their own indented line:
  > 📊 **[Stat here]** — [Source Name](url)
""" if needs_citations else ""

    code_block = """
CODE (REQUIRED for this section):
- Include 1-2 complete, working code examples in fenced blocks with correct language tag
- Code must directly illustrate the concept, not a toy example
- Every non-obvious line gets an inline comment
- After the block: 1-2 sentences explaining what this code achieves and when to use it
""" if needs_code else ""

    slug = re.sub(r"[^a-z0-9]+", "_", section_title.lower())[:30].strip("_")
    image_block = f"""
IMAGE (include exactly one at the most impactful point):
`![Vivid, specific alt text describing what would be shown](IMAGE_PLACEHOLDER_{slug})`
Place it where a diagram, chart, or real photo would most help comprehension.
"""

    return f"""You are a senior writer at a world-class publication. Think Wired, The Atlantic, Harvard Business Review, or Wait But Why.

You write with precision, authority, genuine insight, and a voice that makes complex ideas feel urgent and alive.

You are writing ONE section of a blog post. Your entire focus is this section. Make it the best {target_words} words you have ever written on this topic.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLOG CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full title    : {title}
Topic         : {topic}
Core angle    : {hook_angle}
Audience      : {audience}
Tone          : {tone}
Type          : {blog_kind}
Blog structure: {blog_structure}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THIS SECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Heading       : {section_title}
Target words  : {target_words} — write AT LEAST this many. More depth = better score.

{role_block}
{citation_block}
{code_block}
{image_block}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYNTHESIZED RESEARCH BRIEF
(Facts, quotes, examples extracted from {20} sources — use them liberally)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{research[:6000]}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MASTER WRITING RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOICE
▸ Write like the smartest, most experienced person in the room — who also happens to be a great teacher
▸ Use "you" to speak directly to the reader; use "we" to invite them on the journey
▸ Be direct: cut hedging words. Not "arguably" or "might be" — state facts and label opinions clearly
▸ Confidence without arrogance: bold claims, not bluster

SPECIFICITY — the single biggest quality differentiator
▸ NEVER use vague quantifiers. Replace every one:
  ✗ "many companies"     →  ✓ "74% of Fortune 500 companies" or "Google, Microsoft, and Amazon"
  ✗ "significantly more" →  ✓ "340% higher" or "3.4x more likely"
  ✗ "some experts say"   →  ✓ "[Dr. Sarah Chen], AI researcher at MIT"
  ✗ "recent studies"     →  ✓ "A 2024 Stanford study of 10,000 participants"

RHYTHM
▸ Vary sentence length deliberately. Long sentence to explain complexity. Short one for impact. Repeat.
▸ Max 4 sentences per paragraph. Break it up.
▸ Use ### sub-headings if a section covers 2+ distinct sub-topics

MANDATORY ELEMENTS (every section must have):
▸ One `> **Key insight:** [The single sharpest, most memorable idea in this section]` blockquote
▸ **Bold** on 2-4 critical terms (aids scanning — but ONLY where it genuinely helps)
▸ At least one bullet or numbered list if you're covering 3+ related items

FORBIDDEN PHRASES (writing any of these = failure):
"In today's fast-paced world" | "It goes without saying" | "In conclusion" | "As we can see"
"It is worth noting" | "Needless to say" | "Let's dive in" | "Without further ado"
"The bottom line is" | "In this blog/article/post" | "I hope this helps" | "Happy coding"
"In summary" | "To wrap up" | "As mentioned above" | "As previously stated"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Start DIRECTLY and ONLY with `## {section_title}` — zero preamble, zero meta-commentary.
Write the complete section. Hit the word target. Make every sentence earn its place.
"""


def _bangla_prompt(section_title, target_words, topic, title, audience, tone,
                   hook_angle, research, is_first, is_last, blog_structure,
                   needs_citations, writing_brief, prev_tail):
    if is_first:
        role_block = f"""
ভূমিকা বিভাগ — পাঠককে তাৎক্ষণিকভাবে আকৃষ্ট করুন।
মূল কোণ: "{hook_angle}"

খোলার কৌশল (সবচেয়ে শক্তিশালীটি বেছে নিন):
  ক) একটি চমকপ্রদ, নির্দিষ্ট পরিসংখ্যান যা সবকিছু পুনর্বিন্যাস করে
  খ) একটি ৩-বাক্যের জীবন্ত মাইক্রো-গল্প যা পাঠককে একটি বাস্তব পরিস্থিতিতে রাখে
  গ) একটি সাহসী দাবি যা পাঠকের ধারণাকে চ্যালেঞ্জ করে

নিষিদ্ধ শুরু: "আজকের বিশ্বে", "আপনি কি জানেন", "এই ব্লগে আমরা"
"""
    elif is_last:
        role_block = """
উপসংহার — স্থায়ী প্রভাব ফেলুন।
১. শুরুর হুকে ফিরে আসুন (নির্দিষ্ট রেফারেন্স দিন)
২. ৩-৪টি সবচেয়ে গুরুত্বপূর্ণ অন্তর্দৃষ্টির বুলেট তালিকা
৩. পাঠকের জন্য আজই নেওয়া যায় এমন একটি নির্দিষ্ট পদক্ষেপ
৪. একটি উদ্ধৃতিযোগ্য, স্মরণীয় শেষ বাক্য

নিষিদ্ধ: "পরিশেষে", "সারসংক্ষেপে", "আশা করি এটি সহায়ক হয়েছে"
"""
    else:
        role_block = f"""
মূল বিভাগ — প্রকৃত গভীরতা এবং মূল্য প্রদান করুন।
বিভাগ সারসংক্ষেপ: {writing_brief}

কাঠামো:
১. মিনি-হুক (এই বিভাগের জন্য পাঠকের মনোযোগ অর্জন করে এমন ১টি তীক্ষ্ণ বাক্য)
২. মূল ব্যাখ্যা — কেন এবং কীভাবে, শুধু কী নয়
৩. গবেষণা থেকে নির্দিষ্ট তথ্য, নাম, উদ্ধৃতি
৪. একটি আশ্চর্যজনক উপ-বিন্দু
৫. পরবর্তী বিভাগের দিকে প্রবাহিত রূপান্তর বাক্য

পূর্ববর্তী বিভাগের শেষ অংশ:
{prev_tail}
"""

    citation_block = "উৎস (বাধ্যতামূলক): প্রতিটি তথ্যের জন্য [উৎস নাম](url) উল্লেখ করুন। কমপক্ষে ৩টি ভিন্ন উৎস।\n" if needs_citations else ""
    slug = re.sub(r"[^\u0980-\u09FFa-z0-9]+", "_", section_title.lower())[:30].strip("_")

    return f"""আপনি বিশ্বমানের বাংলা প্রকাশনার একজন সিনিয়র লেখক। আপনি কর্তৃত্ব, স্পষ্টতা এবং প্রকৃত অন্তর্দৃষ্টি দিয়ে লেখেন।

আপনি একটি ব্লগ পোস্টের শুধুমাত্র একটি বিভাগ লিখছেন। সম্পূর্ণ ফোকাস এই বিভাগে।

━━━━━━━━━━━━━━━━━━━━━━
ব্লগের প্রেক্ষাপট
━━━━━━━━━━━━━━━━━━━━━━
শিরোনাম     : {title}
বিষয়        : {topic}
মূল কোণ     : {hook_angle}
পাঠক        : {audience}
স্বর         : {tone}
প্রবাহ       : {blog_structure}

━━━━━━━━━━━━━━━━━━━━━━
এই বিভাগ
━━━━━━━━━━━━━━━━━━━━━━
বিভাগ শিরোনাম : {section_title}
লক্ষ্য দৈর্ঘ্য  : {target_words} শব্দ (কমপক্ষে এতগুলো লিখুন)

{role_block}
{citation_block}
ছবি: `![নির্দিষ্ট বর্ণনামূলক alt টেক্সট](IMAGE_PLACEHOLDER_{slug})`

━━━━━━━━━━━━━━━━━━━━━━
সংশ্লেষিত গবেষণা সংক্ষিপ্তসার
━━━━━━━━━━━━━━━━━━━━━━
{research[:6000]}

━━━━━━━━━━━━━━━━━━━━━━
লেখার নিয়ম
━━━━━━━━━━━━━━━━━━━━━━
▸ আত্মবিশ্বাসী, সরাসরি কণ্ঠস্বর — "আপনি" এবং "আমরা" ব্যবহার করুন
▸ প্রতিটি অস্পষ্ট পরিমাপক গবেষণার নির্দিষ্ট সংখ্যা বা নামে প্রতিস্থাপন করুন
▸ বাক্যের দৈর্ঘ্য পরিবর্তন করুন। দীর্ঘ বাক্য। তারপর ছোট। এটি গতি তৈরি করে।
▸ `> **মূল অন্তর্দৃষ্টি:** [এই বিভাগের সবচেয়ে গুরুত্বপূর্ণ ধারণা]` একটি অন্তর্ভুক্ত করুন
▸ ২-৩টি মূল শব্দ **বোল্ড** করুন
▸ ৩+ সম্পর্কিত আইটেমের জন্য বুলেট তালিকা ব্যবহার করুন

নিষিদ্ধ: "পরিশেষে বলা যায়" | "এটা বলা বাহুল্য" | "আজকের ডিজিটাল বিশ্বে" | "উপরে উল্লেখিত"

━━━━━━━━━━━━━━━━━━━━━━
আউটপুট
━━━━━━━━━━━━━━━━━━━━━━
`## {section_title}` দিয়ে সরাসরি শুরু করুন। কোনো প্রিঅ্যাম্বল নেই। সম্পূর্ণ বিভাগ লিখুন।
"""


def _default_tasks(topic):
    return [
        {"id": 1, "title": f"The Uncomfortable Truth About {topic}",
         "target_words": 280, "requires_research": False, "requires_citations": False,
         "requires_code": False,
         "writing_brief": "Hook the reader with a surprising, counterintuitive opening about this topic"},
        {"id": 2, "title": "What the Data Actually Reveals",
         "target_words": 450, "requires_research": True, "requires_citations": True,
         "requires_code": False,
         "writing_brief": "Present the core statistics and research findings with specific numbers"},
        {"id": 3, "title": "Why Most People Get This Wrong",
         "target_words": 450, "requires_research": True, "requires_citations": True,
         "requires_code": False,
         "writing_brief": "Expose the most common misconceptions and explain the real mechanisms"},
        {"id": 4, "title": "Real-World Examples That Change Everything",
         "target_words": 420, "requires_research": True, "requires_citations": True,
         "requires_code": False,
         "writing_brief": "3 specific case studies with names, outcomes, and lessons"},
        {"id": 5, "title": "The Playbook That Actually Works",
         "target_words": 400, "requires_research": True, "requires_citations": False,
         "requires_code": False,
         "writing_brief": "Practical step-by-step framework the reader can apply immediately"},
        {"id": 6, "title": "What Happens If You Ignore This",
         "target_words": 320, "requires_research": True, "requires_citations": True,
         "requires_code": False,
         "writing_brief": "Consequences and stakes — make the reader feel the urgency"},
        {"id": 7, "title": "Start Here, Start Now",
         "target_words": 220, "requires_research": False, "requires_citations": False,
         "requires_code": False,
         "writing_brief": "Inspiring conclusion with callback to opening, 3-4 key takeaways, and one specific action"},
    ]
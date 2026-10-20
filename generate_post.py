import anthropic
import os
import json
from datetime import date

client = anthropic.Anthropic()
today = date.today()

# Load skill (system prompt)
with open("blog-skill.md", "r") as f:
    system_prompt = f.read()

# Load topics
with open("blog-topics.md", "r") as f:
    lines = f.readlines()

topics = []
for line in lines:
    line = line.strip()
    if not line.startswith("- ["):
        continue
    bracket_end = line.index("]")
    schedule = line[3:bracket_end].strip()
    topic = line[bracket_end + 1:].strip()
    topics.append({"topic": topic, "schedule": schedule})

# Schedule logic
DAY_NAMES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
today_name = DAY_NAMES[today.weekday()]
day_of_year = today.timetuple().tm_yday

def is_scheduled_today(schedule):
    if schedule == "daily":
        return True
    if schedule.startswith("weekly-"):
        return today_name == schedule.split("-")[1]
    if schedule == "every-other-day":
        return day_of_year % 2 == 0
    if schedule == "biweekly":
        return day_of_year % 14 == 0
    return False

eligible = [t for t in topics if is_scheduled_today(t["schedule"])]

if not eligible:
    print(f"📅 No posts scheduled for today ({today_name}). Exiting.")
    exit(0)

# History check (skip topics published in last 30 days)
HISTORY_FILE = ".blog-history.json"
try:
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
except FileNotFoundError:
    history = {}

def recently_published(topic):
    if topic not in history:
        return False
    last = date.fromisoformat(history[topic])
    return (today - last).days < 30

fresh = [t for t in eligible if not recently_published(t["topic"])]
chosen = fresh[0] if fresh else eligible[0]
topic = chosen["topic"]

print(f"✅ Writing post on: {topic}")

slug = (topic.lower()
        .replace(" ", "-")
        .replace(":", "")
        .replace("'", "")
        .replace(",", "")
        .replace("?", "")
        .replace("!", "")
        .replace("&", "and")
        .replace("/", "-"))

# Format date for display
date_display = today.strftime("%B %-d, %Y")

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2500,
    system=system_prompt,
    messages=[
        {
            "role": "user",
            "content": f"""Write a blog post about: "{topic}"

Today's date: {today.isoformat()}

Output in this EXACT format — nothing before the opening ---, no extra commentary after:

---
layout: ../../layouts/BaseLayout.astro
title: "TITLE HERE - Gulo AI Blog"
description: "SEO meta description under 155 chars including primary keyword"
keywords: "primary keyword, secondary keyword, Canadian IT"
ogDescription: "Open Graph description (can match description)"
twitterTitle: "Shorter title for Twitter"
slug: "{slug}"
author: "Gulo AI"
date: "{today.isoformat()}"
tags: ["tag1", "tag2", "tag3"]
published: true
type: "article"
publishDate: "{today.isoformat()}T00:00:00Z"
---

<style>
  .post-hero {{ padding: 2.25rem 0; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; }}
  .post-hero .container {{ max-width: 800px; margin: 0 auto; }}
  .post-meta {{ color: rgba(255,255,255,0.7); margin-bottom: 1rem; font-size: 0.9rem; }}
  .post-body {{ max-width: 800px; margin: 0 auto; padding: 3rem 1rem; color: var(--color-gray); line-height: 1.8; }}
  .post-body h2 {{ margin-top: 2.5rem; margin-bottom: 1rem; color: var(--color-dark); }}
  .post-body h3 {{ margin-top: 1.75rem; color: var(--color-dark); }}
  .post-body ul, .post-body ol {{ padding-left: 1.5rem; margin-bottom: 1rem; }}
  .post-body li {{ margin-bottom: 0.4rem; }}
  .post-body blockquote {{ border-left: 4px solid var(--color-primary); padding-left: 1.25rem; margin: 1.5rem 0; font-style: italic; color: #555; }}
  .cta-block {{ background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%); color: white; border-radius: 10px; padding: 2rem; margin-top: 3rem; }}
  .cta-block h3 {{ color: white; margin-top: 0; }}
  .cta-block p {{ color: rgba(255,255,255,0.85); }}
  .cta-block a {{ display: inline-block; background: white; color: #0f3460; font-weight: 600; padding: 0.65rem 1.5rem; border-radius: 6px; text-decoration: none; margin-top: 0.5rem; }}
  .cta-block a:hover {{ background: #e8ecf5; }}
  .back-link {{ margin-top: 3rem; padding-top: 2rem; border-top: 1px solid var(--color-gray-light); }}
  .back-link a {{ color: var(--color-primary); font-weight: 500; }}
</style>

<section class="post-hero">
  <div class="container">
    <div class="post-meta">{date_display} · 7 min read</div>
    <h1 style="color:white; margin-bottom: 1rem;">TITLE HERE (no "- Gulo AI Blog" suffix)</h1>
    <p style="color:rgba(255,255,255,0.8); font-size:1.1rem;">One sentence subtitle or lede that hooks the reader.</p>
  </div>
</section>

<div class="post-body">

Write the full 600-800 word post body here using ## subheadings, bullet points where appropriate.
Include an FAQ section at the end with 2-3 questions.

<div class="cta-block">
  <h3>Ready to Take the Next Step?</h3>
  <p>Mention the relevant Gulo AI service here and how it helps.</p>
  <a href="/contact">Talk to Our Team →</a>
</div>

<div class="back-link">
  <a href="/blog">← Back to Blog</a>
</div>

</div>"""
        }
    ]
)

post_content = message.content[0].text

# Save post
post_dir = "src/pages/blog"
os.makedirs(post_dir, exist_ok=True)
filename = f"{post_dir}/{today.isoformat()}-{slug}.md"

with open(filename, "w") as f:
    f.write(post_content)

print(f"📝 Saved: {filename}")

# Update history
history[topic] = today.isoformat()
with open(HISTORY_FILE, "w") as f:
    json.dump(history, f, indent=2)

print(f"📚 History updated.")

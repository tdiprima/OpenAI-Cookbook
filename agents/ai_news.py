"""
Web scraping of Google News RSS + full-text fetch via newspaper3k, then parallel GPT summarization and a final mash-up.
"""
import asyncio
import os
import urllib.parse
from datetime import datetime, timedelta

import feedparser
from newspaper import Article
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tweak these if you wanna
SEARCH_TERM = "artificial intelligence"
MAX_ARTICLES = 3
MAX_PARALLEL = 3  # concurrent GPT calls


# ─── AGENT: Web Retriever ──────────────────────────────────────────────────────
def fetch_recent_articles(query: str, max_results: int = 3):
    """
    Grab top N articles from Google News RSS for `query` in last 7 days.
    """
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
    # Google News RSS with a time filter
    q = urllib.parse.quote_plus(f"{query} when:7d")
    rss_url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    entries = feed.entries[:max_results]
    articles = []
    for e in entries:
        art = Article(e.link)
        art.download()
        art.parse()
        articles.append({"title": e.title, "url": e.link, "published": e.published, "body": art.text})
    return articles


# ─── AGENT: GPT Summarizer ─────────────────────────────────────────────────────
PROMPT_TMPL = """\
Role:
You're an AI research assistant summarizing the latest AI-news. Keep it "fire" and straight to the point.

Input Article:
Title: {title}
URL: {url}
Published: {published}

Content:
\"\"\"{body}\"\"\"

Output:
• 2–3 tiny paragraphs (≤300 words)
• No fluff, no opinions
• Cite any tweets or sources mentioned
"""

sem = asyncio.Semaphore(MAX_PARALLEL)


async def summarize_article(a: dict) -> str:
    async with sem:
        prompt = PROMPT_TMPL.format(**a)
        resp = await aclient.chat.completions.create(model="gpt-4o-mini",
                                                     messages=[{"role": "system", "content": prompt}], temperature=0.2)
        return resp.choices[0].message.content.strip()


# ─── ORCHESTRATOR ─────────────────────────────────────────────────────────────
async def main():
    print(f"🔍 Fetching up to {MAX_ARTICLES} articles for \"{SEARCH_TERM}\" from last 7 days...")
    arts = fetch_recent_articles(SEARCH_TERM, MAX_ARTICLES)
    if not arts:
        print("No articles found. Try a different query.")
        return

    # 1) parallel mini-summaries
    tasks = [summarize_article(a) for a in arts]
    mini = await asyncio.gather(*tasks)

    # 2) final aggregator
    combo = "\n\n---\n\n".join(mini)
    final_prompt = f"""\
Role:
You are the same assistant. Combine these mini-summaries into ONE killer digest (2 short paragraphs ≤300 words):

\"\"\"{combo}\"\"\"
"""
    final = await aclient.chat.completions.create(model="gpt-4o-mini",
                                                  messages=[{"role": "system", "content": final_prompt}],
                                                  temperature=0.2)
    print("\n🚀 FINAL DIGEST:\n")
    print(final.choices[0].message.content)


if __name__ == "__main__":
    asyncio.run(main())

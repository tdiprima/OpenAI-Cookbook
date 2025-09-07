"""
Web scraping of Google News RSS + full-text fetch via requests/BeautifulSoup, then parallel GPT summarization and a final mash-up.
"""

import asyncio
import os
import urllib.parse

import feedparser
import requests
from bs4 import BeautifulSoup
from openai import AsyncOpenAI

aclient = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tweak these if you wanna
SEARCH_TERM = "artificial intelligence"
MAX_ARTICLES = 3
MAX_PARALLEL = 3  # concurrent GPT calls


# ─── AGENT: Web Retriever ──────────────────────────────────────────────────────
def fetch_article_content(url: str) -> str:
    """
    Fetch and extract text content from a URL using requests + BeautifulSoup
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find main content areas
        content_selectors = [
            "article",
            '[role="main"]',
            ".article-content",
            ".post-content",
            ".entry-content",
            ".content",
            "main",
        ]

        content = ""
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                content = elements[0].get_text(strip=True, separator=" ")
                break

        # Fallback to body if no specific content area found
        if not content:
            content = soup.get_text(strip=True, separator=" ")

        # Clean up excessive whitespace
        content = " ".join(content.split())

        # Truncate if too long (keep first 2000 chars to avoid token limits)
        if len(content) > 2000:
            content = content[:2000] + "..."

        return content

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


def fetch_recent_articles(query: str, max_results: int = 3):
    """
    Grab top N articles from Google News RSS for `query` in last 7 days.
    """
    try:
        # Google News RSS with a time filter
        q = urllib.parse.quote_plus(f"{query} when:7d")
        rss_url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"

        feed = feedparser.parse(rss_url)
        entries = feed.entries[:max_results]
        articles = []

        for e in entries:
            print(f"📰 Fetching: {e.title}")
            body = fetch_article_content(e.link)

            if body:  # Only add if we successfully got content
                articles.append(
                    {
                        "title": e.title,
                        "url": e.link,
                        "published": e.published,
                        "body": body,
                    }
                )

        return articles

    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return []


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
        try:
            prompt = PROMPT_TMPL.format(**a)
            resp = await aclient.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error summarizing article {a['title']}: {e}")
            return f"Error summarizing: {a['title']}"


# ─── ORCHESTRATOR ─────────────────────────────────────────────────────────────
async def main():
    print(
        f'🔍 Fetching up to {MAX_ARTICLES} articles for "{SEARCH_TERM}" from last 7 days...'
    )
    arts = fetch_recent_articles(SEARCH_TERM, MAX_ARTICLES)

    if not arts:
        print(
            "No articles found. Try a different query or check your internet connection."
        )
        return

    print(f"✅ Found {len(arts)} articles. Summarizing...")

    # 1) parallel mini-summaries
    tasks = [summarize_article(a) for a in arts]
    mini = await asyncio.gather(*tasks)

    # Filter out error messages
    valid_summaries = [s for s in mini if not s.startswith("Error summarizing")]

    if not valid_summaries:
        print("❌ No successful summaries generated.")
        return

    # 2) final aggregator
    combo = "\n\n---\n\n".join(valid_summaries)
    final_prompt = f"""\
Role:
You are the same assistant. Combine these mini-summaries into ONE killer digest (2 short paragraphs ≤300 words):

\"\"\"{combo}\"\"\"
"""

    try:
        final = await aclient.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": final_prompt}],
            temperature=0.2,
        )
        print("\n🚀 FINAL DIGEST:\n")
        print(final.choices[0].message.content)
    except Exception as e:
        print(f"Error generating final digest: {e}")
        print("\n📋 INDIVIDUAL SUMMARIES:\n")
        for i, summary in enumerate(valid_summaries, 1):
            print(f"{i}. {summary}\n")


if __name__ == "__main__":
    asyncio.run(main())

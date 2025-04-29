**What's happening:**

1. **Web Retriever** grabs top `MAX_ARTICLES` from Google News RSS filtered to the last 7 days.  
2. **GPT Summarizers** fire off in parallel (async) to boil each full article down.  
3. **Orchestrator** glues the mini-summaries into one succinct, source-cited AI update.

---

## AI Agent Guide

### 🚀 1. Web Retriever Agent  
- **What it does:**  
  - Hits Google News's RSS feed for "artificial intelligence" filtered to the last 7 days.  
  - Grabs the top `MAX_ARTICLES` links.  
  - Uses **newspaper3k** to download and parse each article's full text.  
- **Analogy:** Think of it like a news-hunting drone swooping in, grabbing the headlines and the juicy meat of each story.  

### 🤖 2. GPT Summarizer Agent  
- **What it does:**  
  - Spins up up to `MAX_PARALLEL` async calls to OpenAI.  
  - Feeds each article's title, URL, date, and body into a lean prompt.  
  - Gets back a **2–3 tiny-paragraph** summary per article.  
- **Why async?** So you don't wait on one "brain" to finish before starting the next—parallel processing FTW.  

### 🔗 3. Orchestrator  
- **Mini-summaries ➡️ Mega-digest:**  
  1. **Gather** the mini-summaries.  
  2. **Stitch** them together with `---` dividers.  
  3. **Fire** one final GPT call to mash them into a single, super-concise digest (again, 2 short paragraphs, ≤300 words).  
- **Analogy:** It's like taking three TikToks and editing them into one 30-second highlight reel.  

### ⚙️ Key Configs  
- **`SEARCH_TERM`**: change it to whatever AI topic you're stalking.  
- **`MAX_ARTICLES`**: how many stories you want.  
- **`MAX_PARALLEL`**: how many GPT calls at once (don't overload your API quota).  

### 💡 Why it Rocks  
1. **No logins**—just scrapey-scrape RSS + newspaper3k.  
2. **Fast**—parallel GPT calls.  
3. **ADHD-friendly output**—tiny chunks, no fluff, emojis optional.  

And that's it—three mini-agents working together to give you a lightning-fast AI news briefing. ⚡

<br>

# ara-ai-computer

Demo use cases for the [Ara Hackathon Tour](https://ara-hackathons.vercel.app) by DayDreamers — showcasing what you can build on the AI computer.

## Live Demo

**[ara-ai-computer.vercel.app](https://ara-sdk-test.vercel.app)**

## Use Cases

| Agent | What it does |
|-------|-------------|
| **Chief of Staff** | Triages messages across channels, categorizes urgency, drafts replies |
| **Research Assistant** | Web research, synthesis, saves to knowledge base, hands off to Quiz Master |
| **Project Manager** | Chat-based task tracking, async standups, overdue alerts |
| **Content Creator** | Raw ideas → LinkedIn/Twitter/newsletter drafts, hands off to Editor for de-slopping |
| **Finance Tracker** | Log expenses via chat, auto-categorize, track budget, weekly summaries |

## Stack

- **Backend**: [Ara SDK](https://docs.ara.so) — agents deployed on Ara's cloud runtime with sandboxed execution
- **Frontend**: Single HTML file with vanilla JS
- **Proxy**: Vercel serverless function (`/api/run`) to avoid CORS
- **Hosting**: Vercel

## Setup

```bash
# 1. Clone
git clone https://github.com/cyu60/ara-ai-computer.git
cd ara-ai-computer

# 2. Python env
python3.13 -m venv .venv
source .venv/bin/activate
pip install ara-sdk

# 3. Configure
export ARA_ACCESS_TOKEN="your-jwt-from-ara-settings"

# 4. Deploy agents
python3 app.py deploy --on-existing update

# 5. Test locally
python3 app.py run --workflow finance-tracker --message "coffee $4.50"

# 6. Deploy frontend
vercel env add ARA_RUNTIME_KEY production  # paste your runtime key
vercel --prod
```

## Architecture

```
User (browser)
  → /api/run (Vercel serverless proxy)
    → Ara Cloud Runtime
      → Agent sandbox (isolated execution)
        → Responds via same path
```

Each agent has its own sandbox with persistent filesystem, memory, and tools. Agents can hand off to each other (e.g., Content Creator → Editor).

## License

MIT

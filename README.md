# Ara AI Computer

> Built by [DayDreamers](https://daydreamers.club) for the Ara Hackathon Tour 2026

Five real-world AI agent use cases running on [Ara](https://ara.so) — the agentic operating system. Each agent has its own cloud sandbox, persistent memory, and can hand off tasks to specialist sub-agents. Interact with all of them from a single chat interface.

**Live demo**: [ara-sdk-test.vercel.app](https://ara-sdk-test.vercel.app)

## What's Inside

### Agents

| Agent | Description | Hands off to |
|-------|-------------|-------------|
| **Chief of Staff** | Triages incoming messages across WhatsApp, Telegram, and iMessage. Categorizes as urgent/actionable/FYI, surfaces what matters. | Reply Drafter |
| **Research Assistant** | Searches the web, synthesizes findings into markdown briefs, saves them to the sandbox filesystem as a growing knowledge base. | Quiz Master |
| **Project Manager** | Lightweight task board via chat. Tracks status, assignees, deadlines. Runs async standups and flags overdue items. | — |
| **Content Creator** | Takes a raw idea or experience and drafts platform-ready content for LinkedIn, Twitter/X, or newsletters. | Editor |
| **Finance Tracker** | Log expenses by texting ("coffee $4.50"). Auto-categorizes, tracks against budget, answers spending questions. | — |

### Sub-agents

| Agent | Role |
|-------|------|
| **Reply Drafter** | Drafts context-aware replies matching conversation tone. Never sends without approval. |
| **Quiz Master** | Generates quizzes from saved research briefs. Tracks scores over time. |
| **Editor** | Cuts AI slop — hedging, em dashes, filler, generic intros. Makes drafts sound human. |

### Scheduled Hooks

| Hook | Schedule | What it does |
|------|----------|-------------|
| Daily Research Digest | 9 AM UTC | Sends morning digest of new findings on tracked topics |
| Morning Standup | 10 AM UTC weekdays | Triggers async standup via Project Manager |
| Overdue Check | 5 PM UTC weekdays | Pings assignees about overdue tasks |
| Weekly Spending Summary | 6 PM UTC Sundays | Sends weekly expense breakdown |

## Architecture

```
Browser (chat UI)
  |
  v
/api/run (Vercel serverless proxy)
  |
  v
Ara Cloud Runtime (ara-api-prd.up.railway.app)
  |
  v
Agent Sandbox
  ├── Persistent filesystem (briefs, task boards, expense logs)
  ├── Memory & context assembly
  ├── Tool execution (browser automation, web search)
  └── Sub-agent handoff (e.g., Content Creator → Editor)
```

## Getting Started

### Prerequisites

- Python 3.10+
- An [Ara](https://ara.so) account (get your access token from Settings > System > Auth Token)
- [Vercel CLI](https://vercel.com/docs/cli) (for frontend deployment)

### 1. Clone and install

```bash
git clone https://github.com/cyu60/ara-ai-computer.git
cd ara-ai-computer

python3 -m venv .venv
source .venv/bin/activate
pip install ara-sdk
```

### 2. Configure

```bash
export ARA_ACCESS_TOKEN="your-jwt-from-ara-settings"
```

### 3. Deploy agents to Ara

```bash
python3 app.py deploy --on-existing update
```

This creates your app on Ara's cloud runtime and writes a `.runtime-key.local` file.

### 4. Test from the CLI

```bash
python3 app.py run --workflow finance-tracker --message "coffee $4.50"
python3 app.py run --workflow chief-of-staff --message "I have 3 unread messages"
python3 app.py run --workflow content-creator --message "Write a LinkedIn post about AI agents"
```

### 5. Deploy the frontend

```bash
vercel env add ARA_RUNTIME_KEY production  # paste the key from .runtime-key.local
vercel --prod
```

## Customizing

Add your own agent in `app.py`:

```python
@app.subagent(
    id="my-agent",
    instructions="You are a ...",
    handoff_to=["editor"],  # optional: delegate to other agents
    sandbox=sandbox(),
)
def my_agent(event=None):
    """Description of what this agent does."""
```

Then redeploy: `python3 app.py deploy --on-existing update`

Add it to the `AGENTS` array in `index.html` to make it appear in the chat UI.

## Built With

- [Ara SDK](https://docs.ara.so) — agent runtime, sandboxing, multi-channel messaging
- [Vercel](https://vercel.com) — frontend hosting + serverless proxy
- [DayDreamers](https://daydreamers.club) — hackathon organizers

## License

MIT

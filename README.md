# Ara AI Computer

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen?style=flat-square)](https://ara-sdk-test.vercel.app)
[![Deploy](https://img.shields.io/badge/Vercel-deployed-black?style=flat-square&logo=vercel)](https://vercel.com)
[![Ara SDK](https://img.shields.io/badge/Ara_SDK-0.1.1-purple?style=flat-square)](https://docs.ara.so)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)

> Built by [DayDreamers](https://daydreamers.live) for the Ara Hackathon Tour 2026

Five real-world AI agent use cases running on [Ara](https://ara.so) — the agentic operating system. Each agent has its own cloud sandbox, persistent memory, and can hand off tasks to specialist sub-agents. Interact with all of them from a single chat interface.

## The Problem

AI assistants today are one-shot tools — you ask a question, get an answer, and start over. There's no persistent context, no coordination between tasks, and no way to automate your personal workflows across messaging, research, content, and finances.

**Ara AI Computer** shows what it looks like when AI agents actually *live* on your computer:
- A **Chief of Staff** that triages your messages and only surfaces what matters
- A **Research Assistant** that builds a growing knowledge base you can quiz yourself on
- A **Project Manager** that tracks tasks and runs standups without you opening Jira
- A **Content Creator** that turns raw ideas into polished posts across platforms
- A **Finance Tracker** you can text "coffee $4.50" and get weekly spending reports

Built for the DayDreamers hackathon tour to show participants what's possible with agent-first development.

## Built With

![Ara SDK](https://img.shields.io/badge/Ara_SDK-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python_3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-black?style=for-the-badge&logo=vercel)
![JavaScript](https://img.shields.io/badge/Vanilla_JS-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## Features

### Agents

| Agent | Description | Hands off to |
|-------|-------------|-------------|
| **Chief of Staff** | Triages incoming messages across WhatsApp, Telegram, and iMessage. Categorizes as urgent/actionable/FYI. | Reply Drafter |
| **Research Assistant** | Searches the web, synthesizes findings into markdown briefs, saves them to the sandbox filesystem. | Quiz Master |
| **Project Manager** | Chat-based task board with status tracking, assignees, deadlines. Runs async standups. | — |
| **Content Creator** | Raw ideas into LinkedIn, Twitter/X, or newsletter drafts. | Editor |
| **Finance Tracker** | Log expenses via chat, auto-categorize, track against budget. | — |

### Sub-agents

| Agent | Role |
|-------|------|
| **Reply Drafter** | Drafts context-aware replies matching conversation tone. Never sends without approval. |
| **Quiz Master** | Generates quizzes from saved research briefs. Tracks scores over time. |
| **Editor** | Cuts AI slop — hedging, em dashes, filler, generic intros. Makes drafts sound human. |

### Scheduled Hooks

| Hook | Schedule | What it does |
|------|----------|-------------|
| Daily Research Digest | 9 AM UTC | Morning digest of new findings on tracked topics |
| Morning Standup | 10 AM UTC weekdays | Triggers async standup via Project Manager |
| Overdue Check | 5 PM UTC weekdays | Pings assignees about overdue tasks |
| Weekly Spending Summary | 6 PM UTC Sundays | Weekly expense breakdown |

## Architecture

```
┌──────────────────────────────────────────┐
│          Browser (Chat UI)               │
│  ┌──────────────┐  ┌─────────────────┐   │
│  │  Agent List   │  │  Chat Window    │   │
│  │  (sidebar)    │  │  (messages)     │   │
│  └──────────────┘  └───────┬─────────┘   │
└────────────────────────────┼─────────────┘
                             │ POST /api/run
                      ┌──────▼──────┐
                      │   Vercel    │
                      │  Serverless │
                      │   Proxy     │
                      └──────┬──────┘
                             │ Bearer auth
                      ┌──────▼──────┐
                      │  Ara Cloud  │
                      │   Runtime   │
                      └──────┬──────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
      ┌───────▼───┐  ┌──────▼──────┐ ┌─────▼─────┐
      │  Agent    │  │  Sub-agent  │ │  Cron     │
      │  Sandbox  │  │  Handoff    │ │  Hooks    │
      │ (files,   │  │ (editor,   │ │ (standups,│
      │  memory)  │  │  drafter)  │ │  digests) │
      └───────────┘  └─────────────┘ └───────────┘
```

## Project Structure

```
ara-ai-computer/
├── app.py              # Agent definitions (5 agents, 3 sub-agents, 4 hooks)
├── index.html          # Chat frontend (single file, vanilla JS)
├── api/
│   └── run.js          # Vercel serverless proxy for Ara API
├── .env                # ARA_ACCESS_TOKEN (not committed)
├── .runtime-key.local  # Runtime key from deploy (not committed)
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- An [Ara](https://ara.so) account (get your access token from Settings > System > Auth Token)
- [Vercel CLI](https://vercel.com/docs/cli) (for frontend deployment)

### App Setup

```bash
git clone https://github.com/cyu60/ara-ai-computer.git
cd ara-ai-computer

python3 -m venv .venv
source .venv/bin/activate
pip install ara-sdk
```

### Configure & Deploy Agents

```bash
export ARA_ACCESS_TOKEN="your-jwt-from-ara-settings"
python3 app.py deploy --on-existing update
```

### Test from CLI

```bash
python3 app.py run --workflow finance-tracker --message "coffee $4.50"
python3 app.py run --workflow chief-of-staff --message "I have 3 unread messages"
python3 app.py run --workflow content-creator --message "Write a LinkedIn post about AI agents"
```

### Deploy Frontend

```bash
vercel env add ARA_RUNTIME_KEY production  # paste key from .runtime-key.local
vercel --prod
```

## Customizing

Add your own agent in `app.py`:

```python
@app.subagent(
    id="my-agent",
    instructions="You are a ...",
    handoff_to=["editor"],  # optional
    sandbox=sandbox(),
)
def my_agent(event=None):
    """Description of what this agent does."""
```

Redeploy: `python3 app.py deploy --on-existing update`

Then add it to the `AGENTS` array in `index.html` to show it in the chat UI.

## License

MIT

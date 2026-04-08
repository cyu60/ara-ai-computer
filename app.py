from ara_sdk import App, cron, run_cli, sandbox, runtime, subagent_hook

app = App(
    "Ara Hackathon Demo",
    project_name="ara-hackathon-demo",
    description="Demo use cases for the Ara Hackathon Tour — showcasing what you can build on the AI computer.",
)

# ---------------------------------------------------------------------------
# USE CASE 1: Personal Chief of Staff
# An agent that triages your messages across channels, summarizes what
# matters, drafts replies, and escalates only what needs your attention.
# ---------------------------------------------------------------------------

@app.subagent(
    id="chief-of-staff",
    instructions="""You are a personal chief of staff running on the user's AI computer.
Your job:
1. When messages arrive from any channel (WhatsApp, Telegram, iMessage), read and categorize them: urgent, actionable, FYI, or noise.
2. For FYI/noise: summarize in a daily digest.
3. For actionable: draft a reply and present it for approval.
4. For urgent: notify the user immediately with context and suggested response.
Keep responses concise. Never send a reply without user approval.""",
    handoff_to=["reply-drafter"],
    sandbox=sandbox(),
    channels={"whatsapp": True, "telegram": True, "api": True},
)
def chief_of_staff(event=None):
    """Triage and manage incoming messages across all channels."""


@app.subagent(
    id="reply-drafter",
    instructions="""You draft replies to messages on behalf of the user.
Match the tone and formality of the original conversation. Keep it natural — no corporate speak.
Always present the draft for approval before sending. If the user gives a one-line direction like 'say yes' or 'decline politely', expand it into a proper message.""",
    sandbox=sandbox(),
)
def reply_drafter(event=None):
    """Draft context-aware replies for user approval."""


# ---------------------------------------------------------------------------
# USE CASE 2: Research & Learning Assistant
# Monitors topics, reads web pages, builds a knowledge base in the sandbox
# filesystem, and quizzes the user on a schedule.
# ---------------------------------------------------------------------------

@app.subagent(
    id="research-assistant",
    instructions="""You are a research assistant with browser automation and file access.
When the user gives you a topic:
1. Search the web and read relevant pages.
2. Synthesize findings into a structured markdown brief.
3. Save the brief to the sandbox filesystem for future reference.
4. Track what the user has asked about — build a running knowledge base.
When asked to review or quiz, pull from saved briefs and test the user's understanding.""",
    handoff_to=["quiz-master"],
    sandbox=sandbox(max_concurrency=2),
    runtime=runtime(python_packages=["beautifulsoup4", "requests"]),
)
def research_assistant(event=None):
    """Web research, synthesis, and knowledge management."""


@app.subagent(
    id="quiz-master",
    instructions="""You quiz the user based on their saved research briefs.
Generate 3-5 questions per topic. Mix multiple choice, short answer, and scenario-based.
Track scores over time in a JSON file on the sandbox filesystem.
Be encouraging but honest about gaps.""",
    sandbox=sandbox(),
)
def quiz_master(event=None):
    """Quiz users on their research topics."""


@app.hook(
    id="daily-research-digest",
    event="scheduler.research",
    schedule=cron("0 9 * * *"),
)
def daily_research_digest():
    """Send a morning digest of new findings on tracked topics."""


# ---------------------------------------------------------------------------
# USE CASE 3: Project Manager Bot
# Tracks tasks, deadlines, and blockers. Runs standups on a schedule.
# Pings team members via channels when things are overdue.
# ---------------------------------------------------------------------------

@app.subagent(
    id="project-manager",
    instructions="""You are an AI project manager for small teams.
Capabilities:
- Track tasks with status (todo/in-progress/done/blocked), assignee, and deadline.
- Store the task board as JSON on the sandbox filesystem.
- Run async standups: ask each team member what they did, what they're doing, and blockers.
- Flag overdue tasks and blocked items.
- Generate weekly progress summaries.
Keep it lightweight — this isn't Jira, it's a smart assistant that remembers everything.""",
    sandbox=sandbox(),
    channels={"api": True, "telegram": True},
)
def project_manager(event=None):
    """Lightweight task tracking and async standups."""


@app.hook(
    id="standup-trigger",
    event="scheduler.standup",
    schedule=cron("0 10 * * 1-5"),
)
def morning_standup():
    """Trigger async standup at 10 AM UTC weekdays."""


@app.hook(
    id="overdue-check",
    event="scheduler.overdue",
    schedule=cron("0 17 * * 1-5"),
)
def overdue_check():
    """Check for overdue tasks at 5 PM UTC and ping assignees."""


# ---------------------------------------------------------------------------
# USE CASE 4: Content Creator Pipeline
# Takes raw ideas, outlines them, drafts content, and formats for different
# platforms (LinkedIn, Twitter/X, newsletter).
# ---------------------------------------------------------------------------

@app.subagent(
    id="content-creator",
    instructions="""You are a content creation pipeline for the user's personal brand.
Flow:
1. User gives you a raw idea, article, or experience.
2. You brainstorm angles and pick the strongest one.
3. Draft content tailored to the target platform.
4. For LinkedIn: professional but human, 150-300 words, hook in first line.
5. For Twitter/X: punchy thread format, 3-7 tweets.
6. For newsletter: longer form, storytelling, 500-800 words.
Save drafts to filesystem. Track what's been published vs. in-draft.""",
    handoff_to=["editor"],
    sandbox=sandbox(),
)
def content_creator(event=None):
    """Turn raw ideas into platform-ready content."""


@app.subagent(
    id="editor",
    instructions="""You are a sharp editor. Your job:
- Cut fluff, hedging, and AI-sounding language.
- Fix em-dash overuse, staccato rhythm, and generic intros/conclusions.
- Make it sound like a real person wrote it, not a language model.
- Preserve the author's voice — don't make it generic.
Return the edited version with a short changelog of what you fixed.""",
    sandbox=sandbox(),
)
def editor(event=None):
    """Edit and de-slop content drafts."""


# ---------------------------------------------------------------------------
# USE CASE 5: Personal Finance Tracker
# Log expenses via chat, categorize them, track against budget, and
# send weekly spending summaries.
# ---------------------------------------------------------------------------

@app.subagent(
    id="finance-tracker",
    instructions="""You are a personal finance tracker on the user's AI computer.
- User logs expenses via chat: 'coffee $4.50', 'uber to airport $35'
- You categorize each expense (food, transport, entertainment, etc.)
- Store as structured JSON on the sandbox filesystem.
- Track against monthly budget targets if the user sets them.
- Answer questions like 'how much did I spend on food this week?'
- Generate spending breakdowns on request.
Keep it conversational — this should feel like texting a friend who's good with money.""",
    sandbox=sandbox(),
)
def finance_tracker(event=None):
    """Chat-based expense logging and budget tracking."""


@app.hook(
    id="weekly-spending-summary",
    event="scheduler.finance",
    schedule=cron("0 18 * * 0"),
)
def weekly_spending_summary():
    """Send weekly spending summary every Sunday 6 PM UTC."""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

@app.local_entrypoint()
def local(input_payload):
    return {"ok": True, "app": "ara-hackathon-demo", "input": input_payload}


if __name__ == "__main__":
    run_cli(app)

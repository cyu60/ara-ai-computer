from ara_sdk import App, cron, run_cli, sandbox

app = App("Ara Hackathon Demo", project_name="ara-hackathon-demo")


@app.subagent(
    handoff_to=["idea-coach"],
    sandbox=sandbox(),
)
def hackathon_assistant(event=None):
    """Help hackathon participants brainstorm and build with Ara."""


@app.subagent(
    id="idea-coach",
    instructions="You help hackers refine their project ideas. Ask clarifying questions about their use case, suggest technical approaches using Ara's capabilities, and help them scope to a 4-hour build.",
    sandbox=sandbox(),
)
def idea_coach(event=None):
    """Coach participants on scoping and refining hackathon ideas."""


@app.hook(
    id="submission-reminder",
    event="scheduler.reminder",
    schedule=cron("0 16 * * *"),
)
def submission_reminder():
    """Remind participants to submit before deadline."""


@app.local_entrypoint()
def local(input_payload):
    return {"ok": True, "app": "ara-hackathon-demo", "input": input_payload}


if __name__ == "__main__":
    run_cli(app)

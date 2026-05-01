# Framework Selector — Interactive Advisor

This tool asks you a short series of questions about your project and then recommends the most suitable AI agent orchestration framework.

## Usage

```bash
# Interactive mode (requires keyboard input)
python framework_selector/agent.py

# Demo mode — no input needed, no API key required
python framework_selector/agent.py --demo
```

## Sample Session

```
╭─────────────────────────────────────────────────────────╮
│  🤖  AI Agent Orchestration Framework Advisor           │
│  Answer a few questions and I'll recommend a framework  │
╰─────────────────────────────────────────────────────────╯

Question 1 of 5
Does your project involve multiple AI agents collaborating with each other?
  a) No – a single agent is enough
  b) Yes – agents have free-form conversations
  c) Yes – agents have specific roles / responsibilities

Your answer (a/b/c or 1/2/3): a

...

✅  Recommendation
  🏆 Recommended framework: LangChain
     Composable chains + tools; best single-agent starting point

📝  Real-Life Example: LangChain — Customer Support Bot
  ... (full runnable code snippet shown here)
```

## Questions Asked

| # | Topic |
|---|-------|
| 1 | Single vs multi-agent |
| 2 | Need for loops / self-correction |
| 3 | Overall complexity |
| 4 | Code execution requirement |
| 5 | Rich shared state requirement |

Answers are scored and the framework with the highest score wins.

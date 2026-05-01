# CrewAI Example — Content Marketing Crew

## Overview

This example shows how to build a **role-based content production crew** using CrewAI, where three specialist agents collaborate sequentially to produce a polished blog post.

## Real-Life Use Case

> A marketing team needs a blog post on a given topic every week.
>
> The crew:
> 1. **Researcher** — gathers facts, statistics, and key insights
> 2. **Writer** — transforms the research brief into a 500-600 word structured blog post
> 3. **Editor** — polishes the draft for clarity, tone, grammar, and SEO

Each agent receives the output of the previous task as **context**, forming a clean assembly-line pipeline.

## Architecture

```
 ┌─────────────────────────────────────────────────────────┐
 │                    CrewAI Crew                          │
 │                                                         │
 │  ┌────────────┐    ┌──────────────┐    ┌─────────────┐  │
 │  │ Researcher │───►│    Writer    │───►│   Editor    │  │
 │  │            │    │              │    │             │  │
 │  │ research_  │    │ write_task   │    │ edit_task   │  │
 │  │ task       │    │ (uses ↑)     │    │ (uses ↑)    │  │
 │  └────────────┘    └──────────────┘    └─────────────┘  │
 │                                                         │
 │  Process: SEQUENTIAL                                    │
 └─────────────────────────────────────────────────────────┘
```

## Running the Example

```bash
# With a real LLM
export OPENAI_API_KEY=sk-...
python examples/crewai/example.py

# Custom topic
python examples/crewai/example.py --topic "Serverless architecture in 2025"

# Demo mode (no API key needed)
python examples/crewai/example.py --demo
```

## Key CrewAI Concepts Demonstrated

| Concept | Description |
|---------|-------------|
| `Agent(role, goal, backstory)` | Defines who the agent is and what it is trying to achieve |
| `Task(description, expected_output, agent)` | A concrete piece of work assigned to one agent |
| `context=[...]` | Passes the outputs of previous tasks as input to this task |
| `Crew(agents, tasks, process)` | Assembles the team and defines execution order |
| `Process.sequential` | Tasks run one after another; each output feeds the next |
| `crew.kickoff()` | Starts the crew and returns the final output |

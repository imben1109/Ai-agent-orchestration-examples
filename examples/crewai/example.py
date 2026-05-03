#!/usr/bin/env python3
"""
CrewAI Example — Content Marketing Crew
=======================================
Real-life scenario: A crew of three specialised agents — Researcher, Writer,
and Editor — collaborate to produce a polished blog post.

Run:
    export OPENAI_API_KEY=sk-...
    python examples/crewai/example.py

    # Demo mode (no API key required)
    python examples/crewai/example.py --demo
"""

from __future__ import annotations

import argparse


# ---------------------------------------------------------------------------
# Real CrewAI pipeline (requires OPENAI_API_KEY)
# ---------------------------------------------------------------------------

def run_real_crew(topic: str) -> None:
    from crewai import Agent, Task, Crew, Process
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # --- Define crew members ---

    researcher = Agent(
        role="Senior Content Researcher",
        goal="Find accurate, up-to-date facts and statistics on the given topic",
        backstory=(
            "You are a meticulous researcher who digs deep into credible sources "
            "to gather data that will inform high-quality content. "
            "You always cite your reasoning and focus on relevance."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Transform research notes into an engaging, well-structured blog post",
        backstory=(
            "You craft compelling narratives that make complex topics accessible "
            "to a general audience while staying factually accurate. "
            "You write in a clear, conversational tone."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    editor = Agent(
        role="Senior Editor",
        goal="Polish the draft for clarity, tone, grammar, and SEO",
        backstory=(
            "With 10 years of editorial experience, you refine prose to meet "
            "publication standards and maximise reader engagement. "
            "You ensure the article has a strong headline and clear call-to-action."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # --- Define tasks ---

    research_task = Task(
        description=f"Research the topic: '{topic}'. Produce a bullet-point brief with key facts, statistics, and insights.",
        expected_output="A concise research brief (bullet points) with 5-8 key data points.",
        agent=researcher,
    )

    write_task = Task(
        description=(
            "Using the research brief, write a 500-600 word blog post. "
            "Include: an engaging title, an introduction, three body sections with subheadings, "
            "and a conclusion with a call-to-action."
        ),
        expected_output="A 500-600 word blog post in Markdown format.",
        agent=writer,
        context=[research_task],
    )

    edit_task = Task(
        description=(
            "Edit the blog post for clarity, flow, grammar, and SEO. "
            "Ensure the headline is compelling and includes the main keyword. "
            "Output the final publication-ready article."
        ),
        expected_output="A polished, publication-ready blog post in Markdown format.",
        agent=editor,
        context=[write_task],
    )

    # --- Assemble crew and run ---

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, write_task, edit_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL PUBLISHED ARTICLE")
    print("=" * 60)
    print(result)


# ---------------------------------------------------------------------------
# Demo mode — simulated crew output
# ---------------------------------------------------------------------------

def run_demo() -> None:
    print("\n[DEMO MODE — simulated CrewAI pipeline, no API key required]\n")

    topic = "AI Agent Orchestration Frameworks in 2025"

    print(f"Topic: {topic}\n")

    steps = [
        (
            "Senior Content Researcher",
            "Research Brief",
            (
                "• AI agent market expected to reach $47B by 2030 (MarketsandMarkets, 2024)\n"
                "• LangChain: 80k+ GitHub stars; most popular framework as of 2024\n"
                "• Microsoft AutoGen adopted by Fortune 500 companies for code automation\n"
                "• CrewAI grew 500% in downloads in Q1 2025\n"
                "• LangGraph introduced persistent stateful agents solving hallucination loops\n"
                "• Key trend: from single LLM calls → orchestrated multi-agent workflows\n"
                "• Gartner: 30% of enterprise apps will include agentic AI by 2026"
            ),
        ),
        (
            "Content Writer",
            "Draft Blog Post",
            (
                "# The Rise of AI Agent Orchestration: What You Need to Know in 2025\n\n"
                "Artificial intelligence has moved beyond simple chatbots. Today, teams of "
                "specialised AI agents work in concert to tackle complex, multi-step tasks — "
                "from writing code to analysing datasets to publishing marketing content.\n\n"
                "## Why Orchestration Matters\n"
                "Single LLM prompts hit a ceiling. Agent orchestration frameworks break tasks "
                "into manageable steps, route work to specialised agents, and maintain state "
                "across interactions.\n\n"
                "## The Leading Frameworks\n"
                "LangChain dominates with 80k+ GitHub stars. LangGraph adds stateful loops. "
                "AutoGen enables code-executing multi-agent conversations. CrewAI brings "
                "role-based collaboration inspired by human teams.\n\n"
                "## Who Is Using Them?\n"
                "Fortune 500 companies use AutoGen for automated code review. Marketing "
                "agencies deploy CrewAI crews for content at scale. Research labs rely "
                "on LangGraph for iterative hypothesis testing.\n\n"
                "## Get Started Today\n"
                "Run `pip install langchain crewai langgraph pyautogen` and explore the "
                "examples in this repository to find the right tool for your project."
            ),
        ),
        (
            "Senior Editor",
            "Final Article (Publication Ready)",
            (
                "# AI Agent Orchestration in 2025: The Frameworks Powering the Next Wave of AI\n\n"
                "Artificial intelligence has moved far beyond simple chatbots. "
                "Teams of specialised AI agents now work in concert to tackle complex, "
                "multi-step tasks — from writing and executing code to producing polished "
                "marketing content.\n\n"
                "## Why Orchestration Is the Next Big Shift\n"
                "...(polished version of draft)...\n\n"
                "*Ready to build your first AI agent? Star this repo and run "
                "`python framework_selector/agent.py` to get a personalised recommendation.*"
            ),
        ),
    ]

    for role, output_name, content in steps:
        print(f"\n{'─'*60}")
        print(f"  [{role}] → {output_name}")
        print(f"{'─'*60}")
        print(content)

    print(
        "\n\n[To run with a real LLM, set OPENAI_API_KEY and run without --demo]"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CrewAI content marketing crew example")
    parser.add_argument("--demo", action="store_true", help="Run demo without an API key")
    parser.add_argument(
        "--topic",
        default="AI Agent Orchestration Frameworks in 2025",
        help="Blog post topic",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_real_crew(args.topic)

#!/usr/bin/env python3
"""
LangGraph Example — Iterative Research & Writing Agent
======================================================
Real-life scenario: An agent that drafts an article, critiques its own draft,
then revises it — looping until a quality threshold is reached.

Run:
    export OPENAI_API_KEY=sk-...
    python examples/langgraph/example.py

    # Demo mode (no API key required)
    python examples/langgraph/example.py --demo
"""

from __future__ import annotations

import argparse
import operator
from typing import Annotated, TypedDict


# ---------------------------------------------------------------------------
# State definition
# ---------------------------------------------------------------------------

class ResearchState(TypedDict):
    topic: str
    draft: str
    critique: str
    revisions: Annotated[int, operator.add]  # summed automatically by LangGraph


# ---------------------------------------------------------------------------
# Real agent (requires OPENAI_API_KEY)
# ---------------------------------------------------------------------------

def build_graph():
    from langchain_openai import ChatOpenAI
    from langgraph.graph import StateGraph, END

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # --- Node functions ---

    def research_and_draft(state: ResearchState) -> dict:
        response = llm.invoke(
            f"Write a concise 3-paragraph article about: {state['topic']}"
        )
        print(f"\n[NODE: draft] Generated draft ({len(response.content)} chars)")
        return {"draft": response.content, "revisions": 1}

    def critique_draft(state: ResearchState) -> dict:
        response = llm.invoke(
            "Critique this article and list 2-3 specific, actionable improvements:\n\n"
            + state["draft"]
        )
        print(f"\n[NODE: critique] Critique generated")
        return {"critique": response.content}

    def revise_draft(state: ResearchState) -> dict:
        response = llm.invoke(
            "Revise the article below based on this critique. "
            "Keep it to 3 paragraphs.\n\n"
            f"Article:\n{state['draft']}\n\n"
            f"Critique:\n{state['critique']}"
        )
        print(f"\n[NODE: revise] Revision {state['revisions']} done")
        return {"draft": response.content, "revisions": 1}

    # --- Routing ---

    def should_continue(state: ResearchState) -> str:
        """Loop for up to 2 critique+revise cycles, then end."""
        if state["revisions"] < 3:
            return "critique"
        return END

    # --- Build the graph ---

    graph = StateGraph(ResearchState)
    graph.add_node("draft",   research_and_draft)
    graph.add_node("critique", critique_draft)
    graph.add_node("revise",  revise_draft)

    graph.set_entry_point("draft")
    graph.add_conditional_edges("draft",  should_continue)
    graph.add_edge("critique", "revise")
    graph.add_conditional_edges("revise", should_continue)

    return graph.compile()


def run_real_agent(topic: str) -> None:
    app = build_graph()
    print(f"\nTopic: {topic}")
    print("Running iterative draft → critique → revise loop...\n")
    result = app.invoke({"topic": topic, "revisions": 0, "draft": "", "critique": ""})
    print("\n" + "=" * 60)
    print("FINAL ARTICLE")
    print("=" * 60)
    print(result["draft"])
    print(f"\n(Total revision cycles: {result['revisions']})")


# ---------------------------------------------------------------------------
# Demo mode — no LLM calls
# ---------------------------------------------------------------------------

def run_demo() -> None:
    print("\n[DEMO MODE — simulated LangGraph flow, no API key required]\n")

    topic = "The future of AI agent orchestration"
    print(f"Topic: {topic}\n")

    state: ResearchState = {"topic": topic, "draft": "", "critique": "", "revisions": 0}

    # Simulate draft node
    state["draft"] = (
        "[Mock draft] AI agent orchestration is evolving rapidly. "
        "Frameworks like LangChain, LangGraph, AutoGen, and CrewAI enable "
        "developers to build powerful multi-step agents. The future will bring "
        "more specialised, collaborative, and self-improving systems."
    )
    state["revisions"] = 1
    print(f"[NODE: draft] Draft created ({len(state['draft'])} chars)")

    # Simulate critique node
    state["critique"] = (
        "[Mock critique] 1. Add specific statistics. "
        "2. Mention real industry use cases. "
        "3. Conclude with actionable advice for developers."
    )
    print("[NODE: critique] Critique generated")

    # Simulate revise node
    state["draft"] = (
        "[Mock revised draft] AI agent orchestration has seen 300% growth in 2024. "
        "Companies use LangGraph for iterative research pipelines, AutoGen for "
        "automated code review, and CrewAI for content production. "
        "Developers should start with LangChain and progress to multi-agent "
        "frameworks as their use cases mature."
    )
    state["revisions"] = 2
    print(f"[NODE: revise] Revision complete ({len(state['draft'])} chars)")

    print("\n" + "=" * 60)
    print("FINAL ARTICLE (after 1 critique+revise cycle)")
    print("=" * 60)
    print(state["draft"])

    print(
        "\n[To run with a real LLM, set OPENAI_API_KEY and run without --demo]"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LangGraph iterative research agent example")
    parser.add_argument("--demo", action="store_true", help="Run demo without an API key")
    parser.add_argument(
        "--topic",
        default="The impact of AI agent orchestration on software development",
        help="Article topic",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_real_agent(args.topic)

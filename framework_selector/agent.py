#!/usr/bin/env python3
"""
Framework Selector — Interactive AI Agent Orchestration Advisor
==============================================================
Run:  python framework_selector/agent.py
      python framework_selector/agent.py --demo   (no API key needed)

The agent asks you a series of questions about your project requirements,
scores the four major frameworks, prints its recommendation, and then shows
a real-life code snippet for the winning framework.
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Callable

# ---------------------------------------------------------------------------
# Optional rich output – falls back to plain print if not installed
# ---------------------------------------------------------------------------
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.table import Table
    from rich import print as rprint

    console = Console()

    def _panel(title: str, body: str, style: str = "cyan") -> None:
        console.print(Panel(body, title=title, border_style=style))

    def _ask(prompt: str) -> str:
        return Prompt.ask(f"[bold yellow]{prompt}[/bold yellow]")

except ImportError:
    console = None  # type: ignore[assignment]

    def _panel(title: str, body: str, style: str = "cyan") -> None:  # type: ignore[misc]
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        print(body)

    def _ask(prompt: str) -> str:  # type: ignore[misc]
        return input(f"\n{prompt}: ").strip()


# ---------------------------------------------------------------------------
# Framework metadata
# ---------------------------------------------------------------------------

FRAMEWORKS = {
    "LangChain": {
        "tagline": "Composable chains + tools; best single-agent starting point",
        "strengths": [
            "Huge ecosystem of ready-made tools and integrations",
            "Simple chain composition (pipe operator `|`)",
            "Great docs and community support",
            "Low barrier to entry",
        ],
        "weaknesses": [
            "Can feel verbose for simple tasks",
            "No native support for cyclic/looping flows",
        ],
        "ideal_for": "Single-agent apps, RAG pipelines, chatbots",
        "real_life_example": "customer_support_bot",
    },
    "LangGraph": {
        "tagline": "Stateful graph agent; ideal when you need loops & branching",
        "strengths": [
            "Models complex flows as a graph (nodes + edges)",
            "Built-in typed state passed between nodes",
            "Conditional edges for dynamic routing",
            "Handles retries and self-correction loops naturally",
        ],
        "weaknesses": [
            "Steeper learning curve than plain LangChain",
            "More boilerplate for simple tasks",
        ],
        "ideal_for": "Iterative research/writing agents, self-correcting pipelines",
        "real_life_example": "iterative_research_agent",
    },
    "AutoGen": {
        "tagline": "Conversation-based multi-agent; agents chat to solve problems",
        "strengths": [
            "Agents communicate through natural-language messages",
            "Built-in code execution sandbox",
            "Easy to add new specialist agents",
            "Good for code-generation + testing workflows",
        ],
        "weaknesses": [
            "Conversation-heavy; harder to control exact flow",
            "Can be token-expensive due to verbose messages",
        ],
        "ideal_for": "Multi-agent code generation, data analysis, automated QA",
        "real_life_example": "data_analysis_pipeline",
    },
    "CrewAI": {
        "tagline": "Role-based crew; agents have defined roles, goals & tasks",
        "strengths": [
            "Intuitive role/goal/backstory model",
            "Sequential and parallel task execution",
            "Built-in agent memory and delegation",
            "Works well with LangChain tools",
        ],
        "weaknesses": [
            "Less flexible for ad-hoc tool routing",
            "Newer framework – API still evolving",
        ],
        "ideal_for": "Content pipelines, research + writing crews, business workflows",
        "real_life_example": "content_marketing_crew",
    },
}


# ---------------------------------------------------------------------------
# Questions and scoring logic
# ---------------------------------------------------------------------------

@dataclass
class Question:
    text: str
    options: list[str]                   # displayed options (a, b, c, …)
    score_fn: Callable[[str], dict[str, int]]  # returns {framework: delta_score}


def _score_agents(answer: str) -> dict[str, int]:
    a = answer.lower()
    if a in ("b", "2"):   # yes – multiple agents conversing
        return {"AutoGen": 3, "CrewAI": 2}
    if a in ("c", "3"):   # yes – role-based
        return {"CrewAI": 3, "AutoGen": 1}
    return {"LangChain": 2, "LangGraph": 1}


def _score_loops(answer: str) -> dict[str, int]:
    a = answer.lower()
    if a in ("a", "1"):   # yes – needs loops/cycles
        return {"LangGraph": 4, "AutoGen": 1}
    return {"LangChain": 3, "LangGraph": 0}


def _score_complexity(answer: str) -> dict[str, int]:
    a = answer.lower()
    if a in ("a", "1"):   # simple / prototype
        return {"LangChain": 3}
    if a in ("b", "2"):   # medium
        return {"LangChain": 1, "LangGraph": 2, "CrewAI": 1}
    # complex
    return {"LangGraph": 2, "AutoGen": 3, "CrewAI": 2}


def _score_code_exec(answer: str) -> dict[str, int]:
    a = answer.lower()
    if a in ("a", "1"):   # yes
        return {"AutoGen": 4}
    return {"LangChain": 1, "LangGraph": 1, "CrewAI": 1}


def _score_state(answer: str) -> dict[str, int]:
    a = answer.lower()
    if a in ("a", "1"):   # yes – rich shared state
        return {"LangGraph": 3, "AutoGen": 1}
    return {"LangChain": 2, "CrewAI": 1}


QUESTIONS: list[Question] = [
    Question(
        text="Does your project involve multiple AI agents collaborating with each other?",
        options=[
            "a) No – a single agent is enough",
            "b) Yes – agents have free-form conversations",
            "c) Yes – agents have specific roles / responsibilities",
        ],
        score_fn=_score_agents,
    ),
    Question(
        text="Does the agent need to loop, retry, or self-correct its own output?",
        options=[
            "a) Yes – it should iterate until quality criteria are met",
            "b) No – a straight pipeline is fine",
        ],
        score_fn=_score_loops,
    ),
    Question(
        text="How would you describe the complexity of your use case?",
        options=[
            "a) Simple / prototype",
            "b) Medium – a few tools or retrieval steps",
            "c) Complex – many steps, tools, or agents",
        ],
        score_fn=_score_complexity,
    ),
    Question(
        text="Does the agent need to write and **execute** code as part of its work?",
        options=[
            "a) Yes",
            "b) No",
        ],
        score_fn=_score_code_exec,
    ),
    Question(
        text="Does your agent need to maintain and pass rich shared state between steps?",
        options=[
            "a) Yes – typed state that evolves across many steps",
            "b) No – simple conversation history is enough",
        ],
        score_fn=_score_state,
    ),
]


# ---------------------------------------------------------------------------
# Real-life example snippets
# ---------------------------------------------------------------------------

EXAMPLES: dict[str, tuple[str, str]] = {
    "customer_support_bot": (
        "LangChain — Customer Support Bot",
        '''
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub

# --- Tools available to the agent ---

@tool
def lookup_order(order_id: str) -> str:
    """Look up an order status by ID."""
    # In production: query your database
    return f"Order {order_id} is shipped and will arrive in 2 days."

@tool
def search_knowledge_base(query: str) -> str:
    """Search the support knowledge base for answers."""
    # In production: vector similarity search
    return "Our return policy allows returns within 30 days of purchase."

# --- Build the agent ---

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, [lookup_order, search_knowledge_base], prompt)
executor = AgentExecutor(agent=agent, tools=[lookup_order, search_knowledge_base], verbose=True)

# --- Run ---

result = executor.invoke({
    "input": "Hi, my order #12345 hasn't arrived yet. What's your return policy?"
})
print(result["output"])
''',
    ),
    "iterative_research_agent": (
        "LangGraph — Iterative Research & Writing Agent",
        '''
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import operator

# --- Shared state definition ---

class ResearchState(TypedDict):
    topic: str
    draft: str
    critique: str
    revisions: Annotated[int, operator.add]   # auto-increments

# --- Node functions ---

llm = ChatOpenAI(model="gpt-4o-mini")

def research_and_draft(state: ResearchState) -> ResearchState:
    response = llm.invoke(
        f"Write a concise 3-paragraph article about: {state['topic']}"
    )
    return {"draft": response.content, "revisions": 1}

def critique_draft(state: ResearchState) -> ResearchState:
    response = llm.invoke(
        f"Critique this article and list specific improvements:\\n\\n{state['draft']}"
    )
    return {"critique": response.content}

def revise_draft(state: ResearchState) -> ResearchState:
    response = llm.invoke(
        f"Revise the article based on this critique:\\n\\nArticle:\\n{state['draft']}"
        f"\\n\\nCritique:\\n{state['critique']}"
    )
    return {"draft": response.content, "revisions": 1}

def should_continue(state: ResearchState) -> str:
    """Loop until the article has been revised twice."""
    return "critique" if state["revisions"] < 3 else END

# --- Build the graph ---

graph = StateGraph(ResearchState)
graph.add_node("draft",   research_and_draft)
graph.add_node("critique", critique_draft)
graph.add_node("revise",  revise_draft)

graph.set_entry_point("draft")
graph.add_conditional_edges("draft",   should_continue)
graph.add_edge("critique", "revise")
graph.add_conditional_edges("revise",  should_continue)

app = graph.compile()

# --- Run ---

result = app.invoke({"topic": "The future of AI agent orchestration", "revisions": 0})
print(result["draft"])
''',
    ),
    "data_analysis_pipeline": (
        "AutoGen — Automated Data Analysis Pipeline",
        '''
import autogen

config_list = [{"model": "gpt-4o-mini", "api_key": "YOUR_KEY"}]

llm_config = {
    "config_list": config_list,
    "cache_seed": 42,
    "temperature": 0,
}

# --- Define specialist agents ---

analyst = autogen.AssistantAgent(
    name="DataAnalyst",
    system_message=(
        "You are a Python data analyst. Write clean pandas/matplotlib code "
        "to explore and visualise datasets. Always explain your findings."
    ),
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message=(
        "Review the analyst's code and findings. "
        "Point out statistical pitfalls and suggest improvements."
    ),
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="NEVER",          # fully automated
    code_execution_config={"work_dir": "/tmp/autogen_workspace"},
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda msg: "ANALYSIS COMPLETE" in msg.get("content", ""),
)

# --- Kick off the group chat ---

groupchat = autogen.GroupChat(agents=[user_proxy, analyst, critic], messages=[], max_round=12)
manager  = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message=(
        "Analyse the Titanic dataset (use seaborn.load_dataset). "
        "Show survival rates by class and gender, then say ANALYSIS COMPLETE."
    ),
)
''',
    ),
    "content_marketing_crew": (
        "CrewAI — Content Marketing Crew",
        '''
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# --- Define the crew members ---

researcher = Agent(
    role="Senior Content Researcher",
    goal="Find accurate, up-to-date facts and statistics on the given topic",
    backstory=(
        "You are a meticulous researcher who digs deep into credible sources "
        "to gather data that will inform high-quality content."
    ),
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Content Writer",
    goal="Transform research notes into an engaging, well-structured blog post",
    backstory=(
        "You craft compelling narratives that make complex topics accessible "
        "to a general audience while staying factually accurate."
    ),
    llm=llm,
    verbose=True,
)

editor = Agent(
    role="Senior Editor",
    goal="Polish the draft for clarity, tone, and SEO",
    backstory=(
        "With 10 years of editorial experience, you refine prose "
        "to meet publication standards and maximise reader engagement."
    ),
    llm=llm,
    verbose=True,
)

# --- Define the tasks ---

research_task = Task(
    description="Research the latest trends in AI agent orchestration frameworks in 2024-2025.",
    expected_output="A bullet-point brief with key facts, statistics, and quotes.",
    agent=researcher,
)

write_task = Task(
    description="Write a 600-word blog post based on the research brief.",
    expected_output="A polished blog post with an introduction, three sections, and a conclusion.",
    agent=writer,
    context=[research_task],
)

edit_task = Task(
    description="Edit the blog post for clarity, flow, and SEO keywords.",
    expected_output="A publication-ready blog post.",
    agent=editor,
    context=[write_task],
)

# --- Assemble the crew and run ---

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff()
print(result)
''',
    ),
}


# ---------------------------------------------------------------------------
# Demo mode (no API key needed)
# ---------------------------------------------------------------------------

DEMO_ANSWERS = ["a", "b", "b", "b", "b"]  # single agent, no loops, medium, no exec, no state


# ---------------------------------------------------------------------------
# Main advisor logic
# ---------------------------------------------------------------------------

def run_advisor(demo: bool = False) -> None:
    _panel(
        "🤖  AI Agent Orchestration Framework Advisor",
        "Answer a few questions and I will recommend the best framework for your project.",
        style="bold blue",
    )

    scores: dict[str, int] = {fw: 0 for fw in FRAMEWORKS}
    answers: list[str] = []

    for i, q in enumerate(QUESTIONS):
        print()
        _panel(
            f"Question {i+1} of {len(QUESTIONS)}",
            q.text + "\n\n" + "\n".join(q.options),
            style="green",
        )

        if demo:
            answer = DEMO_ANSWERS[i]
            print(f"(demo) auto-answer: {answer}")
        else:
            answer = _ask("Your answer (a/b/c or 1/2/3)").strip().lower()

        answers.append(answer)
        deltas = q.score_fn(answer)
        for fw, delta in deltas.items():
            scores[fw] += delta

    # --- Print score table ---
    print()
    _panel("📊  Scoring Summary", _build_score_text(scores), style="magenta")

    # --- Recommendation ---
    winner = max(scores, key=lambda fw: scores[fw])
    runner_up = sorted(scores, key=lambda fw: scores[fw], reverse=True)[1]

    rec_text = (
        f"🏆  Recommended framework: [bold]{winner}[/bold]\n"
        f"    {FRAMEWORKS[winner]['tagline']}\n\n"
        f"🥈  Runner-up: {runner_up}\n"
        f"    {FRAMEWORKS[runner_up]['tagline']}"
    )
    try:
        from rich import print as rp
        _panel("✅  Recommendation", rec_text, style="bold green")
    except ImportError:
        _panel("Recommendation", rec_text.replace("[bold]", "").replace("[/bold]", ""), style="bold green")

    # --- Strengths & weaknesses ---
    fw_info = FRAMEWORKS[winner]
    detail = (
        "Strengths:\n"
        + "\n".join(f"  ✔ {s}" for s in fw_info["strengths"])
        + "\n\nWeaknesses:\n"
        + "\n".join(f"  ✘ {w}" for w in fw_info["weaknesses"])
        + f"\n\nIdeal for: {fw_info['ideal_for']}"
    )
    _panel(f"ℹ️  About {winner}", detail, style="cyan")

    # --- Real-life example ---
    example_key = fw_info["real_life_example"]
    title, code = EXAMPLES[example_key]
    # Escape Rich markup characters so code brackets are displayed literally
    try:
        from rich.markup import escape as rich_escape
        safe_code = rich_escape(code)
    except ImportError:
        safe_code = code
    _panel(f"📝  Real-Life Example: {title}", safe_code, style="yellow")

    print("\nAll framework examples live in the `examples/` directory.\n")


def _build_score_text(scores: dict[str, int]) -> str:
    lines = []
    max_score = max(scores.values()) or 1
    for fw, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * int(score / max_score * 20)
        lines.append(f"  {fw:<12} {bar:<20} {score}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Agent Orchestration Framework Advisor")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with pre-set answers (no keyboard input required, no API key needed)",
    )
    args = parser.parse_args()
    run_advisor(demo=args.demo)

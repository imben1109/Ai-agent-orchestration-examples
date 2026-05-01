#!/usr/bin/env python3
"""
LangChain Example — Customer Support ReAct Agent
=================================================
Real-life scenario: A customer-support agent that can look up order status
and search a knowledge base to answer customer questions.

Run:
    export OPENAI_API_KEY=sk-...
    python examples/langchain/example.py

    # Demo mode (no API key required — uses mock logic)
    python examples/langchain/example.py --demo
"""

from __future__ import annotations

import argparse


# ---------------------------------------------------------------------------
# Mock tools used in demo mode (no dependencies required)
# ---------------------------------------------------------------------------

_MOCK_ORDER_DB = {
    "12345": "Shipped — estimated delivery in 2 days.",
    "99999": "Processing — not yet shipped.",
}


def _mock_lookup_order(order_id: str) -> str:
    return _MOCK_ORDER_DB.get(order_id, f"Order {order_id} not found.")


def _mock_search_kb(query: str) -> str:
    if "return" in query.lower():
        return "Our return policy allows returns within 30 days of purchase with a receipt."
    if "shipping" in query.lower():
        return "Standard shipping takes 3-5 business days. Express shipping takes 1-2 days."
    return "Please contact support@example.com for further assistance."


# ---------------------------------------------------------------------------
# LangChain tools (only imported when a real LLM is requested)
# ---------------------------------------------------------------------------

def _make_langchain_tools():
    from langchain.tools import tool

    @tool
    def lookup_order(order_id: str) -> str:
        """Look up the shipping status of an order by its ID."""
        return _mock_lookup_order(order_id)

    @tool
    def search_knowledge_base(query: str) -> str:
        """Search the support knowledge base for policy and product information."""
        return _mock_search_kb(query)

    return [lookup_order, search_knowledge_base]


# ---------------------------------------------------------------------------
# Real agent (requires OPENAI_API_KEY)
# ---------------------------------------------------------------------------

def run_real_agent(question: str) -> None:
    from langchain_openai import ChatOpenAI
    from langchain.agents import create_react_agent, AgentExecutor
    from langchain import hub

    tools = _make_langchain_tools()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Pull the standard ReAct prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

    print(f"\nQuestion: {question}\n")
    result = executor.invoke({"input": question})
    print(f"\nAnswer: {result['output']}")


# ---------------------------------------------------------------------------
# Demo mode — mock logic only, no dependencies needed
# ---------------------------------------------------------------------------

def run_demo() -> None:
    print("\n[DEMO MODE — mock logic, no API key or packages required]\n")

    question = "What is the status of order #12345, and what is your return policy?"
    print(f"Customer question: {question}\n")

    print("--- Agent thinks: I should look up the order status first.")
    order_status = _mock_lookup_order("12345")
    print(f"--- Tool (lookup_order) returned: {order_status}")

    print("\n--- Agent thinks: Now I should check the return policy.")
    kb_result = _mock_search_kb("return policy")
    print(f"--- Tool (search_knowledge_base) returned: {kb_result}")

    print(
        "\n--- Agent final answer:\n"
        f"Your order #12345 is on its way — {order_status} "
        f"Regarding returns: {kb_result}"
    )

    print(
        "\n[To run with a real LLM, set OPENAI_API_KEY and run without --demo]"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LangChain customer-support agent example")
    parser.add_argument("--demo", action="store_true", help="Run demo without an API key")
    parser.add_argument(
        "--question",
        default="My order #12345 hasn't arrived yet. Also, what is your return policy?",
        help="Question to ask the agent",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_real_agent(args.question)


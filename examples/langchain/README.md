# LangChain Example — Customer Support ReAct Agent

## Overview

This example shows how to build a **single-agent customer-support bot** using LangChain's ReAct agent pattern.

The agent has two tools:
- `lookup_order` — queries an order database by ID
- `search_knowledge_base` — retrieves policy/product information

## Real-Life Use Case

> A customer emails: *"My order #12345 hasn't arrived yet. What's your return policy?"*
>
> The agent:
> 1. **Thinks** — "I need to check the order status AND look up the return policy."
> 2. **Acts** — calls `lookup_order("12345")`
> 3. **Observes** — "Order 12345 is shipped, arriving in 2 days."
> 4. **Acts** — calls `search_knowledge_base("return policy")`
> 5. **Observes** — "Returns are accepted within 30 days."
> 6. **Answers** — combines both facts into a friendly reply.

## Architecture

```
User question
      │
      ▼
 ReAct Agent (LLM)
  ├─ Thought: what do I need to do?
  ├─ Action: call a tool
  ├─ Observation: read tool output
  └─ Repeat until → Final Answer
```

## Running the Example

```bash
# With a real LLM
export OPENAI_API_KEY=sk-...
python examples/langchain/example.py

# Custom question
python examples/langchain/example.py --question "Where is my order #99999?"

# Demo mode (no API key needed)
python examples/langchain/example.py --demo
```

## Key LangChain Concepts Demonstrated

| Concept | Description |
|---------|-------------|
| `@tool` decorator | Turns a Python function into a LangChain tool with a docstring-based description |
| `create_react_agent` | Builds a ReAct (Reason + Act) agent from an LLM, tools, and a prompt |
| `AgentExecutor` | Runs the agent loop, handles tool calls, and enforces `max_iterations` |
| LangChain Hub | Fetches community-maintained prompts (`hwchase17/react`) |

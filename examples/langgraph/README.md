# LangGraph Example — Iterative Research & Writing Agent

## Overview

This example shows how to build a **stateful, cyclic agent** using LangGraph that:
1. **Drafts** an article on a given topic
2. **Critiques** its own draft
3. **Revises** based on the critique
4. Loops steps 2–3 until quality criteria are met

## Real-Life Use Case

> A marketing team needs a polished blog post on a new product launch.
>
> The agent:
> 1. Writes an initial 3-paragraph draft
> 2. Self-critiques: "Too vague — needs statistics and examples"
> 3. Revises the draft to add specifics
> 4. Checks if enough revisions have been done → if not, loops back to step 2
> 5. Returns the final polished article

## Architecture (Graph)

```
        ┌──────────┐
        │  START   │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │  draft   │  ← Writes initial article
        └────┬─────┘
             │ (revisions < 3?)
             ▼
        ┌──────────┐
        │ critique │  ← Reviews draft, lists improvements
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │  revise  │  ← Rewrites draft based on critique
        └────┬─────┘
             │ (revisions >= 3?)
             ▼
        ┌──────────┐
        │   END    │
        └──────────┘
```

## Running the Example

```bash
# With a real LLM
export OPENAI_API_KEY=sk-...
python examples/langgraph/example.py

# Custom topic
python examples/langgraph/example.py --topic "Quantum computing for beginners"

# Demo mode (no API key needed)
python examples/langgraph/example.py --demo
```

## Key LangGraph Concepts Demonstrated

| Concept | Description |
|---------|-------------|
| `TypedDict` state | Typed shared state passed between all nodes |
| `Annotated[int, operator.add]` | Auto-accumulates the revision counter across nodes |
| `StateGraph` | The graph builder — nodes and edges are added here |
| `add_conditional_edges` | Routes to different nodes based on the current state |
| `graph.compile()` | Produces a runnable `Pregel` app from the graph definition |

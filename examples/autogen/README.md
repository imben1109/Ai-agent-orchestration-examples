# AutoGen Example — Automated Data Analysis Pipeline

## Overview

This example shows how to build a **multi-agent data analysis pipeline** using Microsoft AutoGen, where:
- A **DataAnalyst** agent writes Python analysis code
- A **StatsCritic** agent reviews findings for statistical correctness
- A **UserProxy** agent executes code automatically in a local sandbox

## Real-Life Use Case

> A data team needs to quickly analyse a dataset and produce visualisations.
>
> The pipeline:
> 1. UserProxy sends the analysis request
> 2. DataAnalyst writes pandas + matplotlib code and explains the findings
> 3. UserProxy **executes the code** in a sandbox (no human involved)
> 4. StatsCritic reviews the results for correctness
> 5. DataAnalyst incorporates feedback and declares ANALYSIS COMPLETE

## Architecture

```
UserProxy ◄──────────────────────────────► GroupChatManager (LLM)
    │                                              │
    │  executes code                    routes messages to
    │                                              │
    ▼                                    ┌─────────┴──────────┐
 Sandbox                            DataAnalyst          StatsCritic
(local Python)                    (writes code)        (reviews output)
```

## Running the Example

```bash
# With a real LLM (code will be executed in /tmp/autogen_workspace)
export OPENAI_API_KEY=sk-...
python examples/autogen/example.py

# Demo mode — prints a simulated conversation (no API key needed)
python examples/autogen/example.py --demo
```

## Key AutoGen Concepts Demonstrated

| Concept | Description |
|---------|-------------|
| `AssistantAgent` | An LLM-backed agent with a custom `system_message` defining its role |
| `UserProxyAgent` | Represents the human; can execute code automatically when `human_input_mode="NEVER"` |
| `GroupChat` | Container for all agents; the manager selects who speaks next |
| `GroupChatManager` | LLM that decides which agent should respond at each turn |
| `is_termination_msg` | Lambda that ends the conversation when a keyword is found |
| `code_execution_config` | Tells the UserProxy where to run generated code (`work_dir`) |

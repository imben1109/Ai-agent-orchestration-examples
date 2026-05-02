# AI Agent Orchestration Examples

A hands-on repository demonstrating popular **AI agent orchestration frameworks** through an interactive advisor, annotated code examples, and real-life use-case walkthroughs.

---

## What You Will Find Here

| Path | What it does |
|------|-------------|
| [`framework_selector/`](./framework_selector/) | Interactive CLI agent that **asks you questions**, recommends a framework, and shows a matching real-life example |
| [`examples/langchain/`](./examples/langchain/) | Tool-calling ReAct agent built with **LangChain** |
| [`examples/langgraph/`](./examples/langgraph/) | Stateful, cyclic multi-step agent built with **LangGraph** |
| [`examples/autogen/`](./examples/autogen/) | Multi-agent conversation built with **AutoGen** |
| [`examples/crewai/`](./examples/crewai/) | Role-based crew of autonomous agents built with **CrewAI** |

---

## Quick Start

\`\`\`bash
# 1. Clone and enter the repo
git clone https://github.com/imben1109/Ai-agent-orchestration-examples.git
cd Ai-agent-orchestration-examples

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the interactive framework advisor
python framework_selector/agent.py
\`\`\`

> **Note:** Set your \`OPENAI_API_KEY\` environment variable before running any example that calls a real LLM. Each example also supports a \`--demo\` flag to run with mock responses without an API key.

---

## Framework Overview

### 1. LangChain
**Best for:** Building LLM-powered apps with reusable chains and tools.

- 🔗 Composable chain primitives (\`LLMChain\`, \`SequentialChain\`)
- 🛠 Rich tool/retriever ecosystem (search, SQL, code execution, …)
- 🤖 ReAct & OpenAI-functions agent styles built-in
- 📚 Large community & documentation

**Real-life use case:** Customer-support bot that looks up orders in a database, searches a knowledge base, and drafts polite replies.

---

### 2. LangGraph
**Best for:** Agents that require **cycles**, branching, and persistent state between steps.

- 🔄 Models agent logic as a directed graph (nodes = actions, edges = transitions)
- 💾 Built-in state management via typed \`TypedDict\` state objects
- 🔀 Supports conditional edges (if/else routing between tools)
- 🔌 First-class integration with LangChain tools and LLMs

**Real-life use case:** Research assistant that iteratively refines a report — searches the web, critiques its own draft, then rewrites until quality criteria are met.

---

### 3. AutoGen (Microsoft)
**Best for:** **Multi-agent** systems where specialized agents collaborate through conversation.

- 💬 Agents communicate via structured messages
- 👥 Roles: \`AssistantAgent\`, \`UserProxyAgent\`, \`GroupChatManager\`
- 🧩 Code-execution sandbox included
- 🔁 Configurable conversation termination conditions

**Real-life use case:** Automated data-analysis pipeline: one agent writes Python, a second executes it, a third critiques the results, and a manager decides when the task is done.

---

### 4. CrewAI
**Best for:** Defining a **crew of specialised role-based agents** working toward a shared goal.

- 🧑‍💼 Agents have roles, goals, and backstories
- 📋 Tasks are delegated and executed sequentially or in parallel
- 🗂 Built-in memory and inter-agent delegation
- 🔗 Compatible with LangChain tools

**Real-life use case:** Content marketing crew — a researcher gathers facts, a writer drafts an article, and an editor polishes it before publishing.

---

## Choosing a Framework — Decision Guide

\`\`\`
Do you need multiple agents collaborating?
├── Yes, with free-form conversation  ──► AutoGen
├── Yes, with defined roles/tasks     ──► CrewAI
└── No, single agent is enough
    ├── Do you need cycles/loops in the agent's flow?
    │   ├── Yes  ──► LangGraph
    │   └── No   ──► LangChain
    └── (run `python framework_selector/agent.py` for a personalised recommendation)
\`\`\`

---

## Programming Language Support

All examples in this repository are written in **Python 3.10+**.

The frameworks themselves also have official SDKs in other languages:

| Framework | Python | JavaScript / TypeScript | Java | Open Source | License | GitHub Stars |
|-----------|:------:|:-----------------------:|:----:|:-----------:|---------|:------------:|
| [LangChain](https://github.com/langchain-ai/langchain) | ✅ (`langchain`) | ✅ ([LangChain.js](https://github.com/langchain-ai/langchainjs)) | ❌ | ✅ | MIT | ~136k |
| [LangGraph](https://github.com/langchain-ai/langgraph) | ✅ (`langgraph`) | ✅ ([LangGraph.js](https://github.com/langchain-ai/langgraphjs)) | ❌ | ✅ | MIT | ~31k |
| [AutoGen](https://github.com/microsoft/autogen)        | ✅ (`pyautogen`) | ❌ (Python only) | ❌ | ✅ | CC-BY-4.0 | ~58k |
| [CrewAI](https://github.com/crewAIInc/crewAI)         | ✅ (`crewai`)    | ❌ (Python only) | ❌ | ✅ | MIT | ~50k |

> ⭐ Star counts are approximate values checked in May 2026. None of the four frameworks currently provide an official Java SDK.

> **Why Python for the examples?**  All four frameworks have the most complete features and community support in Python, and the LLM/data-science ecosystem (pandas, matplotlib, seaborn, …) is primarily Python-first.

---

## Repository Structure

\`\`\`
.
├── README.md
├── requirements.txt
├── framework_selector/
│   ├── README.md
│   └── agent.py            # Interactive advisor CLI
├── examples/
│   ├── langchain/
│   │   ├── README.md
│   │   └── example.py
│   ├── langgraph/
│   │   ├── README.md
│   │   └── example.py
│   ├── autogen/
│   │   ├── README.md
│   │   └── example.py
│   └── crewai/
│       ├── README.md
│       └── example.py
└── tests/
    ├── conftest.py
    ├── test_framework_selector.py
    ├── test_langchain_example.py
    ├── test_langgraph_example.py
    ├── test_autogen_example.py
    └── test_crewai_example.py
\`\`\`

---

## Running the Tests

The test suite uses **pytest** and runs entirely without an API key — all tests exercise demo/mock logic only.

\`\`\`bash
# Install test dependency (already in requirements.txt)
pip install pytest

# Run all tests
pytest tests/ -v

# Run tests for a specific module
pytest tests/test_framework_selector.py -v
pytest tests/test_langchain_example.py -v
\`\`\`

| Test file | What it covers |
|-----------|----------------|
| \`test_framework_selector.py\` | FRAMEWORKS/EXAMPLES structure, all 5 scoring functions, \`_build_score_text\`, full demo run + recommendation scenarios |
| \`test_langchain_example.py\` | Mock order lookup tool, mock knowledge-base tool, demo run output |
| \`test_langgraph_example.py\` | \`ResearchState\` TypedDict, demo run node labels & content |
| \`test_autogen_example.py\` | Multi-agent demo conversation: speakers, code snippet, termination keyword |
| \`test_crewai_example.py\` | Crew pipeline demo: roles, outputs per step, statistics presence |

---

## Contributing

Pull requests are welcome! If you add a new framework example, please:
1. Follow the existing \`examples/<framework>/\` structure.
2. Add a \`README.md\` inside the new folder.
3. Update the table at the top of this file.

---

## License

MIT

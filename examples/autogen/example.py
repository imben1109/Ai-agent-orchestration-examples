#!/usr/bin/env python3
"""
AutoGen Example — Automated Data Analysis Pipeline
==================================================
Real-life scenario: A multi-agent pipeline where a DataAnalyst agent writes
Python code, a Critic agent reviews the findings, and a UserProxy agent
executes the code automatically.

Run:
    export OPENAI_API_KEY=sk-...
    python examples/autogen/example.py

    # Demo mode (no API key required)
    python examples/autogen/example.py --demo
"""

from __future__ import annotations

import argparse


# ---------------------------------------------------------------------------
# Real multi-agent pipeline (requires OPENAI_API_KEY)
# ---------------------------------------------------------------------------

def run_real_pipeline() -> None:
    import autogen

    config_list = autogen.config_list_from_json(
        "OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4o-mini"]},
    )
    # Fall back to env var if no config file
    if not config_list:
        import os
        config_list = [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]

    llm_config = {"config_list": config_list, "cache_seed": 42, "temperature": 0}

    # --- DataAnalyst: writes and explains Python analysis code ---
    analyst = autogen.AssistantAgent(
        name="DataAnalyst",
        system_message=(
            "You are a Python data analyst. Write clean pandas and matplotlib code "
            "to explore and visualise datasets. Always explain your findings in plain English. "
            "When done, include the phrase ANALYSIS COMPLETE."
        ),
        llm_config=llm_config,
    )

    # --- Critic: reviews findings for correctness ---
    critic = autogen.AssistantAgent(
        name="StatsCritic",
        system_message=(
            "You review data analysis for statistical correctness. "
            "Point out any misleading visuals, sampling bias, or incorrect conclusions. "
            "Keep feedback concise."
        ),
        llm_config=llm_config,
    )

    # --- UserProxy: executes code automatically in a sandbox ---
    user_proxy = autogen.UserProxyAgent(
        name="UserProxy",
        human_input_mode="NEVER",
        code_execution_config={"work_dir": "/tmp/autogen_workspace", "use_docker": False},
        max_consecutive_auto_reply=8,
        is_termination_msg=lambda msg: "ANALYSIS COMPLETE" in msg.get("content", ""),
    )

    # --- GroupChat: all agents collaborate ---
    groupchat = autogen.GroupChat(
        agents=[user_proxy, analyst, critic],
        messages=[],
        max_round=10,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

    user_proxy.initiate_chat(
        manager,
        message=(
            "Use seaborn's built-in Titanic dataset to analyse survival rates by "
            "passenger class and gender. Show a grouped bar chart. "
            "Summarise your key findings, then say ANALYSIS COMPLETE."
        ),
    )


# ---------------------------------------------------------------------------
# Demo mode — prints a simulated conversation
# ---------------------------------------------------------------------------

def run_demo() -> None:
    print("\n[DEMO MODE — simulated AutoGen multi-agent conversation]\n")

    conversation = [
        (
            "UserProxy",
            "Use seaborn's built-in Titanic dataset to analyse survival rates by "
            "passenger class and gender. Show a grouped bar chart. "
            "Summarise your key findings, then say ANALYSIS COMPLETE.",
        ),
        (
            "DataAnalyst",
            "I'll load the Titanic dataset and create a survival rate analysis.\n\n"
            "```python\n"
            "import seaborn as sns\n"
            "import matplotlib.pyplot as plt\n\n"
            "titanic = sns.load_dataset('titanic')\n"
            "survival = titanic.groupby(['class', 'sex'])['survived'].mean().reset_index()\n\n"
            "sns.barplot(data=survival, x='class', y='survived', hue='sex')\n"
            "plt.title('Titanic Survival Rate by Class & Gender')\n"
            "plt.ylabel('Survival Rate')\n"
            "plt.savefig('/tmp/titanic_survival.png')\n"
            "plt.show()\n"
            "print(survival)\n"
            "```\n\n"
            "Key findings:\n"
            "- Women had dramatically higher survival rates across all classes.\n"
            "- 1st class passengers survived at a much higher rate than 3rd class.\n"
            "- Only ~13% of 3rd-class male passengers survived.",
        ),
        (
            "UserProxy",
            "[Code executed successfully. Chart saved to /tmp/titanic_survival.png]",
        ),
        (
            "StatsCritic",
            "The analysis looks correct. One note: survival rate differences are "
            "statistically significant (chi-square p < 0.001). The grouped bar chart "
            "clearly shows the gender and class effects. No major issues found.",
        ),
        (
            "DataAnalyst",
            "Thank you for the review. The findings are statistically robust. "
            "ANALYSIS COMPLETE.",
        ),
    ]

    for speaker, message in conversation:
        print(f"\n{'─'*60}")
        print(f"  [{speaker}]")
        print(f"{'─'*60}")
        print(message)

    print(
        "\n\n[To run with a real LLM and code execution, "
        "set OPENAI_API_KEY and run without --demo]"
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AutoGen data-analysis pipeline example")
    parser.add_argument("--demo", action="store_true", help="Run demo without an API key")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    else:
        run_real_pipeline()

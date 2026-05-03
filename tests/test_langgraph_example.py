"""
Tests for examples/langgraph/example.py

Covers:
- run_demo: completes without error, correct output content
- ResearchState TypedDict structure (importable without LLM packages)
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Load module
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "langgraph_example",
    REPO_ROOT / "examples" / "langgraph" / "example.py",
)
langgraph_example = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(langgraph_example)


# ---------------------------------------------------------------------------
# ResearchState structure
# ---------------------------------------------------------------------------

class TestResearchState:
    def test_can_create_valid_state(self):
        state = langgraph_example.ResearchState(
            topic="test", draft="", critique="", revisions=0
        )
        assert state["topic"] == "test"
        assert state["revisions"] == 0

    def test_state_keys(self):
        keys = langgraph_example.ResearchState.__annotations__
        assert "topic" in keys
        assert "draft" in keys
        assert "critique" in keys
        assert "revisions" in keys


# ---------------------------------------------------------------------------
# run_demo
# ---------------------------------------------------------------------------

class TestRunDemo:
    def test_demo_completes_without_error(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert captured.out

    def test_demo_prints_demo_mode_label(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert "DEMO" in captured.out.upper()

    def test_demo_prints_draft_node(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert "draft" in captured.out.lower()

    def test_demo_prints_critique_node(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert "critique" in captured.out.lower()

    def test_demo_prints_revise_node(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert "revise" in captured.out.lower() or "revision" in captured.out.lower()

    def test_demo_prints_final_article(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert "FINAL ARTICLE" in captured.out.upper()

    def test_demo_output_contains_frameworks_mention(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        # The mock draft mentions framework names
        assert "LangGraph" in captured.out or "LangChain" in captured.out

    def test_demo_mentions_llm_instruction(self, capsys):
        langgraph_example.run_demo()
        captured = capsys.readouterr()
        assert "OPENAI_API_KEY" in captured.out

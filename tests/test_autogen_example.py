"""
Tests for examples/autogen/example.py

Covers:
- run_demo: completes without error, conversation output structure
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
    "autogen_example",
    REPO_ROOT / "examples" / "autogen" / "example.py",
)
autogen_example = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(autogen_example)


# ---------------------------------------------------------------------------
# run_demo
# ---------------------------------------------------------------------------

class TestRunDemo:
    def test_demo_completes_without_error(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert captured.out

    def test_demo_prints_demo_mode_label(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "DEMO" in captured.out.upper()

    def test_demo_shows_user_proxy_speaker(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "UserProxy" in captured.out

    def test_demo_shows_data_analyst_speaker(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "DataAnalyst" in captured.out

    def test_demo_shows_stats_critic_speaker(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "StatsCritic" in captured.out

    def test_demo_contains_code_snippet(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "```python" in captured.out

    def test_demo_contains_titanic(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "titanic" in captured.out.lower() or "Titanic" in captured.out

    def test_demo_ends_with_analysis_complete(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "ANALYSIS COMPLETE" in captured.out

    def test_demo_mentions_llm_instruction(self, capsys):
        autogen_example.run_demo()
        captured = capsys.readouterr()
        assert "OPENAI_API_KEY" in captured.out

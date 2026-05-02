"""
Tests for examples/crewai/example.py

Covers:
- run_demo: completes without error, crew pipeline output structure
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
    "crewai_example",
    REPO_ROOT / "examples" / "crewai" / "example.py",
)
crewai_example = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(crewai_example)


# ---------------------------------------------------------------------------
# run_demo
# ---------------------------------------------------------------------------

class TestRunDemo:
    def test_demo_completes_without_error(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert captured.out

    def test_demo_prints_demo_mode_label(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "DEMO" in captured.out.upper()

    def test_demo_shows_researcher_role(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "Researcher" in captured.out

    def test_demo_shows_writer_role(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "Writer" in captured.out

    def test_demo_shows_editor_role(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "Editor" in captured.out

    def test_demo_shows_research_brief(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "Research Brief" in captured.out

    def test_demo_shows_blog_post_draft(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "Blog Post" in captured.out or "blog post" in captured.out.lower()

    def test_demo_shows_final_article(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "Final Article" in captured.out or "Publication Ready" in captured.out

    def test_demo_contains_statistics(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        # Research brief should include at least one statistic
        assert "$" in captured.out or "%" in captured.out

    def test_demo_mentions_llm_instruction(self, capsys):
        crewai_example.run_demo()
        captured = capsys.readouterr()
        assert "OPENAI_API_KEY" in captured.out

"""
Tests for framework_selector/agent.py

Covers:
- FRAMEWORKS / EXAMPLES / QUESTIONS / DEMO_ANSWERS structural integrity
- Each scoring function with all valid inputs
- _build_score_text output format
- Full demo run (no API key, no ML packages)
"""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import the module under test
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

from framework_selector import agent  # noqa: E402  (after sys.path manipulation)

FRAMEWORK_NAMES = {"LangChain", "LangGraph", "AutoGen", "CrewAI"}


# ---------------------------------------------------------------------------
# Structural / metadata tests
# ---------------------------------------------------------------------------

class TestFrameworksStructure:
    def test_all_four_frameworks_present(self):
        assert set(agent.FRAMEWORKS.keys()) == FRAMEWORK_NAMES

    def test_each_framework_has_required_keys(self):
        required = {"tagline", "strengths", "weaknesses", "ideal_for", "real_life_example"}
        for name, info in agent.FRAMEWORKS.items():
            missing = required - set(info.keys())
            assert not missing, f"{name} is missing keys: {missing}"

    def test_strengths_and_weaknesses_are_non_empty_lists(self):
        for name, info in agent.FRAMEWORKS.items():
            assert isinstance(info["strengths"], list) and info["strengths"], \
                f"{name} has empty strengths"
            assert isinstance(info["weaknesses"], list) and info["weaknesses"], \
                f"{name} has empty weaknesses"

    def test_every_framework_example_exists_in_examples_dict(self):
        for name, info in agent.FRAMEWORKS.items():
            key = info["real_life_example"]
            assert key in agent.EXAMPLES, \
                f"{name}'s example key '{key}' not found in EXAMPLES"

    def test_examples_contain_title_and_code(self):
        for key, value in agent.EXAMPLES.items():
            assert len(value) == 2, f"EXAMPLES['{key}'] should be a (title, code) tuple"
            title, code = value
            assert isinstance(title, str) and title, f"EXAMPLES['{key}'] title is empty"
            assert isinstance(code, str) and code, f"EXAMPLES['{key}'] code is empty"

    def test_demo_answers_length_matches_questions(self):
        assert len(agent.DEMO_ANSWERS) == len(agent.QUESTIONS), (
            "DEMO_ANSWERS must have one entry per question"
        )

    def test_questions_have_text_options_and_score_fn(self):
        for i, q in enumerate(agent.QUESTIONS):
            assert q.text, f"Question {i} has empty text"
            assert q.options, f"Question {i} has no options"
            assert callable(q.score_fn), f"Question {i} score_fn is not callable"


# ---------------------------------------------------------------------------
# Scoring function tests
# ---------------------------------------------------------------------------

class TestScoringFunctions:
    # _score_agents
    def test_score_agents_single(self):
        result = agent._score_agents("a")
        assert "LangChain" in result
        assert "LangGraph" in result

    def test_score_agents_conversational(self):
        result = agent._score_agents("b")
        assert result.get("AutoGen", 0) > 0

    def test_score_agents_role_based(self):
        result = agent._score_agents("c")
        assert result.get("CrewAI", 0) > 0

    def test_score_agents_case_insensitive(self):
        assert agent._score_agents("B") == agent._score_agents("b")
        assert agent._score_agents("C") == agent._score_agents("c")

    def test_score_agents_numeric_alias(self):
        assert agent._score_agents("2") == agent._score_agents("b")
        assert agent._score_agents("3") == agent._score_agents("c")

    # _score_loops
    def test_score_loops_yes(self):
        result = agent._score_loops("a")
        assert result.get("LangGraph", 0) > 0

    def test_score_loops_no(self):
        result = agent._score_loops("b")
        assert result.get("LangChain", 0) > 0

    def test_score_loops_numeric_alias(self):
        assert agent._score_loops("1") == agent._score_loops("a")
        assert agent._score_loops("2") == agent._score_loops("b")

    # _score_complexity
    def test_score_complexity_simple(self):
        result = agent._score_complexity("a")
        assert result.get("LangChain", 0) > 0

    def test_score_complexity_medium(self):
        result = agent._score_complexity("b")
        assert result.get("LangChain", 0) > 0 or result.get("LangGraph", 0) > 0

    def test_score_complexity_complex(self):
        result = agent._score_complexity("c")
        assert result.get("AutoGen", 0) > 0 or result.get("LangGraph", 0) > 0

    # _score_code_exec
    def test_score_code_exec_yes(self):
        result = agent._score_code_exec("a")
        assert result.get("AutoGen", 0) > 0

    def test_score_code_exec_no(self):
        result = agent._score_code_exec("b")
        assert isinstance(result, dict)

    # _score_state
    def test_score_state_yes(self):
        result = agent._score_state("a")
        assert result.get("LangGraph", 0) > 0

    def test_score_state_no(self):
        result = agent._score_state("b")
        assert isinstance(result, dict)

    def test_all_scoring_return_dicts_with_valid_framework_keys(self):
        for fn in [
            agent._score_agents, agent._score_loops,
            agent._score_complexity, agent._score_code_exec, agent._score_state,
        ]:
            for answer in ("a", "b", "c", "1", "2", "3"):
                result = fn(answer)
                assert isinstance(result, dict), f"{fn.__name__}('{answer}') returned non-dict"
                for key in result:
                    assert key in FRAMEWORK_NAMES, \
                        f"{fn.__name__}('{answer}') returned unknown framework key '{key}'"
                for value in result.values():
                    assert isinstance(value, int) and value >= 0, \
                        f"{fn.__name__}('{answer}') returned non-positive-int score"


# ---------------------------------------------------------------------------
# _build_score_text
# ---------------------------------------------------------------------------

class TestBuildScoreText:
    def test_contains_all_framework_names(self):
        scores = {"LangChain": 5, "LangGraph": 3, "AutoGen": 1, "CrewAI": 2}
        text = agent._build_score_text(scores)
        for fw in FRAMEWORK_NAMES:
            assert fw in text

    def test_sorted_by_score_descending(self):
        scores = {"LangChain": 10, "LangGraph": 5, "AutoGen": 2, "CrewAI": 3}
        text = agent._build_score_text(scores)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        assert lines[0].startswith("LangChain"), "Highest scorer should be first"

    def test_handles_zero_scores(self):
        scores = {"LangChain": 0, "LangGraph": 0, "AutoGen": 0, "CrewAI": 0}
        text = agent._build_score_text(scores)
        assert isinstance(text, str)

    def test_returns_string(self):
        scores = {"LangChain": 9, "LangGraph": 4, "AutoGen": 0, "CrewAI": 3}
        assert isinstance(agent._build_score_text(scores), str)


# ---------------------------------------------------------------------------
# Full demo run
# ---------------------------------------------------------------------------

class TestDemoRun:
    def test_demo_completes_without_error(self, capsys):
        agent.run_advisor(demo=True)
        captured = capsys.readouterr()
        output = captured.out

        # Check all four framework names appear somewhere in output
        for fw in FRAMEWORK_NAMES:
            assert fw in output, f"Framework '{fw}' not found in demo output"

    def test_demo_prints_recommendation(self, capsys):
        agent.run_advisor(demo=True)
        captured = capsys.readouterr()
        # With the default DEMO_ANSWERS (single agent, no loops, medium, no exec, no state)
        # LangChain should win
        assert "LangChain" in captured.out

    def test_demo_prints_real_life_example(self, capsys):
        agent.run_advisor(demo=True)
        captured = capsys.readouterr()
        # The code snippet for LangChain should appear
        assert "lookup_order" in captured.out or "customer" in captured.out.lower()

    def test_demo_answers_lead_to_autogen_recommendation(self, capsys, monkeypatch):
        """Override DEMO_ANSWERS so AutoGen should win."""
        monkeypatch.setattr(
            agent, "DEMO_ANSWERS",
            ["b", "b", "c", "a", "b"]  # multi-agent conversation, complex, code exec
        )
        agent.run_advisor(demo=True)
        captured = capsys.readouterr()
        assert "AutoGen" in captured.out

    def test_demo_answers_lead_to_langgraph_recommendation(self, capsys, monkeypatch):
        """Override DEMO_ANSWERS so LangGraph should win."""
        monkeypatch.setattr(
            agent, "DEMO_ANSWERS",
            ["a", "a", "b", "b", "a"]  # single agent, needs loops, medium, no exec, rich state
        )
        agent.run_advisor(demo=True)
        captured = capsys.readouterr()
        assert "LangGraph" in captured.out

    def test_demo_answers_lead_to_crewai_recommendation(self, capsys, monkeypatch):
        """Override DEMO_ANSWERS so CrewAI should win."""
        monkeypatch.setattr(
            agent, "DEMO_ANSWERS",
            ["c", "b", "c", "b", "b"]  # role-based agents, no loops, complex
        )
        agent.run_advisor(demo=True)
        captured = capsys.readouterr()
        assert "CrewAI" in captured.out

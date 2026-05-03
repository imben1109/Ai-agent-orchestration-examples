"""
Tests for examples/langchain/example.py

Covers:
- _mock_lookup_order: known IDs, unknown ID
- _mock_search_kb: return, shipping, and unrecognised queries
- run_demo: completes without error, produces expected output
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Load module without triggering __main__ block
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "langchain_example",
    REPO_ROOT / "examples" / "langchain" / "example.py",
)
langchain_example = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(langchain_example)


# ---------------------------------------------------------------------------
# _mock_lookup_order
# ---------------------------------------------------------------------------

class TestMockLookupOrder:
    def test_known_order_12345(self):
        result = langchain_example._mock_lookup_order("12345")
        assert "Shipped" in result

    def test_known_order_99999(self):
        result = langchain_example._mock_lookup_order("99999")
        assert "Processing" in result

    def test_unknown_order_returns_not_found(self):
        result = langchain_example._mock_lookup_order("00000")
        assert "not found" in result.lower()

    def test_returns_string(self):
        assert isinstance(langchain_example._mock_lookup_order("12345"), str)

    def test_unknown_order_includes_id_in_message(self):
        result = langchain_example._mock_lookup_order("ABCDE")
        assert "ABCDE" in result


# ---------------------------------------------------------------------------
# _mock_search_kb
# ---------------------------------------------------------------------------

class TestMockSearchKb:
    def test_return_policy_query(self):
        result = langchain_example._mock_search_kb("return policy")
        assert "return" in result.lower()
        assert "30 days" in result

    def test_shipping_query(self):
        result = langchain_example._mock_search_kb("shipping time")
        assert "shipping" in result.lower() or "business days" in result.lower()

    def test_unrecognised_query_returns_contact_info(self):
        result = langchain_example._mock_search_kb("purple unicorn warranty")
        assert "support@example.com" in result

    def test_returns_string_for_any_query(self):
        for query in ("return", "shipping", "anything", "", "123"):
            assert isinstance(langchain_example._mock_search_kb(query), str)

    def test_case_insensitive_return_match(self):
        lower = langchain_example._mock_search_kb("return")
        upper = langchain_example._mock_search_kb("RETURN")
        assert lower == upper

    def test_case_insensitive_shipping_match(self):
        lower = langchain_example._mock_search_kb("shipping")
        upper = langchain_example._mock_search_kb("SHIPPING")
        assert lower == upper


# ---------------------------------------------------------------------------
# run_demo
# ---------------------------------------------------------------------------

class TestRunDemo:
    def test_demo_completes_without_error(self, capsys):
        langchain_example.run_demo()
        captured = capsys.readouterr()
        assert captured.out  # something was printed

    def test_demo_prints_demo_mode_label(self, capsys):
        langchain_example.run_demo()
        captured = capsys.readouterr()
        assert "DEMO" in captured.out.upper()

    def test_demo_shows_order_status(self, capsys):
        langchain_example.run_demo()
        captured = capsys.readouterr()
        assert "12345" in captured.out
        assert "Shipped" in captured.out

    def test_demo_shows_return_policy(self, capsys):
        langchain_example.run_demo()
        captured = capsys.readouterr()
        assert "return" in captured.out.lower()

    def test_demo_mentions_llm_instruction(self, capsys):
        langchain_example.run_demo()
        captured = capsys.readouterr()
        assert "OPENAI_API_KEY" in captured.out

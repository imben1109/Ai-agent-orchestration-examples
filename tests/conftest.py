"""
Shared pytest fixtures and sys.path configuration.

All example modules are loaded via importlib to avoid naming conflicts
(every example is called `example.py`) and to keep them independent of
any installed ML packages.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the repo root importable so `framework_selector.agent` can be resolved
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))

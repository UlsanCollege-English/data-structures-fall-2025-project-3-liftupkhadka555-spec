"""Compatibility shim for tests that import `flight_planner` from the project root.

This file loads the implementation from `src/flight_planner.py` and re-exports its
public symbols so existing tests which expect `from flight_planner import ...`
continue to work without changing the tests.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Dict

_impl_path = Path(__file__).with_name("src") / "flight_planner.py"
if not _impl_path.exists():
    raise ImportError(f"Could not find implementation module at {_impl_path!s}")

_spec = importlib.util.spec_from_file_location("_flight_planner_impl", _impl_path)
_module = importlib.util.module_from_spec(_spec)  # type: ModuleType
# Register the module in sys.modules prior to executing it so decorated/processed
# classes (e.g. dataclasses) can find their defining module via sys.modules.
if _spec and _spec.name:
    sys.modules[_spec.name] = _module
assert _spec and _spec.loader
_spec.loader.exec_module(_module)

# Re-export all public names from the implementation module into this module.
_public_names = [n for n in dir(_module) if not n.startswith("_")]
globals().update({name: getattr(_module, name) for name in _public_names})

__all__ = _public_names

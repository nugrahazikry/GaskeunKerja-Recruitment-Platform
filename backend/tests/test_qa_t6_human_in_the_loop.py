"""Area 5 QA T6: human-in-the-loop test.

Confirms no code path can finalize a candidate (write an hr_decisions row) without
explicit HR action — the "assist, never decide" claim. Implemented as a real static
check over the actual source tree (not just a one-off manual grep, so it stays valid as
the codebase changes) rather than a runtime test, since the property being verified is
about which code paths exist, not what a particular running instance does.
"""

import ast
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parent.parent

# Files where repo.hr_decisions.create(...) is allowed to appear.
ALLOWED_CALL_SITES = {
    "routers/decisions.py",  # the real HR-authenticated endpoint
    "seed/load_demo_data.py",  # seed-only, for the 2 pre-scripted synthetic candidates
}


def _find_hr_decisions_create_calls(py_file: Path) -> bool:
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "create":
                # crude but sufficient: matches `repo.hr_decisions.create(...)` /
                # `hr_decisions.create(...)` shaped calls
                value = node.func.value
                if isinstance(value, ast.Attribute) and value.attr == "hr_decisions":
                    return True
                if isinstance(value, ast.Name) and value.id == "hr_decisions":
                    return True
    return False


def test_hr_decisions_create_only_called_from_allowed_sites():
    offending_files = []
    for py_file in BACKEND_ROOT.rglob("*.py"):
        if ".venv" in py_file.parts or "__pycache__" in py_file.parts or "tests" in py_file.parts:
            continue
        relative = py_file.relative_to(BACKEND_ROOT).as_posix()
        if relative in ALLOWED_CALL_SITES:
            continue
        if _find_hr_decisions_create_calls(py_file):
            offending_files.append(relative)

    assert not offending_files, (
        f"hr_decisions.create() called from unexpected file(s): {offending_files} — "
        f"only {ALLOWED_CALL_SITES} should ever finalize a candidate's decision"
    )


def test_decisions_router_requires_hr_authentication():
    """Confirms the one real (non-seed) call site is actually gated by HR auth, not
    just conventionally colocated with it."""
    source = (BACKEND_ROOT / "routers" / "decisions.py").read_text(encoding="utf-8")
    assert "get_current_hr" in source, "decisions router no longer imports the HR auth dependency"

    tree = ast.parse(source)
    record_decision_fn = next(
        (node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "record_decision"),
        None,
    )
    assert record_decision_fn is not None, "record_decision function not found in decisions.py"

    arg_sources = ast.unparse(record_decision_fn.args)
    assert "get_current_hr" in arg_sources, "record_decision's signature no longer depends on get_current_hr"

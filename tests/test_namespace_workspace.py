"""Persistent project-level tests for the compiler namespace workspace.

These tests replace the old top-level workspace-repair assertions and verify the
PEP 420 namespace package layout, import resolution, namespace module execution,
and wheel contents.
"""

import shutil
import subprocess
import tomllib
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

MEMBERS = {
    "ast_nodes": "ast_nodes",
    "codegen": "codegen",
    "pypp_lexer": "pypp_lexer",
    "pypp_parser": "pypp_parser",
}


def _run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )


def test_legacy_workspace_repair_file_removed():
    assert not (ROOT / "test_workspace_repair.py").exists()


def test_compiler_namespace_is_pep420():
    assert not (ROOT / "compiler" / "__init__.py").exists()


def test_namespace_member_imports_resolve():
    import compiler.ast_nodes
    import compiler.codegen
    import compiler.pypp_lexer
    import compiler.pypp_parser

    assert compiler.ast_nodes.__file__.startswith(
        str(ROOT / "compiler" / "ast_nodes")
    )
    assert compiler.codegen.__file__.startswith(str(ROOT / "compiler" / "codegen"))
    assert compiler.pypp_lexer.__file__.startswith(
        str(ROOT / "compiler" / "pypp_lexer")
    )
    assert compiler.pypp_parser.__file__.startswith(
        str(ROOT / "compiler" / "pypp_parser")
    )


def test_codegen_main_module_imports_resolve():
    import compiler.codegen.main

    assert hasattr(compiler.codegen.main, "main")


def test_parser_main_module_imports_resolve():
    import compiler.pypp_parser.main

    assert hasattr(compiler.pypp_parser.main, "parse_source_code")


def test_codegen_starts_via_namespace_path():
    result = _run(
        ["uv", "run", "--package", "codegen", "python", "-m", "compiler.codegen.main"]
    )
    assert result.returncode == 0, result.stderr


def test_cross_member_imports_use_compiler_namespace():
    codegen_source = (ROOT / "compiler" / "codegen" / "main.py").read_text()
    parser_source = (ROOT / "compiler" / "pypp_parser" / "main.py").read_text()

    for old in ("import pypp_parser", "import ast_nodes", "import pypp_lexer"):
        assert old not in codegen_source
        assert old not in parser_source

    assert "import compiler.pypp_parser" in codegen_source
    assert "import compiler.ast_nodes" in codegen_source
    assert "from compiler.ast_nodes" in parser_source
    assert "from compiler.pypp_lexer" in parser_source


@pytest.mark.parametrize("member", list(MEMBERS))
def test_member_manifest_dev_mode_dirs_point_to_workspace_root(member):
    path = ROOT / "compiler" / member / "pyproject.toml"
    data = tomllib.loads(path.read_text())
    assert data["tool"]["hatch"]["build"]["dev-mode-dirs"] == ["../.."]


def test_wheels_contain_only_namespace_trees():
    dist_dir = ROOT / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    for member in MEMBERS:
        package = member.replace("_", "-")
        build = _run(["uv", "build", "--wheel", "--package", package])
        assert build.returncode == 0, build.stderr

    wheels = list(dist_dir.glob("*.whl"))
    assert len(wheels) == len(MEMBERS), f"expected {len(MEMBERS)} wheels, got {wheels}"

    for member in MEMBERS:
        matches = [w for w in wheels if w.name.startswith(member)]
        assert len(matches) == 1, f"expected one {member} wheel, got {matches}"
        wheel = matches[0]

        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
            namespace_prefix = f"compiler/{member}/"

            assert any(
                n.startswith(namespace_prefix) for n in names
            ), f"{wheel.name} is missing {namespace_prefix} tree"
            assert not any(
                n.startswith(f"{member}/") for n in names
            ), f"{wheel.name} contains top-level {member}/ package"
            assert "compiler/__init__.py" not in names

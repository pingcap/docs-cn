"""Regression checks for repository and documentation defaults."""

import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import yaml


ROOT = Path(__file__).resolve().parents[1]


def check_ci_security(content):
    workflow = yaml.safe_load(content)
    # PyYAML treats the unquoted "on" key as True under YAML 1.1.
    trigger = workflow.get("on", workflow.get(True))
    assert trigger == ["pull_request"], trigger
    assert workflow.get("permissions") == {"contents": "read"}
    return workflow


ci_workflow = (ROOT / ".github/workflows/ci.yaml").read_text()
workflow = check_ci_security(ci_workflow)

# Comments must not hide changes to the active trigger or permissions.
for unsafe_workflow in (
    ci_workflow.replace(
        "on: [pull_request]",
        "# on: [pull_request]\non: [pull_request_target]",
        1,
    ),
    ci_workflow.replace("contents: read", "contents: write", 1),
):
    try:
        check_ci_security(unsafe_workflow)
    except AssertionError:
        pass
    else:
        raise AssertionError("Unsafe CI configuration was accepted")

checkout_steps = [
    step
    for job in workflow["jobs"].values()
    for step in job.get("steps", [])
    if step.get("uses", "").startswith("actions/checkout@")
]
assert checkout_steps
assert all(
    step.get("with", {}).get("persist-credentials") is False
    for step in checkout_steps
)

install_commands = [
    line.split("#", 1)[0]
    for line in ci_workflow.splitlines()
    if re.search(r"\bnpm\s+ci\b", line.split("#", 1)[0])
]
assert install_commands
assert all(
    re.search(r"(?:^|\s)--ignore-scripts(?:=true)?(?:\s|$)", command)
    for command in install_commands
)
assert all("--include=dev" in command for command in install_commands)

# Exercise tool selection in an isolated fixture, without running npm or network calls.
with tempfile.TemporaryDirectory(prefix="docs-tool-check-") as directory:
    fixture = Path(directory) / "repo with spaces"
    scripts = fixture / "scripts"
    scripts.mkdir(parents=True)
    local_bin = fixture / "node_modules/.bin"
    local_bin.mkdir(parents=True)
    (fixture / "test.md").write_text("# Test\n")
    (scripts / "markdown-link-check.tpl").write_text("{}\n")

    global_bin = Path(directory) / "bin"
    global_bin.mkdir()
    forbidden_marker = Path(directory) / "global-tool-ran"
    local_marker = Path(directory) / "local-tool-ran"
    env = dict(os.environ, PATH=f"{global_bin}{os.pathsep}{os.environ['PATH']}")
    env["FORBIDDEN_TOOL_MARKER"] = str(forbidden_marker)
    env["LOCAL_TOOL_MARKER"] = str(local_marker)
    for binary in ("markdown-link-check", "remark", "npx"):
        tool = global_bin / binary
        tool.write_text('#!/bin/sh\nprintf ran > "$FORBIDDEN_TOOL_MARKER"\nexit 99\n')
        tool.chmod(0o755)

    for filename, binary in (
        ("verify-links.sh", "markdown-link-check"),
        ("verify-link-anchors.sh", "remark"),
    ):
        script = scripts / filename
        shutil.copyfile(ROOT / "scripts" / filename, script)
        tool = local_bin / binary

        def run_check():
            return subprocess.run(
                ["bash", str(script)], cwd=directory, env=env,
                capture_output=True, text=True, timeout=30,
            )

        # Neither a missing nor a non-executable local tool may trigger a fallback.
        for state in ("missing", "not executable"):
            if state == "not executable":
                tool.write_text('#!/bin/sh\nexit 0\n')
                tool.chmod(0o644)
            result = run_check()
            assert result.returncode != 0, (filename, state, result)
            assert "npm ci --ignore-scripts --include=dev" in result.stderr
            assert not forbidden_marker.exists(), (filename, state)

        tool.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$LOCAL_TOOL_MARKER"\n')
        tool.chmod(0o755)
        result = run_check()
        assert result.returncode == 0, (filename, result)
        assert local_marker.exists(), filename
        arguments = local_marker.read_text().splitlines()
        assert ("./test.md" if binary == "markdown-link-check" else "--frail") in arguments
        assert not forbidden_marker.exists(), filename
        local_marker.unlink()

deployment = (ROOT / "check-before-deployment.md").read_text()
permission_commands = [
    line.strip()
    for line in deployment.splitlines()
    if re.search(r"\bchmod\b", line)
]
unsafe_permission_patterns = (
    re.compile(r"\bchmod\b[^\n]*\b[0-7]{2,3}[2367]\b"),
    re.compile(r"\b(?:a|ugo|go|g|o)[+=][^\s,]*w"),
)
assert not any(
    pattern.search(command)
    for command in permission_commands
    for pattern in unsafe_permission_patterns
)
assert "sudo install -d -o tidb -g tidb -m 700" in deployment
assert "sudo chmod -R u=rwX,go=" in deployment

dm_quick_start = (ROOT / "dm/quick-start-with-dm.md").read_text()
assert "--nogpgcheck" not in dm_quick_start
assert "不要通过禁用签名验证来绕过错误" in dm_quick_start

vector_quick_start = (ROOT / "ai/vector-search-get-started-using-python.md").read_text()
model_calls = re.findall(
    r"SentenceTransformer\s*\((.*?)\)", vector_quick_start, re.DOTALL
)
assert model_calls
assert all(
    re.search(r"\btrust_remote_code\s*=\s*False\b", call)
    for call in model_calls
)
assert not any(
    re.search(r"\btrust_remote_code\s*=\s*True\b", call)
    for call in model_calls
)

print("safer default checks passed")

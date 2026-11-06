"""Regression checks for repository and documentation defaults."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


ci_workflow = (ROOT / ".github/workflows/ci.yaml").read_text()
install_commands = re.findall(r"run:\s*(npm ci[^\n]*)", ci_workflow)
assert install_commands
assert all("--ignore-scripts" in command for command in install_commands)
assert all("--include=dev" in command for command in install_commands)

deployment = (ROOT / "check-before-deployment.md").read_text()
assert not re.search(r"chmod(?:\s+-R)?\s+777\b", deployment)
assert "sudo install -d -o tidb -g tidb -m 700" in deployment
assert "sudo chmod -R u=rwX,go=" in deployment

dm_quick_start = (ROOT / "dm/quick-start-with-dm.md").read_text()
assert "--nogpgcheck" not in dm_quick_start
assert "不要通过禁用签名验证来绕过错误" in dm_quick_start

vector_quick_start = (ROOT / "ai/vector-search-get-started-using-python.md").read_text()
assert "trust_remote_code=True" not in vector_quick_start
assert "trust_remote_code=False" in vector_quick_start

print("safer default checks passed")

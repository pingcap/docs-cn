"""Check that deployment guidance does not prescribe published admin passwords."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HAPROXY = (ROOT / "best-practices/haproxy-best-practices.md").read_text(
    encoding="utf-8"
)
GRAFANA = (ROOT / "deploy-monitoring-services.md").read_text(encoding="utf-8")
DEFAULT_ADMIN_PASSWORD = re.compile(
    r"^\s*admin_password\s*=\s*(?:\"{1,3}|'{1,3})?admin"
    r"(?:\"{1,3}|'{1,3})?\s*(?:[;#].*)?$",
    re.IGNORECASE | re.MULTILINE,
)
DEFAULT_ADMIN_PASSWORD_EXAMPLES = (
    "admin_password=admin",
    ' admin_password = "admin"',
    "admin_password = '''admin''' # comment",
)

assert "stats auth admin:pingcap123" not in HAPROXY
assert "bind <management-ip>:8080" in HAPROXY
assert "stats auth <admin-user>:<strong-password>" in HAPROXY
assert "不要将 HAProxy 监控页面直接暴露到公网" in HAPROXY
assert "stats admin if TRUE" in HAPROXY
assert "跨站请求伪造（CSRF）" in HAPROXY

assert all(
    DEFAULT_ADMIN_PASSWORD.search(assignment)
    for assignment in DEFAULT_ADMIN_PASSWORD_EXAMPLES
)
assert not DEFAULT_ADMIN_PASSWORD.search(GRAFANA)
assert "admin_user = <grafana-admin-user>" in GRAFANA
assert 'admin_password = """<grafana-strong-password>"""' in GRAFANA
assert "不要使用 `admin` 作为密码" in GRAFANA
assert "已有实例使用当前管理员账户" in GRAFANA
assert "可以选择 **Skip**" not in GRAFANA
assert "不要选择 **Skip**" in GRAFANA

print("admin credential guidance checks passed")

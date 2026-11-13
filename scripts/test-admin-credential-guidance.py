"""Check that deployment guidance keeps monitoring administration restricted."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HAPROXY = (ROOT / "best-practices/haproxy-best-practices.md").read_text(
    encoding="utf-8"
)
GRAFANA = (ROOT / "deploy-monitoring-services.md").read_text(encoding="utf-8")
FIREWALL = (ROOT / "check-before-deployment.md").read_text(encoding="utf-8")
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
assert not re.search(
    r"^\s*stats\s+admin\s+if\s+TRUE\b", HAPROXY, re.IGNORECASE | re.MULTILINE
)
assert "stats admin if AUTH_ADMIN" in HAPROXY
assert "监控页面保持为只读" in HAPROXY

assert all(
    DEFAULT_ADMIN_PASSWORD.search(assignment)
    for assignment in DEFAULT_ADMIN_PASSWORD_EXAMPLES
)
assert not DEFAULT_ADMIN_PASSWORD.search(GRAFANA)
assert "admin_user = <grafana-admin-user>" in GRAFANA
assert 'admin_password = """<grafana-strong-password>"""' in GRAFANA
assert "不要使用 `admin` 作为密码" in GRAFANA
assert "已有实例使用当前管理员账户" in GRAFANA
assert "$__file{PATH}" in GRAFANA
assert "chmod 600 conf/grafana.ini" in GRAFANA
assert "可以选择 **Skip**" not in GRAFANA
assert "不要选择 **Skip**" in GRAFANA
assert '--web.listen-address="127.0.0.1:9090"' in GRAFANA
assert "--web.enable-admin-api" not in GRAFANA
assert "不启用 Prometheus 管理 API" in GRAFANA
assert "将 `--web.external-url` 设置为" in GRAFANA
assert "`http://127.0.0.1:9090`" in GRAFANA
assert "在 **Access** 处，选择 **Server**" in GRAFANA

assert not re.search(r"systemctl\s+(?:stop|disable)\b[^\n]*\bfirewalld\b", FIREWALL)
assert not re.search(r"--set-default-zone(?:=|\s+)trusted\b", FIREWALL)
assert "仅允许可信来源访问必需端口" in FIREWALL
assert "--add-rich-rule" in FIREWALL
assert "<management-network-cidr>" in FIREWALL
assert "<prometheus-ip>/32" in FIREWALL
assert all(
    f'port port="{port}"' in FIREWALL
    for port in (
        "2379",
        "2380",
        "8300",
        "9094",
        "10080",
        "20180",
    )
)
assert all(
    port in FIREWALL
    for port in (
        "3000",
        "3930",
        "8234",
        "9000",
        "9090",
        "9093",
        "9100",
        "9115",
        "12020",
        "20170",
        "20292",
    )
)
assert "NgMonitoring" in FIREWALL
assert "firewall-cmd --reload" in FIREWALL

print("admin credential guidance checks passed")

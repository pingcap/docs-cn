"""Check that deployment guidance does not prescribe published admin passwords."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HAPROXY = (ROOT / "best-practices/haproxy-best-practices.md").read_text()
GRAFANA = (ROOT / "deploy-monitoring-services.md").read_text()

assert "stats auth admin:pingcap123" not in HAPROXY
assert "bind <management-ip>:8080" in HAPROXY
assert "stats auth <admin-user>:<strong-password>" in HAPROXY
assert "不要将 HAProxy 监控页面直接暴露到公网" in HAPROXY
assert "stats admin if TRUE" in HAPROXY
assert "如果只需查看监控信息，请删除此配置项" in HAPROXY

assert "admin_password = admin" not in GRAFANA
assert "admin_user = <grafana-admin-user>" in GRAFANA
assert "admin_password = <grafana-strong-password>" in GRAFANA
assert "不要使用 `admin` 作为密码" in GRAFANA
assert "可以选择 **Skip**" not in GRAFANA
assert "不要选择 **Skip**" in GRAFANA

print("admin credential guidance checks passed")

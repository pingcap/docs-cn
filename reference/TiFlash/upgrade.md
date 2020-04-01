# 升级 TiFlash 节点
下载新版 TiFlash binary 到中控机
可以更新到新版 ansible，然后使用 ansible-playbook local_prepare.yml
或者手动下载 TiFlash binary 并覆盖到 resource/bin/tiflash
滚动升级 TiFlash 
ansible-playbook rolling_update.yml --tags tiflash
滚动升级 TiDB 监控组件
ansible-playbook rolling_update_monitor.yml

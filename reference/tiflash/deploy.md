# TiFlash 集群部署
## 推荐硬件配置
TiFlash 单独部署模式
  * 最低配置：32 VCore, 64 GB RAM, 1 SSD + n HDD。
  * 推荐配置：48 VCore, 128 GB RAM, 1 NVMe SSD + n SSD。

部署机器不限，最少一台即可。单台机器可以使用多盘，同时不推荐单机多实例部署。

推荐用一个 SSD 盘来缓冲 TiKV 同步数据的实时写入，该盘性能不低于 TiKV 所使用的硬盘，建议是性能更好的 NVMe SSD。该 SSD 盘容量建议不小于 10% 总容量，否则它可能成为这个节点的能承载的数据量的瓶颈。而其他硬盘，可以选择部署多块 HDD 或者普通 SSD，当然更好的硬盘会带来更好的性能。

TiFlash 支持多目录存储，所以无需使用 RAID。

TiFlash 和 TiKV 部署在相同节点模式
可以参考 TiKV 节点的硬件配置，并且适当增加内存和 CPU 核数。请不要将 TiFlash 与 TiKV 同盘部署，以防互相干扰。硬盘选择标准同上。

硬盘总容量大致为整个 TiKV 集群的需同步数据容量 / 副本数 / 2。例如整体  TiKV 的规划容量为三副本则 TiFlash 的推荐容量为 TiKV 集群的 ⅙ 。用户可以选择同步部分表数据而非全部。

## 针对 TiDB 的版本要求
目前 TiFlash 的测试基于 TiDB 3.1 版本的相关组件（TiDB、PD、TiKV、TiFlash），该版本的下载方式可参考以下安装部署步骤。

## 安装部署
目前安装部署 TiFlash 可能有两种场景：

全新部署
在原有 TiDB 集群上新增 TiFlash 组件

注意：
请确保在开启 TiFlash 进程之前开启 PD 的 Placement Rules 功能（方法见后）。
请务必确保在 TiFlash 运行期间不要关闭 Placement Rules 功能。
### 全新部署
目前全新部署 TiFlash 场景提供两种安装方式：

离线安装包安装 TiFlash
手动替换 binary 安装 TiFlash
#### 离线安装包安装 TiFlash
离线安装包安装 TiFlash 的步骤如下：

请先下载对应版本的离线包，并解压
3.1 rc版：
```
curl -o tidb-ansible-tiflash-3.1-rc.tar.gz https://download.pingcap.org/tidb-ansible-tiflash-3.1-rc.tar.gz
tar zxvf tidb-ansible-tiflash-3.1-rc.tar.gz
```
编辑 `inventory.ini` 配置文件，相比于部署 TiDB 集群的配置，需要额外在 `[tiflash_servers]` 下配置 tiflash servers 所在的 ip (目前只支持ip，不支持域名)。如果希望自定义部署目录，请配置 data_dir 参数，不需要则不加。如果希望多盘部署，则以逗号分隔各部署目录。（注意每个 data_dir 目录的上级目录需要赋予 tidb 用户写权限）例如：
```
[tiflash_servers]
192.168.1.1 data_dir=/data1/tiflash/data,/data2/tiflash/data
```
按照 ansible 部署流程 完成集群部署的剩余步骤。
验证 TiFlash 已部署成功的方式：通过 `pd-ctl store http://your-pd-address` 查询可以观测到所部署的 TiFlash 实例状态为 “Up”。

### 在原有 TiDB 集群上新增 TiFlash 组件
首先确认当前 TiDB 的版本支持 TiFlash，否则请先按照 TiDB 升级操作指南升级 TiDB 集群。
需要在 pd-ctl (tidb-ansible 目录下的 resources/bin 包含对应的二进制文件)中输入 `config set enable-placement-rules true` 命令。
编辑 `inventory.ini` 配置文件，需要在 `[tiflash_servers]` 下配置 tiflash servers 所在的 ip(目前只支持ip，不支持域名)。如果希望自定义部署目录，请配置 data_dir 参数，不需要则不加。如果希望多盘部署，则以逗号分隔各部署目录。（注意每个 data_dir 目录的上级目录需要赋予 tidb 用户写权限）例如：
```
[tiflash_servers]
192.168.1.1 data_dir=/data1/tiflash/data,/data2/tiflash/data
```
  * 注意：即使 TiFlash 与 TiKV 同机部署，TiFlash 也会采用与 TiKV 不同的默认端口，默认 9000，无特殊需要可以不用指定，有需要也可用 tcp_port=xxx 指定”

首先需要更新tidb-ansible到3.1 rc版
执行 `ansible-playbook local_prepare.yml`
执行 `ansible-playbook -t tiflash deploy.yml`
执行 `ansible-playbook -t tiflash start.yml`
执行 `ansible-playbook rolling_update_monitor.yml`
验证 TiFlash 已部署成功的方式：通过 `pd-ctl store http://your-pd-address` 查询可以观测到所部署的 TiFlash 实例状态为 “Up”

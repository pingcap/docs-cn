---
title: TiDB 弹性伸缩 & 下线方案
category: deployment
---

# TiDB 弹性伸缩 & 下线 方案

## 用户场景

被操作环境是由 tidb-ansible 部署,根据部署情况选择用户场景设置,本次案例默认操作已经做主机互信

### 主机用户场景

+ A 场景
  - 客户集群主机拥有小用户(非 root 用户,且 root 用户无法远程登录),小用户拥有 sudo 权限
  - 此时：`ansible_user` 等同于 `deploy_user`.
  - 如果未做互信请在命令后添加 `-k` 或者 `-k -K` 参数 ( -k 为 `ansible_user` 密码, -K 为 `ansible_become_user` 密码 )
  - 使用以下代码块即可

    ```
    # ssh via root:
    # ansible_user = root
    # ansible_become = true
    # ansible_become_user = tidb   
    
    # ssh via normal user
    ansible_user = tidb
    ```

+ B 场景
  - 客户集群主机有 root 权限，无服务运行小权限用户( TiDB 推荐使用非 root 用户启动进程, 当检测到用户为 root 时, 无法启动服务 )
  - 此时: `ansible_become_user` 等同 `deploy_user` ( depoly_user 不为 root )
  - 执行 deploy.yml 时需要取消 `# ansible_become = true` 注释 
  - 如果未做互信请在命令后添加 `-k` 参数，-k 为 `ansible_user` 密码
  - 使用以下代码块即可

    ```
    # ssh via root:
    ansible_user = root
    # ansible_become = true
    ansible_become_user = tidb
     
    # ssh via normal user
    #ansible_user = tidb
    ```

-----

## 扩容 & 修复节点

扩容与修复单节点方式类似  

扩容 PD 与 TiKV TiDB 操作步骤不同, 操作时请分开操作

### 现有集群

最小集群规模,更多请参考[部署建议](https://github.com/pingcap/docs-cn/blob/master/op-guide/recommendation.md)

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3, Monitor|
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |


### 扩容 tikv & tidb

本次新增 tidb3 与 tikv4 

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3, Monitor |
| **node101** | **172.16.10.101**|**TiDB3** |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |
| **node102** | **172.16.10.102**|**TiKV4** |

以下为具体操作步骤

- 更新 inventory.ini 文件
    - 添加 IP 到 inventory.ini 
    - 注意修改用户场景
- 初始化新增机器
    - 之前机器不会被初始化，只会操作新机器，需要 root 权限
     `ansible-playbook bootstrap.yml -D`
- 在新节点部署相应服务
    - 不会影响已存在的服务运行  
     `ansible-playbook deploy.yml -D`
- 滚动重启节点
     `ansible-playbook rolling_update.yml --tags=tidb -l 172.16.10.101`
     `ansible-playbook rolling_update.yml --tags=tikv -l 172.16.10.102`


### 扩容 PD 节点

tikv tidb 需要更新配置文件中 pd 参数，所以扩容 PD 节点需要滚动重启所有节点。

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3,Monitor | 
| **node104** | **172.16.10.104**|**PD4** |
| node101 | 172.16.10.101|TiDB3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |
| node102 | 172.16.10.102 | TiKV4 |

以下为具体操作步骤

- 更新 inventory.ini 文件
    - 添加 IP 到 inventory.ini 
    - 注意修改用户场景
- 初始化新增机器
    - 之前机器不会被初始化，只会操作新机器，需要 root 权限
     `ansible-playbook bootstrap.yml -D`
- 在新节点部署相应服务
    - 不会影响已存在的服务运行  
     `ansible-playbook deploy.yml -D`
- 登录新增 pd 节点
    - 修改 PD 配置文件
        - `{{ deploy_dir }}/scripts/run_pd.sh`
        - 删除 `--initial-cluster=""`
        - 新增 `--join="http://172.16.10.1:2379"`
    - 手动启动 PD 节点
        - `{deploy_dir}/scripts/start_pd.sh`
    - 通过 pd-api 查看是否有相应的节点信息
        - `curl http://172.16.10.1:2379/pd/api/v1/members` 
- 滚动重启 tidb & tikv 节点，滚动重启时刷新 tidb & tikv 配置文件
    `ansible-playbook rolling_update.yml --tags=tidb`
    `ansible-playbook rolling_update.yml --tags=tikv`


-----

## 下线

### 下线 TiDB 节点

下线 TiDB 节点不影响后端服务

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| **node2** | **172.16.10.2** | PD2, **TiDB2** |
| node3 | 172.16.10.3 | PD3,Monitor | 
| node104 | 172.16.10.104|PD4 |
| node101 | 172.16.10.101|TiDB3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |
| node102 | 172.16.10.102 | TiKV4 |


以下为具体操作步骤

- 更新 inventory.ini 文件
    - 在 inventory.ini 删除相应 TiDB 节点信息
- 更新负载均衡信息
    - 在负载均衡器内删除节点信息
- ssh 登录相应 TiDB 节点
    - 停止 TiDB 服务
        - `{deploy_dir}/scripts/stop_tidb.sh`
    - 随后可选择是否删除 TiDB 目录
        - 本次示例中 TiDB 目录还有 PD 服务，因此不可删除 `{{deploy_dir}}`

### 下线 TiKV 节点

下线 TiKV 节点不影响后端服务;一旦执行下线后，不可取消相应操作，请谨慎操作。  


| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3,Monitor | 
| node104 | 172.16.10.104|PD4 |
| node101 | 172.16.10.101|TiDB3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| **node6** | **172.16.10.6** | **TiKV3** |
| node102 | 172.16.10.102 | TiKV4 |


以下为具体操作步骤

- 使用 pd-ctl 工具检查 `replica-schedule-limit` 参数
    - `./pd-ctl -u "http://172.16.10.1:2379"`
        - config show
            - { "replica-schedule-limit": 8  } // 控制 TIKV 下线速度;如果为 0 , 不执行下线操作
            - `config set replica-schedule-limit 4 ` // 最多同时进行 4 个 replica 调度
- 使用 pd-ctl 工具下线 TiKV 节点
    - `./pd-ctl -u "http://172.16.10.1:2379"`
        - stote //查询 172.16.10.5 tikv 节点 ID，例如 ID 为 3
        - store delete 3 // 下线store 3
        - stote 3 // 查询 store 状态是否为 offline 
    - 更多用法参考[PD Control 使用说明](https://github.com/pingcap/docs-cn/blob/master/op-guide/pd-control.md)
- 更新 inventory.ini 文件
    - 在 inventory.ini 删除相应 TiKV 节点信息
- 等待 TiKV 节点变成 Tombstone 状态后执行以下操作
- ssh 登录相应 TiKV 节点
    - 停止 TiKV 服务
        - {deploy_dir}/scripts/stop_tikv.sh
    - 随后可选择是否删除 TiKV 目录
- 重新启用该 TiKV 节点
    - {deploy_dir} 未被删除且 TiKV 状态已经为 Tombstone 。
    - 检查该节点 TIKV 服务是否还在运行，如果为运行状态，请关闭。  
        - `{deploy_dir}/scripts/stop_tikv.sh`
    - 删除 data 目录
        - `{deploy_dir}/data`
    - 重新启动 TiKV 服务
        - `{deploy_dir}/scripts/start_tikv.sh`
    - 观察日志是否正确运行
        - 如果正常，更新 inventory.ini 


### 下线 PD 节点

 下线 PD 节点，剩余线上运行 PD 节点数量请保持单数。

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| **node3** | **172.16.10.3** | **PD3**,Monitor | 
| node104 | 172.16.10.104|PD4 |
| node101 | 172.16.10.101|TiDB3 |
| node4 | 172.16.10.4 | TiKV1 |
| node5 | 172.16.10.5 | TiKV2 |
| node6 | 172.16.10.6 | TiKV3 |
| node102 | 172.16.10.102 | TiKV4 |



以下为具体操作步骤

- 使用 pd-ctl 工具下线 PD 节点
    - `./pd-ctl -u "http://172.16.10.1:2379"`
        - member // 显示所有成员的信息
        - member leader  // 显示 leader 的信息
        - member delete name pd3 // 下线 "pd3" ; RC4 版本以上使用本步骤
        - member delete pd3 // 下线 "pd3" ; RC4 版本以前使用本步骤
    - 更多用法参考[PD Control 使用说明](https://github.com/pingcap/docs-cn/blob/master/op-guide/pd-control.md#member-leader--delete)
- 下线后停止 PD 服务
     - `{deploy_dir}/scripts/stop_pd.sh`
     - 随后可选择是否删除 PD 目录
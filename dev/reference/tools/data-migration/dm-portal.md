---
title: DM Portal 简介
category: reference
---

# DM Portal 简介

当前版本的 DM 提供了丰富多样的功能特性，包括 [Table routing](/reference/tools/data-migration/features/overview.md#table-routing)，[Black & white table lists](/reference/tools/data-migration/features/overview.md#black-white-table-lists)，[Binlog event filter](/reference/tools/data-migration/features/overview.md#binlog-event-filter)，[Column mapping](/reference/tools/data-migration/features/overview.md#column-mapping) 等。但这些功能特性同时也增加了用户使用 DM 的复杂度，尤其在编写 [DM 任务配置](/reference/tools/data-migration/configure/task-configuration-file.md)的时候。

针对这个问题，DM 提供了一个精简的网页程序 DM Portal，能够帮助用户以可视化的方式去配置需要的同步任务，并且生成可以直接让 DM 直接执行的 `task.yaml` 文件。

## 功能描述

### 同步模式配置

支持 DM 的三种同步模式：

- 全量同步
- 增量同步
- All（全量+增量）

### 实例信息配置

支持配置库表同步路由方式，能够支持 DM 中分库分表合并的配置方式。

### binlog 过滤配置

支持对数据库、数据表配置 binlog event 过滤。

### 配置文件生成

支持配置文件创建，能够将配置文件下载到本地并且同时会在 dm-portal 服务器的 `/tmp/` 目录下自动创建。

### 使用限制

当前的 DM 配置可视化生成页面能够覆盖绝大部分的 DM 配置场景，但也有一定的使用限制：

- 不支持 [Column mapping](/reference/tools/data-migration/features/overview.md#column-mapping)
- 不支持 [Binlog event filter](/reference/tools/data-migration/features/overview.md#binlog-event-filter) 的 SQL pattern 方式
- 编辑功能不支持解析用户之前写的 `task.yaml` 文件，页面只能编辑由页面生成的 `task.yaml` 文件
- 编辑功能不支持修改实例配置信息，如果用户需要调整实例配置，需要重新生成 `task.yaml` 文件
- 页面的上游实例配置仅用于获取上游库表结构，DM-worker 里依旧需要配置对应的上游实例信息
- 生成的 `task.yaml` 中，默认 mydumper-path 为 `./bin/mydumper`，如果实际使用其他路径，需要在生成的配置文件中进行手动修改。

## 部署使用

### Binarey 部署

DM Portal 可以在 [dm-portal-latest.tar.gz](https://download.pingcap.org/dm-portal-latest.tar.gz) 下载，通过 `./dm-portal` 的命令即可直接启动。

* 如果在本地启动，浏览器访问 `127.0.0.1:8280` 即可使用。
* 如果在服务器上启动，需要为服务器上配置访问代理。

### DM Ansible 部署

可以使用 DM Ansible 部署 DM Portal，具体部署方法参照[使用 DM Ansible 部署 DM 集群](/how-to/deploy/data-migration-with-ansible.md)。

## 使用说明

### 新建规则

#### 功能描述

用于新建一个 `task.yaml` 文件，需要选择同步模式、配置上下游实例、配置库表路由，配置 binlog 过滤。

#### 操作步骤

* 登录 dm-portal 页面，点击**新建任务规则**。

### 基础信息配置

#### 功能描述

用于填写任务名称，以及选择任务类型。

#### 前置条件

已选择**新建同步规则**。

#### 操作步骤

* 填写任务名称。
* 选择任务类型。
![DM Portal BasicConfig](/media/dm-portal-basicconfig.png)

### 实例信息配置

#### 功能描述

用于配置上下游实例信息，包括 Host、Port、Username、Password。

#### 前置条件

已填写任务名称和选择任务类型。

#### 注意事项

如果任务类型选择**增量**或者 **All**，在配置上游实例信息时候，还需要配置 binlog-file 和 binlog-pos。

#### 操作步骤

* 填写上游实例信息。
* 填写下游实例信息。
* 点击**下一步**。

![DM Portal InstanceConfig](/media/dm-portal-instanceconfig.png)

### binlog 过滤配置

#### 功能描述

用于配置上游的 binlog 过滤，可以选择需要过滤的 DDL/DML，并且在数据库上配置的 filter 后会自动给其下的数据表继承。

#### 前置条件

已经配置好上下游实例信息并且连接验证没问题。

#### 注意事项

* binlog 过滤配置只能在上游实例处进行修改编辑，一旦数据库或者数据表被移动到下游实例后，就不可以进行修改编辑。
* 在数据库上配置的 binlog 过滤会自动被其下的数据表继承。

#### 操作步骤

* 点击需要配置的数据库或者数据表。
* 点击编辑按钮，选择需要过滤的 binlog 类型。

![DM Portal InstanceShow](/media/dm-portal-instanceshow.png)

![DM Portal BinlogFilter 1](/media/dm-portal-binlogfilter-1.png)

![DM Portal BinlogFilter 2](/media/dm-portal-binlogfilter-2.png)

### 库表路由配置

#### 功能描述

可以选择需要同步的数据库和数据表，并且进行修改名称、合并库、合并表等操作。可以对上一步操作进行撤销，可以对库表路由配置进行全部重置。在完成任务配置后，DM Portal 会帮忙生成对应的 `task.yaml` 文件。

#### 前置条件

* 已经配置好需要的 binlog 过滤规则。

#### 注意事项

* 在合并库表操作的时候，不允许批量操作，只能一个个拖动。
* 在合表库表操作的时候，只能对数据表进行拖动操作，不能对数据库进行数据库进行拖动操作。

#### 操作步骤

* 在**上游实例**处，选择需要同步的数据库和数据表。
* 点击移动按钮，将需要同步的库表移动至**下游实例**处。
* 点击右键按钮，可以对库表进行改名操作。
* 选中需要操作的数据表，可以拖动至别的数据表图标上创建出合并表；可以拖动到数据库图标上移动至该库下；可以拖动到 target-instance 图标上移动到一个新的数据库下。
* 点击**完成**，自动下载 `task.yaml` 到本地，并且在 DM Portal 服务器上的 `/tmp/` 目录下自动创建一份 `task.yaml` 配置文件。

##### 移动同步库表

![DM Portal TableRoute 1](/media/dm-portal-tableroute-1.png)

![DM Portal TableRoute 2](/media/dm-portal-tableroute-2.png)

##### 右键修改库表名称

![DM Portal ChangeTableName](/media/dm-portal-changetablename.png)

##### 合并数据表操作

![DM Portal MergeTable 1](/media/dm-portal-mergetable-1.png)

![DM Portal MergeTable 2](/media/dm-portal-mergetable-2.png)

##### 移动数据表至其他数据库

![DM Portal MoveToDB 1](/media/dm-portal-movetodb-1.png)

![DM Portal MoveToDB 2](/media/dm-portal-movetodb-2.png)

##### 移动数据表至新建默认数据库

![DM Portal MoveToNewDB 1](/media/dm-portal-movetonewdb-1.png)

![DM Portal MoveToNewDB 2](/media/dm-portal-movetonewdb-2.png)

##### 撤销本次操作

![DM Portal Revert](/media/dm-portal-revert.png)

##### 清空下游实例

![DM Portal Reset](/media/dm-portal-reset.png)

##### 完成并下载

![DM Portal GenerateConfig](/media/dm-portal-generateconfig.png)

### 编辑规则

#### 功能描述

可以将之前创建的 `task.yaml` 上传后，解析出来之前的填写的配置信息，对部分配置进行修改。

#### 前置条件

* 已经创建出 `task.yaml` 文件。
* 非 DM Portal 创建出来的 `task.yaml` 文件不可使用。

#### 注意事项

* 不允许修改实例配置信息

#### 操作步骤

* 在首页，点击**编辑同步规则**。
* 选择上传 `task.yaml` 文件。
* 解析成功后，页面会自动跳转。

![DM Portal EditConfig](/media/dm-portal-editconfig.png)

![DM Portal UploadConfig](/media/dm-portal-uploadconfig.png)

---
title: 从 Parquet 文件迁移数据到 TiDB
summary: 介绍如何使用 TiDB Lightning 从 Parquet 文件迁移数据到 TiDB。
---

# 从 Parquet 文件迁移数据到 TiDB

本文介绍如何从 Apache Hive 中生成 Parquet 文件以及如何使用 TiDB Lightning 从 Parquet 文件迁移数据到 TiDB。

如果你从 Amazon Aurora 中导出 Parquet 文件，请参照[从 Amazon Aurora 迁移数据到 TiDB](/migrate-aurora-to-tidb.md)。

## 前提条件

- [使用 TiUP 安装 TiDB Lightning](/migration-tools.md)
- [获取 TiDB Lightning 所需下游数据库权限](/tidb-lightning/tidb-lightning-requirements.md#目标数据库权限要求)

## 第 1 步：准备 Parquet 文件

本节描述如何从 Hive 中导出能被 TiDB Lightning 读取的 Parquet 文件。

Hive 中每个表都能通过标注 `STORED AS PARQUET LOCATION '/path/in/hdfs'` 的形式将表数据导出到 Parquet 文件中。因此，如果你需要导出一张名叫 `test` 的表，请执行以下步骤：

1. 在 Hive 中执行如下 SQL 语句：

    ```sql
    CREATE TABLE temp STORED AS PARQUET LOCATION '/path/in/hdfs'
    AS SELECT * FROM test;
    ```

    执行上述语句后，表数据就成功导出到 HDFS 系统里。

2. 使用 `hdfs dfs -get` 命令将 Parquet 文件导出到本地：

    ```shell
    hdfs dfs -get /path/in/hdfs /path/in/local
    ```

    完成导出后，如果你需要将 HDFS 里导出的 Parquet 文件删除，可以直接将这个临时表 (`temp`) 删掉：

    ```sql
    DROP TABLE temp;
    ```

3. 从 Hive 导出的 Parquet 文件可能不带有 `.parquet` 的后缀，无法被 TiDB Lightning 正确识别。因此，在进行导入之前，需要对导出的文件进行重命名，添加 `.parquet` 后缀，将完整的文件名修改为 TiDB Lightning 能识别的格式 `${db_name}.${table_name}.parquet`。更多文件类型和命名规则，请参考 [TiDB Lightning 数据源](/tidb-lightning/tidb-lightning-data-source.md)。你也可以通过设置正确的[自定义表达式](/tidb-lightning/tidb-lightning-data-source.md#自定义文件匹配)匹配数据文件。

4. 将所有 Parquet 文件放到统一目录下，例如 `/data/my_datasource/` 或 `s3://my-bucket/sql-backup`。TiDB Lightning 将递归地寻找该目录及其子目录内的所有 `.parquet` 文件。

## 第 2 步：创建目标表结构

在将 Parquet 文件导入 TiDB 前，你必须为 Parquet 文件提供表结构。你可以通过以下任一方法创建表结构：

* **方法一**：使用 TiDB Lightning 创建表结构。

    编写包含 DDL 语句的 SQL 文件：

    - 文件名格式为 `${db_name}-schema-create.sql`，其内容需包含 `CREATE DATABASE` 语句。
    - 文件名格式为 `${db_name}.${table_name}-schema.sql`，其内容需包含 `CREATE TABLE` 语句。

* **方法二**：手动在下游 TiDB 建库和表。

## 第 3 步：编写配置文件

新建文件 `tidb-lightning.toml`，包含以下内容：

```toml
[lightning]
# 日志
level = "info"
file = "tidb-lightning.log"

[tikv-importer]
# "local"：默认使用该模式，适用于 TiB 级以上大数据量，但导入期间下游 TiDB 无法对外提供服务。
backend = "local"
# # "tidb"：TiB 级以下数据量也可以采用 `tidb` 后端模式，下游 TiDB 可正常提供服务。关于导入模式更多信息请参阅：https://docs.pingcap.com/zh/tidb/stable/tidb-lightning-overview#tidb-lightning-整体架构
# 设置排序的键值对的临时存放地址，目标路径必须是一个空目录，目录空间须大于待导入数据集的大小。建议设为与 `data-source-dir` 不同的磁盘目录并使用闪存介质，独占 I/O 会获得更好的导入性能。
sorted-kv-dir = "${sorted-kv-dir}"

[mydumper]
# 源数据目录
data-source-dir = "${data-path}" # 本地或 S3 路径，例如：'s3://my-bucket/sql-backup'

[tidb]
# 目标集群的信息
host = ${host}                # 例如：172.16.32.1
port = ${port}                # 例如：4000
user = "${user_name}"         # 例如："root"
password = "${password}"      # 例如："rootroot"
status-port = ${status-port}  # 导入过程 Lightning 需要在从 TiDB 的“状态端口”获取表结构信息，例如：10080
pd-addr = "${ip}:${port}"     # 集群 PD 的地址，Lightning 通过 PD 获取部分信息，例如 172.16.31.3:2379。当 backend = "local" 时 status-port 和 pd-addr 必须正确填写，否则导入将出现异常。
```

关于配置文件更多信息，可参阅 [TiDB Lightning 配置参数](/tidb-lightning/tidb-lightning-configuration.md)。

## 第 4 步：执行导入

1. 运行 `tidb-lightning`。

    - 如果从 Amazon S3 导入，需先将有权限访问该 S3 后端存储的账号的 SecretKey 和 AccessKey 作为环境变量传入 Lightning 节点。

        ```shell
        export AWS_ACCESS_KEY_ID=${access_key}
        export AWS_SECRET_ACCESS_KEY=${secret_key}
        ```

        此外，TiDB Lightning 还支持从 `~/.aws/credentials` 读取凭证文件。

    - 如果直接在命令行中启动程序，可能会因为 `SIGHUP` 信号而退出，建议配合 `nohup` 或 `screen` 等工具运行 `tidb-lightning`：

        ```shell
        nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out 2>&1 &
        ```

2. 导入开始后，可以采用以下任意方式查看进度：

    - 通过 `grep` 日志关键字 `progress` 查看进度，默认 5 分钟更新一次。
    - 通过监控面板查看进度，请参考 [TiDB Lightning 监控](/tidb-lightning/monitor-tidb-lightning.md)。
    - 通过 Web 页面查看进度，请参考 [Web 界面](/tidb-lightning/tidb-lightning-web-interface.md)。

    导入完毕后，TiDB Lightning 会自动退出。

3. 检查导入是否成功。

    查看 `tidb-lightning.log` 日志末尾是否有 `the whole procedure completed` 信息，如果有，表示导入成功。如果没有，则表示导入遇到了问题，可根据日志中的 error 提示解决遇到的问题。

    > **注意：**
    >
    > 无论导入成功与否，最后一行都会显示 `tidb lightning exit`。它只是表示 TiDB Lightning 正常退出，不代表任务完成。

如果导入过程中遇到问题，请参见 [TiDB Lightning 常见问题](/tidb-lightning/tidb-lightning-faq.md)。

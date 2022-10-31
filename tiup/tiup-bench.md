---
title: 使用 TiUP bench 组件压测 TiDB
aliases: ['/docs-cn/dev/tiup/tiup-bench/','/docs-cn/dev/reference/tools/tiup/bench/']
---

# 使用 TiUP bench 组件压测 TiDB

在测试数据库性能时，经常需要对数据库进行压测，为了满足这一需求，TiUP 集成了 bench 组件。TiUP bench 组件提供多种压测的 workloads ，其命令入口如下：

{{< copyable "shell-root" >}}

```bash
tiup bench tpcc   # 以 TPC-C 作为 workload 压测
tiup bench tpch   # 以 TPC-H 作为 workload 压测
tiup bench ch     # 以 CH-benCHmark 作为 workload 压测
tiup bench ycsb   # 以 YCSB 作为 workload 压测
tiup bench rawsql # 以自定义 SQL 文件作为 workload 压测
```

其中 tpcc, tpch, ch, rawsql 支持如下命令行参数：

```bash
  -t, --acThreads int         OLAP 并发线程数，仅适用于 CH-benCHmark (默认 1)
      --conn-params string    数据库连接参数，例如：
                              `--conn-params tidb_isolation_read_engines='tiflash'` 设置 TiDB 查询走 TiFlash ，
                              `--conn-params sslmode=disable` 设置连接 PostgreSQL 不启用加密
      --count int             总执行次数, 0 表示无限次
  -D, --db string             被压测数据库名称 (默认为 "test")
  -d, --driver string         数据库驱动: mysql, postgres (默认 "mysql")
      --dropdata              在 prepare 之前清除历史数据
  -h, --help                  bench 命令自身的帮助信息
  -H, --host strings          数据库的主机地址 (默认 ["127.0.0.1"])
      --ignore-error          忽略压测时数据库报出的错误
      --interval duration     两次报告输出时间的间隔 (默认 10s)
      --isolation int         隔离级别 0: Default, 1: ReadUncommitted,
                              2: ReadCommitted, 3: WriteCommitted, 4: RepeatableRead,
                              5: Snapshot, 6: Serializable, 7: Linerizable
      --max-procs int         runtime.GOMAXPROCS
      --output string         输出格式 plain, table, json (default "plain")
  -p, --password string       数据库密码
  -P, --port ints             数据库端口 (默认 [4000])
      --pprof string          pprof 地址
      --silence               压测过程中不打印错误信息
  -S, --statusPort int        TiDB 状态端口 (默认 10080)
  -T, --threads int           压测并发线程数 (默认 16)
      --time duration         总执行时长 (默认 2562047h47m16.854775807s)
  -U, --user string           压测时使用的数据库用户 (默认 "root")
```

- `--host` 和 `--port` 支持以逗号分隔传入多个值，以启用客户端负载均衡，例如指定 `--host 172.16.4.1,172.16.4.2 --port 4000,4001` 时，负载程序将以 round-robin 方式连接到 172.16.4.1:4000, 172.16.4.1:4001, 172.16.4.2:4000, 172.16.4.2:4001 这 4 个实例上。
- `--conn-params` 需要符合 [query string](https://en.wikipedia.org/wiki/Query_string) 格式，不同数据库支持不同参数，如：
  - `--conn-params tidb_isolation_read_engines='tiflash'` 设置 TiDB 查询走 TiFlash 。
  - `--conn-params sslmode=disable` 设置连接 PostgreSQL 不启用加密。
- 当运行 CH-benCHmark 时，可以通过 `--ap-host`, `--ap-port`, `--ap-conn-params` 来指定独立的 tidb 实例用于 AP 查询。

下文分别介绍如何使用 TiUP 运行 TPC-C, TPC-H 以及 YCSB 测试。

## 使用 TiUP 运行 TPC-C 测试

TiUP bench 组件支持如下运行 TPC-C 测试的命令和参数：

```bash
Available Commands:
  check       检查数据一致性
  cleanup     清除数据
  prepare     准备数据
  run         开始压测

Flags:
      --check-all            运行所有的一致性检测
  -h, --help                 tpcc 的帮助信息
      --partition-type int   分区类型 (默认 1)
                             1: HASH, 2: RANGE,
                             3: LIST (like HASH),
                             4: LIST (like RANGE)
      --parts int            分区仓库 的数量 (默认 1)
      --warehouses int       仓库的数量 (默认 10)
```

### TPC-C 测试步骤

完整的测试流程可以参考[如何对 TiDB 进行 TPC-C 测试](/benchmark/benchmark-tidb-using-tpcc.md)，下面列举简化步骤：

1. 通过 HASH 使用 4 个分区创建 4 个仓库：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 --parts 4 prepare
    ```

2. 运行 TPC-C 测试：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 --time 10m run
    ```

3. 检查一致性：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 check
    ```

4. 清理数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 cleanup
    ```

当需要测试大数据集时，直接写入通常较慢，也可以通过如下命令生成 csv 数据集，然后通过 [lightning](/tidb-lightning/tidb-lightning-overview.md) 导入。

- 生成 CSV 文件：

  {{< copyable "shell-regular" >}}

  ```shell
  tiup bench tpcc --warehouses 4 prepare --output-dir data --output-type=csv
  ```

- 为指定的表生成 CSV 文件：

  {{< copyable "shell-regular" >}}

  ```shell
  tiup bench tpcc --warehouses 4 prepare --output-dir data --output-type=csv --tables history,orders
  ```

## 使用 TiUP 运行 TPC-H 测试

TiUP bench 组件支持如下运行 TPC-H 测试的命令和参数：

```bash
Available Commands:
  cleanup     清除数据
  prepare     准备数据
  run         开始压测

Flags:
      --check            检查输出数据，只有 scale 因子为 1 时有效
  -h, --help             tpch 的帮助信息
      --queries string   所有的查询语句 (默认 "q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22")
      --sf int           scale 因子
```

## TPC-H 测试步骤

1. 准备数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

2. 运行 TPC-H 测试，根据是否检查结果执行相应命令：

    - 检查结果：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup bench tpch --count=22 --sf=1 --check=true run
        ```

    - 不检查结果：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup bench tpch --count=22 --sf=1 run
        ```

3. 清理数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch cleanup
    ```

## 使用 TiUP 运行 YCSB 测试

### 测试 TiDB

1. 准备数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench ycsb load tidb -p tidb.instances="127.0.0.1:4000" -p recordcount=10000
    ```

2. 运行 YCSB 测试：

    {{< copyable "shell-regular" >}}

    ```shell
    # 默认读写比例为 95:5
    tiup bench ycsb run tidb -p tidb.instances="127.0.0.1:4000" -p operationcount=10000
    ```

### 测试 TiKV

1. 准备数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench ycsb load tikv -p tikv.pd="127.0.0.1:2379" -p recordcount=10000
    ```

2. 运行 YCSB 测试：

    {{< copyable "shell-regular" >}}

    ```shell
    # 默认读写比例为 95:5
    tiup bench ycsb run tikv -p tikv.pd="127.0.0.1:2379" -p operationcount=10000
    ```

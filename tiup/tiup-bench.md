---
title: 使用 TiUP bench 组件压测 TiDB
aliases: ['/docs-cn/dev/tiup/tiup-bench/','/docs-cn/dev/reference/tools/tiup/bench/']
---

# 使用 TiUP bench 组件压测 TiDB

在测试数据库性能时，经常需要对数据库进行压测，为了满足这一需求，TiUP 集成了 bench 组件。目前，TiUP bench 组件提供 TPC-C 和 TPC-H 两种压测的 workload，其命令参数如下：

{{< copyable "shell-root" >}}

```bash
tiup bench
```

```
Starting component `bench`: /home/tidb/.tiup/components/bench/v1.5.0/bench 
Benchmark database with different workloads

Usage:
  tiup bench [command]

Available Commands:
  help        帮助信息
  tpcc        以 TPC-C 作为 workload 压测
  tpch        以 TPC-H 作为 workload 压测

Flags:
      --count int           总执行次数, 0 表示无限次
  -D, --db string           被压测数据库名称 (默认为 "test")
  -d, --driver string       数据库驱动: mysql
      --dropdata            在 prepare 之前清除历史数据
  -h, --help                bench 命令自身的帮助信息
  -H, --host string         数据库的主机地址 (默认 "127.0.0.1")
      --ignore-error        忽略压测时数据库报出的错误
      --interval duration   两次报告输出时间的间隔 (默认 10s)
      --isolation int       隔离级别 0: Default, 1: ReadUncommitted, 
                            2: ReadCommitted, 3: WriteCommitted, 4: RepeatableRead, 
                            5: Snapshot, 6: Serializable, 7: Linerizable
      --max-procs int       runtime.GOMAXPROCS
  -p, --password string     数据库密码
  -P, --port int            数据库端口 (默认 4000)
      --pprof string        pprof 地址
      --silence             压测过程中不打印错误信息
      --summary             只打印 Summary
  -T, --threads int         压测并发线程数 (默认 16)
      --time duration       总执行时长 (默认 2562047h47m16.854775807s)
  -U, --user string         压测时使用的数据库用户 (默认 "root")
```

下文分别介绍如何使用 TiUP 运行 TPC-C 测试和 TPC-H 测试。

## 使用 TiUP 运行 TPC-C 测试

TiUP bench 组件支持如下运行 TPC-C 测试的命令和参数：

```bash
Available Commands:
  check       检查数据一致性
  cleanup     清除数据
  prepare     准备数据
  run         开始压测

Flags:
      --check-all        运行所有的一致性检测
  -h, --help             tpcc 的帮助信息
      --output string    准备数据时生成 csv 文件的目录
      --parts int        分区仓库 的数量(默认 1)
      --tables string    指定用于生成文件的表，多个表用逗号分割，只有设置了 output 时才有效。默认生成所有的表
      --warehouses int   仓库的数量 (默认 10)
```

### TPC-C 测试步骤

1. 通过 HASH 使用 4 个分区创建 4 个仓库：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 --parts 4 prepare
    ```

2. 运行 TPC-C 测试：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 run
    ```

3. 清理数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 cleanup
    ```

4. 检查一致性：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 check
    ```

5. 生成 CSV 文件：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data
    ```

6. 为指定的表生成 CSV 文件：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data --tables history,orders
    ```

7. 开启 pprof：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data --pprof :10111
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
        tiup bench tpch --sf=1 --check=true run
        ```

    - 不检查结果：

        {{< copyable "shell-regular" >}}

        ```shell
        tiup bench tpch --sf=1 run
        ```

3. 清理数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch cleanup
    ```

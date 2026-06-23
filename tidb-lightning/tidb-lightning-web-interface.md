---
title: TiDB Lightning Web 界面
summary: 了解 TiDB Lightning Web 界面的移除以及推荐的替代方案。
---

# TiDB Lightning Web 界面

> **警告：**
>
> 从 TiDB v8.5.7 开始，TiDB Lightning 不再支持 Web 界面。从 v8.5.6 开始，TiDB Lightning Web 界面已废弃。实际上，该 Web UI 自 v8.4.0 起已无法正常构建。

要使用 TiDB Lightning 导入数据，请使用 TiDB Lightning 命令行工具：`tidb-lightning` 用于导入任务，`tidb-lightning-ctl` 用于 checkpoint 和故障排查操作。

- 关于基本操作流程，参见 [TiDB Lightning 快速上手](/get-started-with-tidb-lightning.md)。
- 关于命令行参数，参见 [TiDB Lightning 命令行参数](/tidb-lightning/tidb-lightning-command-line-full.md)。

要检查导入进度，可以在 TiDB Lightning 日志中搜索 `progress` 关键字，或使用 [TiDB Lightning 监控面板](/tidb-lightning/monitor-tidb-lightning.md)。

对于新的数据导入负载，你也可以使用 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句。

> **注意：**
>
> 如果你使用的是仍带有 TiDB Lightning Web 界面的早期版本 TiDB，可以参考以下内容。

TiDB Lightning 支持在网页上查看导入进度或执行一些简单任务管理，这就是 TiDB Lightning 的**服务器模式**。本文将介绍服务器模式下的 Web 界面和一些常见操作。

启用服务器模式的方式有如下几种：

1. 在启动 `tidb-lightning` 时加上命令行参数 `--server-mode`。

    ```sh
    tiup tidb-lightning --server-mode --status-addr :8289
    ```

2. 在配置文件中设置 `lightning.server-mode`。

    ```toml
    [lightning]
    server-mode = true
    status-addr = ':8289'
    ```

TiDB Lightning 启动后，可以访问 `http://127.0.0.1:8289` 来管理程序（实际的 URL 取决于你的 `status-addr` 设置）。

服务器模式下，TiDB Lightning 不会立即开始运行，而是通过用户在 web 页面提交（多个）**任务**来导入数据。

## TiDB Lightning Web 首页

![TiDB Lightning Web 首页](/media/lightning-web-frontpage.png)

标题栏上图标所对应的功能，从左到右依次为：

| 图标 | 功能 |
|:----|:----|
| "TiDB Lightning" | 点击即返回首页 |
| ⚠ | 显示**前一个**任务的所有错误信息 |
| ⓘ | 列出当前及队列中的任务，可能会出现一个标记提示队列中任务的数量 |
| + | 提交单个任务 |
| ⏸/▶ | 暂停/继续当前操作 |
| ⟳ | 设置网页自动刷新 |

标题栏下方的三个面板显示了不同状态下的所有表：

* Active：当前正在导入这些表
* Completed：这些表导入成功或失败
* Pending：这些表还没有被处理

每个面板都包含用于描述表状态的卡片。

## 提交任务

点击标题栏的 **+** 图标提交任务。

![提交任务对话框](/media/lightning-web-submit.png)

任务 (task) 为 TOML 格式的文件，具体参考 [TiDB Lightning 任务配置](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)。你也可以点击 **UPLOAD** 上传一个本地的 TOML 文件。

点击 **SUBMIT** 运行任务。如果当前有任务正在运行，新增任务会加入队列并在当前任务结束后执行。

## 查看导入进度

点击首页表格卡片上的 **>** 图标，查看表格导入的详细进度。

![表格导入进度](/media/lightning-web-table.png)

该页显示每张表的引擎文件的导入过程。

点击标题栏上的 **TiDB Lightning** 返回首页。

## 管理任务

单击标题栏上的 **ⓘ** 图标来管理当前及队列中的任务。

![任务管理页面](/media/lightning-web-queue.png)

每个任务都是依据提交时间来标记。点击该任务将显示 JSON 格式的配置文件。

点击任务上的 **⋮** 可以对该任务进行管理。你可以立即停止任务，或重新排序队列中的任务。

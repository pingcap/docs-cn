---
title: TiDB Lightning Web 界面
summary: 了解 TiDB Lightning 的服务器模式——通过 Web 界面来控制 TiDB Lightning。
---

# TiDB Lightning Web 界面

TiDB Lightning 支持在网页上查看导入进度或执行一些简单任务管理，这就是 TiDB Lightning 的**服务器模式**。本文将介绍服务器模式下的 Web 界面和一些常见操作。

启用服务器模式的方式有如下几种：

1. 在启动 `tidb-lightning` 时加上命令行参数 `--server-mode`。

    ```sh
    ./tidb-lightning --server-mode --status-addr :8289
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

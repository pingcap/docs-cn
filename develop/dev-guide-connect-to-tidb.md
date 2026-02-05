---
title: 连接到 TiDB
summary: 连接到 TiDB 的方式概览。
---

# 连接到 TiDB

TiDB 高度兼容 MySQL 协议，这使得大多数客户端驱动程序和 ORM 框架可以像连接到 MySQL 一样地连接到 TiDB。

- 如需手动执行 SQL（用于连接测试、调试或快速验证），可以通过 [MySQL CLI 工具](/develop/dev-guide-mysql-tools.md) 连接到 TiDB。

- 如果希望通过图形界面工具进行连接，可参考以下常用 GUI 工具的相关文档：

    - [JetBrains DataGrip](/develop/dev-guide-gui-datagrip.md)
    - [DBeaver](/develop/dev-guide-gui-dbeaver.md)
    - [VS Code](/develop/dev-guide-gui-vscode-sqltools.md)
    - [MySQL Workbench](/develop/dev-guide-gui-mysql-workbench.md)
    - [Navicat](/develop/dev-guide-gui-navicat.md)

- 如需基于 TiDB 构建应用程序，可以根据所使用的编程语言和框架[选择合适的驱动或 ORM](/develop/dev-guide-choose-driver-or-orm.md)。

- 如需从边缘环境通过 HTTP 连接到 {{{ .starter }}} 或 {{{ .essential }}} 集群，可以使用 [TiDB Cloud Serverless Driver](/develop/serverless-driver.md)。需要注意的是，Serverless Driver 目前处于 beta 阶段，仅适用于 {{{ .starter }}} 或 {{{ .essential }}} 集群。

## 需要帮助？

- 在 [AskTUG 论坛](https://asktug.com/?utm_source=docs-cn-dev-guide) 上提问
- [提交 TiDB Cloud 工单](https://tidb.support.pingcap.com/servicedesk/customer/portals)
- [提交 TiDB 工单](/support.md)
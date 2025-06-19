---
title: ticloud serverless sql-user delete
summary: `ticloud serverless sql-user delete` 命令的参考。
---

# ticloud serverless sql-user delete

删除 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user delete [flags]
```

## 示例

在交互模式下删除 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user delete
```

在非交互模式下删除 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user delete -c <cluster-id> --user <user-name>
```

## 标志

在非交互模式下，你需要手动输入必需的标志。在交互模式下，你只需按照 CLI 提示填写即可。

| 标志                    | 描述                                | 是否必需 | 说明                                    |
|-------------------------|-------------------------------------|----------|------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                     | 是       | 仅在非交互模式下生效。                  |
| --force                 | 删除 SQL 用户时不需要确认。         | 否       | 仅在非交互模式下生效。                  |
| -h, --help              | 显示此命令的帮助信息。              | 否       | 在非交互模式和交互模式下都有效。        |

## 继承的标志

| 标志                  | 描述                                                                                     | 是否必需 | 说明                                                                                                |
|----------------------|------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                        | 否       | 仅在非交互模式下生效。在交互模式下，对某些 UI 组件禁用颜色可能不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。         | 否       | 在非交互模式和交互模式下都有效。                                                                      |
| -D, --debug          | 启用调试模式。                                                                            | 否       | 在非交互模式和交互模式下都有效。                                                                      |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

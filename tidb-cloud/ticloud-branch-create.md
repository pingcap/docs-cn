---
title: ticloud serverless branch create
summary: `ticloud serverless branch create` 命令的参考。
---

# ticloud serverless branch create

为 TiDB Cloud Serverless 集群创建一个[分支](/tidb-cloud/branch-overview.md)：

```shell
ticloud serverless branch create [flags]
```

## 示例

在交互模式下为 TiDB Cloud Serverless 集群创建分支：

```shell
ticloud serverless branch create
```

在非交互模式下为 TiDB Cloud Serverless 集群创建分支：

```shell
ticloud serverless branch create --cluster-id <cluster-id> --display-name <branch-name>
```

在非交互模式下从另一个分支的指定时间点创建分支：

```shell
ticloud serverless branch create --cluster-id <cluster-id> --display-name <branch-name> --parent-id <parent-branch-id> --parent-timestamp <parent-timestamp>
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志                  | 描述                                                                                               | 是否必需 | 说明                                                |
|---------------------------|-----------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| -c, --cluster-id string   | 指定要在其中创建分支的集群 ID。                                     | 是      | 仅在非交互模式下有效。                 |
| -n, --display-name string | 指定要创建的分支名称。                                                           | 是      | 仅在非交互模式下有效。                 |
| --parent-id string        | 指定父分支的 ID。默认值为集群 ID。                                                       | 否       | 仅在非交互模式下有效。                 |
| --parent-timestamp string | 指定父分支的时间戳，格式为 RFC3339，例如 `2024-01-01T00:00:00Z`。默认值为当前时间。  | 否       | 仅在非交互模式下有效。                 |
| -h, --help                | 显示此命令的帮助信息。                                                                  | 否       | 在非交互和交互模式下都可用。 |

## 继承的参数标志

| 参数标志             | 描述                                                                                          | 是否必需 | 说明                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。 |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下都可用。                                                             |
| -D, --debug          | 启用调试模式。                                                                                   | 否       | 在非交互和交互模式下都可用。                                                             |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。

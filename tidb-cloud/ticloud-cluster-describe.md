---
title: ticloud serverless cluster describe
summary: `ticloud serverless describe` 命令的参考。
---

# ticloud serverless describe

获取 TiDB Cloud Serverless 集群的信息（例如集群配置和集群状态）：

```shell
ticloud serverless describe [flags]
```

或使用以下别名命令：

```shell
ticloud serverless get [flags]
```

## 示例

在交互模式下获取 TiDB Cloud Serverless 集群的信息：

```shell
ticloud serverless describe
```

在非交互模式下获取 TiDB Cloud Serverless 集群的信息：

```shell
ticloud serverless describe --cluster-id <cluster-id>
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志                | 描述                       | 是否必需 | 说明                                                 |
|-------------------------|-----------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。             | 是      | 仅在非交互模式下有效。                  |
| -h, --help              | 显示此命令的帮助信息。 | 否       | 在非交互和交互模式下都可用。 |

## 继承的参数标志

| 参数标志             | 描述                                                                                          | 是否必需 | 说明                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。 |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下都可用。                                                             |
| -D, --debug          | 启用调试模式。                                                                                    | 否       | 在非交互和交互模式下都可用。                                                             |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建一个 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。

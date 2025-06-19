---
title: ticloud serverless cluster list
summary: `ticloud serverless list` 命令的参考。
---

# ticloud serverless list

列出项目中的所有 TiDB Cloud Serverless 集群：

```shell
ticloud serverless list [flags]
```

或使用以下别名命令：

```shell
ticloud serverless ls [flags]
```

## 示例

在交互模式下列出所有 TiDB Cloud Serverless 集群：

```shell
ticloud serverless list
```

在非交互模式下列出指定项目中的所有 TiDB Cloud Serverless 集群：

```shell
ticloud serverless list -p <project-id>
```

在非交互模式下以 JSON 格式列出指定项目中的所有 TiDB Cloud Serverless 集群：

```shell
ticloud serverless list -p <project-id> -o json
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志               | 描述                                                                                                              | 是否必需 | 说明                                                 |
|------------------------|------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -p, --project-id string | 指定项目的 ID。                                                                                                   | 是       | 仅在非交互模式下有效。                               |
| -h, --help             | 显示此命令的帮助信息。                                                                                           | 否       | 在非交互和交互模式下均有效。                         |
| -o, --output string    | 指定输出格式（默认为 `human`）。有效值为 `human` 或 `json`。要获取完整结果，请使用 `json` 格式。               | 否       | 在非交互和交互模式下均有效。                         |

## 继承的参数标志

| 参数标志              | 描述                                                                                                | 是否必需 | 说明                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                   | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                   | 否       | 在非交互和交互模式下均有效。                                                                           |
| -D, --debug          | 启用调试模式。                                                                                       | 否       | 在非交互和交互模式下均有效。                                                                           |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

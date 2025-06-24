---
title: ticloud serverless region
summary: `ticloud serverless region` 命令的参考。
aliases: ['/tidbcloud/ticloud-serverless-regions']
---

# ticloud serverless region

列出 TiDB Cloud Serverless 的所有可用地域：

```shell
ticloud serverless region [flags]
```

## 示例

列出 TiDB Cloud Serverless 的所有可用地域：

```shell
ticloud serverless region
```

以 JSON 格式列出 TiDB Cloud Serverless 集群的所有可用地域：

```shell
ticloud serverless region -o json
```

## 标志

在非交互模式下，你需要手动输入必需的标志。在交互模式下，你只需按照 CLI 提示填写即可。

| 标志                | 描述                                                                                                              | 是否必需 | 注意                                                 |
|---------------------|--------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -o, --output string | 指定输出格式（默认为 `human`）。有效值为 `human` 或 `json`。要获取完整结果，请使用 `json` 格式。 | 否       | 在非交互和交互模式下都有效。 |
| -h, --help          | 显示此命令的帮助信息。                                                                                       | 否       | 在非交互和交互模式下都有效。 |

## 继承的标志

| 标志                 | 描述                                                                                | 是否必需 | 注意                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                  | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。 |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下都有效。                                                             |
| -D, --debug          | 启用调试模式。                                                                         | 否       | 在非交互和交互模式下都有效。                                                             |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建[议题](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

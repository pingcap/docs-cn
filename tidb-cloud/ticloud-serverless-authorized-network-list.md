---
title: ticloud serverless authorized-network list
summary: `ticloud serverless authorized-network list` 命令的参考文档。
---

# ticloud serverless authorized-network list

列出所有授权网络：

```shell
ticloud serverless authorized-network list [flags]
```

## 示例

在交互模式下列出所有授权网络：

```shell
ticloud serverless authorized-network list
```

在非交互模式下列出所有授权网络：

```shell
ticloud serverless authorized-network list -c <cluster-id>
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写这些信息。

| 参数标志                 | 描述                                                                                                   | 是否必需 | 说明                                 |
|------------------------|--------------------------------------------------------------------------------------------------------|----------|-------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                                                                                          | 是       | 仅在非交互模式下有效。                |
| --output string        | 指定输出格式（默认为 `human`）。有效值为 `human` 或 `json`。要获取完整结果，请使用 `json` 格式。          | 否       | 在非交互和交互模式下均可使用。         |
| -h, --help             | 显示此命令的帮助信息。                                                                                    | 否       | 在非交互和交互模式下均可使用。         |

## 继承的参数标志

| 参数标志              | 描述                                                                                    | 是否必需 | 说明                                                                                      |
|----------------------|----------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------|
| --no-color          | 禁用输出中的颜色。                                                                      | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                      |
| -P, --profile string | 指定此命令使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。          | 否       | 在非交互和交互模式下均可使用。                                                              |
| -D, --debug         | 启用调试模式。                                                                          | 否       | 在非交互和交互模式下均可使用。                                                              |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。

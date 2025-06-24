---
title: ticloud serverless export download
summary: `ticloud serverless export download` 命令的参考。
---

# ticloud serverless export download

将 TiDB Cloud Serverless 集群的导出数据下载到本地存储：

```shell
ticloud serverless export download [flags]
```

## 示例

在交互模式下下载导出数据：

```shell
ticloud serverless export download
```

在非交互模式下下载导出数据：

```shell
ticloud serverless export download -c <cluster-id> -e <export-id>
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志               | 描述                                                                                                | 是否必需 | 说明                                                 |
|------------------------|-----------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                                                                                      | 是       | 仅在非交互模式下有效。                               |
| -e, --export-id string  | 指定导出任务的 ID。                                                                                  | 是       | 仅在非交互模式下有效。                               |
| --output-path string    | 指定保存下载数据的目标路径。如果未指定，数据将下载到当前目录。                                      | 否       | 仅在非交互模式下有效。                               |
| --concurrency int       | 指定下载并发数。默认值为 `3`。                                                                       | 否       | 在非交互和交互模式下均有效。                         |
| --force                 | 无需确认直接下载导出数据。                                                                           | 否       | 在非交互和交互模式下均有效。                         |
| -h, --help             | 显示此命令的帮助信息。                                                                               | 否       | 在非交互和交互模式下均有效。                         |

## 继承的参数标志

| 参数标志              | 描述                                                                                                | 是否必需 | 说明                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                   | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                   | 否       | 在非交互和交互模式下均有效。                                                                           |
| -D, --debug          | 启用调试模式。                                                                                       | 否       | 在非交互和交互模式下均有效。                                                                           |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

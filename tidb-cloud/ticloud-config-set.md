---
title: ticloud config set
summary: `ticloud config set` 命令的参考。
---

# ticloud config set

配置活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)的属性：

```shell
ticloud config set <property-name> <value> [flags]
```

可以配置的属性包括 `public-key`、`private-key` 和 `api-url`。

| 属性        | 描述                                                              | 是否必需 |
|-------------|------------------------------------------------------------------|----------|
| public-key  | 指定 TiDB Cloud API 的公钥。                                      | 是       |
| private-key | 指定 TiDB Cloud API 的私钥。                                      | 是       |
| api-url     | 指定 TiDB Cloud 的基础 API URL（默认为 `https://api.tidbcloud.com`）。| 否       |

> **注意：**
>
> 如果你想为特定用户配置文件配置属性，可以在命令中添加 `-P` 标志并指定目标用户配置文件名称。

## 示例

为活动配置文件设置 public-key 的值：

```shell
ticloud config set public-key <public-key>
```

为特定配置文件 `test` 设置 public-key 的值：

```shell
ticloud config set public-key <public-key> -P test
```

设置 API 主机：

```shell
ticloud config set api-url https://api.tidbcloud.com
```

> **注意：**
>
> TiDB Cloud API URL 默认为 `https://api.tidbcloud.com`。通常情况下，你不需要设置它。

## 标志

| 标志       | 描述                     |
|------------|--------------------------|
| -h, --help | 显示此命令的帮助信息。   |

## 继承的标志

| 标志                  | 描述                                                                                     | 是否必需 | 说明                                                                                                |
|----------------------|------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                        | 否       | 仅在非交互模式下生效。在交互模式下，对某些 UI 组件禁用颜色可能不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。         | 否       | 在非交互模式和交互模式下都有效。                                                                      |
| -D, --debug          | 启用调试模式。                                                                            | 否       | 在非交互模式和交互模式下都有效。                                                                      |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

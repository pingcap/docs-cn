---
title: ticloud config create
summary: `ticloud config create` 命令的参考。
---

# ticloud config create

创建[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)以存储用户配置设置：

```shell
ticloud config create [flags]
```

> **注意：**
>
> 在创建用户配置文件之前，你需要[创建 TiDB Cloud API 密钥](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

## 示例

在交互模式下创建用户配置文件：

```shell
ticloud config create
```

在非交互模式下创建用户配置文件：

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## 标志

在非交互模式下，你需要手动输入必需的标志。在交互模式下，你只需按照 CLI 提示填写即可。

| 标志                  | 描述                                   | 是否必需 | 说明                                    |
|-----------------------|----------------------------------------|----------|------------------------------------------|
| -h, --help            | 显示此命令的帮助信息。                 | 否       | 在非交互模式和交互模式下都有效。        |
| --private-key string  | 指定 TiDB Cloud API 的私钥。           | 是       | 仅在非交互模式下生效。                  |
| --profile-name string | 指定配置文件的名称（不能包含 `.`）。   | 是       | 仅在非交互模式下生效。                  |
| --public-key string   | 指定 TiDB Cloud API 的公钥。           | 是       | 仅在非交互模式下生效。                  |

## 继承的标志

| 标志                  | 描述                                                                                     | 是否必需 | 说明                                                                                                |
|----------------------|------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                        | 否       | 仅在非交互模式下生效。在交互模式下，对某些 UI 组件禁用颜色可能不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。         | 否       | 在非交互模式和交互模式下都有效。                                                                      |
| -D, --debug          | 启用调试模式。                                                                            | 否       | 在非交互模式和交互模式下都有效。                                                                      |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

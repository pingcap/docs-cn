---
title: ticloud config describe
summary: `ticloud config describe` 命令的参考。
---

# ticloud config describe

获取特定[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)的属性信息：

```shell
ticloud config describe <profile-name> [flags]
```

或使用以下别名命令：

```shell
ticloud config get <profile-name> [flags]
```

## 示例

描述用户配置文件：

```shell
ticloud config describe <profile-name>
```

## 标志

| 标志       | 描述              |
|------------|--------------------------|
| -h, --help | 显示此命令的帮助信息。 |

## 继承的标志

| 标志                 | 描述                                   | 是否必需 | 注意                                                                                                                    |
|----------------------|-----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                      | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。 |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下都有效。                                                                      |
| -D, --debug          | 启用调试模式。                                                                                   | 否       | 在非交互和交互模式下都有效。                                                             |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建[议题](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。

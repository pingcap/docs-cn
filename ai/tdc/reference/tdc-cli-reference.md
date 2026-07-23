---
title: tdc CLI 参考
summary: 参考 tdc 全局参数、输出与查询行为、dry-run 规则、help 形式、错误、命令 family 和文件系统 alias。
---

# tdc CLI 参考

本文说明 tdc 命令 surface 共享的行为。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 语法

```text
tdc <command> [subcommand] [required flags] [optional flags] [global flags]
```

tdc 仅接受长 flag，`-p` 之类的单字母 flag 会被拒绝。

生成的 usage 中，required flag 位于 optional flag 之前，optional flag 使用方括号：

```text
tdc db describe-db-cluster
  --db-cluster-id <string>
  [--output <string>]
  [--view <string>]
```

## 全局 flag

| Flag | 说明 |
| --- | --- |
| `--profile <string>` | 选择本地 profile，默认为 `default` |
| `--region <string>` | 为当前命令覆盖 canonical region |
| `--output <string>` | 输出 `json` 或 `text`，默认为 `json` |
| `--query <string>` | 在输出前应用 JMESPath expression |
| `--debug` | 输出已脱敏 debug diagnostic |
| `--help` | 显示帮助 |
| `--version` | 显示 tdc 版本信息 |

## 输出

结构化 control-plane 命令默认返回 JSON：

```bash
tdc db list-db-clusters
```

使用 text 输出进行终端查看：

```bash
tdc db list-db-clusters --output text
```

`tdc fs read-file` 和 `tdc fs copy-file --to-stdout` 等 raw byte 命令会直接写出文件内容。

## JMESPath query

`--query` 在命令成功后、输出渲染前执行：

```bash
tdc db list-db-clusters \
  --query 'clusters[].{id:id,name:display_name,state:state}'

tdc organization list-projects \
  --query 'projects[?type == `tidbx_virtual`].id' \
  --output text
```

无效 expression 会失败，不会用 partial output 替换命令结果。

## Dry-run

会修改资源的 control-plane 命令会显式声明 `--dry-run`。命令先验证本地参数、profile、凭证、region 和请求结构，然后输出执行计划，但不修改远端资源。

```bash
tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

只读命令拒绝 `--dry-run`。Dry run 不是通用的全局模拟参数，只在命令帮助明确显示时可用。

## Help 与 version 形式

```bash
tdc help
tdc db help
tdc db create-db-cluster help
tdc --help
tdc db --help
tdc db create-db-cluster --help
tdc --version
tdc fs --version
```

`help` 是导航命令树的 command，`--help` 是每个命令上的惯例 flag，两者有意共存。

## 错误与退出行为

人类可读错误使用稳定 prefix：

```text
tdc [ERROR]: <message>
```

错误写入 stderr，成功结果写入 stdout。用法和配置错误会在修改远端资源前以非零状态码退出；运行时和远端 API 错误同样返回非零状态码。交互式配置被中断时返回退出码 `130`。

`--debug` 可以显示已脱敏 request 和 resolution context，但不得显示 API key、FS token、DB password、SQL text、file content 或 connection string。

## 命令 family

| 命令 | 用途 |
| --- | --- |
| `tdc configure` | 配置本地 profile |
| `tdc update` | 检查或应用 release update |
| `tdc organization` | 查看 project |
| `tdc db` | 管理 Starter cluster、branch 和 SQL |
| `tdc fs` | 管理文件系统、file、layer、pack 和 mount |
| `tdc fs-git` | 管理 mounted filesystem 上的 Git workspace |
| `tdc fs-journal` | 管理可验证 journal |
| `tdc fs-vault` | 管理 secret 和 delegated access |

查看完整命令和 flag：

```bash
tdc <family> help
tdc <family> <command> help
```

## 文件系统 alias mapping

| Alias | Canonical command |
| --- | --- |
| `cp` | `copy-file` |
| `cat` | `read-file` |
| `ls` | `list-files` |
| `stat` | `describe-file` |
| `mv` | `move-file` |
| `rm` | `delete-file` |
| `mkdir` | `create-directory` |
| `chmod` | `chmod-file` |
| `symlink` | `create-symlink` |
| `hardlink` | `create-hardlink` |
| `grep` | `search-file-content` |
| `find` | `find-files` |
| `mount` | `mount-file-system` |
| `drain` | `drain-file-system` |
| `umount` | `unmount-file-system` |

Alias 与 canonical command 使用相同的长参数、认证、输出、查询和错误行为。

## 相关文档

- [安装、配置和更新 tdc](/ai/tdc/guides/tdc-install-configure-update.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)

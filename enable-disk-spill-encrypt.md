---
title: 为 TiDB 落盘文件开启加密
summary: 了解如何为 TiDB 落盘文件开启加密。
---

# 为 TiDB 落盘文件开启加密

当配置项 `oom-use-tmp-storage` 为 `true` 时，如果单条 SQL 语句的内存使用超出 `mem-quota-query` 的限制，某些算子可以将执行时的中间结果作为临时文件落盘保存，直到查询执行完成之后将它们删除。

用户可以开启落盘文件加密功能，防止攻击者通过读取临时文件来访问数据。

## 配置方法

要启用落盘文件加密功能，可以在 TiDB 配置文件中的 `[security]` 部分，配置 [`spilled-file-encryption-method`](/tidb-configuration-file.md#spilled-file-encryption-method) 选项：

```toml
[security]
spilled-file-encryption-method = "aes128-ctr"
```

`spilled-file-encryption-method` 的可选值为 `aes128-ctr` 和 `plaintext`。默认值为 `plaintext`，表示不启用加密。

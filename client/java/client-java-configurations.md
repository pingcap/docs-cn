---
title: Java Client 配置参数
aliases: ['/docs-cn/dev/client/java/client-java-configuration/','/docs-cn/dev/reference/client/java/client-java-configuration/']
---

# Java Client 配置参数

本文介绍了与部署使用 Java Client 相关的配置参数。

## ThreadPool 配置 JVM 参数

以下包括 ThreadPool 相关的参数及其默认配置，可通过 JVM 参数传入。

```
# Client 端 batchGet 请求的线程池大小
tikv.batch_get_concurrency=20
# Client 端 batchPut 请求的线程池大小
tikv.batch_put_concurrency=20
# Client 端 batchDelete 请求的线程池大小
tikv.batch_delete_concurrency=20
# Client 端 batchScan 请求的线程池大小
tikv.batch_scan_concurrency=5
# Client 端 deleteRange 请求的线程池大小
tikv.delete_range_concurrency=20
```
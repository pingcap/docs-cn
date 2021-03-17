---
title: 使用 Java Client
---

# 使用 Java Client

Java Client 是一个 TiKV 的客户端, 可以通过 gRPC 直接连接 TiKV。

Java Client 的最新版本可以在这里下载：[下载地址](https://github.com/tikv/client-java/releases)

也可以通过 Maven 依赖在 Jar 包中使用 Java Client。

```xml
<dependency>
    <groupId>org.tikv</groupId>
    <artifactId>tikv-client-java</artifactId>
    <version>3.1.0</version>
</dependency>
```

## 编译最新版本的 Java Client

通过 github 拉取最新代码后，可以通过以下命令编译最新的 Java Client：

```commandline
mvn clean install -Dmaven.test.skip=true
```

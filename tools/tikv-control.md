---
title: TiKV Control 使用说明
category: tools
---

# TiKV Control 使用说明

TiKV Control (tikv-ctl) 是随 TiKV 附带的一个简单的管理工具，以下简称 tikv-ctl。
在编译 tikv 时，tikv-ctl 命令也会同时被编译出来，而通过 ansible 部署的集群，在
对应的 `tidb-ansible/resources/bin` 目录下也会有这个二进制文件。

## 通用参数

tikv-ctl 有两种运行模式：远程模式和本地模式。前者通过 `--host` 选项接受 TiKV
的服务地址作为参数，后者则需要 `--db` 选项来指定本地 TiKV 数据目录路径。对于
远程模式，如果 TiKV 启动了 SSL，则 tikv-ctl 也需要指定相关的证书文件，例如：

> $ tikv-ctl --ca-path ca.pem --cert-path client.pem --key-path client-key.pem --host 127.0.0.1:21060 <subcommands>

除此之外，tikv-ctl 还有两个简单的命令 `--to-hex` 和 `--to-escaped`，用于对 key
的形式作简单的变换。一般我们使用 `escaped` 形式。一个简单的例子如下：

> $ tikv-ctl --to-escaped 0xaaff
> \252\377
> $ tikv-ctl --to-hex "\252\377"
> AAFF

注意在命令行上指定 `escaped` 形式的 key 时，需要用双引号引起来，否则 bash 会将
反斜杠吃掉，从而得到错误的结果。

---
title: 部署 TiDB Lightning
aliases: ['/docs-cn/dev/tidb-lightning/deploy-tidb-lightning/','/docs-cn/dev/reference/tools/tidb-lightning/deployment/']
---

# 部署 TiDB Lightning

本文主要介绍 TiDB Lightning 进行数据导入的硬件需求，以及手动部署 TiDB Lightning 的方式。Lightning 不同的导入模式，其硬件要求有所不同，请先阅读：

- [Physical Import Mode 必要条件及限制](/tidb-lightning/tidb-lightning-physical-import-mode.md#必要条件及限制)
- [Logical Import Mode 必要条件及限制](/tidb-lightning/tidb-lightning-logical-import-mode.md#必要条件及限制)

## 使用 TiUP 联网部署（推荐）

1. 执行如下命令安装 TiUP 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

   安装完成后，`~/.bashrc` 已将 TiUP 加入到路径中，你需要新开一个终端或重新声明全局变量 `source ~/.bashrc` 来使用 TiUP。(也可能是`~/.profile`，以 TiUP 输出为准。)

2. 安装 TiUP DM 组件：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install tidb-lightning
    ```

## 手动部署

### 下载 TiDB Lightning 安装包

参考[工具下载](/download-ecosystem-tools.md)文档下载 TiDB Lightning 安装包（TiDB Lightning 完全兼容较低版本的 TiDB 集群，建议选择最新稳定版本）。

解压 Lightning 压缩包即可获得 `tidb-lightning` 可执行文件。

```bash
tar -zxvf tidb-lightning-${version}-linux-amd64.tar.gz
chmod +x tidb-lightning
```

### 升级 TiDB Lightning

你可以通过替换二进制文件升级 TiDB Lightning，无需其他配置。重启 TiDB Lightning 的具体操作参见 [FAQ](/tidb-lightning/tidb-lightning-faq.md#如何正确重启-tidb-lightning)。

如果当前有运行的导入任务，推荐任务完成后再升级 TiDB Lightning。否则，你可能需要从头重新导入，因为无法保证断点可以跨版本工作。
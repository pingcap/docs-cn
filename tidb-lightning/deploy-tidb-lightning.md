---
title: Deploy TiDB Lightning
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
aliases: ['/docs/dev/tidb-lightning/deploy-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/deployment/']
---

# Deploy TiDB Lightning

This document describes the hardware requirements of using TiDB Lightning to import data, and how to deploy it manually. Requirements on hardware resources vary with the import modes. For details, refer to the following docs:

- [Physical Import Mode Requirements and Limitations](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)
- [Logical Import Mode Requirements and Limitations](/tidb-lightning/tidb-lightning-logical-import-mode.md)

## Online deployment using TiUP (recommended)

1. Install TiUP using the following command:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    This command automatically adds TiUP to the `PATH` environment variable. You need to start a new terminal session or run `source ~/.bashrc` before you can use TiUP. (According to your environment, you may need to run `source ~/.profile`. For the specific command, check the output of TiUP.)

2. Install TiDB Lightning using TiUP:

    ```shell
    tiup install tidb-lightning
    ```

## Manual deployment

### Download TiDB Lightning binaries

Refer to [Download TiDB Tools](/download-ecosystem-tools.md) and download TiDB Lightning binaries. TiDB Lightning is completely compatible with early versions of TiDB. It is recommended to use the latest version of TiDB Lightning.

Unzip the TiDB Lightning binary package to obtain the `tidb-lightning` executable file:

```bash
tar -zxvf tidb-lightning-${version}-linux-amd64.tar.gz
chmod +x tidb-lightning
```

### Upgrade TiDB Lightning

You can upgrade TiDB Lightning by replacing the binaries alone without further configurations. After the upgrade, you need to restart TiDB Lightning. For details, see [How to properly restart TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning).

If an import task is running, we recommend you to wait until it finishes before upgrading TiDB Lightning. Otherwise, there might be chances that you need to reimport from scratch, because there is no guarantee that checkpoints work across versions.

---
title: Create a Private Mirror
summary: Learn how to create a private mirror.
aliases: ['/tidb/dev/tiup-mirrors','/docs/dev/tiup/tiup-mirrors/','/docs/dev/reference/tools/tiup/mirrors/']
---

# Create a Private Mirror

When creating a private cloud, usually, you need to use an isolated network environment, where the official mirror of TiUP is not accessible. Therefore, you can create a private mirror, which is mainly implemented by the `mirror` command. You can also use the `mirror` command for offline deployment.

## TiUP `mirror` overview

Execute the following command to get the help information of the `mirror` command:

{{< copyable "shell-regular" >}}

```bash
tiup mirror --help
```

```bash
The 'mirror' command is used to manage a component repository for TiUP, you can use
it to create a private repository, or to add new component to an existing repository.
The repository can be used either online or offline.
It also provides some useful utilities to help managing keys, users and versions
of components or the repository itself.
Usage:
  tiup mirror <command> [flags]
Available Commands:
  init        Initialize an empty repository
  sign        Add signatures to a manifest file
  genkey      Generate a new key pair
  clone       Clone a local mirror from remote mirror and download all selected components
  publish     Publish a component
Flags:
  -h, --help          help for mirror
      --repo string   Path to the repository
Global Flags:
      --skip-version-check   Skip the strict version check, by default a version must be a valid SemVer string
Use "tiup mirror [command] --help" for more information about a command.
```

The `tiup mirror clone` command is used to build a local mirror. The basic usage is as follows:

{{< copyable "shell-regular" >}}

```bash
tiup mirror clone <target-dir> [global-version] [flags]
```

- `target-dir`: used to specify the directory in which cloned data is stored.
- `global-version`: used to quickly set a global version for all components.

The `tiup mirror clone` command provides many optional flags (might provide more in the future). These flags can be divided into the following categories according to their intended usages:

- Determines whether to use prefix matching to match the version when cloning

    If the `--prefix` flag is specified, the version number is matched by prefix for the clone. For example, if you specify `--prefix` as "v5.0.0", then "v5.0.0-rc", and "v5.0.0" are matched.

- Determines whether to use the full clone

    If you specify the `--full` flag, you can clone the official mirror fully.

    > **Note:**
    >
    > If `--full`, `global-version` flags, and the component versions are not specified, only some meta information is cloned.

- Determines whether to clone packages from the specific platform

    If you want to clone packages only for a specific platform, use `-os` and `-arch` to specify the platform. For example:

    - Execute the `tiup mirror clone <target-dir> [global-version] --os=linux` command to clone for linux.
    - Execute the `tiup mirror clone <target-dir> [global-version] --arch=amd64` command to clone for amd64.
    - Execute the `tiup mirror clone <target-dir> [global-version] --os=linux --arch=amd64` command to clone for linux/amd64.

- Determines whether to clone a specific version of a package

    If you want to clone only one version (not all versions) of a component, use `--<component>=<version>` to specify this version. For example:

    - Execute the `tiup mirror clone <target-dir> --tidb v5.1.0` command to clone the v5.1.0 version of the TiDB component.
    - Execute the `tiup mirror clone <target-dir> --tidb v5.1.0 --tikv all` command to clone the v5.1.0 version of the TiDB component and all versions of the TiKV component.
    - Execute the `tiup mirror clone <target-dir> v5.1.0` command to clone the v5.1.0 version of all components in a cluster.

## Usage examples

This section introduces the usage examples of the `mirror` command.

The repository that is cloned using `tiup mirror clone` can be shared among hosts either by sharing the files via SCP, NFS or by making the repository available over the HTTP or HTTPS protocol. Use `tiup mirror set <location>` to specify the location of the repository.

Refer to [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md#method-2-deploy-tiup-offline) to install the TiUP offline mirror, deploy a TiDB cluster, and start it.

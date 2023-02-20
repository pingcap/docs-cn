---
title: Manage TiUP Components with TiUP Commands
summary: Learn how to manage TiUP components using TiUP commands.
aliases: ['/tidb/dev/manage-tiup-component','/docs/dev/tiup/manage-tiup-component/','/docs/dev/reference/tools/tiup/manage-component/']
---

# Manage TiUP Components with TiUP Commands

You can use the following TiUP commands to manage components in the TiUP ecosystem:

- list: Queries the component list. By using this TiUP command, you can see all the optional components to install and all the optional versions of each component.
- install: Installs the specific version of a component.
- update: Updates a component to the latest version.
- uninstall: Uninstalls a component.
- status: Checks the status of a running component.
- clean: Cleans up the instance on which a component is deployed.
- help: Prints the help information. If you append another TiUP command to this command, the usage of the appended command is printed.

This document introduces the common component management operations and the corresponding TiUP commands.

## Query the component list

You can use the `tiup list` command to query the component list. This usage of this command is as follows:

- `tiup list`: checks which components can be installed.
- `tiup list ${component}`: checks which versions of a specific component can be installed.

You can also use the following flags in the above commands:

- `--installed`: checks which components or which version of a specific component has been installed locally.
-`--all`: views all components, including the hidden ones
-`--verbose`: views all columns (including installed versions and supported platforms)

Example 1: View all currently installed components.

{{< copyable "shell-regular" >}}

```shell
tiup list --installed
```

Example 2: Get a list of the TiKV component of all installable versions from the server.

{{< copyable "shell-regular" >}}

```shell
tiup list tikv
```

## Install components

You can use the `tiup install` command to query the component list. This usage of this command is as follows:

- `tiup install <component>`: installs the latest stable version of a specified component.
- `tiup install <component>:[version]`: installs the specified version of a specified component.

Example 1: Use TiUP to install the latest stable version of TiDB.

{{< copyable "shell-regular" >}}

```shell
tiup install tidb
```

Example 2: Use TiUP to install the nightly version of TiDB.

{{< copyable "shell-regular" >}}

```shell
tiup install tidb:nightly
```

Example 3: Use TiUP to install TiKV v6.6.0.

{{< copyable "shell-regular" >}}

```shell
tiup install tikv:v6.6.0
```

## Upgrade components

After a new version of a component is published, you can use the `tiup update` command to upgrade this component. The usage of this command is basically the same as that of `tiup install`, except for the following flags:

- `--all`: Upgrades all components.
- `--nightly`: Upgrades to the nightly version.
- `--self`: Upgrades TiUP itself to the latest version.
- `--force`: Forcibly upgrades to the latest version.

Example 1: Upgrade all components to the latest versions.

{{< copyable "shell-regular" >}}

```shell
tiup update --all
```

Example 2: Upgrade all components to the nightly version.

{{< copyable "shell-regular" >}}

```shell
tiup update --all --nightly
```

Example 3: Upgrade TiUP to the latest version.

{{< copyable "shell-regular" >}}

```shell
tiup update --self
```

## Operate components

After the installation is complete, you can use the `tiup <component>` command to start the corresponding component:

```shell
tiup [flags] <component>[:version] [args...]

Flags:
  -T, --tag string                     Specifies the tag for the component instance.
```

To use this command, you need to specify the component name and the optional version. If no version is specified, the latest stable version (installed) of this component is used.

Before the component is started, TiUP creates a directory for it, and then puts this component into the directory for operation. The component generates all the data in this directory, and the name of this directory is the tag name specified when the component operates. If no tag is specified, a tag name is randomly generated. This working directory will be *automatically deleted* when the instance is terminated.

If you want to start the same component multiple times and reuse the previous working directory, you can use `--tag` to specify the same name when the component is started. After the tag is specified, the working directory will *not be automatically deleted* when the instance is terminated, which makes it convenient to reuse the working directory.

Example 1: Operate TiDB v6.6.0.

{{< copyable "shell-regular" >}}

```shell
tiup tidb:v6.6.0
```

Example 2: Specify the tag with which TiKV operates.

{{< copyable "shell-regular" >}}

```shell
tiup --tag=experiment tikv
```

### Query the operating status of a component

You can use the `tiup status` command to check the operating status of a component:

{{< copyable "shell-regular" >}}

```shell
tiup status
```

By executing this command, you will get a list of instances, one instance per line. The list contains the following columns:

- `Name`: The tag name of the instance.
- `Component`: The component name of the instance.
- `PID`: The process ID of the operating instance.
- `Status`: The instance status. `RUNNING` means that the instance is operating. `TERM` means that the instance is terminated.
- `Created Time`: The starting time of the instance.
- `Directory`: The working directory of the instance, which can be specified using `--tag`.
- `Binary`: The executable program of the instance, which can be specified using `--binpath`.
- `Args`: The arguments of the operating instance.

### Clean component instance

You can use the `tiup clean` command to clean up component instances and delete the working directory. If the instance is still operating before the cleaning, the related process is killed first. The command usage is as follows:

{{< copyable "shell-regular" >}}

```bash
tiup clean [tag] [flags]
```

The following flag is supported:

- `--all`: Cleans up all instance information.

In the above command, `tag` is the instance tag to be cleaned. If `--all` is used, no tag is passed.

Example 1: Clean up the component instance with the `experiment` tag name.

{{< copyable "shell-regular" >}}

```shell
tiup clean experiment
```

Example 2: Clean up all component instances.

{{< copyable "shell-regular" >}}

```shell
tiup clean --all
```

### Uninstall components

The components installed using TiUP take up local disk space. If you do not want to keep too many components of old versions, you can check which versions of a component are currently installed, and then uninstall this component.

You can use the `tiup uninstall` command to uninstall all versions or specific versions of a component. This command also supports uninstalling all components. The command usage is as follows:

{{< copyable "shell-regular" >}}

```bash
tiup uninstall [component][:version] [flags]
```

The following flags are supported in this command:

- `--all`: Uninstalls all components or versions.
- `--self`: Uninstalls TiUP itself.

`component` is the component to be uninstalled. `version` is the version to be uninstalled. Both `component` and `version` can be ignored in the `tiup uninstall` command. If you ignore either one of these two, you need to add the `--all` flag.

- If the version is ignored, adding `--all` means to uninstall all versions of this component.
- If the version and the component are both ignored, adding `--all` means to uninstall all components of all versions.

Example 1: Uninstall TiDB v6.6.0.

{{< copyable "shell-regular" >}}

```shell
tiup uninstall tidb:v6.6.0
```

Example 2: Uninstall TiKV of all versions.

{{< copyable "shell-regular" >}}

```shell
tiup uninstall tikv --all
```

Example 3: Uninstall all installed components.

{{< copyable "shell-regular" >}}

```shell
tiup uninstall --all
```

---
title: tiup mirror clone
---

# tiup mirror clone

The command `tiup mirror clone` is used to clone an existing mirror or clone some of its components to create a new mirror. The new mirror has the same components as the old one, but uses a different signature key.

## Syntax

```shell
tiup mirror clone <target-dir> [global version] [flags]
```

- `<target-dir>` is used to set the local path to the cloned mirror. If the path does not exist, TiUP automatically creates one.
- If `[global version]` is specified, TiUP tries to clone all components of the specified version. If some components do not have the specified version, then TiUP clones its latest version.

## Options

### -f, --full

- Whether to clone the whole mirror. If this option is set, other options becomes ignored and TiUP completely clones all components of all versions from the targeted mirror.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

### -a, --arch

- Only clones components that can run on the specified platform.
- Data type: `STRING`
- Default: "amd64,arm64"

### -o, --os

- Only clones components that can run on the specified operating system.
- Data type: `STRING`
- Default: "linux,darwin"

### --prefix

- Whether to only match the prefix of versions. By default, TiUP downloads a component version when it is strictly matched. If this option is set, TiUP also downloads component versions of which prefixes are matched.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

### --{component}

- Specifies the version list of the component to be cloned. Fill component names in `{component}`. You can run [`tiup list --all`](/tiup/tiup-command-list.md) to view available component names.
- Data type: Strings
- Default: Null

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

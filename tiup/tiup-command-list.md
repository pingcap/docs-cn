---
title: tiup list
---

# tiup list

The command `tiup list` is used to get the list of available components of a mirror.

## Syntax

```shell
tiup list [component] [flags]
```

`[component]` is an optional parameter used to specify a certain component. If `[component]` is set, TiUP lists all versions of the specified component; if not, TiUP lists all components.

## Options

### --all

- Displays all components. By default, TiUP does not show hidden components.
- Data type: `BOOLEAN`
- Default: false

### --installed

- Only displays components and versions that have been installed.
- Data type: `BOOLEAN`
- Default: false

### --verbose

- Displays installed component versions in the components list.
- Data type: `BOOLEAN`
- Default: false

## Outputs

- If `[component]` is not set:
    - If `--verbose` is specified: TiUP outputs a component information list consisting of `Name` (component name), `Installed` (installed versions), `Owner` (component owner), and `Description` (component description).
    - If `--verbose` is not specified: TiUP outputs a component information list consisting of `Name` (component name), `Owner` (component owner), and `Description` (component description).
- If `[component]` is set:
    - If the specified component exists: TiUP outputs a version information list of the specified component, consisting of `Version` (version number), `Installed` (installation status), `Release` (release date), and `Platforms` (supported platforms).
    - If the specified component does not exist: TiUP reports the error `failed to fetch component: unknown component`.

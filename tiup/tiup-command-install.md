---
title: tiup install
---

# tiup install

The `tiup install` command is used for component installation. It downloads the component package of a specified version from the mirror repository and decompresses it in the local TiUP data directory for later use. In addition, when TiUP needs to run a component that does not exist in the mirror repository, it tries to download the component first and then runs it automatically. If the component does not exist in the repository, an error is reported.

## Syntax

```shell
tiup install <component1>[:version] [component2...N] [flags]
```

`<component1>` and `<component2>` represent component names, and `[version]` represents an optional version number. If `version` is not added, the latest stable version of the specified component is installed. `[component2...N]` means that you can specify multiple components or multiple versions of the same component at the same time.

## Option

None

## Output

- Normally outputs the download information of the component.
- If the component does not exist, the `The component "%s" not found` error is reported.
- If the version does not exist, the `version %s not supported by component %s` error is reported.

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)

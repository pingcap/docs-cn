---
title: tiup mirror publish
---

# tiup mirror publish

The command `tiup mirror publish` is used to publish a new component or a new version of an existing component. Only component owner that has the access to the target component can publish it. To add a new component owner, see the usage of the [`grant` command](/tiup/tiup-command-mirror-grant.md).

## Syntax

```shell
tiup mirror publish <comp-name> <version> <tarball> <entry> [flags]
```

The meaning of each parameter is as follows:

- `<comp-name>`: The name of the components, such as `tidb`. It is recommended to use a string that matches the regular expression `^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$`.
- `<version>`: The version of the component to be published. The version number needs to follow the requirements of [Semantic Versioning](https://semver.org/).
- `<tarball>`: The local directory of the `.tar.gz` package. You need to put dependencies and the executable file of the component in this package. TiUP uploads this package to the mirror.
- `<entry>`: The location of the component's executable file in `<tarball>`.

## Options

### -k, --key

- Specifies the component owner's private key. The client uses the private key to sign `{component}.json` files.
- Data type: `STRING`
- Default: "${TIUP_HOME}/keys/private.json"

### --arch

- Specifies the platform on which the binary files in `<tarball>` can run. For a single `<tarball>` package, you can only choose the platform from the following options:

    - `amd64`: Indicates that the files run on AMD64 machines.
    - `arm64`: Indicates that the files run on ARM64 machines.
    - `any`: Indicates that the files, such as scripts, run on both AMD64 and ARM64 machines.

- Data type: `STRING`
- Default: "${GOARCH}"

> **Note:**
>
> If `--arch` is set to `any`, then `--os` must be set to `any` as well.

### --os

- Specifies the operating system on which the binary files in `<tarball>` can run. For a single `<tarball>` package, you can only choose the operating system from the following options:

    - `linux`: Indicates that the files run on the Linux operating system.
    - `darwin`: Indicates that the files run on the Darwin operating system.
    - `any`: Indicates that the files, such as scripts, run on both the Linux and Darwin operating systems.

- Data type: `STRING`
- Default: "${GOOS}"

> **Note:**
>
> If `--os` is set to `any`, then `--arch` must be set to `any` as well.

### --desc

- Specifies the description of the component.
- Data type: `String`
- Default: NULL

### --hide

- Specifies whether the component is hidden. If it is a hidden component, it can be seen in the result list of `tiup list -all`, but not in that of `tiup list`.
- Data type: `STRING`
- Default: NULL

### --standalone

- Controls whether the component can run standalone. This option is currently **NOT available**.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Outputs

- If the command is executed successfully, there is no output.
- If the component owner is not authorized to modify the target component:
    - If the mirror is a remote mirror, TiUP reports the error `Error: The server refused, make sure you have access to this component`.
    - If the mirror is a local mirror, TiUP reports the error `Error: the signature is not correct`.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

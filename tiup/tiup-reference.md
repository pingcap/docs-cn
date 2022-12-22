---
title: TiUP Reference
---

# TiUP Reference

TiUP serves as the package manager of the TiDB ecosystem. It manages components in the TiDB ecosystem, such as TiDB, PD, and TiKV.

## Syntax

```shell
tiup [flags] <command> [args...]        # Executes a command
# or
tiup [flags] <component> [args...]      # Runs a component
```

You can use the `--help` command to get the information of a specific command. The summary of each command shows its parameters and their usage. Mandatory parameters are shown in angle brackets, and optional parameters are shown in square brackets.

`<command>` represents the command name. For the list of supported commands, see the [Command list](#command-list) below. `<component>` represents the component name. For the list of supported components, see the [Component list](#component-list) below.

## Options

### --binary

- If you enable this option, the specified binary file path is printed.

    - Executing `tiup --binary <component>` will have the path of the latest stable installed `<component>` component printed. If `<component>` is not installed, an error is returned.
    - Executing `tiup --binary <component>:<version>` will have the path of the installed `<component>` component's `<version>` printed. If this `<version>` is not printed, an error is returned.

- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

> **Note:**
>
> This option can only be used in commands of the `tiup [flags] <component> [args...]` format.

### --binpath

> **Note:**
>
> This option can only be used in commands of the `tiup [flags] <component> [args...]` format.

- Specifies the path of the component to be executed. When a component is executed, if you do not want to use the binary file in the TiUP mirror, you can add this option to specify using the binary file in a custom path.
- Data type: `STRING`

### -T, --tag

- Specifies a tag for the component to be started. Some components need to use disk storage during the execution, and TiUP allocates a temporary storage directory for this execution. If you want TiUP to allocate a fixed directory, you can use `-T/--tag` to specify the name of the directory, so that the same batch of files can be read and written in multiple executions with the same tag.
- Data type: `STRING`

### -v, --version

Prints the TiUP version.

### --help

Prints the help information.

## Command list

TiUP has multiple commands, and these commands have multiple sub-commands. For the specific commands and their detailed descriptions, click the corresponding links in the list below:

- [install](/tiup/tiup-command-install.md): Installs a component.
- [list](/tiup/tiup-command-list.md): Shows the component list.
- [uninstall](/tiup/tiup-command-uninstall.md): Uninstalls a component.
- [update](/tiup/tiup-command-update.md): Updates the installed component.
- [status](/tiup/tiup-command-status.md): Shows the running status of a component.
- [clean](/tiup/tiup-command-clean.md): Cleans the data directory of a component.
- [mirror](/tiup/tiup-command-mirror.md): Manages the mirror.
- [telemetry](/tiup/tiup-command-telemetry.md): Enables or disables the telemetry.
- [completion](/tiup/tiup-command-completion.md): Completes the TiUP command.
- [env](/tiup/tiup-command-env.md): Shows the TiUP-related environment variables.
- [help](/tiup/tiup-command-help.md): Shows the help information of a command or component.

## Component list

- [cluster](/tiup/tiup-component-cluster.md): Manages the TiDB cluster in a production environment.
- [dm](/tiup/tiup-component-dm.md): Manages the TiDB Data Migration (DM) cluster in a production environment.

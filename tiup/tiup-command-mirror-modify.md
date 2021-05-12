---
title: tiup mirror modify
---

# tiup mirror modify

The `tiup mirror modify` command is used to modify published components. Only valid component owners can modify the components that they have published on their own. For the method to publish a component, refer to the [`publish` command](/tiup/tiup-command-mirror-publish.md).

## Syntax

```shell
tiup mirror modify <component>[:version] [flags]
```

Each parameter is explained as follows:

- `<component>`: the component name
- `[version]`: the component version to modify. If it is not specified, the entire component is modified.

## Options

### -k, --key

- Specifies the component owner's private key used for signing the component information (`{component}.json`).
- Data type: `STRING`
- If this option is not specified in the command, `"${TIUP_HOME}/keys/private.json"` is used by default to sign the component information.

### --yank

Marks a specified component or version as unavailable.

- After the component is marked as unavailable, you can neither see it in the result list of `tiup list` nor install the new version of the component.
- After a component version is marked as unavailable, you can neither see it in the result list of `tiup list <component>` nor install this version.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

### --hide

- Specifies whether to hide the component. If a component is hidden, you cannot see it in the result list of `tiup list`. To see the hidden component, you can use `tiup list --all`.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

> **Note:**
>
> This option can only be applied to the component, not to the component version.

### --standalone

- Controls whether the component can run standalone. This option is currently **NOT available**.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

> **Note:**
>
> This option can only be applied to the component, not to the component version.

## Outputs

- If the command is executed successfully, there is no output.
- If the component owner is not authorized to modify the target component:
    - If the mirror is a remote mirror, TiUP reports the error `Error: The server refused, make sure you have access to this component`.
    - If the mirror is a local mirror, TiUP reports the error `Error: the signature is not correct`.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

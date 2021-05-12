---
title: tiup mirror grant
---

# tiup mirror grant

The `tiup mirror grant` command is used to introduce a component owner to the current mirror.

Component owners can use their keys to publish new components or to modify components they previously published. Before adding a new component owner, the component owner to be added needs to send his or her own public key to the mirror administrator.

> **Note:**
>
> This command is only supported when the current mirror is a local mirror.

## Syntax

```shell
tiup mirror grant <id> [flags]
```

`<id>` stands for the component owner's ID, which must be unique in the whole mirror. It is recommended to use an ID that matches the regular expression `^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$`.

## Options

### -k, --key

- Specifies the key of the introduced component owner. This key can either be public or private. If it is a private key, TiUP converts it to the corresponding public key before storing it in the mirror.
- A key can be used by only one component owner.
- Data type: `STRING`
- Default: "${TIUP_HOME}/keys/private.json"

### -n, --name

- Specifies the name of the component owner. The name is displayed on the `Owner` field of the component list. If `-n/--name` is not specified, `<id>` is used as the component owner's name.
- Data type: `STRING`
- Default: `<id>`

### Outputs

- If the command is executed successfully, there is no output.
- If the component owner's ID is duplicated, TiUP reports the error `Error: owner %s exists`.
- If the key is used by another component owner, TiUP reports the error `Error: key %s exists`.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

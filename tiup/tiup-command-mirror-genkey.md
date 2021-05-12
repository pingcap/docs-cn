---
title: tiup mirror genkey
---

# tiup mirror genkey

TiUP [mirror](/tiup/tiup-mirror-reference.md), according its definition, has three roles of users:

- Mirror administrators: They have the permission to modify `root.json`, `index.json`, `snapshot.json`, and `timestamp.json`.
- Component owners: They have the permission to modify the corresponding component.
- Normal users: They can download and use the components.

 Because TiUP requires the signature of the corresponding owner/administrator to modify a file, owners/administrators must have his or her own private key. The command `tiup mirror genkey` is used to generate a private key.

> **Warning:**
>
> **DO NOT** transmit private keys over the Internet.

## Syntax

```shell
tiup mirror genkey [flags]
```

## Options

### -n, --name

- Specifies the name of the key, which also determines the name of the final generated file. The path of the generated private key file is `${TIUP_HOME}/keys/{name}.json`. `TIUP_HOME` refers to the home directory of TiUP, which is `$HOME/.tiup` by default. `name` refers to the private key name that `-n/--name` specifies.
- Data type: `STRING`
- Default: "private"

### -p, --public

- Shows the corresponding public key of the private key specified in the option `-n/--name`.
- TiUP does not create a new private key when `-p/--public` is specified. If the private key specified in `-n/--name` does not exist, TiUP returns an error.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

### --save

- Saves the information of the public key as a file in the current directory. The file name is `{hash-prefix}-public.json`. `hash-prefix` is the first 16 bits of the key ID.
- Data type: `BOOLEAN`
- This option is disabled by default and its default value is `false`. To enable this option, you can add this option to the command, and pass the `true` value or do not pass any value.

## Outputs

- If `-p/--public` is not specified:
    - If the private key specified in `-n/--name` exists: TiUP outputs `Key already exists, skipped`.
    - If the private key specified in `-n/--name` does not exist: TiUP outputs `private key have been write to ${TIUP_HOME}/keys/{name}.json`.
- If `-p/--public` is specified:
    - If the private key specified in `-n/--name` does not exist: TiUP reports the error `Error: open ${TIUP_HOME}/keys/{name}.json: no such file or directory`.
    - If the private key specified in `-n/--name` exists: TiUP outputs the content of the corresponding public key.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

---
title: tiup mirror sign
---

# tiup mirror sign

The `tiup mirror sign` command is used to sign the metadata files (*.json）defined in TiUP [mirror](/tiup/tiup-mirror-reference.md). These metadata files might be stored on the local file system or remotely stored using the HTTP protocol to provide a signature entry.

## Syntax

```shell
tiup mirror sign <manifest-file> [flags]
```

`<manifest-file>` is the address of the file to be signed, which has two forms:

- Network address, which starts with HTTP or HTTPS, such as `http://172.16.5.5:8080/rotate/root.json`
- Local file path, which is a relative path or an absolute path

If it is a network address, this address must provide the following features:

- Supports the access via `http get` that returns the complete content of the signed file (including the `signatures` field).
- Supports the access via `http post`. The client adds the signature to the `signatures` field of the content that is returned by `http get` and posts to this network address.

## Options

### -k, --key

- Specifies the location of the private key used for signing the `{component}.json` file.
- Data type: `STRING`
- - If this option is not specified in the command, `"${TIUP_HOME}/keys/private.json"` is used by default.

### --timeout

- Specifies the access timeout time for signing through the network. The unit is in seconds.
- Data type: `INT`
- Default: 10

> **Note:**
>
> This option is valid only when `<manifest-file>` is a network address.

## Output

- If the command is executed successfully, there is no output.
- If the file has been signed by the specified key, TiUP reports the error `Error: this manifest file has already been signed by specified key`.
- If the file is not a valid manifest, TiUP reports the error `Error: unmarshal manifest: %s`.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

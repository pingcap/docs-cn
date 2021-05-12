---
title: tiup mirror set
---

# tiup mirror set

The `tiup mirror set` command is used to switch the current mirror and supports two forms of mirrors: local file system and remote network address.

The address of the official mirror is `https://tiup-mirrors.pingcap.com`.

## Syntax

```shell
tiup mirror set <mirror-addr> [flags]
```

`<mirror-addr>` is the mirror address, which has two forms:

- Network address: starts with `http` or `https`. For example, `http://172.16.5.5:8080`, `https://tiup-mirrors.pingcap.com`.
- Local file path: the absolute path of the mirror directory. For example, `/path/to/local-tiup-mirror`.

## Option

### -r, --root

This option specifies the root certificate.

As the most critical part of mirror security, the root certificate of each mirror is different from one another. When you use the network mirror, it might suffer from man-in-the-middle attacks. To avoid such attacks, it is recommended to manually download the root certificate of the root network mirror to the local:

```
wget <mirror-addr>/root.json -O /path/to/local/root.json
```

Perform a manual check to ensure that the root certificate is correct, and then switch the mirror by manually specifying the root certificate:

```
tiup mirror set <mirror-addr> -r /path/to/local/root.json
```

In the steps above, if the mirror is attacked before the `wget` command, you can find that the root certificate is incorrect. If the mirror is attacked after the `wget` command, TiUP will find that the mirror does not match the root certificate.

- Data type: `String`
- Default: `{mirror-dir}/root.json`

## Output

None

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

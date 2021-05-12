---
title: tiup mirror
---

# tiup mirror

In TiUP, [mirror](/tiup/tiup-mirror-reference.md) is an important concept. TiUP currently supports two forms of mirroring:

- Local mirror: the TiUP client and the mirror are on the same machine, and the client accesses the mirror through the file system.
- Remote mirror: the TiUP client and the mirror are not on the same machine, and the client accesses the mirror through network.

The `tiup mirror` command is used to manage mirrors and provides ways to create mirrors, distribute components, and manage keys.

## Syntax

```shell
tiup mirror <command> [flags]
```

`<command>` stands for sub-commands. For the list of supported sub-commands, refer to the [command list](#command-list) below.

## Option

None

## Command list

- [genkey](/tiup/tiup-command-mirror-genkey.md): generates the private key file
- [sign](/tiup/tiup-command-mirror-sign.md): signs a specific file using a private key file
- [init](/tiup/tiup-command-mirror-init.md): initiates an empty mirror
- [set](/tiup/tiup-command-mirror-set.md): sets the current mirror
- [grant](/tiup/tiup-command-mirror-grant.md): grants a new component owner for the current mirror
- [publish](/tiup/tiup-command-mirror-publish.md): publishes new components to the current mirror
- [modify](/tiup/tiup-command-mirror-modify.md): modifies the attributes of the components in the current mirror
- [rotate](/tiup/tiup-command-mirror-rotate.md): updates the root certificate in the current mirror
- [clone](/tiup/tiup-command-mirror-clone.md): clones a new mirror from an existing one
- [merge](/tiup/tiup-command-mirror-merge.md): merges mirrors

[<< Back to the previous page - TiUP Reference command list](/tiup/tiup-reference.md#command-list)

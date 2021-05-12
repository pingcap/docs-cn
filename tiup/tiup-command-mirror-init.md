---
title: tiup mirror init
---

# tiup mirror init

The command `tiup mirror init` is used to initialize an empty mirror. The initialized mirror does not contain any components or component owners. The command only generates the following files for the initialized mirror:

```
+ <mirror-dir>                                  # Mirror's root directory
|-- root.json                                   # Mirror's root certificate
|-- 1.index.json                                # Component/user index
|-- snapshot.json                               # Mirror's latest snapshot
|-- timestamp.json                              # Mirror's latest timestamp
|--+ keys                                       # Mirror's private key (can be moved to other locations)
   |-- {hash1..hashN}-root.json                 # Private key of the root certificate
   |-- {hash}-index.json                        # Private key of the indexes
   |-- {hash}-snapshot.json                     # Private key of the snapshots
   |-- {hash}-timestamp.json                    # Private key of the timestamps
```

For the specific usage and content format of the above files, refer to [TiUP Mirror Reference Guide](/tiup/tiup-mirror-reference.md).

## Syntax

```shell
tiup mirror init <path> [flags]
```

`<path>` is used to specify a local directory where TiUP generates and stores mirror files. The local directory can be a relative path. If the specified directory already exists, it must be empty; if it does not exist, TiUP creates it automatically.

## Options

### -k, --key-dir

- Specifies the directory where TiUP generates private key files. If the specified directory does not exist, TiUP automatically creates it.
- Data type: `STRING`
- If this option is not specified in the command, TiUP generates private key files in `{path}/keys` by default.

### Outputs

- If the command is executed successfully, there is no output.
- If the specified `<path>` is not empty, TiUP reports the error `Error: the target path '%s' is not an empty directory`.
- If the specified `<path>` is not a directory, TiUP reports the error `Error: fdopendir: not a directory`.

[<< Back to the previous page - TiUP Mirror command list](/tiup/tiup-command-mirror.md#command-list)

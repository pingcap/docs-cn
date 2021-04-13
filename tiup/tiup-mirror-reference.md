---
title: TiUP Mirror Reference Guide
summary: Learn the general information of TiUP mirrors.
---

# TiUP Mirror Reference Guide

TiUP mirrors are TiUP's component warehouse, which stores components and their metadata. TiUP mirrors take the following two forms:

+ Directory on the local disk: serves the local TiUP client, which is called a local mirror in this document.
+ HTTP mirror started based on the remote disk directory: serves the remote TiUP client, which is called a remote mirror in this document.

## Create and update mirror

You can create a TiUP mirror using one of the following two methods:

+ Execute `tiup mirror init` to create a mirror from scratch.
+ Execute `tiup mirror clone` to clone from an existing mirror.

After the mirror is created, you can add components to or delete components from the mirror using the `tiup mirror` commands. TiUP updates a mirror by adding files and assigning a new version number to it, rather than deleting any files from the mirror.

## Mirror structure

A typical mirror structure is as follows:

```
+ <mirror-dir>                                  # Mirror's root directory
|-- root.json                                   # Mirror's root certificate
|-- {2..N}.root.json                            # Mirror's root certificate
|-- {1..N}.index.json                           # Component/user index
|-- {1..N}.{component}.json                     # Component metadata
|-- {component}-{version}-{os}-{arch}.tar.gz    # Component binary package
|-- snapshot.json                               # Mirror's latest snapshot
|-- timestamp.json                              # Mirror's latest timestamp
|--+ commits                                    # Mirror's update log (deletable)
   |--+ commit-{ts1..tsN}
      |-- {N}.root.json
      |-- {N}.{component}.json
      |-- {N}.index.json
      |-- {component}-{version}-{os}-{arch}.tar.gz
      |-- snapshot.json
      |-- timestamp.json
|--+ keys                                       # Mirror's private key (can be moved to other locations)
   |-- {hash1..hashN}-root.json                 # Private key of the root certificate
   |-- {hash}-index.json                        # Private key of the indexes
   |-- {hash}-snapshot.json                     # Private key of the snapshots
   |-- {hash}-timestamp.json                    # Private key of the timestamps
```

> **Note:**
>
> + The `commits` directory stores the logs generated in the process of mirror update and is used to roll back the mirror. You can delete the old log directories regularly when the disk space is insufficient.
> + The private key stored in the `keys` directory is sensitive. It is recommended to keep it separately.

### Root directory

In a TiUP mirror, the root certificate is used to store the public key of other metadata files. Each time any metadata file (`*.json`) is obtained, TiUP client needs to find the corresponding public key in the installed `root.json` based on the metadata file type (root, index, snapshot, timestamp). Then TiUP client uses the public key to verify whether the signature is valid.

The root certificate's format is as follows:

```
{
    "signatures": [                                             # Each metadata file has some signatures which are signed by several private keys corresponding to the file.
        {
            "keyid": "{id-of-root-key-1}",                      # The ID of the first private key that participates in the signature. This ID is obtained by hashing the content of the public key that corresponds to the private key.
            "sig": "{signature-by-root-key-1}"                  # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {                                                 # The signed part.
        "_type": "root",                                        # The type of this file. root.json's type is root.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "roles": {                                              # Records the keys used to sign each metadata file.
            "{role:index,root,snapshot,timestamp}": {           # Each involved metadata file includes index, root, snapshot, and timestamp.
                "keys": {                                       # Only the key's signature recorded in `keys` is valid.
                    "{id-of-the-key-1}": {                      # The ID of the first key used to sign {role}.
                        "keytype": "rsa",                       # The key's type. Currently, the key type is fixed as rsa.
                        "keyval": {                             # The key's payload.
                            "public": "{public-key-content}"    # The public key's content.
                        },
                        "scheme": "rsassa-pss-sha256"           # Currently, the scheme is fixed as rsassa-pss-sha256.
                    },
                    "{id-of-the-key-N}": {                      # The ID of the Nth key used to sign {role}.
                        "keytype": "rsa",
                        "keyval": {
                            "public": "{public-key-content}"
                        },
                        "scheme": "rsassa-pss-sha256"
                    }
                },
                "threshold": {N},                               # Indicates that the metadata file needs at least N key signatures.
                "url": "/{role}.json"                           # The address from which the file can be obtained. For index files, prefix it with the version number (for example, /{N}.index.json).
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to create a new {N+1}.root.json every time you update the file, and set its version to N + 1.
    }
}
```

### Index

The index file records all the components in the mirror and the owner information of the components.

The index file's format is as follows:

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "index",                                       # The file type.
        "components": {                                         # The component list.
            "{component1}": {                                   # The name of the first component.
                "hidden": {bool},                               # Whether it is a hidden component.
                "owner": "{owner-id}",                          # The component owner's ID.
                "standalone": {bool},                           # Whether it is a standalone component.
                "url": "/{component}.json",                     # The address from which the component can be obtained. You need to prefix it with the version number (for example, /{N}.{component}.json).
                "yanked": {bool}                                # Indicates whether the component is marked as deleted.
            },
            ...
            "{componentN}": {                                   # The name of the Nth component.
                ...
            },
        },
        "default_components": ["{component1}".."{componentN}"], # The default component that a mirror must contain. Currently, this field defaults to empty (disabled).
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "owners": {
            "{owner1}": {                                       # The ID of the first owner.
                "keys": {                                       # Only the key's signature recorded in `keys` is valid.
                    "{id-of-the-key-1}": {                      # The first key of the owner.
                        "keytype": "rsa",                       # The key's type. Currently, the key type is fixed as rsa.
                        "keyval": {                             # The key's payload.
                            "public": "{public-key-content}"    # The public key's content.
                        },
                        "scheme": "rsassa-pss-sha256"           # Currently, the scheme is fixed as rsassa-pss-sha256.
                    },
                    ...
                    "{id-of-the-key-N}": {                      # The Nth key of the owner.
                        ...
                    }
                },
                "name": "{owner-name}",                         # The name of the owner.
                "threshod": {N}                                 # Indicates that the components owned by the owner must have at least N valid signatures.
            },
            ...
            "{ownerN}": {                                       # The ID of the Nth owner.
                ...
            }
        }
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to create a new {N+1}.index.json every time you update the file, and set its version to N + 1.
    }
}
```

### Component

The component's metadata file records information of the component-specific platform and the version.

The component metadata file's format is as follows:

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "component",                                   # The file type.
        "description": "{description-of-the-component}",        # The description of the component.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "id": "{component-id}",                                 # The globally unique ID of the component.
        "nightly": "{nightly-cursor}",                          # The nightly cursor, and the value is the latest nightly version number (for example, v5.0.0-nightly-20201209).
        "platforms": {                                          # The component's supported platforms (such as darwin/amd64, linux/arm64).
            "{platform-pair-1}": {
                "{version-1}": {                                # The semantic version number (for example, v1.0.0).
                    "dependencies": null,                       # Specifies the dependency relationship between components. The field is not used yet and is fixed as null.
                    "entry": "{entry}",                         # The relative path of the entry binary file in the tar package.
                    "hashs": {                                  # The checksum of the tar package. sha256 and sha512 are used.
                        "sha256": "{sum-of-sha256}",
                        "sha512": "{sum-of-sha512}",
                    },
                    "length": {length-of-tar},                  # The length of the tar package.
                    "released": "{release-time}",               # The release date of the version.
                    "url": "{url-of-tar}",                      # The download address of the tar package.
                    "yanked": {bool}                            # Indicates whether this version is disabled.
                }
            },
            ...
            "{platform-pair-N}": {
                ...
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to create a new {N+1}.{component}.json every time you update the file, and set its version to N + 1.
}
```

### Snapshot

The snapshot file records the version number of each metadata file:

The snapshot file's structure is as follows:

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "snapshot",                                    # The file type.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "meta": {                                               # Other metadata files' information.
            "/root.json": {
                "length": {length-of-json-file},                # The length of root.json
                "version": {version-of-json-file}               # The version of root.json
            },
            "/index.json": {
                "length": {length-of-json-file},
                "version": {version-of-json-file}
            },
            "/{component-1}.json": {
                "length": {length-of-json-file},
                "version": {version-of-json-file}
            },
            ...
            "/{component-N}.json": {
                ...
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": 0                                            # The version number of this file, which is fixed as 0.
    }
```

### Timestamp

The timestamp file records the checksum of the current snapshot.

The timestamp file's format is as follows:

```
{
    "signatures": [                                             # The file's signature.
        {
            "keyid": "{id-of-index-key-1}",                     # The ID of the first private key that participates in the signature.
            "sig": "{signature-by-index-key-1}",                # The signed part of this file by this private key.
        },
        ...
        {
            "keyid": "{id-of-root-key-N}",                      # The ID of the Nth private key that participates in the signature.
            "sig": "{signature-by-root-key-N}"                  # The signed part of this file by this private key.
        }
    ],
    "signed": {
        "_type": "timestamp",                                   # The file type.
        "expires": "{expiration-date-of-this-file}",            # The expiration time of the file. If the file expires, the client rejects the file.
        "meta": {                                               # The information of snapshot.json.
            "/snapshot.json": {
                "hashes": {
                    "sha256": "{sum-of-sha256}"                 # snapshot.json's sha256.
                },
                "length": {length-of-json-file}                 # The length of snapshot.json.
            }
        },
        "spec_version": "0.1.0",                                # The specified version followed by this file. If the file structure is changed in the future, the version number needs to be upgraded. The current version number is 0.1.0.
        "version": {N}                                          # The version number of this file. You need to overwrite timestamp.json every time you update the file, and set its version to N + 1.
```

## Client workflow

The client uses the following logic to ensure that the files downloaded from the mirror are safe:

+ A `root.json` file is included with the binary when the client is installed.
+ The running client performs the following tasks based on the existing `root.json`:
    1. Obtain the version from `root.json` and mark it as `N`.
    2. Request `{N+1}.root.json` from the mirror. If the request is successful, use the public key recorded in `root.json` to verify whether the file is valid.
    3. Request `timestamp.json` from the mirror and use the public key recorded in `root.json` to verify whether the file is valid.
    4. Check whether the checksum of `snapshot.json` recorded in `timestamp.json` matches the checksum of the local `snapshot.json`. If the two do not match, request the latest `snapshot.json` from the mirror and use the public key recorded in `root.json` to verify whether the file is valid.
    5. Obtain the version number `N` of the `index.json` file from `snapshot.json` and request `{N}.index.json` from the mirror. Then use the public key recorded in `root.json` to verify whether the file is valid.
    6. For components such as `tidb.json` and `tikv.json`, the client obtains the version numbers `N` of the components from `snapshot.json` and requests `{N}.{component}.json` from the mirror. Then the client uses the public key recorded in `index.json` to verify whether the file is valid.
    7. For component's tar files, the client obtains the URLs and checksums of the files from `{component}.json` and request the URLs for the tar packages. Then the client verifies whether the checksum is correct.

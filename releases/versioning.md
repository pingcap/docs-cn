---
title: TiDB Versioning
summary: Learn the version numbering system of TiDB.
---

# TiDB Versioning

<Important>

It is recommended to always upgrade to the latest patch release of your release series.

</Important>

TiDB offers two release series:

* Long-Term Support Releases
* Development Milestone Releases (introduced in TiDB v6.0.0)

To learn about the support policy for major releases of TiDB, see [TiDB Release Support Policy](https://en.pingcap.com/tidb-release-support-policy/).

## Release versioning

TiDB versioning has the form of `X.Y.Z`. `X.Y` represents a release series.

- Since TiDB 1.0, `X` increments every year. Each `X` release introduces new features and improvements.
- `Y` increments from 0. Each `Y` release introduces new features and improvements.
- In the first release of a release series, `Z` is set to 0 by default. For patch releases, `Z` increments from 1.

For the versioning system of TiDB v5.0.0 and earlier versions, refer to [Historical versioning](#historical-versioning-deprecated).

## Long-Term Support releases

Long-Term Support (LTS) versions are released approximately every six months and introduce new features, improvements, bug fixes and security vulnerability fixes.

LTS releases are versioned as `X.Y.Z`. `Z` defaults to 0.

Example versions:

- 6.1.0
- 5.4.0

During the lifecycle of LTS, patch releases are made available on demand. Patch releases contain bug fixes and security vulnerability fixes, and do not introduce new features.

Patch releases are versioned as `X.Y.Z`. `X.Y` is consistent with the corresponding LTS versioning. The patch number `Z` increments from 1.

Example version:

- 6.1.1

<Note>

v5.1.0, v5.2.0, v5.3.0, v5.4.0 were released only two months after their preceding releases, but all four releases are LTS and provide patch releases.

</Note>

## Development Milestone Releases

Development Milestone Releases (DMR) are released approximately every two months that do not contain LTS. DMR versions introduce new features, improvements and bug fixes. TiDB does not provide patch releases based on DMR, and any related bugs are fixed in the subsequent release series.

DMRs are versioned as `X.Y.Z`. `Z` defaults to 0. A `-DMR` suffix is appended to the version number.

Example version:

- 6.0.0-DMR

## Versioning of TiDB ecosystem tools

Some TiDB tools are released together with the TiDB server and use the same version numbering system, such as TiDB Lightning. Some TiDB tools are released separately from the TiDB server and use their own version numbering system, such as TiUP and TiDB Operator.

## Historical versioning (deprecated)

### General Availability releases

General Availability (GA) releases are stable versions of the current release series of TiDB. GA versions are released after Release Candidate (RC) versions. GA can be used in production environments.

Example versions:

- 1.0
- 2.1 GA
- 5.0 GA

### Release Candidate releases

Release Candidate (RC) releases introduce new features and improvements. RC versions are significantly more stable than Beta versions. RC can be used for early testing, but are not suitable for production.

Example versions:

- RC1
- 2.0-RC1
- 3.0.0-rc.1

### Beta releases

Beta releases introduces new features and improvements. Beta versions are greatly improved over Alpha versions and have eliminated critical bugs, but still contain some bugs. Beta releases are available for users to test the latest features.

Example versions:

- 1.1 Beta
- 2.1 Beta
- 4.0.0-beta.1

### Alpha releases

Alpha releases are internal releases for testing and introduce new features and improvements. Alpha releases are the initial versions of the current release series. Alpha releases might have some bugs and are available for users to test the latest features.

Example version:

- 1.1 Alpha

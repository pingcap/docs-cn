---
title: Deploying Recommendations
category: deployment
---

## Deploying Recommendations

To learn the TiDB architecture, see [TiDB Architecture](../README.md#TiDB-Architecture).

The following table lists the recommended hardware for each components.

<table>
  <tr>
    <td>Component</td>
    <td># of CPU Cores</td>
    <td>Memory</td>
    <td>Disk Type</td>
    <td>Disk</td>
    <td># of Instances</td>
  </tr>
  <tr>
    <td>TiDB</td>
    <td>8+</td>
    <td>16G+ </td>
    <td></td>
    <td></td>
    <td>2+</td>
  </tr>
  <tr>
    <td>PD</td>
    <td>8+</td>
    <td>16G+ </td>
    <td></td>
    <td>200G+</td>
    <td>3+</td>
  </tr>
  <tr>
    <td>TiKV</td>
    <td>8+</td>
    <td>16G+ </td>
    <td>SSD</td>
    <td>200G~500G</td>
    <td>3+</td>
  </tr>
</table>


**Deployment tips:**

* Deploy only one TiKV instance on one disk.

* Don’t deploy the PD instance and TiKV instance on the same disk

* The TiDB instance can be deployed to the same disk with either PD or TiKV.

* The size of the disk for TiKV does not exceed 500G. This is to avoid a long data recovering time in case of disk failure.

* Use SSD for TiKV.
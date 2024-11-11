---
title: TiDB 路线图
summary: 了解 TiDB 未来的发展方向，包括新特性和改进提升。
---

# TiDB 路线图

TiDB 路线图展示了 TiDB 未来的计划。随着我们发布长期稳定版本 (LTS)，这个路线图将会持续更新。通过路线图，你可以预先了解 TiDB 的未来规划，以便你关注进度，了解关键里程碑，并对开发工作提出反馈。

在开发过程中，路线图可能会根据用户需求和反馈进行调整，请不要根据路线图的内容制定上线计划。如果你有功能需求，或者想提高某个特性的优先级，请在 [GitHub](https://github.com/pingcap/tidb/issues) 上提交 issue。

> **注意：**
> 
> 没有被注明 GA 的特性，均为实验特性。

## TiDB 重要特性规划

<table class="ace-table" data-ace-table-col-widths="234;324;290;261"><colgroup><col width="234" /><col width="324" /><col width="290" /><col width="261" /></colgroup>
<thead>
<tr>
<td style="width: 64.6172px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-BH0JdDLIPoKVN5xdM8sczrQKnEg"><strong>类别</strong></div>
</td>
<td style="width: 152.898px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-UycndX864oN2axxMnc9crvian1g"><strong>2024 年底版本</strong></div>
</td>
<td style="width: 188.875px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-UZT8dxC59o8NgMxkh1ycnhlhnrd"><strong>2025 年中版本</strong></div>
</td>
<td style="width: 138.609px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-AXBCd3glgoHqaGxVP0EcNclunGg"><strong>未来版本</strong></div>
</td>
</tr>
</thead>
<tbody>
<tr>
<td style="width: 64.6172px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-J8zzdnUrfoUW6LxZGsZcClL9nfh"><strong>可扩展性与性能</strong></div>
<div class="ace-line ace-line old-record-id-VeXadmHAVo392Hxn1fGctBwxnGO">提供更强的扩展能力和更快的性能，支持超大规模的工作负载，优化资源利用，提升集群性能。</div>
<div class="ace-line ace-line old-record-id-XXrRd5lj2onKruxE1qrchYmTnTk">&nbsp;</div>
</td>
<td style="width: 152.898px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-BNuAdZzhPoxHgUxYoaYcHxLxnn5" data-list="bullet">
<div><strong>TiKV</strong><strong> 数据缓存 </strong></div>
<div class="ace-line ace-line old-record-id-YexvdhMsKoVAdPxZgF6cdcJmnic">TiKV 在内存中维护数据的最近版本，减少对多版本数据的反复扫描，进而提升性能。</div>
</li>
<li class="ace-line ace-line old-record-id-NUIcdz5IIoKMjrxBtL1cigP6nbd" data-list="bullet">
<div><strong>自动配置统计信息收集的并行度(GA)</strong></div>
<div class="ace-line ace-line old-record-id-HhfWd7LzroUgAExf51cccos5nog">TiDB 根据部署的节点数以及硬件规格自动设置统计信息收集的任务并行度和扫描并发度，提升收集速度。</div>
</li>
<li class="ace-line ace-line old-record-id-DOlKdUHs4opS3MxQ9bRcDZJXnMc" data-list="bullet">
<div><strong>加速数据库恢复</strong></div>
<div class="ace-line ace-line old-record-id-Zlw9dAvAjoP3xOxiTq9cy1t5n9b">缩短全量数据库恢复和 Point-in-time recovery (PITR) 所需的时间。</div>
</li>
<li class="ace-line ace-line old-record-id-RcNdd7wfBo76Ssx2P2scIEienpd" data-list="bullet">
<div><strong>支持不限大小的事务</strong></div>
<div class="ace-line ace-line old-record-id-QKOgdFrHcofLv9xNYW2cDA6LnDj">未提交事务所处理的数据量，不再依赖 TiDB 节点的可用内存大小。提升事务及批量任务的成功率。</div>
</li>
<li class="ace-line ace-line old-record-id-BnACdrjK9oQvozxVVRNcxR1qn1d" data-list="bullet">
<div><strong>TiProxy 根据负载转发流量(GA)</strong></div>
<div class="ace-line ace-line old-record-id-GnLSdQT2Rogtnjxdh01cl7ibnAg">TiProxy 依据目标 TiDB 的负载对流量进行转发，以此充分利用硬件资源.</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-PyMOdYmSzoTfuCxIQXqcmpdZnA8">&nbsp;</div>
</td>
<td style="width: 188.875px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-PXbOdZtjCoQNKwxdcMNc7h8EnLJ" data-list="bullet">
<div><strong>PD</strong><strong> 的路由功能微服务化</strong></div>
<div class="ace-line ace-line old-record-id-T3d1dU1ZBogbDSxryaicxPHTnEe">实现路由服务（Region 元数据的访问、更新）在 PD 中的独立部署，路由服务完全改造为无状态服务（无强领导者）、易于扩展，避免 PD 成为集群资源瓶颈。</div>
</li>
<li class="ace-line ace-line old-record-id-MfJWd6jDyozERkxWtf1ceWVPnMc" data-list="bullet">
<div><strong>减少统计信息收集时的 I/O 消耗(GA)</strong></div>
<div class="ace-line ace-line old-record-id-Th6CdtdkOoBJr1xm37LcfGiInqd">当抽取部分数据样本做统计信息收集时，TiKV上只扫描样本，以减少统计信息收集所消耗的时间和资源。</div>
</li>
<li class="ace-line ace-line old-record-id-NQC9dsyHooMIcZxSSsKcOHN2nne" data-list="bullet">
<div><strong>移除将</strong><strong><code>Limit</code></strong><strong> 算子下推到 </strong><strong>TiKV</strong><strong> 的已知限制</strong></div>
</li>
<li class="ace-line ace-line old-record-id-T5AsdOO6gowbHdxquuZcCTFVnxh" data-list="bullet">
<div><strong>Cascades optimizer </strong></div>
<div class="ace-line ace-line old-record-id-OuXxduvOdomKj2xHuXScr7qSnfb">引入更成熟强大的优化器框架，扩展当前优化的基础能力。</div>
</li>
<li class="ace-line ace-line old-record-id-OhV3dbdoVooQiixz4vAcRycynVb" data-list="bullet">
<div><strong>增强 </strong><strong>DDL</strong><strong> 执行框架</strong></div>
<div class="ace-line ace-line old-record-id-O84ydY06DoonakxVb6wcIVpGnbf">提供可扩展的并行 DDL 执行框架，提升 DDL 的性能和稳定性。</div>
</li>
<li class="ace-line ace-line old-record-id-NeAwdIeIvoJ924xxPhYccWamnLg" data-list="bullet">
<div><strong>增强 </strong><strong>TiCDC</strong><strong> 的扩展性</strong></div>
<div class="ace-line ace-line old-record-id-BIMWdye37o7j1LxeXQCcAoannxb">推出新的 TiCDC 架构，提升 TiCDC 的扩展性以及性能。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-UrqJdd6HxoYxSxxuIHqcsqFjnrd">&nbsp;</div>
</td>
<td style="width: 138.609px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-X3OadgUMgomG6dxZL5Rcgebanjf" data-list="bullet">
<div><strong>表级别的负载均衡</strong></div>
<div class="ace-line ace-line old-record-id-IJledcA7ro7CWuxN1EUcfJpVn3f">PD 根据每个表上各 region 的负载决定数据的调度策略。</div>
</li>
<li class="ace-line ace-line old-record-id-KCDZd18Ezoxu5txXRDucy0Nkn1g" data-list="bullet">
<div><strong>处理大数据量的系统表</strong></div>
<div class="ace-line ace-line old-record-id-MvbmdZFqhoHVTaxNdzPcvg9vnJg">当系统表中存有大量数据时，提升查询系统表的查询性能。</div>
</li>
<li class="ace-line ace-line old-record-id-PAP1d8g59oVqYJxEBQocTYQqn9c" data-list="bullet">
<div><strong>增强区域元数据存储的可扩展性</strong></div>
<div class="ace-line ace-line old-record-id-CnOLd4e8soopeMxiOubcl8KWnNc">增强 Region 元数据存储的可扩展性。将Region 元数据存储从 PD 迁移到 TiKV，存储层可以轻松实现无限制的扩展。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-KHERdW56Do5zVdx3WChc187Vn6c">&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 64.6172px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-TXDDdeT5FoaYL3xl2n0cMudjnjR"><strong>SQL</strong><strong> 功能</strong></div>
<div class="ace-line ace-line old-record-id-NsEbdds1foTmUoxUeV5c3EVInpb">前沿的 SQL 功能，提升了兼容性、灵活性和易用性，助力复杂查询和现代应用的高效运行。</div>
<div class="ace-line ace-line old-record-id-BZrcdM2lCoEhz8xuTjcc2HydnJf">&nbsp;</div>
</td>
<td style="width: 152.898px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-RO9fdGqcpoeddmxARuwcIutAnDf" data-list="bullet">
<div><strong>支持向量搜索功能</strong></div>
<div class="ace-line ace-line old-record-id-MaQ4dxxFHoDR9lxdtCVcQH9enPg">支持向量数据类型、向量索引及高性能向量搜索能力，同时具备向量和关系数据混合查询能力。</div>
</li>
<li class="ace-line ace-line old-record-id-PKQxdbSibo1hshxxkc3cHKqHnVb" data-list="bullet">
<div><strong>外键成为正式功能（GA）</strong></div>
</li>
<li class="ace-line ace-line old-record-id-V9R6dKaxwooDKzx6AEKceJvQnGc" data-list="bullet">
<div><strong>分区表全局索引成为正式功能（GA）</strong></div>
<div class="ace-line ace-line old-record-id-BLSFdw3NgoGglYxdjtjcrpionae">解除分区表唯一键必须包含分区建的限制，提升分区表非分区列的查询性能</div>
</li>
</ul>
</td>
<td style="width: 188.875px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-Arutdr4jao7Xfzx4wC9cvT1fnVg" data-list="bullet">
<div><strong>支持修改分区表的列类型</strong></div>
<div class="ace-line ace-line old-record-id-JGC0dGFzIo8QGRxS09wcboQfnrh">用户可以修改分区中列的类型，无论是否是分区键。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-OxjEdaEx3oVBlKxZF3IcXjpJnQb">&nbsp;</div>
</td>
<td style="width: 138.609px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-OuZQdI2JEoBDnXx4SwMcS9wSnmf" data-list="bullet">
<div><strong>支持物化视图</strong></div>
<div class="ace-line ace-line old-record-id-S9frdhfRloiFtYx8hd7cyxf5nJh">支持物化视图功能，改进预处理能力，优化计算效率，进一步提升数据分析性能</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-NdlgdBkIzowbY7xNUXwcLciFnVg">&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 64.6172px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-LrdSdtKScozpcdxZsMLczD4hndd"><strong>稳定性与高可用</strong></div>
<div class="ace-line ace-line old-record-id-K3b0dTnCpoGpsIxlkgYcZ3b7npd">确保持续运行，提升系统容错能力，为用户提供稳定可靠的使用体验。</div>
<div class="ace-line ace-line old-record-id-LKfZdDLq5o2wPHx0KA8cQaCpnNh">&nbsp;</div>
</td>
<td style="width: 152.898px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-L2k9dhmbco5TejxoDdKcIhGunxh" data-list="bullet">
<div><strong>限制备份任务的内存消耗</strong></div>
</li>
<li class="ace-line ace-line old-record-id-Hxa3dyckJoKsIVxlk0cc5Nj6n6b" data-list="bullet">
<div><strong>限制统计信息收集的内存消耗（GA）</strong></div>
</li>
<li class="ace-line ace-line old-record-id-KB4tdF0YdoKLslx75bocYfmvnDd" data-list="bullet">
<div><strong>管理大量的 </strong><strong>SQL</strong><strong> Binding（GA）</strong></div>
<div class="ace-line ace-line old-record-id-Qft3dlbCloTz5txGriccPi0vn7L">提升 SQL Binding 的使用体验，鼓励用户创建和管理大量的执行计划，以稳定数据库性能。</div>
</li>
<li class="ace-line ace-line old-record-id-R0d9dcUtVoAjNGxieJFczM0Tnif" data-list="bullet">
<div><strong>资源组增强对复杂 </strong><strong>SQL</strong><strong> 的控制（GA）</strong></div>
<div class="ace-line ace-line old-record-id-IcQsdbnx8oUgJbxKaxYcyLKbn9e">在复杂 SQL 完成前间歇性衡量它的 RU 消耗，避免它在执行期间对整个系统的产生过大影响。</div>
</li>
<li class="ace-line ace-line old-record-id-BuH1dgPsVos8z9xtaKxcCsSjnIg" data-list="bullet">
<div><strong>自动切换超预期查询的资源组（GA）</strong></div>
<div class="ace-line ace-line old-record-id-J98edjLl1oXQhRxZnafcYJZAn7c">当一个查询被认定为 runaway query，用户可以选择将其置入一个特定资源组，为其资源消耗设置上限。</div>
</li>
<li class="ace-line ace-line old-record-id-Yd9Ld8Arvom4mKxtuCScAo94npI" data-list="bullet">
<div><strong>限制表元信息的内存消耗（GA）</strong></div>
<div class="ace-line ace-line old-record-id-Br7sdYtfHoRNcGxifiVcGof3nGb">减小大规模集群下表的元信息对内存的消耗，提升大规模集群的稳定性。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-KkoidMWqqokAY0xvoLcc2nc6nJg">&nbsp;</div>
</td>
<td style="width: 188.875px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-SWd0dSxb7o0RGAxvlmqcW4FCnrg" data-list="bullet">
<div><strong>更可靠的数据备份 </strong></div>
<div class="ace-line ace-line old-record-id-NufVdj4oKoiAnFx54pGc3S7unGg">减少数据备份过程中可能出现的内存不足等问题，并确保备份数据的可用性。</div>
</li>
<li class="ace-line ace-line old-record-id-Ct5ydWjXJoisndxElzqc1fTsnnY" data-list="bullet">
<div><strong>常用算子均可落盘</strong></div>
<div class="ace-line ace-line old-record-id-UVKedpT5AoMSopxLUgccobjPnfg">HashAgg、Sort、TopN、HashJoin、WindowFunction、IndexJoin 和 IndexHashJoin 等常用算子均可落盘，进一步降低 OOM 风险。</div>
</li>
<li class="ace-line ace-line old-record-id-Pru6dxvw3orEv5x99TQcHap9n2e" data-list="bullet">
<div><strong>实例级执行计划缓存 （GA）</strong></div>
<div class="ace-line ace-line old-record-id-CvpIdXGj1ospZcxV56ncZ6jtnRb">同一个 TiDB 实例的所有会话可以共享执行计划缓存，提升内存利用率。</div>
</li>
<li class="ace-line ace-line old-record-id-W7EPdrJIIo8uqSxj28ncKN7wnbh" data-list="bullet">
<div><strong>资源组优先满足限额内定义的用量(RU) （GA）</strong></div>
<div class="ace-line ace-line old-record-id-NKmKdKowAoESHXxnJ2VcwcInnih">动态管调整 Burstable 资源组使用的资源上限。在不影响其他资源组限额的情况下，充分利用剩余资源。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-RazQd5qovoctOGxJcNocPH58nug">&nbsp;</div>
</td>
<td style="width: 138.609px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-ZjTXdkUEfoqzPXxcktecM6IOnmh" data-list="bullet">
<div><strong>自适应资源组</strong></div>
<div class="ace-line ace-line old-record-id-YSBzdrm0LojVkxxLRxsccZT7nuQ">资源组根据过往的运行情况自动调整资源组的 RU 设定。</div>
</li>
<li class="ace-line ace-line old-record-id-TAEEdhgx8oKEToxzJngcfnLTnub" data-list="bullet">
<div><strong>强化的内存保护</strong></div>
<div class="ace-line ace-line old-record-id-Rg6EdeByYojOy0xJc7bcO5cynoc">TiDB 主动对所有模块的内存使用进行监控，阻止一切可能影响系统稳定的内存操作。</div>
</li>
<li class="ace-line ace-line old-record-id-DfLVdzhqDoF7G1xkIMac1661nUd" data-list="bullet">
<div><strong>自动 </strong><strong>SQL</strong><strong> 绑定</strong></div>
<div class="ace-line ace-line old-record-id-VuO7dPqzxoZE6oxmzx0cZHefnte">通过对 SQL 运行指标的收集和分析，对一部分执行计划自动创建绑定，提升 TP 类系统的执行计划稳定性。</div>
</li>
<li class="ace-line ace-line old-record-id-Y881d9bCpoEgZ1xCkSxch4fZnvc" data-list="bullet">
<div><strong>多版本统计信息</strong></div>
<div class="ace-line ace-line old-record-id-H0XBd0xwpoNkijxfTdncnTCZnjK">当统计信息被更新后，用户可以查看统计信息的过往版本，并能够选择恢复过去某个版本的统计信息。</div>
</li>
<li class="ace-line ace-line old-record-id-FgJzdPA20oFwwCx1TcfcbS4onV0" data-list="bullet">
<div><strong>分布式统计信息收集</strong></div>
<div class="ace-line ace-line old-record-id-Mgh1dRVPIoYmxgxs4aGcWNkjnAh">统计信息收集支持在多个 TiDB 节点上并行进行，提升收集效率。</div>
</li>
</ul>
</td>
</tr>
<tr>
<td style="width: 64.6172px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-F9kedDuSUohy57xqRiwcsVCqnsg"><strong>数据库管理与可观测性</strong></div>
<div class="ace-line ace-line old-record-id-Uj6AdPoiIoVkyAxVM1HcdMt7nU0">通过主动监控和管理，确保系统平稳运行。</div>
</td>
<td style="width: 152.898px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-E9ZddaQ2HoPiBmxHcyfczad8nNt" data-list="bullet">
<div><strong>可靠地终止操作（GA）</strong></div>
<div class="ace-line ace-line old-record-id-RuvudWRbXoPZLVxVZlzconxUnff">正在运行中的 SQL 语句能够被立即终止，并从 TiDB 和 TiKV 中释放相应的资源。</div>
</li>
<li class="ace-line ace-line old-record-id-WAFud3NNFooELCxfmzDcdDsCncd" data-list="bullet">
<div><strong>切换资源组的权限控制（GA）</strong></div>
<div class="ace-line ace-line old-record-id-MnLsdUA29ocutJxzcnFcX9UqnTL">只有被授予特定权限的用户，才可以切换自身的资源组，防止资源被滥用。</div>
</li>
<li class="ace-line ace-line old-record-id-S8iKd4kikonxJuxDl4JcTvoqn0f" data-list="bullet">
<div><strong>增加对 </strong><strong>TiDB</strong><strong> 和 </strong><strong>TiKV</strong><strong> CPU 时间的观测（GA）</strong></div>
<div class="ace-line ace-line old-record-id-DUU9dZnOzoILD3xNysZcxGsDnsf">在 statements 记录、慢日志中增加 TiDB 和 TiKV CPU 时间的指标，方便快速定位 造成 TiDB 或者 TiKV CPU 飙升的语句。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-PaTGd5EuNoVSjFxEtgEchvSUnzh">&nbsp;</div>
</td>
<td style="width: 188.875px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-KmEcdLdRgoj7MtxphDJcrCjwngc" data-list="bullet">
<div><strong>细粒度定制统计信息收集策略（GA）</strong></div>
<div class="ace-line ace-line old-record-id-C1oMdlrpXohFgcxL4dMcN7Hpnib">用户可以针对特定表修改统计信息收集的策略，比如健康度。</div>
</li>
<li class="ace-line ace-line old-record-id-MTsYd34gPord9ox9OLPcN6UDn1d" data-list="bullet">
<div><strong>Workload Repository（</strong><strong>GA</strong><strong>）</strong></div>
<div class="ace-line ace-line old-record-id-ZVhfd2aYZoyN02xfiUWcTcBlnTd">TiDB 持久化内存中记录的负载信息，包括累计统计数据和实时统计数据，有助于故障排查和分析。</div>
</li>
<li class="ace-line ace-line old-record-id-RlmRdtRrgo7CFfxwakicKazYnjb" data-list="bullet">
<div><strong>自动索引推荐（GA）</strong></div>
<div class="ace-line ace-line old-record-id-Z1LPdbsMpoDgEoxBmAMcEnfSnhD">TiDB 自动分析有优化价值的 SQL，推荐创建新索引或删除已有索引。</div>
</li>
<li class="ace-line ace-line old-record-id-MTZGdhDUxoOQR1xqsBZcfa23nob" data-list="bullet">
<div><strong>标准时间模型（GA）</strong></div>
<div class="ace-line ace-line old-record-id-Nfe5dKK30opt57xtdRqcj9uNnTe">对 SQL 的运行时间进行标准化定义，以此为基础定义数据库负载。 通过观测 statements 记录、慢日志、 聚合的集群指标，用户能够准确发现产生异常负载的节点及 SQL。</div>
</li>
<li class="ace-line ace-line old-record-id-DOUydqPVfogfdaxFYthcVa6Unjd" data-list="bullet">
<div><strong>增加对 </strong><strong>TiFlash</strong><strong> CPU 时间的观测（GA）</strong></div>
<div class="ace-line ace-line old-record-id-AW8KdDbeAoKnSox2gJtcrMKWntg">在 statements 记录、慢日志中增加 TiFlash CPU 时间的指标，方便快速定位 造成 TiFlash CPU 飙升的语句。</div>
</li>
</ul>
</td>
<td style="width: 138.609px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-Bs2EdKNInolem5xkR5mcptpLnQh" data-list="bullet">
<div><strong>负载分析</strong></div>
<div class="ace-line ace-line old-record-id-Ay2LdDh7MoiAKEx9SvDc6d9DnR6">分析 Workload Repository 中的过往负载数据，根据分析结果提出优化建议，例如 SQL 调优和统计信息收集策略调整。</div>
</li>
<li class="ace-line ace-line old-record-id-IWITdLDNmowTBMxFPq6cvEginof" data-list="bullet">
<div><strong>全链路监控</strong></div>
<div class="ace-line ace-line old-record-id-TiUvd4Cp4oVMd0xm4HZcHLZcnHe">跟踪单条 SQL 语句在其运行的整个生命周期的时间消耗，包括 TiDB， PD，TiKV 和 TiFlash。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-Wj4Fd0ES4oTurkx5HW1cdwJgnGd">&nbsp;</div>
</td>
</tr>
<tr>
<td style="width: 64.6172px; vertical-align: top;" colspan="1" rowspan="1">
<div class="ace-line ace-line old-record-id-LcSCdO8WGoQIocxMlAacwxDGn5c"><strong>安全</strong></div>
<div class="ace-line ace-line old-record-id-U6dfdPmIio2miZxzKXucuueanRe">增强数据安全与隐私保护</div>
<div class="ace-line ace-line old-record-id-O6vydhv8uo6ihUxGJzecgL8YnlL">&nbsp;</div>
</td>
<td style="width: 152.898px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-O1X0dCIaSoYfmDxIje4ckRlenUh" data-list="bullet">
<div><strong>Google Cloud KMS（</strong><strong>GA</strong><strong>）</strong></div>
<div class="ace-line ace-line old-record-id-Tj6cdGvaaoMVFBx6FeGcYTKVn3e">完善静态加密基于 Google Cloud KMS 的密钥管理机制，使其成为正式功能。</div>
</li>
<li class="ace-line ace-line old-record-id-Wn4rdqsLro3xPMx03m1ckMxunfd" data-list="bullet">
<div><strong>Azure</strong><strong> Key Vault</strong></div>
<div class="ace-line ace-line old-record-id-Ix9sdTTpbodDRlxjWODcw9UunCg">基于 Azure Key Vault 增强静态加密的密钥管理机制。</div>
</li>
<li class="ace-line ace-line old-record-id-Sh27dd0ZcoTDWcx6J6GcEEsknng" data-list="bullet">
<div><strong>基于标记的日志脱敏</strong></div>
<div class="ace-line ace-line old-record-id-VEk6d6FSdoVQd8xEX62cAm13nLb">支持在集群日志中标记敏感信息，然后可以根据使用场景决定是否对其进行脱敏。</div>
</li>
<li class="ace-line ace-line old-record-id-WA4pdYtQsoCWChx2oGocxTusnAe" data-list="bullet">
<div><strong>列级权限管理（GA）</strong></div>
<div class="ace-line ace-line old-record-id-SQzddakvPoHiXix6tD1c8bzunhg">支持兼容 MySQL 的列级权限管理机制。</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-FCYXdeEFXohCRtxmVmUcPjIGn1d">&nbsp;</div>
<div class="ace-line ace-line old-record-id-FCRJdtzlVogIaYx6mFtc3iGznRb">&nbsp;</div>
</td>
<td style="width: 188.875px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-Su8od7z84o7rnyxPuNrc8PoGngc" data-list="bullet">
<div><strong>AWS</strong><strong> 的 </strong><strong>IAM</strong><strong> 认证</strong></div>
<div class="ace-line ace-line old-record-id-Yt5cdY3hzo928jxwZrrcaaYdnfm">TiDB 作为 AWS 第三方 ARN 以访问 AWS IAM。</div>
</li>
<li class="ace-line ace-line old-record-id-JJzFduTAsoTa0Jxv3kJcrqUbnBe" data-list="bullet">
<div><strong>Kerberos 认证（</strong><strong>GA</strong><strong>）</strong></div>
<div class="ace-line ace-line old-record-id-FMTVdogfMom7Z4xM4CCca1wBnkh">支持基于 Kerberos 的身份验证。</div>
</li>
<li class="ace-line ace-line old-record-id-GHnkdr6vEoZWkHxWC2AcD1Fmndc" data-list="bullet">
<div><strong>MFA</strong></div>
<div class="ace-line ace-line old-record-id-R38NdQPGsofBBPxpsficXjU1nEb">增加对多因素认证的支持，增强用户对多因素认证机制的验证。</div>
</li>
<li class="ace-line ace-line old-record-id-ULRQdy1qYoaMwUx9DOGcKnOKnCf" data-list="bullet">
<div><strong>组件之间的 TLS 改进（GA）</strong></div>
<div class="ace-line ace-line old-record-id-TV4bdE4iaocZfjxLRyVcKW4pnMQ">确保 TiDB 集群的所有组件之间的连接支持加密传输。</div>
</li>
<li class="ace-line ace-line old-record-id-I4sRdrMhoo2gn4xdRRAcPG6nnXf" data-list="bullet">
<div><strong>完善动态权限 </strong></div>
<div class="ace-line ace-line old-record-id-CmnRdGRotoJ7rGxZDymcxWswn4J">完善动态权限设计，限制 Super 权限的实现。</div>
</li>
<li class="ace-line ace-line old-record-id-ODi9d1kxLowG9AxcMSNchCI2nIh" data-list="bullet">
<div><strong>FIPS （</strong><strong>GA</strong><strong>）</strong></div>
<div class="ace-line ace-line old-record-id-DDq4d9MzFodu2nxq2osccFkNnPh">加密场景符合 FIPS 标准。</div>
</li>
</ul>
</td>
<td style="width: 138.609px; vertical-align: top;" colspan="1" rowspan="1">
<ul class="list-bullet1">
<li class="ace-line ace-line old-record-id-LLCEdW9VuoalVvxCvhpcnKl2ngn" data-list="bullet">
<div><strong>基于标签的访问控制机制</strong></div>
<div class="ace-line ace-line old-record-id-B1Bedpce6oOoQGxOYnTcSnsNnBE">支持通过配置标签的方式，通过标签形式对数据进行访问控制</div>
</li>
<li class="ace-line ace-line old-record-id-NgfKdUuoxoW2ruxvAJpc5IsEn7d" data-list="bullet">
<div><strong>增强的客户端加密</strong></div>
<div class="ace-line ace-line old-record-id-NpfTd0WINoSqPHxKxDIcLWrDn6d">支持客户端对关键字段加密，增强数据安全性</div>
</li>
<li class="ace-line ace-line old-record-id-WjP7dhljjoMiiZx53yTcDjMOnHe" data-list="bullet">
<div><strong>业务数据动态脱敏</strong></div>
<div class="ace-line ace-line old-record-id-KjkcdeTvUoGHemxT7swcVeVZnAb">基于不同数据应用场景的数据脱敏，保证重要领域的数据安全</div>
</li>
</ul>
<div class="ace-line ace-line old-record-id-Ed0mdDAx5oS6KaxFzlNc7ddsnae">&nbsp;</div>
</td>
</tr>
</tbody>
</table>

> **注意：**
>
> 上述表格中并未列出所有计划发布的内容。另外，不同的服务订阅版本中的功能可能有所不同。
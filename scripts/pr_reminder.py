import sys
import requests
from lxml import etree
from datetime import datetime
from string import Template

docs_cn_url = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr'
docs_url = 'https://github.com/pingcap/docs/pulls?q=is%3Apr'
open_url = '+is%3Aopen+is%3Apr'
close_url = '+is%3Aclosed+label%3Atranslation%2Fdoing'
sig_sql_infra = '+label%3Asig%2Fsql-infra'
sig_planner = '+label%3Asig%2Fplanner'
sig_engine = '+label%3Asig%2Fengine'
sig_scheduling = '+label%3Asig%2Fscheduling'
sig_migrate = '+label%3Asig%2Fmigrate'
sig_tiup = '+label%3Asig%2Ftiup'
sig_bigdata = '+label%3Asig%2Fbigdata'
sig_diagnosis = '+label%3Asig%2Fdiagnosis'
sig_transaction = '+label%3Asig%2Ftransaction'
area_security = '+label%3Aarea%2Fsecurity'
v54 = '+label%3Av5.4'
type_compatibility_change = '+label%3Atype%2Fcompatibility-or-feature-change'
type_oncall = '+label%3AONCALL'
type_bugfix = '+label%3Atype%2Fbug-fix'
type_enhancement = '+label%3Atype%2Fenhancement'
# docs-cn PR URL lists
compat_open_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fcompatibility-or-feature-change'
compat_close_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Aclosed+is%3Apr+label%3Atype%2Fcompatibility-or-feature-change+label%3Atranslation%2Fdoing'
oncall_open_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3AONCALL+is%3Aopen+'
oncall_close_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3AONCALL+is%3Aclosed+label%3Atranslation%2Fdoing+'
bugfix_open_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atype%2Fbug-fix+is%3Aopen+'
bugfix_close_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atype%2Fbug-fix+is%3Aclosed+label%3Atranslation%2Fdoing'
# enhance_open_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fenhancement'
# enhance_close_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atype%2Fenhancement+is%3Aclosed+label%3Atranslation%2Fdoing'
# docs PR URL lists
compat_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fcompatibility-or-feature-change'
compat_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Aclosed+is%3Apr+label%3Atype%2Fcompatibility-or-feature-change+label%3Atranslation%2Fdoing'
oncall_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3AONCALL+is%3Aopen+'
oncall_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3AONCALL+is%3Aclosed+label%3Atranslation%2Fdoing+'
bugfix_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Atype%2Fbug-fix+is%3Aopen+'
bugfix_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Atype%2Fbug-fix+is%3Aclosed+label%3Atranslation%2Fdoing'
# enhance_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fenhancement'
# enhance_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Atype%2Fenhancement+is%3Aclosed+label%3Atranslation%2Fdoing'


def get_pr_no(url):

    page_text = requests.get(url=url).text
    tree = etree.HTML(page_text)
    pr_no = tree.xpath('//div[@class="table-list-header-toggle states flex-auto pl-0"]/a[@class="btn-link selected"]/text()')[1].strip()
    if pr_no:
        if pr_no.endswith('d'):
            return int(pr_no[:-7])
        if pr_no.endswith('n'):
            return int(pr_no[:-5])
    #    print("未抓取到 PR 数目")
    else:
        return 0


TEMPLATE = '''
*************************************************
待处理的 PR 数目报告
查询时间：{date}
待处理 PR 数目如下，按优先级排序
*************************************************

v5.4 发版文档，中文文档截止日期 2021-01-07，英文文档截止日期 2021-01-18

- sig/sql-infra 和 sig/planner

    - docs-cn 仓库中有 {v54_zh_open_sqlinfra_planner} PR 未合并，有 {v54_zh_close_sqlinfra_planner} PR 待翻译
    - docs 仓库中有 {v54_en_open_sqlinfra_planner} PR 未合并，有 {v54_en_close_sqlinfra_planner} PR 待翻译

- sig/engine 和 sig/scheduling

    - docs-cn 仓库中有 {v54_zh_open_engine_scheduling} PR 未合并，有 {v54_zh_close_engine_scheduling} PR 待翻译
    - docs 仓库中有 {v54_en_open_engine_scheduling} PR 未合并，有 {v54_en_close_engine_scheduling} PR 待翻译

- sig/migrate

    - docs-cn 仓库中有 {v54_zh_open_migrate} PR 未合并，有 {v54_zh_close_migrate} PR 待翻译
    - docs 仓库中有 v54_en_open_migrate PR 未合并，有 {v54_en_close_migrate} PR 待翻译

- sig/bigdata、sig/tiup 和 sig/diagnosis

    - docs-cn 仓库中有 {v54_zh_open_bigdata_tiup_diagnosis} PR 未合并，有 {v54_zh_close_bigdata_tiup_diagnosis} PR 待翻译
    - docs 仓库中有 {v54_en_open_bigdata_tiup_diagnosis} PR 未合并，有 {v54_en_close_bigdata_tiup_diagnosis} PR 待翻译

- sig/transaction 和 area/security

    - docs-cn 仓库中有 {v54_zh_open_transaction_security} PR 未合并，有 {v54_zh_close_transaction_security} PR 待翻译
    - docs 仓库中有 {v54_en_open_transaction_security} PR 未合并，有 {v54_en_close_transaction_security} PR 待翻译

*************************************************

type/compatibility-or-feature-change 标签
兼容性变更类文档，刻不容缓，请尽快处理：

- docs-cn 仓库中共有 {compat_open_zh} PR 未合并，有 {compat_close_zh} PR 待翻译

其中：sig/sql-infra
- docs 仓库中有 {compat_open_en} PR 未合并，有 {compat_close_en} PR 待翻译

*************************************************

ONCALL 标签
文档被读者挑出问题，读者反馈不容小视，请尽快处理：

- docs-cn 仓库中有 {oncall_open_zh} PR 未合并，有 {oncall_close_zh} PR 待翻译
- docs 仓库中有 {oncall_open_en} PR 未合并，有 {oncall_close_en} PR 待翻译

*************************************************

type/bug-fix 文档 bug 影响用户体验，请尽快处理：

- docs-cn 仓库中有 {bugfix_open_zh} PR 未合并，有 {bugfix_close_zh} PR 待翻译
- docs 仓库中有 {bugfix_open_en} PR 未合并，有 {bugfix_close_en} PR 待翻译
*************************************************
'''


if __name__ == "__main__":

    data = {
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'v54_zh_open_sqlinfra_planner': str(get_pr_no(docs_cn_url + open_url+ sig_sql_infra + v54) + get_pr_no(docs_cn_url + open_url+ sig_planner + v54)),
        'v54_zh_close_sqlinfra_planner': str(get_pr_no(docs_cn_url + close_url+ sig_sql_infra + v54) + get_pr_no(docs_cn_url + close_url+ sig_planner + v54)),
        'v54_en_open_sqlinfra_planner': str(get_pr_no(docs_url + open_url+ sig_sql_infra + v54) + get_pr_no(docs_url + open_url+ sig_planner + v54)),
        'v54_en_close_sqlinfra_planner': str(get_pr_no(docs_url + close_url+ sig_sql_infra + v54) + get_pr_no(docs_url + close_url+ sig_planner + v54)),
        'v54_zh_open_engine_scheduling': str(get_pr_no(docs_cn_url + open_url+ sig_engine + v54) + get_pr_no(docs_cn_url + open_url+ sig_scheduling + v54)),
        'v54_zh_close_engine_scheduling': str(get_pr_no(docs_cn_url + close_url+ sig_engine + v54) + get_pr_no(docs_cn_url + close_url+ sig_scheduling + v54)),
        'v54_en_open_engine_scheduling': str(get_pr_no(docs_url + open_url+ sig_engine + v54) + get_pr_no(docs_url + open_url+ sig_scheduling + v54)),
        'v54_en_close_engine_scheduling': str(get_pr_no(docs_url + close_url+ sig_engine + v54) + get_pr_no(docs_url + close_url+ sig_scheduling + v54)),
        'v54_zh_open_migrate': str(get_pr_no(docs_cn_url + open_url + sig_migrate + v54)),
        'v54_zh_close_migrate': str(get_pr_no(docs_cn_url + close_url + sig_migrate + v54)),
        'v54_en_open_migrate': str(get_pr_no(docs_url + open_url + sig_migrate + v54)),
        'v54_en_close_migrate': str(get_pr_no(docs_url + close_url + sig_migrate + v54)),
        'v54_zh_open_bigdata_tiup_diagnosis': str(get_pr_no(docs_cn_url + open_url + sig_bigdata + v54) + get_pr_no(docs_cn_url + open_url + sig_tiup + v54) + get_pr_no(docs_cn_url + open_url + sig_diagnosis + v54)),
        'v54_zh_close_bigdata_tiup_diagnosis': str(get_pr_no(docs_cn_url + close_url + sig_bigdata + v54) + get_pr_no(docs_cn_url + close_url + sig_tiup + v54) + get_pr_no(docs_cn_url + close_url + sig_diagnosis + v54)),
        'v54_en_open_bigdata_tiup_diagnosis': str(get_pr_no(docs_url + open_url + sig_bigdata + v54) + get_pr_no(docs_url + open_url + sig_tiup + v54) + get_pr_no(docs_url + open_url + sig_diagnosis + v54)),
        'v54_en_close_bigdata_tiup_diagnosis': str(get_pr_no(docs_url + close_url + sig_bigdata + v54) + get_pr_no(docs_url + close_url + sig_tiup + v54) + get_pr_no(docs_url + close_url + sig_diagnosis + v54)),
        'v54_zh_open_transaction_security': str(get_pr_no(docs_cn_url + open_url + sig_transaction + v54) + get_pr_no(docs_cn_url + open_url + area_security + v54)),
        'v54_zh_close_transaction_security': str(get_pr_no(docs_cn_url + close_url + sig_transaction + v54) + get_pr_no(docs_cn_url + close_url + area_security + v54)),
        'v54_en_open_transaction_security': str(get_pr_no(docs_url + open_url + sig_transaction + v54) + get_pr_no(docs_url + open_url + area_security + v54)),
        'v54_en_close_transaction_security': str(get_pr_no(docs_url + close_url + sig_transaction + v54) + get_pr_no(docs_url + close_url + area_security + v54)),
        'compat_open_zh': str(get_pr_no(compat_open_url_zh)),
        'compat_close_zh': str(get_pr_no(compat_close_url_zh)),
        'compat_open_en': str(get_pr_no(compat_open_url_en)),
        'compat_close_en': str(get_pr_no(compat_close_url_en)),
        'oncall_open_zh': str(get_pr_no(oncall_open_url_zh)),
        'oncall_close_zh': str(get_pr_no(oncall_close_url_zh)),
        'oncall_open_en': str(get_pr_no(oncall_open_url_en)),
        'oncall_close_en': str(get_pr_no(oncall_close_url_en)),
        'bugfix_open_zh': str(get_pr_no(bugfix_open_url_zh)),
        'bugfix_close_zh': str(get_pr_no(bugfix_close_url_zh)),
        'bugfix_open_en': str(get_pr_no(bugfix_open_url_en)),
        'bugfix_close_en': str(get_pr_no(bugfix_close_url_en)),
        'v54_zh_open_sqlinfra_planner_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fsql-infra%2Csig%2Fplanner+label%3Av5.4+is%3Aopen',
        'v54_zh_close_sqlinfra_planner_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fsql-infra%2Csig%2Fplanner+label%3Av5.4+is%3Aclosed',
        'v54_en_open_sqlinfra_planner_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fsql-infra%2Csig%2Fplanner+label%3Av5.4+is%3Aopen',
        'v54_en_close_sqlinfra_planner_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fsql-infra%2Csig%2Fplanner+label%3Av5.4+is%3Aclosed',
        'v54_zh_open_engine_scheduling_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fengine%2Csig%2Fscheduling+label%3Av5.4+is%3Aopen+',
        'v54_zh_close_engine_scheduling_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fengine%2Csig%2Fscheduling+label%3Av5.4+is%3Aclosed',
        'v54_en_open_engine_scheduling_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fengine%2Csig%2Fscheduling+label%3Av5.4+is%3Aopen+',
        'v54_en_close_engine_scheduling_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fengine%2Csig%2Fscheduling+label%3Av5.4+is%3Aclosed',
        'v54_zh_open_migrate_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fmigrate+label%3Av5.4+is%3Aopen',
        'v54_zh_close_migrate_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fmigrate+label%3Av5.4+is%3Aclosed',
        'v54_en_open_migrate_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fmigrate+label%3Av5.4+is%3Aopen',
        'v54_en_close_migrate_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fmigrate+label%3Av5.4+is%3Aclosed',
        'v54_zh_open_bigdata_tiup_diagnosis_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fbigdata%2Csig%2Ftiup%2Csig%2Fdiagnosis+label%3Av5.4+is%3Aopen',
        'v54_zh_close_bigdata_tiup_diagnosis_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Fbigdata%2Csig%2Ftiup%2Csig%2Fdiagnosis+label%3Av5.4+is%3Aclosed',
        'v54_en_open_bigdata_tiup_diagnosis_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fbigdata%2Csig%2Ftiup%2Csig%2Fdiagnosis+label%3Av5.4+is%3Aopen',
        'v54_en_close_bigdata_tiup_diagnosis_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Fbigdata%2Csig%2Ftiup%2Csig%2Fdiagnosis+label%3Av5.4+is%3Aclosed',
        'v54_zh_open_transaction_security_url': 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Asig%2Ftransaction%2Carea%2Fsecurity+label%3Av5.4+is%3Aopen',
        'v54_zh_close_transaction_security_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Ftransaction%2Carea%2Fsecurity+label%3Av5.4+is%3Aclosed',
        'v54_en_open_transaction_security_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Ftransaction%2Carea%2Fsecurity+label%3Av5.4+is%3Aopen',
        'v54_en_close_transaction_security_url': 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Asig%2Ftransaction%2Carea%2Fsecurity+label%3Av5.4+is%3Aclosed',
        'compat_open_url_zh': compat_open_url_zh,
        'compat_close_url_zh': compat_close_url_zh,
        'compat_open_url_en': compat_open_url_en,
        'compat_close_url_en': compat_close_url_en,
        'oncall_open_url_zh': oncall_open_url_zh,
        'oncall_close_url_zh': oncall_close_url_zh,
        'oncall_open_url_en': oncall_open_url_en,
        'oncall_close_url_en': oncall_close_url_en,
        'bugfix_open_url_zh': bugfix_open_url_zh,
        'bugfix_close_url_zh': bugfix_close_url_zh,
        'bugfix_open_url_en': bugfix_open_url_en,
        'bugfix_close_url_en': bugfix_close_url_en
    }

    #    report = TEMPLATE.format(**data)
    #    FILENAME_TMPL = "{date}_report.txt"
    #    filename = FILENAME_TMPL.format(date=data['date'])

    #    with open(filename, 'w') as file:
    #        file.write(report)
    # print(report)

    # Get bot webhook from the environment variables
    URL = sys.argv[1]

    d = Template("""{
        "msg_type": "post",
        "content": {
            "post": {
                "zh-CN": {
                    "title": "待处理的 PR 数目报告",
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": "查询时间：${date}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "待处理 PR 数目如下，按优先级排序"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "*************************************************"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "v5.4 发版文档，中文文档截止日期 2021-01-07，英文文档截止日期 2021-01-18"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- sig/sql-infra 和 sig/planner"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs-cn 仓库中有 ${v54_zh_open_sqlinfra_planner} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_open_sqlinfra_planner_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_zh_close_sqlinfra_planner} PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${v54_zh_close_sqlinfra_planner_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs 仓库中有 ${v54_en_open_sqlinfra_planner} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_open_sqlinfra_planner_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_en_close_sqlinfra_planner} PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${v54_en_close_sqlinfra_planner_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- sig/engine 和 sig/scheduling"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs-cn 仓库中有 ${v54_zh_open_engine_scheduling} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_open_engine_scheduling_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_zh_close_engine_scheduling} PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${v54_zh_close_engine_scheduling_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs 仓库中有 ${v54_en_open_engine_scheduling} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_open_engine_scheduling_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_en_close_engine_scheduling} PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${v54_en_close_engine_scheduling_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- sig/migrate"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs-cn 仓库中有 ${v54_zh_open_migrate} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_open_migrate_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_zh_close_migrate} PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${v54_zh_close_migrate_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs 仓库中有 ${v54_en_open_migrate} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_open_migrate_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_en_close_migrate} PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${v54_en_close_migrate_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "sig/bigdata、sig/tiup 和 sig/diagnosis"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs-cn 仓库中有 ${v54_zh_open_bigdata_tiup_diagnosis} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_open_bigdata_tiup_diagnosis_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_zh_close_bigdata_tiup_diagnosis} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_close_bigdata_tiup_diagnosis_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs 仓库中有 ${v54_en_open_bigdata_tiup_diagnosis} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_open_bigdata_tiup_diagnosis_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_en_close_bigdata_tiup_diagnosis} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_close_bigdata_tiup_diagnosis_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- sig/transaction 和 area/security"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs-cn 仓库中有 ${v54_zh_open_transaction_security} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_open_transaction_security_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_zh_close_transaction_security} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_zh_close_transaction_security_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs 仓库中有 ${v54_en_open_transaction_security} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_open_transaction_security_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${v54_en_close_transaction_security} PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${v54_en_close_transaction_security_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "*************************************************"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "type/compatibility-or-feature-change 标签"
                            }
                        ],
                        [
                            {
                            "tag": "text",
                            "text": "兼容性变更类文档，刻不容缓，请尽快处理："
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs-cn 仓库中有 ${compat_open_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${compat_open_url_zh}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${compat_close_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${compat_close_url_zh}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs 仓库中有 ${compat_open_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${compat_open_url_en}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${compat_close_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${compat_close_url_en}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "*************************************************"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "ONCALL 标签"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "文档被读者挑出问题，读者反馈不容小视，请尽快处理："
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs-cn 仓库中有 ${oncall_open_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${oncall_open_url_zh}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${oncall_close_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${oncall_close_url_zh}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs-cn 仓库中有 ${oncall_open_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${oncall_open_url_en}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${oncall_close_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${oncall_close_url_en}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "*************************************************"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "type/bug-fix 文档 bug 影响用户体验，请尽快处理："
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs-cn 仓库中有 ${bugfix_open_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${bugfix_open_url_zh}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${bugfix_close_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${bugfix_close_url_zh}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs 仓库中有 ${bugfix_open_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${bugfix_open_url_en}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${bugfix_close_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${bugfix_close_url_en}"
                            }
                        ]
                    ]
                }
            }
        }
    }""")

    headers = {
    'Content-Type': 'application/json'
    }

    r_data=d.substitute(data).encode('utf-8')

    r_docs = requests.request("POST", URL, headers=headers, data=r_data)

    print(f'{r_docs.status_code} {r_docs.reason}')
    # print(r_docs.text)

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
area_dm = '+label%3Aarea%2Fdm'
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
enhance_open_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fenhancement'
enhance_close_url_zh = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr+label%3Atype%2Fenhancement+is%3Aclosed+label%3Atranslation%2Fdoing'
# docs PR URL lists
compat_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fcompatibility-or-feature-change'
compat_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Aclosed+is%3Apr+label%3Atype%2Fcompatibility-or-feature-change+label%3Atranslation%2Fdoing'
oncall_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3AONCALL+is%3Aopen+'
oncall_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3AONCALL+is%3Aclosed+label%3Atranslation%2Fdoing+'
bugfix_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Atype%2Fbug-fix+is%3Aopen+'
bugfix_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Atype%2Fbug-fix+is%3Aclosed+label%3Atranslation%2Fdoing'
enhance_open_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Aopen+is%3Apr+label%3Atype%2Fenhancement'
enhance_close_url_en = 'https://github.com/pingcap/docs/pulls?q=is%3Apr+label%3Atype%2Fenhancement+is%3Aclosed+label%3Atranslation%2Fdoing'


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

type/enhancement 文档优化，优化后的文档更易用哦：

- docs-cn 仓库中有 {enhance_open_zh} PR 未合并，有 {enhance_close_zh} PR 待翻译
- docs 仓库中有 {enhance_open_en} PR 未合并，有 {enhance_close_en} PR 待翻译
*************************************************

'''


if __name__ == "__main__":

    data = {
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
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
        'enhance_open_zh': str(get_pr_no(enhance_open_url_zh)),
        'enhance_close_zh': str(get_pr_no(enhance_close_url_zh)),
        'enhance_open_en': str(get_pr_no(enhance_open_url_en)),
        'enhance_close_en': str(get_pr_no(enhance_close_url_en)),
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
        'bugfix_close_url_en': bugfix_close_url_en,
        'enhance_open_url_zh': enhance_open_url_zh,
        'enhance_close_url_zh': enhance_close_url_zh,
        'enhance_open_url_en': enhance_open_url_en,
        'enhance_close_url_en': enhance_close_url_en
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
                    "title": "待处理的非发版文档 PR 数目报告",
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
                                "text": "待处理的非发版文档 PR 数目如下，按优先级排序，我们为发版文档让路，我们为发版文档让路！"
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
                                "text": ""
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
                                "text": ""
                            }
                        ],
                        [
                            {
                            "tag": "text",
                            "text": "P1：兼容性变更类文档，及时告知用户配置项、默认值等变更，助力用户顺利用上新版 TiDB~"
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
                                "text": ""
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
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "P2：用户反馈的文档问题，我们及时改正的热忱带给他们暖心的体验~"
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
                                "text": "- docs 仓库中有 ${oncall_open_en} PR "
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
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "type/bug-fix 标签"
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
                                "text": "P3：已知文档 bug 影响用户体验，让我们一起扫除小虫子吧~"
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
                                "text": ""
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "type/enhancement 标签"
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
                                "text": "P4：优化后的文档，更易读易懂哦~"
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
                                "text": "- docs-cn 仓库中有 ${enhance_open_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${enhance_open_url_zh}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${enhance_close_zh} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${enhance_close_url_zh}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "- docs 仓库中有 ${enhance_open_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${enhance_open_url_en}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${enhance_close_en} PR "
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${enhance_close_url_en}"
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

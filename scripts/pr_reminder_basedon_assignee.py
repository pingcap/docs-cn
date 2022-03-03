from os import close
import sys
import requests
from lxml import etree
from datetime import datetime
from string import Template

docs_cn_url = 'https://github.com/pingcap/docs-cn/pulls?q=is%3Apr'
docs_url = 'https://github.com/pingcap/docs/pulls?q=is%3Apr'
open_url = '+is%3Aopen+is%3Apr'
close_url = '+is%3Aclosed+label%3Atranslation%2Fdoing'
v60 = '+label%3Av6.0'
type_compatibility_change = '+label%3Atype%2Fcompatibility-or-feature-change'
type_oncall = '+label%3AONCALL'
type_bugfix = '+label%3Atype%2Fbug-fix'
type_enhancement = '+label%3Atype%2Fenhancement'
shichun_0415_assignee = '+assignee%3Ashichun-0415'
shichun_0415_author = '+author%3Ashichun-0415'
en_jin19_assignee = '+assignee%3Aen-jin19'
en_jin19_author = '+author%3Aen-jin19'
hfxsd_assignee = '+assignee%3Ahfxsd'
hfxsd_author = '+author%3Ahfxsd'
ran_huang_assignee = '+assignee%3Aran-huang'
ran_huang_author = '+author%3Aran-huang'
qiancai_assignee = '+assignee%3Aqiancai'
qiancai_author = '+author%3Aqiancai'
tomshawn_assignee = '+assignee%3ATomShawn'
tomshawn_author = '+author%3ATomShawn'


def get_pr_no(url):

    page_text = requests.get(url=url).text
    tree = etree.HTML(page_text)
    pr_no = tree.xpath('//div[@class="table-list-header-toggle states flex-auto pl-0"]/a[@class="btn-link selected"]/text()')[1].strip()
    if pr_no:
        if pr_no.endswith('d'):
            return str(pr_no[:-7])
        if pr_no.endswith('n'):
            return str(pr_no[:-5])
    #    print("未抓取到 PR 数目")
    else:
        return 0


TEMPLATE = '''
*************************************************
待处理的 PR 数目报告
查询时间：{date}
待处理 PR 数目如下
*************************************************

v6.0 发版文档，中文文档截止日期 2022-03-25，英文文档截止日期 2022-04-01

- en-jin19

    - docs-cn：有 {en-jin19-zh-assignee-open} 个未合源语 PR 待处理，有 {en-jin19-zh-assignee-close} 个已合源语 PR 待翻译，已翻译了 {en-jin19-zh-author-open} 个 PR 未合并
    - docs：有 {en-jin19-en-assignee-open} 个未合源语 PR 待处理，有 {en-jin19-en-assignee-close} 个已合源语 PR 待翻译，已翻译了 {en-jin19-en-author-open} 个 PR 未合并

- shichun-0415

    - docs-cn：有 {shichun-0415-zh-assignee-open} 个未合源语 PR 待处理，有 {shichun-0415-zh-assignee-close} 个已合源语 PR 待翻译，已翻译了 {shichun-0415-zh-author-open} 个 PR 未合并
    - docs：有 {shichun-0415-en-assignee-open} 个未合源语 PR 待处理，有 {shichun-0415-en-assignee-close} 个已合源语 PR 待翻译，已翻译了 {shichun-0415-en-author-open} 个 PR 未合并

- hfxsd

    - docs-cn：有 {hfxsd-zh-assignee-open} 个未合源语 PR 待处理，有 {hfxsd-zh-assignee-close} 个已合源语 PR 待翻译，已翻译了 {hfxsd-zh-author-open} 个 PR 未合并
    - docs：有 {hfxsd-en-assignee-open} 个未合源语 PR 待处理，有 {hfxsd-en-assignee-close} 个已合源语 PR 待翻译，已翻译了 {hfxsd-en-author-open} 个 PR 未合并

- ran-huang

    - docs-cn：有 {ran-huang-zh-assignee-open} 个未合源语 PR 待处理，有 {ran-huang-zh-assignee-close} 个已合源语 PR 待翻译，已翻译了 {ran-huang-zh-author-open} 个 PR 未合并
    - docs：有 {ran-huang-en-assignee-open} 个未合源语 PR 待处理，有 {ran-huang-en-assignee-close} 个已合源语 PR 待翻译，已翻译了 {ran-huang-en-author-open} 个 PR 未合并

- qiancai

    - docs-cn：有 {qiancai-zh-assignee-open} 个未合源语 PR 待处理，有 {qiancai-zh-assignee-close} 个已合源语 PR 待翻译，已翻译了 {qiancai-zh-author-open} 个 PR 未合并
    - docs：有 {qiancai-en-assignee-open} 个未合源语 PR 待处理，有 {qiancai-en-assignee-close} 个已合源语 PR 待翻译，已翻译了 {qiancai-en-author-open} 个 PR 未合并

- TomShawn

    - docs-cn：有 {tomshawn-zh-assignee-open} 个未合源语 PR 待处理，有 {tomshawn-zh-assignee-close} 个已合源语 PR 待翻译，已翻译了 {tomshawn-zh-author-open} 个 PR 未合并
    - docs：有 {tomshawn-en-assignee-open} 个未合源语 PR 待处理，有 {tomshawn-en-assignee-close} 个已合源语 PR 待翻译，已翻译了 {tomshawn-en-author-open} 个 PR 未合并
*************************************************
'''

if __name__ == "__main__":

    data = {
        'date': datetime.utcnow().strftime('%Y-%m-%d'),
        'shichun_0415_zh_assignee_open': get_pr_no(docs_cn_url + open_url + shichun_0415_assignee + v60),
        'shichun_0415_zh_assignee_close': get_pr_no(docs_cn_url + close_url + shichun_0415_assignee + v60),
        'shichun_0415_zh_author_open': get_pr_no(docs_cn_url + open_url + shichun_0415_author + v60),
        'shichun_0415_en_assignee_open': get_pr_no(docs_url + open_url + shichun_0415_assignee + v60),
        'shichun_0415_en_assignee_close': get_pr_no(docs_url + close_url + shichun_0415_assignee + v60),
        'shichun_0415_en_author_open': get_pr_no(docs_url + open_url + shichun_0415_author + v60),
        'en_jin19_zh_assignee_open': get_pr_no(docs_cn_url + open_url + en_jin19_assignee + v60),
        'en_jin19_zh_assignee_close': get_pr_no(docs_cn_url + close_url + en_jin19_assignee + v60),
        'en_jin19_zh_author_open': get_pr_no(docs_cn_url + open_url + en_jin19_author + v60),
        'en_jin19_en_assignee_open': get_pr_no(docs_url + open_url + en_jin19_assignee + v60),
        'en_jin19_en_assignee_close': get_pr_no(docs_url + close_url + en_jin19_assignee + v60),
        'en_jin19_en_author_open': get_pr_no(docs_url + open_url + en_jin19_author + v60),
        'hfxsd_zh_assignee_open': get_pr_no(docs_cn_url + open_url + hfxsd_assignee + v60),
        'hfxsd_zh_assignee_close': get_pr_no(docs_cn_url + close_url + hfxsd_assignee + v60),
        'hfxsd_zh_author_open': get_pr_no(docs_cn_url + open_url + hfxsd_author + v60),
        'hfxsd_en_assignee_open': get_pr_no(docs_url + open_url + hfxsd_assignee + v60),
        'hfxsd_en_assignee_close': get_pr_no(docs_url + close_url + hfxsd_assignee + v60),
        'hfxsd_en_author_open': get_pr_no(docs_url + open_url + hfxsd_author + v60),
        'ran_huang_zh_assignee_open': get_pr_no(docs_cn_url + open_url + ran_huang_assignee + v60),
        'ran_huang_zh_assignee_close': get_pr_no(docs_cn_url + close_url + ran_huang_assignee + v60),
        'ran_huang_zh_author_open': get_pr_no(docs_cn_url + open_url + ran_huang_author + v60),
        'ran_huang_en_assignee_open': get_pr_no(docs_url + open_url + ran_huang_assignee + v60),
        'ran_huang_en_assignee_close': get_pr_no(docs_url + close_url + ran_huang_assignee + v60),
        'ran_huang_en_author_open': get_pr_no(docs_url + open_url + ran_huang_author + v60),
        'qiancai_zh_assignee_open': get_pr_no(docs_cn_url + open_url + qiancai_assignee + v60),
        'qiancai_zh_assignee_close': get_pr_no(docs_cn_url + close_url + qiancai_assignee + v60),
        'qiancai_zh_author_open': get_pr_no(docs_cn_url + open_url + qiancai_author +v60),
        'qiancai_en_assignee_open': get_pr_no(docs_url + open_url + qiancai_assignee + v60),
        'qiancai_en_assignee_close': get_pr_no(docs_url + close_url + qiancai_assignee + v60),
        'qiancai_en_author_open': get_pr_no(docs_url + open_url + qiancai_author +v60),
        'tomshawn_zh_assignee_open': get_pr_no(docs_cn_url + open_url + tomshawn_assignee + v60),
        'tomshawn_zh_assignee_close': get_pr_no(docs_cn_url + close_url + tomshawn_assignee + v60),
        'tomshawn_zh_author_open': get_pr_no(docs_cn_url + open_url + tomshawn_author + v60),
        'tomshawn_en_assignee_open': get_pr_no(docs_url + open_url + tomshawn_assignee + v60),
        'tomshawn_en_assignee_close': get_pr_no(docs_url + close_url + tomshawn_assignee + v60),
        'tomshawn_en_author_open': get_pr_no(docs_url + open_url + tomshawn_author + v60),
        'shichun_0415_zh_assignee_open_url': docs_cn_url + open_url + shichun_0415_assignee + v60,
        'shichun_0415_zh_assignee_close_url': docs_cn_url + close_url + shichun_0415_assignee + v60,
        'shichun_0415_zh_author_open_url': docs_cn_url + open_url + shichun_0415_author + v60,
        'shichun_0415_en_assignee_open_url': docs_url + open_url + shichun_0415_assignee + v60,
        'shichun_0415_en_assignee_close_url': docs_url + close_url + shichun_0415_assignee + v60,
        'shichun_0415_en_author_open_url': docs_url + open_url + shichun_0415_author + v60,
        'en_jin19_zh_assignee_open_url': docs_cn_url + open_url + en_jin19_assignee + v60,
        'en_jin19_zh_assignee_close_url': docs_cn_url + close_url + en_jin19_assignee + v60,
        'en_jin19_zh_author_open_url': docs_cn_url + open_url + en_jin19_author + v60,
        'en_jin19_en_assignee_open_url': docs_url + open_url + en_jin19_assignee + v60,
        'en_jin19_en_assignee_close_url': docs_url + close_url + en_jin19_assignee + v60,
        'en_jin19_en_author_open_url': docs_url + open_url + en_jin19_author + v60,
        'hfxsd_zh_assignee_open_url': docs_cn_url + open_url + hfxsd_assignee + v60,
        'hfxsd_zh_assignee_close_url': docs_cn_url + close_url + hfxsd_assignee + v60,
        'hfxsd_zh_author_open_url': docs_cn_url + open_url + hfxsd_author + v60,
        'hfxsd_en_assignee_open_url': docs_url + open_url + hfxsd_assignee + v60,
        'hfxsd_en_assignee_close_url': docs_url + close_url + hfxsd_assignee + v60,
        'hfxsd_en_author_open_url': docs_url + open_url + hfxsd_author + v60,
        'ran_huang_zh_assignee_open_url': docs_cn_url + open_url + ran_huang_assignee + v60,
        'ran_huang_zh_assignee_close_url': docs_cn_url + close_url + ran_huang_assignee + v60,
        'ran_huang_zh_author_open_url': docs_cn_url + open_url + ran_huang_author + v60,
        'ran_huang_en_assignee_open_url': docs_url + open_url + ran_huang_assignee + v60,
        'ran_huang_en_assignee_close_url': docs_url + close_url + ran_huang_assignee + v60,
        'ran_huang_en_author_open_url': docs_url + open_url + ran_huang_author + v60,
        'qiancai_zh_assignee_open_url': docs_cn_url + open_url + qiancai_assignee + v60,
        'qiancai_zh_assignee_close_url': docs_cn_url + close_url + qiancai_assignee + v60,
        'qiancai_zh_author_open_url': docs_cn_url + open_url + qiancai_author + v60,
        'qiancai_en_assignee_open_url': docs_url + open_url + qiancai_assignee + v60,
        'qiancai_en_assignee_close_url': docs_url + close_url + qiancai_assignee + v60,
        'qiancai_en_author_open_url': docs_url + open_url + qiancai_author + v60,
        'tomshawn_zh_assignee_open_url': docs_cn_url + open_url + tomshawn_assignee + v60,
        'tomshawn_zh_assignee_close_url': docs_cn_url + close_url + tomshawn_assignee + v60,
        'tomshawn_zh_author_open_url': docs_cn_url + open_url + tomshawn_author + v60,
        'tomshawn_en_assignee_open_url': docs_url + open_url + tomshawn_assignee + v60,
        'tomshawn_en_assignee_close_url': docs_url + close_url + tomshawn_assignee + v60,
        'tomshawn_en_author_open_url': docs_url + open_url + tomshawn_author + v60,
    }

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
                                "text": "待处理 PR 数目如下"
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
                                "text": "v6.0 发版文档，中文文档截止日期 2022-03-25，英文文档截止日期 2022-04-01"
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
                                "text": "- en-jin19"
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
                                "text": "    - docs-cn：有 ${en_jin19_zh_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${en_jin19_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${en_jin19_zh_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${en_jin19_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${en_jin19_zh_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${en_jin19_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：有 ${en_jin19_en_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${en_jin19_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${en_jin19_en_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${en_jin19_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${en_jin19_en_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${en_jin19_en_author_open_url}"
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
                                "text": "- shichun-0415"
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
                                "text": "    - docs-cn：有 ${shichun_0415_zh_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${shichun_0415_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${shichun_0415_zh_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${shichun_0415_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${shichun_0415_zh_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${shichun_0415_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：有 ${shichun_0415_en_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${shichun_0415_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${shichun_0415_en_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${shichun_0415_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${shichun_0415_en_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${shichun_0415_en_author_open_url}"
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
                                "text": "- hfxsd"
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
                                "text": "    - docs-cn：有 ${hfxsd_zh_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${hfxsd_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${hfxsd_zh_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${hfxsd_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${hfxsd_zh_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${hfxsd_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：有 ${hfxsd_en_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${hfxsd_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${hfxsd_en_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${hfxsd_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${hfxsd_en_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${hfxsd_en_author_open_url}"
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
                                "text": "- ran-huang"
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
                                "text": "    - docs-cn：有 ${ran_huang_zh_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${ran_huang_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${ran_huang_zh_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${ran_huang_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${ran_huang_zh_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${ran_huang_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：有 ${ran_huang_en_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${ran_huang_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${ran_huang_en_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${ran_huang_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${ran_huang_en_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${ran_huang_en_author_open_url}"
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
                                "text": "- qiancai"
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
                                "text": "    - docs-cn：有 ${qiancai_zh_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${qiancai_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${qiancai_zh_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${qiancai_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${qiancai_zh_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${qiancai_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：有 ${qiancai_en_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${qiancai_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${qiancai_en_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${qiancai_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${qiancai_en_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${qiancai_en_author_open_url}"
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
                                "text": "- TomShawn"
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
                                "text": "    - docs-cn：有 ${tomshawn_zh_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${tomshawn_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${tomshawn_zh_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${tomshawn_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${tomshawn_zh_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${tomshawn_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：有 ${tomshawn_en_assignee_open} 个未合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待处理",
                                "href": "${tomshawn_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，有 ${tomshawn_en_assignee_close} 个已合源语 PR"
                            },
                            {
                                "tag": "a",
                                "text": "待翻译",
                                "href": "${tomshawn_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "，已翻译了 ${tomshawn_en_author_open} 个 PR"
                            },
                            {
                                "tag": "a",
                                "text": "未合并",
                                "href": "${tomshawn_en_author_open_url}"
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

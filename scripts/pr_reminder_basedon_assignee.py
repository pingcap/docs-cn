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
    if page_text:
        print('Get page text success:', url)
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
    else:
        print('Get page text failed:', url)

def pop_zero_value(**data):

    for item in data:
        if data[item] == '有 0 个未合源语 PR':
            data[item] = ''
            data[item + '_url' + '_text'] = ''
            data[item + '_url'] = ''
        elif data[item] == '有 0 个已合源语 PR':
            data[item] = ''
            data[item + '_url' + '_text'] = ''
            data[item + '_url'] = ''
        elif data[item] == '已翻译了 0 个 PR':
            data[item] = ''
            data[item + '_url' + '_text'] = ''
            data[item + '_url'] = ''
        else:
            continue
    return data


if __name__ == "__main__":

    data_en_jin19 = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'en_jin19_zh_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_cn_url + open_url + en_jin19_assignee + v60)),
        'en_jin19_zh_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_cn_url + close_url + en_jin19_assignee + v60)),
        'en_jin19_zh_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_cn_url + open_url + en_jin19_author + v60)),
        'en_jin19_en_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_url + open_url + en_jin19_assignee + v60)),
        'en_jin19_en_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_url + close_url + en_jin19_assignee + v60)),
        'en_jin19_en_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_url + open_url + en_jin19_author + v60)),
        'en_jin19_zh_assignee_open_url': docs_cn_url + open_url + en_jin19_assignee + v60,
        'en_jin19_zh_assignee_close_url': docs_cn_url + close_url + en_jin19_assignee + v60,
        'en_jin19_zh_author_open_url': docs_cn_url + open_url + en_jin19_author + v60,
        'en_jin19_en_assignee_open_url': docs_url + open_url + en_jin19_assignee + v60,
        'en_jin19_en_assignee_close_url': docs_url + close_url + en_jin19_assignee + v60,
        'en_jin19_en_author_open_url': docs_url + open_url + en_jin19_author + v60,
        'en_jin19_zh_assignee_open_url_text': '待处理。',
        'en_jin19_zh_assignee_close_url_text': '待翻译。',
        'en_jin19_zh_author_open_url_text': '未合并。',
        'en_jin19_en_assignee_open_url_text': '待处理。',
        'en_jin19_en_assignee_close_url_text': '待翻译。',
        'en_jin19_en_author_open_url_text': '未合并。'
    }

    data_shichun_0415 = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'shichun_0415_zh_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_cn_url + open_url + shichun_0415_assignee + v60)),
        'shichun_0415_zh_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_cn_url + close_url + shichun_0415_assignee + v60)),
        'shichun_0415_zh_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_cn_url + open_url + shichun_0415_author + v60)),
        'shichun_0415_en_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_url + open_url + shichun_0415_assignee + v60)),
        'shichun_0415_en_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_url + close_url + shichun_0415_assignee + v60)),
        'shichun_0415_en_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_url + open_url + shichun_0415_author + v60)),
        'shichun_0415_zh_assignee_open_url': docs_cn_url + open_url + shichun_0415_assignee + v60,
        'shichun_0415_zh_assignee_close_url': docs_cn_url + close_url + shichun_0415_assignee + v60,
        'shichun_0415_zh_author_open_url': docs_cn_url + open_url + shichun_0415_author + v60,
        'shichun_0415_en_assignee_open_url': docs_url + open_url + shichun_0415_assignee + v60,
        'shichun_0415_en_assignee_close_url': docs_url + close_url + shichun_0415_assignee + v60,
        'shichun_0415_en_author_open_url': docs_url + open_url + shichun_0415_author + v60,
        'shichun_0415_zh_assignee_open_url_text': '待处理。',
        'shichun_0415_zh_assignee_close_url_text': '待翻译。',
        'shichun_0415_zh_author_open_url_text': '未合并。',
        'shichun_0415_en_assignee_open_url_text': '待处理。',
        'shichun_0415_en_assignee_close_url_text': '待翻译。',
        'shichun_0415_en_author_open_url_text': '未合并。'
    }

    data_ran_huang = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'ran_huang_zh_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_cn_url + open_url + ran_huang_assignee + v60)),
        'ran_huang_zh_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_cn_url + close_url + ran_huang_assignee + v60)),
        'ran_huang_zh_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_cn_url + open_url + ran_huang_author + v60)),
        'ran_huang_en_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_url + open_url + ran_huang_assignee + v60)),
        'ran_huang_en_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_url + close_url + ran_huang_assignee + v60)),
        'ran_huang_en_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_url + open_url + ran_huang_author + v60)),
        'ran_huang_zh_assignee_open_url': docs_cn_url + open_url + ran_huang_assignee + v60,
        'ran_huang_zh_assignee_close_url': docs_cn_url + close_url + ran_huang_assignee + v60,
        'ran_huang_zh_author_open_url': docs_cn_url + open_url + ran_huang_author + v60,
        'ran_huang_en_assignee_open_url': docs_url + open_url + ran_huang_assignee + v60,
        'ran_huang_en_assignee_close_url': docs_url + close_url + ran_huang_assignee + v60,
        'ran_huang_en_author_open_url': docs_url + open_url + ran_huang_author + v60,
        'ran_huang_zh_assignee_open_url_text': '待处理。',
        'ran_huang_zh_assignee_close_url_text': '待翻译。',
        'ran_huang_zh_author_open_url_text': '未合并。',
        'ran_huang_en_assignee_open_url_text': '待处理。',
        'ran_huang_en_assignee_close_url_text': '待翻译。',
        'ran_huang_en_author_open_url_text': '未合并。'
    }

    data_hfxsd = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'hfxsd_zh_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_cn_url + open_url + hfxsd_assignee + v60)),
        'hfxsd_zh_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_cn_url + close_url + hfxsd_assignee + v60)),
        'hfxsd_zh_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_cn_url + open_url + hfxsd_author + v60)),
        'hfxsd_en_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_url + open_url + hfxsd_assignee + v60)),
        'hfxsd_en_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_url + close_url + hfxsd_assignee + v60)),
        'hfxsd_en_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_url + open_url + hfxsd_author + v60)),
        'hfxsd_zh_assignee_open_url': docs_cn_url + open_url + hfxsd_assignee + v60,
        'hfxsd_zh_assignee_close_url': docs_cn_url + close_url + hfxsd_assignee + v60,
        'hfxsd_zh_author_open_url': docs_cn_url + open_url + hfxsd_author + v60,
        'hfxsd_en_assignee_open_url': docs_url + open_url + hfxsd_assignee + v60,
        'hfxsd_en_assignee_close_url': docs_url + close_url + hfxsd_assignee + v60,
        'hfxsd_en_author_open_url': docs_url + open_url + hfxsd_author + v60,
        'hfxsd_zh_assignee_open_url_text': '待处理。',
        'hfxsd_zh_assignee_close_url_text': '待翻译。',
        'hfxsd_zh_author_open_url_text': '未合并。',
        'hfxsd_en_assignee_open_url_text': '待处理。',
        'hfxsd_en_assignee_close_url_text': '待翻译。',
        'hfxsd_en_author_open_url_text': '未合并。'
    }

    data_qiancai = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'qiancai_zh_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_cn_url + open_url + qiancai_assignee + v60)),
        'qiancai_zh_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_cn_url + close_url + qiancai_assignee + v60)),
        'qiancai_zh_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_cn_url + open_url + qiancai_author + v60)),
        'qiancai_en_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_url + open_url + qiancai_assignee + v60)),
        'qiancai_en_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_url + close_url + qiancai_assignee + v60)),
        'qiancai_en_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_url + open_url + qiancai_author + v60)),
        'qiancai_zh_assignee_open_url': docs_cn_url + open_url + qiancai_assignee + v60,
        'qiancai_zh_assignee_close_url': docs_cn_url + close_url + qiancai_assignee + v60,
        'qiancai_zh_author_open_url': docs_cn_url + open_url + qiancai_author + v60,
        'qiancai_en_assignee_open_url': docs_url + open_url + qiancai_assignee + v60,
        'qiancai_en_assignee_close_url': docs_url + close_url + qiancai_assignee + v60,
        'qiancai_en_author_open_url': docs_url + open_url + qiancai_author + v60,
        'qiancai_zh_assignee_open_url_text': '待处理。',
        'qiancai_zh_assignee_close_url_text': '待翻译。',
        'qiancai_zh_author_open_url_text': '未合并。',
        'qiancai_en_assignee_open_url_text': '待处理。',
        'qiancai_en_assignee_close_url_text': '待翻译。',
        'qiancai_en_author_open_url_text': '未合并。'
    }

    data_tomshawn = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'tomshawn_zh_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_cn_url + open_url + tomshawn_assignee + v60)),
        'tomshawn_zh_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_cn_url + close_url + tomshawn_assignee + v60)),
        'tomshawn_zh_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_cn_url + open_url + tomshawn_author + v60)),
        'tomshawn_en_assignee_open': '有 {} 个未合源语 PR'.format(get_pr_no(docs_url + open_url + tomshawn_assignee + v60)),
        'tomshawn_en_assignee_close': '有 {} 个已合源语 PR'.format(get_pr_no(docs_url + close_url + tomshawn_assignee + v60)),
        'tomshawn_en_author_open': '已翻译了 {} 个 PR'.format(get_pr_no(docs_url + open_url + tomshawn_author + v60)),
        'tomshawn_zh_assignee_open_url': docs_cn_url + open_url + tomshawn_assignee + v60,
        'tomshawn_zh_assignee_close_url': docs_cn_url + close_url + tomshawn_assignee + v60,
        'tomshawn_zh_author_open_url': docs_cn_url + open_url + tomshawn_author + v60,
        'tomshawn_en_assignee_open_url': docs_url + open_url + tomshawn_assignee + v60,
        'tomshawn_en_assignee_close_url': docs_url + close_url + tomshawn_assignee + v60,
        'tomshawn_en_author_open_url': docs_url + open_url + tomshawn_author + v60,
        'tomshawn_zh_assignee_open_url_text': '待处理。',
        'tomshawn_zh_assignee_close_url_text': '待翻译。',
        'tomshawn_zh_author_open_url_text': '未合并。',
        'tomshawn_en_assignee_open_url_text': '待处理。',
        'tomshawn_en_assignee_close_url_text': '待翻译。',
        'tomshawn_en_author_open_url_text': '未合并。'
    }

    data = dict(list(data_en_jin19.items()) + list(data_shichun_0415.items()) + list(data_hfxsd.items()) + list(data_qiancai.items()) + list(data_tomshawn.items()) + list(data_ran_huang.items()))

    data = pop_zero_value(**data)

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
                                "text": "    - docs-cn：${en_jin19_zh_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${en_jin19_zh_assignee_open_url_text}",
                                "href": "${en_jin19_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${en_jin19_zh_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${en_jin19_zh_assignee_close_url_text}",
                                "href": "${en_jin19_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${en_jin19_zh_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${en_jin19_zh_author_open_url_text}",
                                "href": "${en_jin19_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：${en_jin19_en_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${en_jin19_en_assignee_open_url_text}",
                                "href": "${en_jin19_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${en_jin19_en_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${en_jin19_en_assignee_close_url_text}",
                                "href": "${en_jin19_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${en_jin19_en_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${en_jin19_en_author_open_url_text}",
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
                                "text": "    - docs-cn：${shichun_0415_zh_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${shichun_0415_zh_assignee_open_url_text}",
                                "href": "${shichun_0415_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${shichun_0415_zh_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${shichun_0415_zh_assignee_close_url_text}",
                                "href": "${shichun_0415_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${shichun_0415_zh_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${shichun_0415_zh_author_open_url_text}",
                                "href": "${shichun_0415_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：${shichun_0415_en_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${shichun_0415_en_assignee_open_url_text}",
                                "href": "${shichun_0415_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${shichun_0415_en_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${shichun_0415_en_assignee_close_url_text}",
                                "href": "${shichun_0415_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${shichun_0415_en_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${shichun_0415_en_author_open_url_text}",
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
                                "text": "    - docs-cn：${hfxsd_zh_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${hfxsd_zh_assignee_open_url_text}",
                                "href": "${hfxsd_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${hfxsd_zh_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${hfxsd_zh_assignee_close_url_text}",
                                "href": "${hfxsd_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${hfxsd_zh_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${hfxsd_zh_author_open_url_text}",
                                "href": "${hfxsd_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：${hfxsd_en_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${hfxsd_en_assignee_open_url_text}",
                                "href": "${hfxsd_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${hfxsd_en_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${hfxsd_en_assignee_close_url_text}",
                                "href": "${hfxsd_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${hfxsd_en_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${hfxsd_en_author_open_url_text}",
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
                                "text": "    - docs-cn：${ran_huang_zh_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${ran_huang_zh_assignee_open_url_text}",
                                "href": "${ran_huang_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${ran_huang_zh_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${ran_huang_zh_assignee_close_url_text}",
                                "href": "${ran_huang_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${ran_huang_zh_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${ran_huang_zh_author_open_url_text}",
                                "href": "${ran_huang_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：${ran_huang_en_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${ran_huang_en_assignee_open_url_text}",
                                "href": "${ran_huang_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${ran_huang_en_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${ran_huang_en_assignee_close_url_text}",
                                "href": "${ran_huang_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${ran_huang_en_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${ran_huang_en_author_open_url_text}",
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
                                "text": "    - docs-cn：${qiancai_zh_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${qiancai_zh_assignee_open_url_text}",
                                "href": "${qiancai_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${qiancai_zh_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${qiancai_zh_assignee_close_url_text}",
                                "href": "${qiancai_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${qiancai_zh_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${qiancai_zh_author_open_url_text}",
                                "href": "${qiancai_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：${qiancai_en_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${qiancai_en_assignee_open_url_text}",
                                "href": "${qiancai_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${qiancai_en_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${qiancai_en_assignee_close_url_text}",
                                "href": "${qiancai_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${qiancai_en_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${qiancai_en_author_open_url_text}",
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
                                "text": "    - docs-cn：${tomshawn_zh_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${tomshawn_zh_assignee_open_url_text}",
                                "href": "${tomshawn_zh_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${tomshawn_zh_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${tomshawn_zh_assignee_close_url_text}",
                                "href": "${tomshawn_zh_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${tomshawn_zh_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${tomshawn_zh_author_open_url_text}",
                                "href": "${tomshawn_zh_author_open_url}"
                            }
                        ],
                        [
                            {
                                "tag": "text",
                                "text": "    - docs：${tomshawn_en_assignee_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${tomshawn_en_assignee_open_url_text}",
                                "href": "${tomshawn_en_assignee_open_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${tomshawn_en_assignee_close}"
                            },
                            {
                                "tag": "a",
                                "text": "${tomshawn_en_assignee_close_url_text}",
                                "href": "${tomshawn_en_assignee_close_url}"
                            },
                            {
                                "tag": "text",
                                "text": "${tomshawn_en_author_open}"
                            },
                            {
                                "tag": "a",
                                "text": "${tomshawn_en_author_open_url_text}",
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
    # # print(r_docs.text)

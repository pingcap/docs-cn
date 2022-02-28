# This script collects data from docs-cn, docs, and docs-tidb-operator,
# and write data to Google Sheets.

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime
from datetime import timedelta


# Get time interval
now_date = datetime.utcnow().strftime('%Y-%m-%d')
d1 = datetime.strptime(str(now_date), '%Y-%m-%d')
now_4d = str(d1 - timedelta(days=4))[0:10]


# Get URLs for requests
url_docs_cn_created = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs-cn%20-author:ti-chi-bot%20created:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_cn_merged = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs-cn%20-author:ti-chi-bot%20merged:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_cn_updated = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs-cn%20-author:ti-chi-bot%20updated:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_created = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs%20-author:ti-chi-bot%20created:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_merged = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs%20-author:ti-chi-bot%20merged:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_updated = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs%20-author:ti-chi-bot%20updated:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_tidb_operator_created = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs-tidb-operator%20-author:ti-chi-bot%20created:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_tidb_operator_merged = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs-tidb-operator%20-author:ti-chi-bot%20merged:' + now_4d + '..' + now_date + '&per_page=100'
url_docs_tidb_operator_updated = 'https://api.github.com/search/issues?q=is:pr%20repo:pingcap/docs-tidb-operator%20-author:ti-chi-bot%20updated:' + now_4d + '..' + now_date + '&per_page=100'


username = '<your GitHub username>'
token = '<your GitHub token>'


# Get PR counts and PR list
def get_pr_list_size(url):
    r = requests.get(url,auth=(username, token))
    if r.status_code == 200:
        r = r.json()
        # Get PR counts and PR list
        total_count = r['total_count']
        if total_count > 0:
            pr_list = []
            for i in range(total_count):
                pr_list.append(r['items'][i]['pull_request']['url'])
            # Get the count of PR sizes
            size_xs, size_s, size_m, size_l, size_xl = 0, 0, 0, 0, 0
            for i in range(total_count):
                for label in r['items'][i]['labels']:
                    if label['name'] == 'size/S':
                        size_s += 1
                    elif label['name'] == 'size/M':
                        size_m += 1
                    elif label['name'] == 'size/L':
                        size_l += 1
                    elif label['name'] == 'size/XL':
                        size_xl += 1
                    elif label['name'] == 'size/XS':
                        size_xs += 1
                    elif label['name'] == 'size/XXL':
                        size_xl += 1
                    else:
                        continue
            return pr_list, total_count, size_xs, size_s, size_m, size_l, size_xl
    else:
        print('Error: ', url + '  ' + str(r.status_code))
        return None


# Get the counts of PR lines and comments
def get_pr_lines_comments(url):

    pr_list = get_pr_list_size(url)[0]
    pr_lines_addition = []
    pr_lines_deletion = []
    pr_comments_count = []
    for pr in pr_list:
        r = requests.get(pr, auth=(username, token))
        if r.status_code == 200:
            print('PR got: ', pr)
            r = r.json()
            pr_lines_addition.append(r['additions'])
            pr_lines_deletion.append(r['deletions'])
            pr_comments_count.append(r['comments'])
        else:
            print('Error: ', url + '  ' + str(r.status_code))
            return None
    total_addition = 0
    total_deletion = 0
    total_comments = 0
    for ele in range(0, len(pr_lines_addition)):
        total_addition += pr_lines_addition[ele]
    for ele in range(0, len(pr_lines_deletion)):
        total_deletion += pr_lines_deletion[ele]
    for ele in range(0, len(pr_comments_count)):
        total_comments += pr_comments_count[ele]
    return total_addition, total_deletion, total_comments


if __name__ == '__main__':

    print('****************************************************')
    print("First, let's get some data from GitHub repositories!")
    print('****************************************************')

    r1 = get_pr_list_size(url_docs_cn_created)
    r2 = get_pr_list_size(url_docs_cn_merged)
    r3 = get_pr_list_size(url_docs_cn_updated)
    r4 = get_pr_lines_comments(url_docs_cn_created)
    r5 = get_pr_lines_comments(url_docs_cn_merged)
    r6 = get_pr_lines_comments(url_docs_cn_updated)
    r7 = get_pr_list_size(url_docs_created)
    r8 = get_pr_list_size(url_docs_merged)
    r9 = get_pr_list_size(url_docs_updated)
    r10 = get_pr_lines_comments(url_docs_created)
    r11 = get_pr_lines_comments(url_docs_merged)
    r12 = get_pr_lines_comments(url_docs_updated)
    r13 = get_pr_list_size(url_docs_tidb_operator_created)
    r14 = get_pr_list_size(url_docs_tidb_operator_merged)
    r15 = get_pr_list_size(url_docs_tidb_operator_updated)
    r16 = get_pr_lines_comments(url_docs_tidb_operator_created)
    r17 = get_pr_lines_comments(url_docs_tidb_operator_merged)
    r18 = get_pr_lines_comments(url_docs_tidb_operator_updated)

    print('********************************************')
    print("OK, let's begin writing to Google Sheets!")
    print('********************************************')

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('<your personal Google Sheets API key in a JSON file>', scope)
    gc = gspread.authorize(credentials)
    time_row = now_4d + ' to ' + now_date

    # Write to the docs-cn-pr-count sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-cn-pr-count')
    r1_write = [time_row, r1[1], r2[1], r3[1]]
    wks.append_row(r1_write)
    print('Successfully write to docs-cn-pr-count!')

    # Write to the docs-cn-size sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-cn-size')
    r2_write = [time_row, r3[2], r3[3], r3[4], r3[5], r3[6]]
    wks.append_row(r2_write)
    print('Successfully write to docs-cn-size!')

    # Write to the docs-cn-lines sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-cn-lines')
    r3_write = [time_row, r4[0], r4[1], r5[0], r3[1]]
    wks.append_row(r3_write)
    print('Successfully write to docs-cn-lines!')

    # Write to the docs-cn-comments sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-cn-comments')
    r4_write = [time_row, r6[2]]
    wks.append_row(r4_write)
    print('Successfully write to docs-cn-comments!')

    # Write to the docs-pr-count sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-pr-count')
    r5_write = [time_row, r7[1], r8[1], r9[1]]
    wks.append_row(r5_write)
    print('Successfully write to docs-pr-count!')

    # Write to the docs-size sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-size')
    r6_write = [time_row, r9[2], r9[3], r9[4], r9[5], r9[6]]
    wks.append_row(r6_write)
    print('Successfully write to docs-size!')

    # Write to the docs-lines sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-lines')
    r7_write = [time_row, r10[0], r10[1], r11[0], r9[1]]
    wks.append_row(r7_write)
    print('Successfully write to docs-lines!')

    # Write to the docs-comments sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-comments')
    r8_write = [time_row, r12[2]]
    wks.append_row(r8_write)
    print('Successfully write to docs-comments!')

    # Write to the docs-tidb-operator-pr-count sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-tidb-operator-pr-count')
    r9_write = [time_row, r13[1], r14[1], r15[1]]
    wks.append_row(r9_write)
    print('Successfully write to docs-tidb-operator-pr-count!')

    # Write to the docs-tidb-operator-size sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-tidb-operator-size')
    r10_write = [time_row, r15[2], r15[3], r15[4], r15[5], r15[6]]
    wks.append_row(r10_write)
    print('Successfully write to docs-tidb-operator-size!')

    # Write to the docs-tidb-operator-lines sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-tidb-operator-lines')
    r11_write = [time_row, r16[0], r16[1], r17[0], r15[1]]
    wks.append_row(r11_write)
    print('Successfully write to docs-tidb-operator-lines!')

    # Write to the docs-tidb-operator-comments sheet
    wks = gc.open('<your Google Sheets name>').worksheet('docs-tidb-operator-comments')
    r12_write = [time_row, r18[2]]
    wks.append_row(r12_write)
    print('Successfully write to docs-tidb-operator-comments!')

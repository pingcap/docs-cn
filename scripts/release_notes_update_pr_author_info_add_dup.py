# This script can replace the bot author info in the release note table with the actual PR authors and add the history duplicated release notes based on issue links and author info.
# Before running this script, you need to get a GitHub personal access token (https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) and save it in a text file.

from github import Github
import re
import openpyxl
import os

release_note_excel = r'/Users/userid/Downloads/patch_6.5.1_release_note_test copy.xlsx'
ext_path = r'/Users/userid/Documents/GitHub/githubid/docs-cn/releases'  # The path of the existing release notes
main_path = r'/Users/githubid/Documents/GitHub/githubid/docs-cn/releases/release-6.5.1.md'  # The path of the release notes in preparation
with open("/Users/githubid/Documents/gh_token.txt", "r") as f: # Read the GitHub personal access token from the gh_token.txt file
    access_token = f.read().strip()

# Get the issue info of the existing release notes
def store_exst_rn(ext_path,main_path):

    exst_notes = []
    exst_issue_nums = []
    exst_note_levels = []

    for maindir, subdir, files in os.walk(ext_path):
        for afile in files:
            file_path = (os.path.join(maindir, afile))
            if file_path.endswith('.md') and not os.path.samefile(file_path,main_path):
                with open(file_path,'r', encoding='utf-8') as fp:
                    level1 = level2 = level3 = ""
                    for line in fp:
                        exst_issue_num = re.search(r'https://github.com/(pingcap|tikv)/\w+/(issues|pull)/\d+', line)
                        authors = re.findall(r'@\[([^\]]+)\]', line) # Get the list of authors in this line
                        if exst_issue_num:
                            if exst_issue_num.group() not in exst_issue_nums:
                                note_level = level1 + level2 + level3
                                note_pair = [exst_issue_num.group(),line.strip(),afile, note_level, authors]
                                exst_issue_nums.append(exst_issue_num.group())
                                exst_notes.append(note_pair)
                            else:
                                continue
                        elif line.startswith("##"):
                            level1 = "> " + line.replace("##","").strip()
                            level2 = level3 = ""
                        elif line.startswith ("+") or line.startswith ("-"):
                            level2 = "> " + line.replace("+","").replace("-","").strip()
                            level3 = ""
                        elif line.startswith ("    +") or line.startswith ("    -"):
                            level3 = "> " + line.replace("    +","").replace("    -","").strip()
                        else:
                            continue
            else:
                pass

    if len(exst_issue_nums) != 0:
        return exst_notes
    else:
        return 0

def get_pr_info_from_github(cp_pr_link,cp_pr_title):

    target_repo_pr_link= cp_pr_link.rsplit('/', 1)[0]
    target_pr_number = re.findall(r'\(#(\d+)\)$', cp_pr_title) # Match the original PR number in the end of the cherry-pick PR

    if target_pr_number:
        if len(target_pr_number) > 1:
            print ("There is more than one match result of original PR number from the cherry-pick title: " + cp_pr_title )
        else:
            pass
    else:
        target_pr_number = re.findall(r'\(#(\d+)\)', cp_pr_title) # Match the original PR number in the cherry-pick PR

    target_pr_link = target_repo_pr_link + '/' + target_pr_number[0]

    # Create a Github object with the access token
    g = Github(access_token)

    pr_info = target_pr_link.split("/")

    # Extract the owner, repository name, and pull request number from the link
    owner, repo, pr_number = pr_info[-4], pr_info[-3], pr_info[-1]

    #print ('Getting the PR info from GitHub: ' + target_pr_link)
    repo_obj = g.get_repo(f"{owner}/{repo}")# Get the repository object
    pr_obj = repo_obj.get_pull(int(pr_number))# Get the pull request object
    pr_author = pr_obj.user.login # Get the author of the pull request

    return(pr_author)

def update_pr_author_and_release_notes(excel_path):

    # Open the excel file
    workbook = openpyxl.load_workbook(excel_path)
    # Specify the target sheet
    sheet = workbook['pr_for_release_note']

    # Get the sheet header
    header = next(sheet.iter_rows(min_row=1, max_row=1, values_only=True)) # Read the first line in the sheet

    # Get the column info
    pr_author_index = header.index('pr_author')
    pr_link_index = header.index('pr_link')
    pr_title_index = header.index('pr_title')
    pr_formated_rn_index = header.index('formated_release_note')
    pr_last_col_index = sheet.max_column
    sheet.insert_cols(pr_last_col_index + 1) # Insert a new column for the dup release notes
    sheet.cell(row=1, column=pr_last_col_index + 1, value='published_release_notes') # Set a column name
    # Go through each row
    for row_index, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        # If pr_author is ti-chi-bot or ti-srebot
        current_pr_author = row[pr_author_index]
        current_formated_rn= row[pr_formated_rn_index]
        if current_pr_author in ['ti-chi-bot', 'ti-srebot']:
           print ("Replacing the author info for row " + str(row_index) + ".")
           actual_pr_author = get_pr_info_from_github(row[pr_link_index], row[pr_title_index]) #Get the PR author according to the cherry-pick PR
           pr_author_cell = sheet.cell(row=row_index, column=pr_author_index+1, value = actual_pr_author)#Fill in the pr_author_cell
           updated_formated_rn = current_formated_rn.replace("[{}](https://github.com/{}".format(current_pr_author, current_pr_author),"[{}](https://github.com/{}".format(actual_pr_author, actual_pr_author))
           formated_release_note_cell = sheet.cell(row=row_index, column=pr_formated_rn_index+1, value = updated_formated_rn) # Fill in the formated_release_note_cell
           current_pr_author = actual_pr_author
        else:
            pass

        ## Add the dup release note info
        issue_link = re.search('https://github.com/(pingcap|tikv)/[\w-]+/issues/\d+', current_formated_rn)
        for note_pair in note_pairs:
            if (issue_link.group() == note_pair[0]) and ((current_pr_author in note_pair[4]) or len(note_pair[4]) == 0): # Add the dup release notes only if the issues link is the same as the existing one and the current author is in the existing author list
                print('A duplicated note is found in row ' + str(row_index) + " from " + note_pair[2] + note_pair[1])
                dup_formated_rn = '- (dup): {} {} {}'.format(note_pair[2], note_pair[3], note_pair[1])
                sheet.cell(row=row_index, column=pr_last_col_index+1, value=dup_formated_rn)
                break
            else:
                pass

    workbook.save(release_note_excel)

if __name__ == '__main__':
    note_pairs = store_exst_rn(ext_path,main_path)
    update_pr_author_and_release_notes(release_note_excel)
    print ("The bot author info in the excel is now replaced with the actual authors.")
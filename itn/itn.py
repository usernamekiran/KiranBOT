import pywikibot
import os
import re
import sys
import time
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz

# script to archive the entries from "Template:In the news"
# thoroughly tested
# has index page
# target pages, comments, and prints need to be updated/removed

site = pywikibot.Site("en", "wikipedia")
#source_page = pywikibot.Page(site, "User:KiranBOT/sandbox")
source_page = pywikibot.Page(site, "Template:In the news")
archive_index_page_title = "Wikipedia:In the news/Posted/Archives"

log_file = os.path.join(os.path.expanduser("~"), "enwiki", "itn", "itn_out.txt")

def format_timestamp(timestamp):
    formatted_timestamp = timestamp.strftime("%H:%M, %d %B %Y")
    return formatted_timestamp

current_date = datetime.now()
current_month_name = current_date.strftime("%B")
current_year = current_date.strftime("%Y")
#archive_page_title = f"User:KiranBOT/sandbox/{current_month_name} {current_year}"
archive_page_title = f"Wikipedia:In the news/Posted/{current_month_name} {current_year}"

prev_date = current_date - relativedelta(months=2)
prev_month_name = prev_date.strftime("%B")
prev_year = prev_date.strftime("%Y")
prev_archive_page_title = f"Wikipedia:In the news/Posted/{prev_month_name} {prev_year}"
#prev_archive_page_title = f"User:KiranBOT/sandbox/{prev_month_name} {prev_year}"

revisions = list(source_page.revisions(content=True))[::-1] # for the total past archive/one time run
#revisions = list(source_page.revisions(total=50, content=True))[::-1] # for daily cron

archive_page = pywikibot.Page(site, archive_page_title)
#archive_index_page_title = "User:KiranBOT/sandbox/index"

edit_counter = 0

for revision in revisions:
    old_revision_id = revision.parentid
    new_revision_id = revision.revid
    new_revision_id_str = str(new_revision_id)
    timestamp = revision.timestamp
    editor_name = revision.user

    prev_month = timestamp - relativedelta(months=2)
    prev_month_name = prev_month.strftime("%B")
    prev_year = prev_month.strftime("%Y")
    prev_archive_page_title = f"Wikipedia:In the news/Posted/{prev_month_name} {prev_year}"
    #prev_archive_page_title = f"User:KiranBOT/sandbox/{prev_month_name} {prev_year}"

    current_month_changes = []
    prev_month_changes = []
    prev_archive_lines = []

    try:
        diff = site.compare(old_revision_id, new_revision_id)
        soup = BeautifulSoup(diff, "html.parser")
        added_elements = soup.find_all("td", class_="diff-addedline diff-side-added")

        # Process additions
        for added_element in added_elements:
            div_elements = added_element.find_all("div")
            for div_element in div_elements:
                text_content = div_element.get_text()

                if not text_content.startswith("| ") and not text_content.startswith("[[Image:"):
                        editor_name = revision.user
                        formatted_timestamp = format_timestamp(timestamp)
                        text_content = text_content.replace("*[[", "*'''RD''' [[").replace("* [[", "*'''RD''' [[")
                        text_content = re.sub(r'\*{{nowrap\|\[\[(.*?)\]\]}}', r"*'''RD''' [[\1]]", text_content)
                        formatted_timestamp = format_timestamp(timestamp)

                        date_parts = formatted_timestamp.split(", ")
                        if len(date_parts) >= 2:
                            timestamp_time = date_parts[0]
                            day_month_year = date_parts[1].split(" ")  
                            day = int(day_month_year[0])
                            month_name = day_month_year[1]
                            year = day_month_year[2]
                            day_month_header = f"{month_name} {day}"
                            archive_page_title = f"Wikipedia:In the news/Posted/{month_name} {year}"
                            #archive_page_title = f"User:KiranBOT/sandbox/{month_name} {year}"

                            archive_page = pywikibot.Page(site, archive_page_title)

                            if not archive_page.exists():
                                archive_page.text = "{{Wikipedia:In the news/Posted/Archives/header}}"
                                archive_page.save("created archive page", minor=True, botflag=True)
                                edit_counter += 1
                                time.sleep(3)

                                # get archive page title
                                archive_page_title = f"Wikipedia:In the news/Posted/{month_name} {year}"

                                # get archive index page content
                                archive_index_page = pywikibot.Page(site, archive_index_page_title)
                                archive_index_text = archive_index_page.text

                                # Find the line that contains <!-- End archive links -->
                                lines = archive_index_text.splitlines()
                                end_archive_line = None
                                for i, line in enumerate(lines):
                                    if "<!-- End archive links -->" in line:
                                        end_archive_line = i
                                        break

                                # add the new archive link to the same line as the existing archive links
                                if end_archive_line is not None:
                                    new_archive_link = f"[[Wikipedia:In the news/Posted/{month_name} {year}|{month_name} {year}]]"
                                    lines[end_archive_line - 1] += f" &bull; {new_archive_link}"

                                # join the lines back together
                                archive_index_text = '\n'.join(lines)

                                # regex pattern to find the January link and replace it with a newline
                                january_link_pattern = r']] &bull; \[\[Wikipedia:In the news/Posted/January(.*?)]]'
                                # replace with newline
                                archive_index_text = re.sub(january_link_pattern, r']]\n* [[Wikipedia:In the news/Posted/January\1]]', archive_index_text)

                                # save the updated archive index page
                                archive_index_page.text = archive_index_text
                                archive_index_page.save(f"updated archive page", minor=True, botflag=True)
                                edit_counter += 1
                                time.sleep(3)
                                ####
                                ####

                            header = f"== {day_month_header} =="
                            if header not in archive_page.text:
                                archive_page.text += "\n" + header

                            entry_found_current = False
                            entry_found_previous = False

                            archive_lines = archive_page.text.split("\n")
                            regex_pattern = re.compile(re.escape(text_content[:30]), re.IGNORECASE) # regardless the similarity ratio, token based/fuzzy match is not effective here
                            last_matching_index = -1

                            for i, line in enumerate(archive_lines):
                                if regex_pattern.search(line):
                                    last_matching_index = i
                                    entry_found_current = True

                            if entry_found_current:
                                archive_page_title = f"Wikipedia:In the news/Posted/{month_name} {year}"
                                #archive_page_title = f"User:KiranBOT/sandbox/{month_name} {year}"
                                latest_archive_page = pywikibot.Page(site, archive_page_title)                                
                                if new_revision_id_str in latest_archive_page.text:
                                    continue  # skip this revision and move to the next one
                                update_message = f"<small>[[special:diff/{new_revision_id}|updated]] by [[User:{editor_name}|{editor_name}]], {formatted_timestamp}</small>"
                                current_month_changes.insert(last_matching_index + 1, text_content + update_message)
                            else:
                                # check previous month's page
                                prev_month = timestamp - relativedelta(months=1)
                                prev_month_name = prev_month.strftime("%B")
                                prev_year = prev_month.strftime("%Y")
                                prev_archive_page_title = f"Wikipedia:In the news/Posted/{prev_month_name} {prev_year}"
                                #prev_archive_page_title = f"User:KiranBOT/sandbox/{prev_month_name} {prev_year}"
                                prev_archive_page = pywikibot.Page(site, prev_archive_page_title)

                                if prev_archive_page.exists():
                                    last_matching_index_prev = -1
                                    prev_archive_lines = prev_archive_page.text.split("\n")

                                for i, line in enumerate(prev_archive_lines):
                                    if regex_pattern.search(line):
                                        last_matching_index_prev = i
                                        entry_found_previous = True

                                if entry_found_previous:
                                    prev_archive_page_title = f"Wikipedia:In the news/Posted/{prev_month_name} {prev_year}"
                                    #prev_archive_page_title = f"User:KiranBOT/sandbox/{prev_month_name} {prev_year}"
                                    latest_prev_archive_page = pywikibot.Page(site, prev_archive_page_title)
                                    if new_revision_id_str in latest_prev_archive_page.text:
                                        continue  # skip this revision and move to the next one
                                    update_message = f"<small>[[special:diff/{new_revision_id}|updated]] by [[User:{editor_name}|{editor_name}]], {formatted_timestamp}</small>"
                                    prev_archive_lines.insert(last_matching_index_prev + 1, f"{text_content} {update_message}")
                                    prev_month_changes.insert(last_matching_index + 1, text_content + update_message)
                                elif not entry_found_current and not entry_found_previous:
                                    archive_page_title = f"Wikipedia:In the news/Posted/{month_name} {year}"
                                    #archive_page_title = f"User:KiranBOT/sandbox/{month_name} {year}"
                                    latest_archive_page = pywikibot.Page(site, archive_page_title)                                      
                                    if new_revision_id_str in latest_archive_page.text:
                                        continue
                                    update_message = f" <small>[[special:diff/{new_revision_id}|added]] by [[User:{editor_name}|{editor_name}]], {formatted_timestamp}</small>"
                                    current_month_changes.append(text_content + update_message)
        
        for change in current_month_changes:
            archive_page.text += "\n" + change

        ####
        #### Process removals
        ####
        
        # define similarity percentage fuzz.token_sort_ratio
        def token_match_percentage(str1, str2):
            return fuzz.token_sort_ratio(str1, str2)

        SIMILARITY_THRESHOLD = 70  # Adjust as per requirements

        removed_elements = soup.find_all("td", class_="diff-deletedline diff-side-deleted")
        for removed_element in removed_elements:
            div_elements = removed_element.find_all("div")
            for div_element in div_elements:
                text_content = div_element.get_text()

                if not text_content.startswith("| "):
                    editor_name = revision.user
                    formatted_timestamp = format_timestamp(timestamp)

                    date_parts = formatted_timestamp.split(", ")
                    if len(date_parts) >= 2:
                        timestamp_time = date_parts[0]
                        day_month_year = date_parts[1].split(" ")  
                        day = int(day_month_year[0])
                        month_name = day_month_year[1]
                        year = day_month_year[2]
                        day_month_header = f"{month_name} {day}"

                    text_content = text_content.replace("*[[", "*'''RD''' [[").replace("* [[", "*'''RD''' [[")
                    text_content = re.sub(r'\*{{nowrap\|\[\[(.*?)\]\]}}', r"*'''RD''' [[\1]]", text_content)

                    # get new revision content
                    new_revision_id_str = str(new_revision_id)
                    revision_content = source_page.getOldVersion(oldid=new_revision_id)
                    new_revision_content = revision_content.split("\n")
                    
                    # check if the removed content is actual removal, or an update
                    is_update = any(token_match_percentage(text_content, new_line) >= SIMILARITY_THRESHOLD for new_line in new_revision_content)
                    
                    # if its an update, skip the removal process
                    if is_update:
                        continue

                    # process the removal, as it is not an update
                    match_length = 15 if text_content.startswith("*'''RD''' [[") else 30
                    archive_lines = archive_page.text.split("\n")
                    regex_pattern = re.compile(re.escape(text_content[:match_length]), re.IGNORECASE)
                    last_matching_index = -1
                    

                    for i, line in enumerate(archive_lines):
                        if regex_pattern.search(line):
                            last_matching_index = i 

                    if last_matching_index != -1:
                        archive_page_title = f"Wikipedia:In the news/Posted/{month_name} {year}"
                        #archive_page_title = f"User:KiranBOT/sandbox/{month_name} {year}"
                        latest_archive_page = pywikibot.Page(site, archive_page_title)
                        if new_revision_id_str in latest_archive_page.text:
                            continue
                        update_message = f" <small>[[special:diff/{new_revision_id}|removed]] by [[User:{editor_name}|{editor_name}]], {formatted_timestamp}</small>"
                        if text_content.startswith("*'''RD''' [["):
                            if last_matching_index < len(archive_lines):
                                archive_lines[last_matching_index] += update_message
                        else:
                            archive_lines.insert(last_matching_index + 1, f"{text_content} {update_message}")
                        archive_page.text = "\n".join(archive_lines)
                        current_month_changes.append(text_content)
                    else:
                        prev_month = timestamp - relativedelta(months=1)
                        prev_month_name = prev_month.strftime("%B")
                        prev_year = prev_month.strftime("%Y")
                        prev_archive_page_title = f"Wikipedia:In the news/Posted/{prev_month_name} {prev_year}"
                        prev_archive_page = pywikibot.Page(site, prev_archive_page_title)

                        if prev_archive_page.exists():
                            prev_archive_lines = prev_archive_page.text.split("\n")
                            last_matching_index_prev = -1
                            for i, line in enumerate(prev_archive_lines):
                                if regex_pattern.search(line):
                                    last_matching_index_prev = i 

                            if last_matching_index_prev != -1:
                                prev_archive_page_title = f"Wikipedia:In the news/Posted/{prev_month_name} {prev_year}"
                                #prev_archive_page_title = f"User:KiranBOT/sandbox/{prev_month_name} {prev_year}"
                                latest_prev_archive_page = pywikibot.Page(site, prev_archive_page_title)
                                if new_revision_id_str in latest_prev_archive_page.text:
                                    continue
                                update_message = f" <small>[[special:diff/{new_revision_id}|removed]] by [[User:{editor_name}|{editor_name}]], {formatted_timestamp}</small>"
                                if text_content.startswith("*'''RD''' [["):
                                    if last_matching_index_prev < len(prev_month_changes):
                                        prev_month_changes[last_matching_index_prev] += update_message
                                else:
                                    prev_month_changes.insert(last_matching_index_prev + 1, f"{text_content} {update_message}")
                            else:
                                # if the removed entry is not found in both the current and the previous archive pages
                                update_message = f" <small>[[special:diff/{new_revision_id}|removed]] by [[User:{editor_name}|{editor_name}]], {formatted_timestamp}</small>"
                                archive_page.text += "\n" + f"{text_content} {update_message}"
                                current_month_changes.append(text_content)

        # save the changes
        if current_month_changes:
            archive_page.save("archived ITN entry", minor=True, botflag=True)
            edit_counter += 1
            time.sleep(3)
        if prev_month_changes:
            prev_archive_page.save("archived ITN entry", minor=True, botflag=True)
            edit_counter += 1
            time.sleep(3)

        #if edit_counter % 10 == 0:
            #time.sleep(5)
            #edit_counter = 0

        if edit_counter >= 500:
            sys.exit()

    except Exception as e:
        print(f"Error: {e}")
        with open(log_file, "a") as f:
            f.write(f"{e}")

import pywikibot
import pandas as pd
import requests
import os
import csv
import html
import time
import shutil
import subprocess
import urllib.request
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from lxml import etree
from datetime import datetime

# Define paths to the required files, and directories using os.path.expanduser
results_dir = os.path.join(os.path.expanduser("~"), "enwiki", "mostrefs", "dump", "csv")
chunks_dir = os.path.join(os.path.expanduser("~"), "enwiki", "mostrefs", "dump", "chunks")
log_file = os.path.join(os.path.expanduser("~"), "enwiki", "mostrefs", "dump", "dump_out.txt")

# Initialize a site object
site = pywikibot.Site("en", "wikipedia")
# Log page
log_page = pywikibot.Page(site, "User:KiranBOT/MOSTREFS/log")

# Clear the contents of log_file
open(log_file, "w").close()

# Print progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"pod initiated successfully at {current_time}.\n")
log_page.text = "* pod initiated successfully at ~~~~~\n"
log_page.save(summary='pod initiated, dump', botflag=True, minor=True)

# Remove the xml chunk directory
try:
    shutil.rmtree(chunks_dir, ignore_errors=True)
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"Error while deleting chunks directory: {e}\n")
    log_page.text += f"\n* error while deleting chunks directory: {e}\n"
    log_page.save(summary='updated log — error occurred', botflag=True, minor=True)
# Print the progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"chunks_dir deleted successfully at {current_time}.\n")
log_page.text += "\n* ''chunks_dir'' deleted successfully at ~~~~~\n"
log_page.save(summary='updated log — chunks_dir deleted', botflag=True, minor=True)

# Sleep
time.sleep(2)

# create the xml chunk directory
os.makedirs(chunks_dir)
# Print the progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"chunks_dir created successfully at {current_time}.\n")
log_page.text += "\n* ''chunks_dir'' created successfully at ~~~~~\n"
log_page.save(summary='updated log — chunks_dir created', botflag=True, minor=True)

## Get the dump file
dump_file = "dump.xml.bz2"
# Print the progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"dump downloading began successfully at {current_time}.\n")
log_page.text += "\n* dump downloading began successfully at ~~~~~\n"
log_page.save(summary='updated log — dump download began', botflag=True, minor=True)

url = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"

save_path = os.path.join(os.path.expanduser("~"), "mostrefs", "dump", dump_file)

urllib.request.urlretrieve(url, save_path)

# Print the progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"dump downloading finished successfully at {current_time}.\n")
log_page.text += "\n* dump downloaded successfully at ~~~~~\n"
log_page.save(summary='updated log — dump download finished', botflag=True, minor=True)

# Sleep
time.sleep(2)

## Extract the file
file_path = os.path.join(os.path.expanduser("~"), "mostrefs", "dump", "dump.xml.bz2")
subprocess.run(["bunzip2", file_path])

# Print the progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"dump file extracted successfully at {current_time}.\n")

## Break the original dump file in chunks.
# set the number of pages per output file
pages_per_file = 1300

# open the input file
dump_file = os.path.join(os.path.expanduser("~"), "mostrefs", "dump", "dump.xml")

# create the first output file
file_count = 1
with open(os.path.join(chunks_dir, f'chunk_{file_count}.xml'), 'wb') as out_file:
    out_file.write(b'<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">\n')

    # iterate over the input file page by page
    page_count = 0
    context = etree.iterparse(dump_file, events=('end',), tag='{http://www.mediawiki.org/xml/export-0.10/}page')
    for event, elem in context:
        # write the page to the current output file
        out_file.write(etree.tostring(elem, pretty_print=True))

        # check if we've reached the page limit
        page_count += 1
        if page_count == pages_per_file:
            out_file.write(b'</mediawiki>')

            # increment the file counter and create a new output file
            file_count += 1
            out_file = open(os.path.join(chunks_dir, f'chunk_{file_count}.xml'), 'wb')
            out_file.write(b'<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" xml:lang="en">\n')
            page_count = 0

        # clear the element to free up memory
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    # close the final output file
    out_file.write(b'</mediawiki>')

# Print the progress
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"{file_count} output files created at {current_time}.\n")
"""
# Delete the dump file
try:
    os.remove(os.path.join(os.path.expanduser("~"), "mostrefs", "dump", "dump.xml"))
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"Error while deleting dump.xml: {e}\n")
    log_page.text += f"\n* ~~~~~ error while deleting ''dump.xml''\n"
    log_page.save(summary='updated log — error', botflag=True, minor=True)
"""

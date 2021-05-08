#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Awesome Search
# @raycast.mode fullOutput
# @raycast.refreshTime 5m
# - @raycast.packageName Quick reference

# Optional parameters:
# @raycast.icon 📖
# @raycast.argument1 { "type": "text", "placeholder": "query?", "optional": false }
# @raycast.argument2 { "type": "text", "placeholder": "languages?", "optional": true }
# @raycast.argument3 { "type": "text", "placeholder": "lists?", "optional": true }

# Documentation:
# @raycast.description Search github awesome lists and more!
# @raycast.author Marko Arezina
# @raycast.authorURL markoarezina.com

import json
import re
import sys
from typing import List
from urllib.parse import quote
from urllib.request import urlopen

API_URL = "http://127.0.0.1:8000"


def parse_list(arg: str) -> str:
    """
    Parse script args containing a list of values.
    Splits tokens by any non-alphanumeric character. 
    """
    return re.split(r'\W+', arg)


def format_url(query: str, languages: List[str], lists: List[str]) -> str:
    query = quote(query)

    languages = [f'language={l}' for l in languages if l != '']
    languages = "&".join(languages)

    lists = [f'awesome-list={l}' for l in lists if l != '']
    lists = "&".join(lists)

    print(f'{API_URL}/search?query={query}&{languages}&{lists}')
    return f'{API_URL}/search?query={query}&{languages}&{lists}'


query = sys.argv[1]
languages = sys.argv[2]
lists = sys.argv[3]

# Split by any non-alphanumeric
languages = re.split(r'\W+', languages)
lists = re.split(r'\W+', lists)

print(query, languages, lists)

query_url = format_url(query, languages, lists)

try:
    with urlopen(query_url) as f:
        result = json.load(f)
except:
    print('Failed loading resources ...')
    sys.exit(0)

for doc in result['docs']:
    name, desc, stars, url = doc['repo_name'], doc['body'], doc['stargazers_count'], doc['svn_url']
    print(
        f'Project: {name} Description: {desc} \n Stars: {stars} URL: {url} \n')

#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Awesome
# @raycast.mode fullOutput
# @raycast.refreshTime 5m
# @raycast.packageName Search

# Optional parameters:
# @raycast.icon 📖
# @raycast.argument1 { "type": "text", "placeholder": "query", "optional": false }
# @raycast.argument2 { "type": "text", "placeholder": "languages (e.g. python)", "optional": true }
# @raycast.argument3 { "type": "text", "placeholder": "sort stars?", "optional": true }

# Documentation:
# @raycast.description Search awesome lists and more!
# @raycast.author Marko Arezina
# @raycast.authorURL https://github.com/mrkarezina

import json
import re
import sys
from typing import List
from urllib.parse import quote
from urllib.request import urlopen

# API_URL = "http://127.0.0.1:8000"
API_URL = "https://awesome-search-dot-graph-intelligence.uc.r.appspot.com"

colors = {
    'green': '\033[92m',
    'red': '\033[91m',
    'end': '\033[0m',
    'yellow': '\033[93m',
}


def parse_list(arg: str) -> str:
    """
    Parse script args containing a list of values.
    Splits tokens by any non-alphanumeric character. 
    """
    return re.split(r'\W+', arg)


def format_url(query: str, languages: List[str], lists: List[str] = [], sort_stars: bool = False) -> str:
    query = quote(query)

    languages = [f'language={l}' for l in languages if l != '']
    languages = "&".join(languages)

    lists = [f'awesome-list={l}' for l in lists if l != '']
    lists = "&".join(lists)

    sort_stars = 'true' if sort_stars else 'false'

    return f"{API_URL}/search?query={query}&{languages}&{lists}&sort-stars={sort_stars}"


query = sys.argv[1]
languages = parse_list(sys.argv[2])
sort_stars = sys.argv[3]

# Default to sort by relevance
if sort_stars.lower() not in ['', '0', 'false']:
    sort_stars = True
else:
    sort_stars = False


query_url = format_url(query, languages, sort_stars=sort_stars)

try:
    with urlopen(query_url) as f:
        result = json.load(f)
except:
    print('Failed loading resources ...')
    sys.exit(0)

for doc in result['docs']:
    name, desc, stars, url = doc['repo_name'], doc['body'], doc['stargazers_count'], doc['svn_url']
    print(f"{colors['green']}{name}{colors['end']} - {desc}")
    print(f"Stars {colors['yellow']}{stars}{colors['end']} {url}\n")

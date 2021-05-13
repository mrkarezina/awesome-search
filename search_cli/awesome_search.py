import argparse
import json
import re
import sys
from typing import List
from urllib.parse import quote
from urllib.request import urlopen

API_URL = "https://awesome-search-dot-graph-intelligence.uc.r.appspot.com"

colors = {
    'green': '\033[92m',
    'red': '\033[91m',
    'end': '\033[0m',
    'yellow': '\033[93m',
}

parser = argparse.ArgumentParser(description='Search preferences.')
parser.add_argument(
    'query', help="Query to search. Use quotes for queries with spaces.")
parser.add_argument('-l', '--languages', default='',
                    required=False, help='Comma delimited list of programming languages to filter by.')
parser.add_argument('--lists', default='',
                    required=False, help='Comma delimited list of terms filtering which awesome lists to search. E.g: django matches awesome-django.')
parser.add_argument('-s', '--stars', action='store_const',
                    const=True, default=False, help='Toggle to sort result by stars.')
parser.add_argument('-r', '--results', default=5, type=int,
                    required=False, help='Results to display.')


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


def fetch_results(query_url: str, results: int):
    try:
        with urlopen(query_url) as f:
            result = json.load(f)
    except:
        print('Failed loading resources ...')
        sys.exit(0)

    for doc in result['docs'][:results]:
        name, desc, stars, url = doc['repo_name'], doc['body'], doc['stargazers_count'], doc['svn_url']
        print(f"{colors['green']}{name}{colors['end']} - {desc}")
        print(f"Stars {colors['yellow']}{stars}{colors['end']} {url}\n")


def main():
    args = parser.parse_args()

    query_url = format_url(args.query,
                           parse_list(args.languages),
                           parse_list(args.lists), sort_stars=args.stars)
    fetch_results(query_url, args.results)

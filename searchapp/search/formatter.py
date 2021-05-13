import re

UNSAFE_CHARS = re.compile('[\\[\\]\\<\\>+]')


def parse(query: str) -> str:
    """
    Remove unsafe characters
    https://github.com/redislabs-training/redis-sitesearch/blob/master/sitesearch/query_parser.py
    """
    query = query.strip().replace("-*", "*")
    query = UNSAFE_CHARS.sub(' ', query)
    query = query.strip()
    return query


def format_query(query, resources, languages, awesome_lists) -> str:
    text_query = parse(query)

    components = []
    if len(resources) > 0:
        sources = "|".join(resources)
        components.append(f"@source:({sources})")
    if len(languages) > 0:
        languages = "|".join(languages)
        components.append(f"@language:({languages})")
    if len(awesome_lists) > 0:
        awesome_lists = " ".join(awesome_lists)
        components.append(f"@lists:({awesome_lists})")

    components = " ".join(components)
    query = f"{components} {text_query}"
    return query

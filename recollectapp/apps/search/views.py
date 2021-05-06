import re

from config.settings import INDEX_NAME
from django_redis import get_redis_connection
from redisearch import Client, Query
from rest_framework.decorators import api_view
from rest_framework.response import Response

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


@api_view(['GET'])
def general_search(request) -> Response:

    client = Client(INDEX_NAME, conn=get_redis_connection())

    query = request.GET.get('query')
    query = parse(query)
    results = client.search(query)
    results = results.docs

    return Response({
        "docs": [doc.__dict__ for doc in results]
    })

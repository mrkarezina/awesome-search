from config.settings import INDEX_NAME
from django_redis import get_redis_connection
from redisearch import Client, Query
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .formatter import format_query

from redis import Redis


@api_view(['GET'])
def general_search(request) -> Response:
    """
    Default full text search on all resources if no sources are specified.

    Faceted search if sources are specified.

    **query**: Query to search.
    **source**: Multiple sources can be specifed.
    """

    client = Client(INDEX_NAME, conn=get_redis_connection())

    query = request.GET.get('query')
    resources = request.GET.getlist('source')
    languages = request.GET.getlist('language')
    awesome_lists = request.GET.getlist('awesome-list')
    query = format_query(query, resources, languages, awesome_lists)
    results = client.search(Query(query))
    results = results.docs

    return Response({
        "docs": [doc.__dict__ for doc in results]
    })


@api_view(['GET'])
def languages(request) -> Response:
    """
    Returns list of languges.
    """
    client = get_redis_connection()
    result = client.smembers('languages')

    return Response({
        "languages": result
    })


@api_view(['GET'])
def awesome_lists(request) -> Response:
    """
    Returns list of awesome lists.
    """
    client = get_redis_connection()
    result = client.smembers('awesome_lists')

    return Response({
        "lists": result
    })

import redisearch
from config.settings import HOST, PORT
from rest_framework.decorators import api_view
from rest_framework.response import Response

INDEX_NAME = "recollectIndexTweets"


@api_view(['GET'])
def general_search(request):

    client = redisearch.Client(INDEX_NAME, host=HOST, port=PORT)

    if request.method == 'GET':
        query = request.GET.get('query')
        results = client.search(query)
        results = results.docs

    return Response({
        "docs": [doc.__dict__ for doc in results]
    })


# Advanced search endpoint with filtering

# if request.method == 'POST':
#     query = request.data.get('query')

#     # TODO: Faceted search for dates
#     # TODO: Select corpera


# Incremental search to power chrome extension

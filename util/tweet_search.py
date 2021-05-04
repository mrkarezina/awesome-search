from redisearch import Client, TextField, IndexDefinition, Query

# Creating a client with a given index name
client = Client("recollectIndexTweets")


# Simple search
# TODO: increase generality of query
# Ie: 0 hits for 'board oF       dirEctorS'
#     1 hits for 'board of       dirEctorS'
results = client.search("""
board oF       dirEctorS
""")

for res in results.docs:
    print(res.body)
    print("---")


# # the result has the total number of results, and a list of documents
# print(res.total) # "2"
# print(res.docs[0].body) # "RediSearch"



# # Searching with complex parameters:
# q = Query("search engine").verbatim().no_content().with_scores().paging(0, 5)
# res = client.search(q)

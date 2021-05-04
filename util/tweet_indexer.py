
# https://docs.tweepy.org/en/latest/api.html?highlight=list#tweepy.API.list_timeline
# Fetch from specific list and insert into redis.

from tweepy import API, OAuthHandler, Cursor
from settings import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import json

from redisearch import Client, TextField, IndexDefinition, Query


auth = OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = API(auth)


# Creating a client with a given index name
client = Client("recollectIndexTweets")

# IndexDefinition is available for RediSearch 2.0+
definition = IndexDefinition(prefix=['tweet:'])

# Creating the index definition and schema
# client.create_index([TextField("body", weight=1)], definition=definition)



# status_list = api.home_timeline(tweet_mode='extended', count=1)
# # https://twitter.com/i/lists/1389386759507693574
# status_list = api.list_timeline(list_id="1389386759507693574", tweet_mode='extended', count=100)

for tweet in Cursor(api.list_timeline,
                       list_id="1389386759507693574",
                       tweet_mode='extended',
                       count=100,
                       lang="en").items(200):
    print(json.dumps(tweet._json))
    print(f'tweet:{tweet.id}', tweet.full_text)
    print("--")
    
    if len(tweet.full_text) > 100:
        # TODO: insert text from retweet
        client.redis.hset(f'tweet:{tweet.id}',
                    mapping={
                        'body': tweet.full_text
                    })

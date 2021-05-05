# Recollect

Learn more from what you read.

Recollect allows you to rediscover your highlights from across the web.


TODO: Architecture: https://redislabs.com/wp-content/uploads/2020/11/redisearch-docs-4.png

TODO: Screenshot showing speed of queries.

## Features
- Centralize highlights across Anki, [hypothes.is](https://web.hypothes.is/), [Readwise API](https://readwise.io/api_deets), Twitter, and Kindle.
- Search highlights, powered by [Redisearch](https://redisearch.io/).
- Resuface highlights similar to the article you're currently reading.
- Daily email with random & relevant highlights to review.
	- Relevant highlights determined by computing the most highlights documents while browsing.
	- Highlights that surfaced most frequently are included in the daily review email.

## Stack
- Frontend - *React*
- Backend - *Django*, *Redis*


## How it works
Highlights across different sources are stored in a variety of keys and data types using Redis.

Card data is stored as a JSON sterilized string.

[django-redis](https://github.com/jazzband/django-redis) is used to configure Redis as the backend for Django's cache. This allows for neatly accessing the [redis-py](https://github.com/andymccurdy/redis-py) client using `get_redis_connection()`. 


### Schema

All type of content / highlights are prefixed with `card`.

TODO: Scheme for rest of data stored in Redis

### Tweets

#### Store
```
SET cards:tweets:{tweet_id} {"tweet_id":"", "body":"", "author_screen_name":""}
```

#### Access
```
GET cards:tweets:{tweet_id}
```


### Search

#### Index
All keys storing card data are prefixed with `card`. This allows for easily defining a Redisearch index with all the different card types we want to search. 
```python
definition = IndexDefinition(prefix=['card:'])
```
Optionally if only specific card types such as Tweets and Kindle Highlights were to be indexed more specifc prefixed could be specified: `prefix=['card:tweets', 'card:kindle']`.

Before making any queries the index need to be built.
```python
client.create_index([TextField("body", weight=0.5),
                     TextField("title", weight=10)], definition=definition)

```
This specifies which hash feilds should be indexed.  Additionaly the weight argument allows for increasing the effect of matches in certain feilds such as "title".

Once the index is created it automatically stays in sync as new hashes are inserted. To add new documents to the index simply create a hash for that document.


#### Queries

Users can search across all their cards. Additionally context for the search can be specified to use only specific corpera such as tweets from the "AI" twitter list from the last 10 days.

Queries are first parsed to remove unsafe characters.


- Index list of tweets.
- Can select "context", specifies the list from which to pull tweets.
- Surface tweets relevant to content currently being browsed.
- Instead of browsing twitter, get daily email with most relevant tweets based on what you browsed on a given day.

Experiment with influencers on: https://medium.springboard.com/30-twitter-influencers-you-have-to-follow-for-ai-machine-learning-977587b6406e


TODO: Scoring function, specific query construction



## Similarity Search

TD-IDF comes out on top in several testing categories. https://towardsdatascience.com/the-best-document-similarity-algorithm-in-2020-a-beginners-guide-a01b9ef8cf05


When computing cosine similarty between TD-IDF representations the length of the document does not matter.
https://stackoverflow.com/questions/39704220/tf-idf-documents-of-different-length


Write custom scoring function: https://oss.redislabs.com/redisearch/Scoring/
https://oss.redislabs.com/redisearch/Extensions/#example_scoring_function

- First need to insert query into hash, calculate td-idf for terms in query
- Then in custom scoring code, for each term in query get tf-idf score
- Consruct array of score
- Similary for document construct array of score
- Calculate cosine similarity and return as score

- Not as fast as Annoy since not O(log n).



### Email

Redis Queue




## Architecture
- Django REST app.
- Create account. (Optional, can have access tokens as config in django app)
	- Submit access token to hypothesis, readwise, and twitter.
- Backend
	- Redis Queue for queing the indexing job
		- New content is fetched
		- Inserted into primary Redis
	- Similarity query.
		- Test between
			- User highlights scentence.
			- Paragraph.
			- Title.
		- RediSearch because of continous indexing capability, no need for batch indexing.
		- Display most similar content.
		- Increment tally of most similar content inside of Redis.
	- Redis Queue for queing the daily email job.
		- Reviews the content in Redis and find the highest ranking content.
		- Send email with highest tallying content.




## Development

Run RediSearch in a container as a daemon.
```
docker run -d -p 6379:6379 redislabs/redisearch:2.0.0
```

### Config

You will need to create a twitter developer account and submit an application to request access to the twitter API. Acceptance should be automated if you provide enough detail.

Copy the keys into `config.ini`.

The API key and secret on the developer dashboard is the consumer key and secret.

The access token and secret is account specific.


## Deployment
Deploymnent:
https://www.bogotobogo.com/DevOps/Docker/Docker_Kubernetes_Minikube_3_Django_with_Redis_Celery.php


TODO: see cloud run deployment


## Resources
Great article on building real time search for documentation: https://redislabs.com/blog/building-real-time-full-text-site-search-with-redisearch/

https://github.com/redislabs-training/redis-sitesearch

https://github.com/RediSearch/redisearch-py


https://github.com/jazzband/django-redis

https://github.com/redis-developer/basic-redis-chat-app-demo-python/tree/master/chat




# TODO
- [ ] Update schema to support cards from multiple users.
- [ ] Redis queue to offload indexing tasks.
- [ ] Custom scoring function for Redisearch td-idf similar. Calculate the vectors and take cosine similarty.
- [ ] Replace postge database
- [ ] Send daily email, script to generate report: https://stackoverflow.com/questions/573618/set-up-a-scheduled-job
- [ ] Configuration script to configure Redis Indexes
- [ ] Setup fresh environment from README to improve instruction replicability.
	- Focus on Redis configuration. 

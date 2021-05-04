# Recollect
Remeber what you read. Mindfull browsing.

## Features
- Resuface highlights similar to the article you're currently reading.
- Index highlights from:
	- [Hypothesis](https://h.readthedocs.io/en/latest/api-reference/v1/)
	- [Readwise API](https://readwise.io/api_deets).
		- Twitter
		- Kindle Higlights
	- Anki Deck
- Send an email with breakdown of content that was most similar to the things you browsed on any given day.
	- Chrome extension keeps count of which content most similar as you browse by upadting count in Redis.

### Backup Plan
- If nearest neighbour search becomes tricky with Redisearch can default to search engine + daily spaced repitition email for your content.


### Applications
- Index list of tweets.
- Can select "context", specifies the list from which to pull tweets.
- Surface tweets relevant to content currently being browsed.
- Instead of browsing twitter, get daily email with most relevant tweets based on what you browsed on a given day.

Experiment with influencers on: https://medium.springboard.com/30-twitter-influencers-you-have-to-follow-for-ai-machine-learning-977587b6406e


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


## Similarity Search

TD-IDF comes out on top in several testing categories. https://towardsdatascience.com/the-best-document-similarity-algorithm-in-2020-a-beginners-guide-a01b9ef8cf05


When computing cosine similarty between TD-IDF representations the length of the document does not matter.
https://stackoverflow.com/questions/39704220/tf-idf-documents-of-different-length




## Development

Run RediSearch in a container as a daemon.
```
docker run -d -p 6379:6379 redislabs/redisearch:2.0.0
```

### Twitter Secrets

You will need to create a twitter developer account and submit an application to request access to the twitter API. Acceptance should be automated if you provide enough detail.

Copy the keys into `config.ini`.

The API key and secret on the developer dashboard is the consumer key and secret.

The access token and secret is account specific.


## Deployment
Deploymnent:
https://www.bogotobogo.com/DevOps/Docker/Docker_Kubernetes_Minikube_3_Django_with_Redis_Celery.php



## Resources
https://github.com/RediSearch/redisearch-py


https://redislabs.com/blog/building-real-time-full-text-site-search-with-redisearch/


https://github.com/jazzband/django-redis

https://github.com/redis-developer/basic-redis-chat-app-demo-python/tree/master/chat




# TODO
- [ ] Send daily email, script to generate report: https://stackoverflow.com/questions/573618/set-up-a-scheduled-job
- [ ] Configuration script to configure Redis Indexes
- [ ] Setup fresh environment from README to improve instruction replicability.
	- Focus on Redis configuration. 
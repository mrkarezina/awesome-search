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


## Deployment
Deploymnent:
https://www.bogotobogo.com/DevOps/Docker/Docker_Kubernetes_Minikube_3_Django_with_Redis_Celery.php



## Resources
https://github.com/RediSearch/redisearch-py


https://redislabs.com/blog/building-real-time-full-text-site-search-with-redisearch/


https://github.com/jazzband/django-redis

https://github.com/redis-developer/basic-redis-chat-app-demo-python/tree/master/chat


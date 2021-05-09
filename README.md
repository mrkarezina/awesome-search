# Awesome Search

Find quality [awesome list](https://github.com/sindresorhus/awesome) resources and more directly in [Raycast](https://raycast.com/).

Powered by blazing fast [RediSearch](https://oss.redislabs.com/redisearch/).

TODO: Architecture: https://redislabs.com/wp-content/uploads/2020/11/redisearch-docs-4.png

TODO: Screenshot showing speed of queries.

## Why
Search results are frequently SEO'd to death. Results are full of low quality tutorials and blogs, making it hard to find the golden resources and niche blogs in all the noise.

The goal of Awesome Search is to build a tool to find high quality resources amidst all the noise. Awesome Search is not meant to act like Google which is great for just about anything, rather focus on curated resources and niche blogs that might not rank as high on Google.

Currently the prototype features searching across awesome lists and resources shared by your Twitter network.

## Features
- Search projects across awesome lists.
- Customize search preferences.
- Add custom sources such as resources shared by your Twitter following or Twitter lists.


## Next Steps
- Integrate with Google Programmable Search Engine.
	- [Pulling results from engineering blogs which don't rank as high on Google](https://twitter.com/mrkarezina/status/1345884177842003970?s=20).


## Stack
- Frontend - *React*
- Backend - *Django*, *Redis(RediSearch + RedisJSON)*


## Installation

To add the script follow the instructions on the [Raycast script commands page](https://github.com/raycast/script-commands).

If you already have a script directory for your Raycast scripts simply copy the `raycast/awesome_search.py` script to it.

TODO: Personalization token.


## How it works
Resources across different sources are stored in a variety of keys and data types using Redis.

Resource data is stored as a JSON sterilized string.

[django-redis](https://github.com/jazzband/django-redis) is used to configure Redis as the backend for Django's cache. This allows for neatly managing the connection for the [redis-py](https://github.com/andymccurdy/redis-py) and [redisearch-py](https://github.com/RediSearch/redisearch-py) client instances using `get_redis_connection()`. 


### Schema

All type of resources are prefixed with `resource:`.

### Github Repos
```
SET resource:github:{owner}:{repo_name} 
{
	'repo_name': resource['name'],
	'body': resource['description'],
	'stargazers_count': resource['stargazers_count'],
	'language': resource['language'],
	'svn_url': resource['svn_url']
}
```

Track which awesome lists a repository appears on. We can then use this set to add a [tag feild](https://oss.redislabs.com/redisearch/Tags/) specifying the awesome lists a resource appears on.
```
SADD resource:github:{owner}:{repo_name}:lists {list}
```

When inserting a new resource, maintain a list of unique awesome lists and languages to implement faceted search.

```
SADD resource:data:languages {language}
```

```
SADD resource:data:awesome_lists {list}
```


### Search

#### Index
All keys storing resource data are prefixed with `resource:`. This allows for easily defining a Redisearch index with all the different resource types we want to search.
```python
definition = IndexDefinition(prefix=['resource:'])
```
Optionally if only specific resources such as Github Repos were to be indexed more specific prefixes could be specified: `prefix=['resource:github']`.

Before making any queries the index need to be built.
```python
self.client.create_index([TextField('body', weight=1),
                                      TextField('repo_name', weight=1),
                                      TextField('language', weight=1)], definition=definition)

```
This specifies which feilds should be indexed.  Additionaly the weight argument allows for increasing the effect of matches in certain feilds such as "repo_name".

Once the index is created it automatically stays in sync as new hashes are inserted. To add new documents to the index simply create a hash for that document.


#### General Search

```
GET /search?query=
```

Full text search across all the resources.

```
FT.SEARCH {index} {query}
```


#### Faceted Search

```
GET /search?query=&source=&language=&awesome-list=
```

Redisearch supports [feild modifiers](https://oss.redislabs.com/redisearch/Query_Syntax/#field_modifiers) in the query. Modifiers can be combined to implement filtering on multiple filed. We use field modifiers to implement faceted search on specific sources, languges, awesome lists.

```
FT.SEARCH {index} @resouce:(tweets|github) @language:(Python|C) @awesome_list:(awesome-python) {query}
```


Alternatively instead of specifying the source (ie: tweet or github) as a feild modifier seperate indexes could be built for each source, by providing a more specific key prefix. Ie: 
```
definition_git = IndexDefinition(prefix=['resource:github'])
definition_tweet = IndexDefinition(prefix=['resource:tweet'])
```

The seperate indexes would result in faster queries but introduce additional complexity for ranking / pagination if the user chooses to search across both sources.


## Development

### Python

Create a new python virtual environment.
```
python -m venv venv
```

Activate virtual environment.
```
source venv/bin/activate
```

Install python dependecies
```
pip install -r requirements.txt
```


### Redis

Start a Docker container running the Redis instance with the Redisearch module.
```
docker run -d -p 6379:6379 redislabs/redisearch:2.0.0
```

### Seed database
Once Redis is up and running seed the database with some awesome list data.

In `settings.py` configure which awesome lists you would like to scrape and the maximum number of repos to insert per list. To quickly get started with a small dataset reduce `MAX_RES_PER_LIST`. 

```
python -m indexer.index
```

### Django

Run tests.
```
python manage.py test
```

Start the django server.
```
python manage.py runserver
```

### Raycast

Raycast automatically reflects any changes in the script. Simply run the script again to debug any changes.




### Config

Follow the steps below to copy the appropriate keys into `config.ini`.

### Twitter

You will need to create a twitter developer account and submit an application to request access to the twitter API. Acceptance should be automated if you provide enough detail.

The API key and secret on the developer dashboard is the consumer key and secret.

The access token and secret is account specific.


### Github


No application is required for the Github API. Request a personal access token [here](https://github.com/settings/tokens).


## Deployment
Deploymnent:
https://www.bogotobogo.com/DevOps/Docker/Docker_Kubernetes_Minikube_3_Django_with_Redis_Celery.php


TODO: see cloud run deployment

https://cloud.google.com/python/django/appengine
+ Redis enterprise cloud

Add double config if it's app engine environment or just local


# TODO
- [ ] Add contributing instructions
- [ ] Use stargazer count to scale relevance
- [ ] Update schema to support cards from multiple users.
- [ ] Configuration script to configure Redis Indexes
- [ ] Setup fresh environment from README to improve instruction replicability.
	- Focus on Redis configuration. 

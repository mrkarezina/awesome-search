# Awesome Search

Find and index quality [awesome list](https://github.com/sindresorhus/awesome) resources directly from [Raycast](https://raycast.com/) or your CLI!

Powered by blazing fast [RediSearch](https://oss.redislabs.com/redisearch/).


![Demo](https://raw.githubusercontent.com/mrkarezina/awesome-search/master/assets/demo.png)


## Why
Search results are frequently SEO'd to death. Results are full of low quality tutorials and blogs, making it hard to find the golden resources and niche blogs in all the noise.

The goal of Awesome Search is to build a tool to find high quality resources amidst all the noise. Awesome Search is not meant to act like Google which is great for just about anything, rather focus on curated resources and niche blogs that might not rank as high on Google.

Currently the prototype features searching across projects featured on awesome lists.


## Features
- Search projects across awesome lists.
- Customize search preferences.
- Submit an awesome list for indexing.


## Next steps

Indexing engineering blogs which might not rank as high in search results. For an example check out [this](https://cse.google.com/cse?cx=7170ef95a8051e78a) programmable search engine which only indexes engineering blogs on [this awesome list](https://github.com/kilimchoi/engineering-blogs).
 
There is also a Users module currently in the Django app. This module is for creating an API key that users can save to the cli app. This allows for restricting accounts that can index new lists thus reducing spam.


## Stack
- CLI - *Python*, *Raycast*
- Backend - *Django*, *Redis (RediSearch)*



## Installation


### CLI

Create and activate a python virtual environment.
```
python -m venv venv
```
```
source venv/bin/activate
```

Then:

```
pip install awesome-search
```

Usage
```
awesome "[query]"
```

Example search django redis projects, sort top results by stars.
```
awesome "django redis" -l python -s
```

#### Options

Comma delimited list of languages.
```
--languages python,javascript
```

Comma delimited list of terms to filter awesome lists results appear on. E.g "redis,django" for awesome-redis, awesome-django.
```
--lists [terms]
```

Sort results by stars.
```
--stars
```

Hits to return.
```
--results 5
```


### Raycast

To add the script follow the instructions on the [Raycast script commands page](https://github.com/raycast/script-commands).

If you already have a script directory for your Raycast scripts simply copy the `raycast/awesome_search.py` script to it.


## How it works
Resources across different sources are stored in a variety of keys and data types using Redis.

Resource data is stored as a JSON sterilized string.

[django-redis](https://github.com/jazzband/django-redis) is used to configure Redis as the backend for Django's cache. This allows for neatly managing the connection for the [redis-py](https://github.com/andymccurdy/redis-py) and [redisearch-py](https://github.com/RediSearch/redisearch-py) client instances using `get_redis_connection()`.

Redis Queue is used to submit new indexing jobs.


### Architecture

![Diagram](https://raw.githubusercontent.com/mrkarezina/awesome-search/master/assets/diagram.png)

### Schema

All types of resources are prefixed with `resource:`. This gives flexibility in extending to new resource types such as blogs.

### Github Repos

We use a set to track which awesome lists a repository appears on. After indexing the contents of the set are added as a document property for [filtering search results]((https://oss.redislabs.com/redisearch/Query_Syntax/#field_modifiers)) by awesome list.
```
SADD resource:github:{owner}:{repo_name}:lists {list}
```

```
SET resource:github:{owner}:{repo_name} 
{
	'repo_name': resource['name'],
	'lists': # SMEMBERS resource:github:{owner}:{repo_name}:lists
	'body': resource['description'],
	'stargazers_count': resource['stargazers_count'],
	'language': resource['language'],
	'svn_url': resource['svn_url']
}
```

Additionally when inserting a new resource, maintain a list of unique awesome lists and languages to implement faceted search.

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

Before making any queries the index needs to be built.
```python
self.client.create_index([TextField('body', weight=1),
                                      TextField('repo_name', weight=1.5),
                                      TextField('language', weight=1),
                                      TagField('lists')], definition=definition)

```
This specifies which fields should be indexed.  Additionally the weight argument allows for increasing the effect of matches in certain fields such as "repo_name".
 
Once the index is created documents are indexed in real time as they are added to Redis. To add new documents to the index simply create a hash for that document.


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

Redisearch supports [field modifiers](https://oss.redislabs.com/redisearch/Query_Syntax/#field_modifiers) in the query. Modifiers can be combined to implement filtering on multiple fields. We use field modifiers to implement faceted search on specific sources, languages, awesome lists.

```
FT.SEARCH {index} @resouce:(tweets|github) @language:(Python|C) @awesome_list:(awesome-python) {query}
```


Alternatively instead of specifying the source (ie: tweet or github) as a field modifier separate indexes could be built for each source, by providing a more specific key prefix. Ie:
```
definition_git = IndexDefinition(prefix=['resource:github'])
definition_tweet = IndexDefinition(prefix=['resource:tweet'])
```

The separate indexes would result in faster queries but introduce additional complexity for ranking / pagination if the user chooses to search across both sources.

## Development

### Python

First `cd searchapp`.

Create a new python virtual environment.
```
python -m venv venv
```

Activate the virtual environment.
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

### Config

The default `config.ini.sample` values are for local development.

Request a personal access token for the Github API [here](https://github.com/settings/tokens).

Copy / set the appropriate keys into `config.ini`.


### Seed database
Once Redis is up and running seed the database with some awesome list data.

In `assets/list_of_lists.txt` configure which awesome lists you would like to scrape and the maximum number of repos to insert per list. To limit the number of projects scraped decrease `MAX_RES_PER_LIST` in `settings.py`. 

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

### CLI

Install the CLI for testing locally.
```
python setup.py install
```


If using Raycast any changes in the script will automatically be reflected. Simply run the script again to debug any changes.


## Deployment

### Redis

Create a Redis instance on [Redis Cloud](https://redislabs.com/redis-enterprise-cloud/overview/). Set the port, host, and password of your instance in the redis section of the `searchapp/config.ini`.



### Backend

For detailed steps for deploying Django on App Engine see the official [documentation](https://cloud.google.com/python/django/appengine).

In the `searchapp/` root.

Set your project ID:
```
gcloud config set project my-project-id
```

[Create a MySQL database](https://cloud.google.com/python/django/appengine#creating_a_cloud_sql_instance). Then set the connection string / password in the deployment `config.ini`.

To deploy run
```
gcloud app deploy
```

### CLI

Create dist bundle.
```
python setup.py sdist
```

Push to PyPi
```
twine upload dist/*
```

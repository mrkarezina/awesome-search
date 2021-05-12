
from typing import List

from config.keys import Keys
from config.settings import (INDEX_NAME, KEY_PREFIX, REDIS_HOST,
                             REDIS_PASSWORD, REDIS_PORT, MAX_RES_PER_LIST)
from redis.exceptions import DataError, ResponseError
from redisearch import Client, IndexDefinition, TextField
from redisearch.client import TagField

from .scrapers import AwesomeScrape, RepoScraper


class Indexer:
    """
    Scrapes repos found on awesome lists. Inserts repo data into Redis.

    **urls**: List of Github awsome lists URLs.
    """

    def __init__(self, urls: List[str], max_per_list: int = MAX_RES_PER_LIST):
        self.urls = urls
        self.client = Client(INDEX_NAME, host=REDIS_HOST,
                             port=REDIS_PORT, password=REDIS_PASSWORD)
        self.keys = Keys(KEY_PREFIX)
        self.max = max_per_list

    def create_index_definition(self, drop_existing=False):
        """
        Create an index definition. Do nothing if it already exists.
        """

        if drop_existing:
            self.client.drop_index()

        definition = IndexDefinition(prefix=[self.keys.pre("resource:")])
        try:
            self.client.create_index([TextField('body', weight=1),
                                      TextField('repo_name', weight=1.5),
                                      TextField('language', weight=1),
                                      TagField('lists')], definition=definition)
        except ResponseError:
            print("Index already exists.")

    def index(self):
        """
        Insert scraped resources into Redis.
        """
        for url in self.urls:
            parent = RepoScraper(url)
            print(f"Creating index for {parent.repo}")

            self.client.redis.sadd(self.keys.awesome_list_list(), parent.repo)
            resources = AwesomeScrape(url).scrape(max_num=self.max)

            # Create set of all awesome lists a repo appears on
            # Required to set tag feild
            for resource in resources:
                try:
                    self.client.redis.sadd(self.keys.github_repo_lists(resource['owner']['login'], resource['name']),
                                           parent.repo)
                except (KeyError, DataError):
                    pass

            for resource in resources:
                try:
                    if resource['language'] is not None:
                        language = resource['language']
                        self.client.redis.sadd(self.keys.language_list(),
                                               language)
                    else:
                        language = ''

                    lists = self.client.redis.smembers(self.keys.github_repo_lists(resource['owner']['login'],
                                                                                   resource['name']))

                    self.client.redis.hset(self.keys.github_repo(resource['owner']['login'], resource['name']),
                                           mapping={
                                               'repo_name': resource['name'],
                                               'lists': ", ".join(lists),
                                               'body': resource['description'],
                                               'stargazers_count': resource['stargazers_count'],
                                               'language': language,
                                               'svn_url': resource['svn_url']
                    })

                except (KeyError, DataError):
                    print(f"Resource missing data: f{resource}")


if __name__ == "__main__":
    indexer = Indexer([
        # "https://github.com/vinta/awesome-python",
        # "https://github.com/JamzyWang/awesome-redis",
        # "https://github.com/sorrycc/awesome-javascript",
        # "https://github.com/sindresorhus/awesome-nodejs",
        # "https://github.com/markets/awesome-ruby",
        # "https://github.com/veggiemonk/awesome-docker",
        # "https://github.com/mjhea0/awesome-flask",
        # "https://github.com/wsvincent/awesome-django",
        # "https://github.com/ramitsurana/awesome-kubernetes",
        # "https://github.com/enaqx/awesome-react",
        # "https://github.com/dzharii/awesome-typescript",
        # "https://github.com/EthicalML/awesome-production-machine-learning",
        # "https://github.com/gramantin/awesome-rails",
        # "https://github.com/uralbash/awesome-pyramid",
        # "https://github.com/krzjoa/awesome-python-data-science",
        "https://github.com/mjhea0/awesome-fastapi",
        "https://github.com/shahraizali/awesome-django",
        "https://github.com/ucg8j/awesome-dash",
        "https://github.com/springload/awesome-wagtail",
        "https://github.com/typeddjango/awesome-python-typing",
        "https://github.com/mcauser/awesome-micropython",
        "https://github.com/faroit/awesome-python-scientific-audio",
        "https://github.com/timofurrer/awesome-asyncio",
        "https://github.com/hbokh/awesome-saltstack"
    ], max_per_list=300)
    indexer.create_index_definition()
    indexer.index()

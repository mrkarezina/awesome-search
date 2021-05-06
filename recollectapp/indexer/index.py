
from typing import List

from config.settings import INDEX_NAME, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT
from redis.exceptions import DataError, ResponseError
from redisearch import Client, IndexDefinition, TextField

from .scrapers import AwesomeScrape, RepoScraper


class Indexer:
    """
    Scrapes repos found on awesome lists. Inserts repo data into Redis.

    **urls**: List of Github awsome lists URLs.
    """

    def __init__(self, urls: List[str]):
        self.urls = urls
        self.client = Client(INDEX_NAME, REDIS_HOST,
                             REDIS_PORT, REDIS_PASSWORD)

    def create_index_definition(self, drop_existing=False):
        """
        Create an index definition. Do nothing if it already exists.
        """

        if drop_existing:
            self.client.drop_index()

        definition = IndexDefinition(prefix=['resource:'])
        try:
            self.client.create_index([TextField('body', weight=1),
                                      TextField('repo_name', weight=1),
                                      TextField('language', weight=1)], definition=definition)
        except ResponseError:
            print("Index already exists.")

    def index(self):
        for url in self.urls:
            parent = RepoScraper(url)
            print(f"Creating index for {parent.repo}")

            resources = AwesomeScrape(url).scrape(max_num=300)

            # Schema
            # 'resource:awesome_list:{parent_name}:{resource_name}'

            # TODO: Use stargazer count to scale relevance?
            for resource in resources:
                try:
                    language = resource['language'] if resource['language'] is not None else ''
                    self.client.redis.hset(f"resource:awesome_list:{parent.repo}:{resource['name']}",
                                           mapping={
                                               'repo_name': resource['name'],
                                               'body': resource['description'],
                                               'stargazers_count': resource['stargazers_count'],
                                               'language': language,
                                               'svn_url': resource['svn_url']
                                           })
                except (KeyError, DataError):
                    print(f"Resource missing data: f{resource}")


if __name__ == "__main__":
    indexer = Indexer([
        "https://github.com/vinta/awesome-python"
    ])
    indexer.create_index_definition()
    # indexer.index()

from unittest import TestCase

from indexer.index import Indexer
from indexer.scrapers import AwesomeScrape


class AwesomeScrapeTests(TestCase):
    def test_awesome_python(self):
        scraper = AwesomeScrape(
            "https://github.com/vinta/awesome-python/README/#")
        repos = scraper.scrape(1)
        for repo in repos:
            self.assertIsNotNone(repo['name'])
            self.assertIsNotNone(repo['full_name'])
            self.assertIsNotNone(repo['description'])


class AwesomeIndexerTests(TestCase):
    def test_awesome_indexer(self):
        indexer = Indexer([
            # "https://github.com/vinta/awesome-python",
            "https://github.com/JamzyWang/awesome-redis",
            "https://github.com/markets/awesome-ruby",
            "https://github.com/mjhea0/awesome-flask"
        ])
        indexer.create_index_definition()
        indexer.index()


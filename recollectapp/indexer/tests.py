from unittest import TestCase

from indexer.index import AwesomeScrape


class AwsomeScrapeTests(TestCase):
    def test_awesome_python(self):
        scraper = AwesomeScrape(
            "https://github.com/vinta/awesome-python/README/#")
        repos = scraper.scrape(2)
        for repos in repos:
            self.assertIsNotNone(repos['name'])
            self.assertIsNotNone(repos['full_name'])
            self.assertIsNotNone(repos['description'])

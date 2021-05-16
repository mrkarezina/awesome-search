from unittest import TestCase

from .awesome_search import format_error, format_results, parse_list, parser


class CLITests(TestCase):
    def test_parse_list(self):
        self.assertEqual(parse_list("python, ruby django |* redis"),
                         ["python", "ruby", "django", "redis"])

    def test_format_error(self):
        args = parser.parse_args(
            ['blah', '-l', 'python,ruby', '--lists', 'ruby,django'])
        result = "No results found for: \"blah\" | Written in: \"python,ruby\" | Featured on: \"ruby,django\" lists"
        self.assertEqual(format_error(args), result)

    def test_format_results(self):
        args = parser.parse_args(['redis', '-r', '1'])
        docs = [{'id': 'awesome:resource:github:andymccurdy:redis-py', 'payload': None, 'repo_name': 'redis-py', 'lists': 'awesome-redis, awesome-python',
                 'body': 'Redis Python Client', 'stargazers_count': '9277', 'language': 'Python', 'svn_url': 'https://github.com/andymccurdy/redis-py'}]
        result = "\x1b[92mredis-py\x1b[0m - Redis Python Client\nStars \x1b[93m9277\x1b[0m https://github.com/andymccurdy/redis-py\n\n"
        self.assertEqual(format_results(docs, args.results), result)

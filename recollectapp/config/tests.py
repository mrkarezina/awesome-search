from unittest import TestCase

from .keys import Keys


class KeyFormattingTests(TestCase):
    def test_repo(self):
        keys = Keys("pre")
        self.assertEqual(keys.github_repo("a", "b"), "pre:resource:github:a:b")
        self.assertEqual(keys.github_repo_lists("a", "b"),
                         "pre:resource:github:a:b:lists")

    def test_lists(self):
        keys = Keys("pre2")
        self.assertEqual(keys.language_list(), "pre2:resource:data:languages")
        self.assertEqual(keys.awesome_list_list(),
                         "pre2:resource:data:awesome_lists")

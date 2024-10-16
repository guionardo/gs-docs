import unittest

from src.github import get_user_repositories


class TestGitHub(unittest.TestCase):
    def test_get_user_repositories(self):
        repos = list(get_user_repositories('guionardo'))
        self.assertGreater(len(repos), 0)
        for repo in repos[0:10]:
            print(repo)
            print(repo.mkdocs)

        print(repo.download_zip())

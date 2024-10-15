import os
import unittest
from tempfile import TemporaryDirectory

import yaml

from src.configuration import GS_DOCS_ENV_PREFIX, loader


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        os.environ.update({f'{GS_DOCS_ENV_PREFIX}TEST': ''})

    def test_loader_from_env(self):
        os.environ[f'{GS_DOCS_ENV_PREFIX}TEST'] = '1234,4567'
        f = loader(list[str], None, 'test')
        v = f()
        self.assertEqual(['1234', '4567'], v)
        f = loader(str, None, 'test')
        v = f()
        self.assertEqual('1234,4567', v)

    def test_loader_from_file(self):
        with TemporaryDirectory() as tmpdir:
            config_file = os.path.join(tmpdir, 'config.yaml')
            with open(config_file, 'w') as f:
                yaml.dump({'test': [1234, 5678]}, f)
            f = loader(list[int], config_file, 'test')
            v = f()
            self.assertEqual([1234, 5678], v)

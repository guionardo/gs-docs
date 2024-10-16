import unittest
from dataclasses import dataclass
from datetime import UTC, datetime

from src.utils import new_dataclass


@dataclass
class ClassTest:
    id: int
    name: str
    dd: datetime


class TestUtils(unittest.TestCase):
    def test_new_dataclass(self):
        source = dict(id=10, name='Test', extra_field=True, dd='2020-01-02 10:00:21')

        dc = new_dataclass(ClassTest, source)
        self.assertEqual(10, dc.id)
        self.assertEqual('Test', dc.name)
        self.assertEqual(datetime(2020, 1, 2, 10, 0, 21, tzinfo=UTC), dc.dd)

import unittest
from data_base import DataBase


class TestDataBaseMethods(unittest.TestCase):

    def setUp(self):
        self.db = DataBase()

    def test_get(self):
        # Test key that is not been set
        self.assertEqual(None, self.db.get('key1'))

        # Test key that is already been set
        self.db.set('key2', 12)
        self.assertEqual(12, self.db.get('key2'))

        # Test for invalid input
        self.assertIsNone(self.db.get(123))

    def test_set(self):
        # Test for invalid inputs
        self.assertIsNone(self.db.set(123, 123))

        # Test for valid values positive, negative
        self.assertEqual(self.db.get('key3'), self.db.set('key3', 1))
        self.assertEqual(self.db.get('key4'), self.db.set('key4', -1))

    def test_increment(self):
        # Test for invalid inputs
        self.assertIsNone(self.db.increment(123))

        # Test for key that does not exist already
        self.assertEqual(1, self.db.increment('unknown_key'))

        # Test key that already present
        self.db.set('increment', 10)
        self.assertEqual(11, self.db.increment('increment'))

    def test_delete(self):
        # Test for invalid inputs
        self.assertIsNone(self.db.delete(123))

        # Delete key that is not present in DB
        self.db.set('delete_key', 10)
        self.assertEqual(self.db.delete('delete_key'), self.db.get('delete_key'))

    def test_delete_value(self):
        # Test for invalid inputs
        self.assertIsNone(self.db.delete_value('abc'))

        # Test for value that exists in DB
        self.db.set('delete_val', 123)
        self.assertEqual(self.db.delete_value(123), self.db.get('delete_val'))

        # Test for value that is not in DB
        self.assertIsNone(self.db.delete_value(9999))


if __name__ == '__main__':
    unittest.main()

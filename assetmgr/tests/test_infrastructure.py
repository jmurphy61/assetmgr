import importlib, time, unittest
from source.infrastructure import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
    
    def test_constructor(self):
        self.assertIsNotNone(self.db)
        self.assertIsInstance(self.db, Database)

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    unittest.main()
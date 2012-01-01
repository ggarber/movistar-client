import unittest
from client import MovistarClient

class MovistarClientTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_status(self):
        client = MovistarClient()
        client.login("hNIF", "DDDDaaaaa")
        status = client.status()
    
        self.assertTrue(status['calls'] > 0)
        self.assertTrue(status['calls'] < 100)
        self.assertTrue(status['calls_cost'] > 0)
        self.assertTrue(status['calls_cost'] < 50)
        self.assertTrue(status['traffic'] > 0)
        self.assertTrue(status['traffic'] < 500000)

if __name__ == '__main__':
    unittest.main()

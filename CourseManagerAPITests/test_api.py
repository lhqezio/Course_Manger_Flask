import flask_unittest, unittest, requests

class TestAPI(unittest.TestCase):
    def test_get_posts(self):
        url = "/api/posts"
        resp = requests.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance()
        self.assertTrue(True)
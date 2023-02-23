from unittest import TestCase
from unittest.mock import patch

import responses

from get_people import ACCESS_TOKEN, requests_get_first


class TryTesting(TestCase):
    @responses.activate
    @patch("main.requests.get", side_effects=["200", "200"])
    def test_requests_get(self, mock_get):
        responses.add(
            **{
                "method": responses.GET,
                "url": "http://example.com/api/123",
                "body": "success",
                "status": 200,
            }
        )
        responses.add(
            **{
                "method": responses.GET,
                "url": "http://example.com/api/123",
                "body": "success",
                "status": 200,
            }
        )
        endpoint = "people"
        params = {"access_token": ACCESS_TOKEN, "limit": 1}
        actual = requests_get_first(endpoint, params)
        expected = "200"
        self.assertTrue(True)

    def test_always_fails(self):
        self.assertTrue(False)

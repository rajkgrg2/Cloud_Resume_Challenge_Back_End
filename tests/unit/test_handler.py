import os
import re
import json
import unittest
from unittest import mock
from ..backend import app

import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from backend import app


class TestLambdaHandler(unittest.TestCase):
    @mock.patch.dict(os.environ, {"TABLENAME": "visitor_counter_table"})
    def test_lambda_handler(self):
        # Check AWS creds
        assert "AWS_ACCESS_KEY_ID" in os.environ
        assert "AWS_SECRET_ACCESS_KEY" in os.environ

        ret = app.lambda_handler("", "")

        # Assert return keys
        self.assertIn("statusCode", ret)
        self.assertIn("headers", ret)
        self.assertIn("body", ret)

        # Check for CORS in Headers
        self.assertIn("Access-Control-Allow-Origin", ret["headers"])
        self.assertIn("Access-Control-Allow-Methods", ret["headers"])
        self.assertIn("Access-Control-Allow-Headers", ret["headers"])

        # Check status code
        if ret["statusCode"] == 200:
            self.assertIn("visit_count", ret["body"])
            self.assertTrue(json.loads(ret["body"])["visit_count"].isnumeric())
        else:
            self.assertEqual(json.loads(ret["body"])["visit_count"], -1)


if __name__ == "__main__":
    unittest.main()


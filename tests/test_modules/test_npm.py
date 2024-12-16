from django.test import Client
from unittest.mock import patch
import json

from tests.test_utils import MockResponse


@patch("packages.modules.npm.requests.get")
def test_get_package(mock_get):
    # Mock the response for the main package (minimatch)
    def mock_response(url):
        if "minimatch" in url:
            return MockResponse(
                {
                    "name": "minimatch",
                    "versions": {
                        "3.1.2": {
                            "name": "minimatch",
                            "version": "3.1.2",
                            "description": "A library for matching file paths",
                            "dependencies": {
                                "brace-expansion": "^1.1.11"
                            },
                        }
                    },
                }
            )
        elif "brace-expansion" in url:
            return MockResponse(
                {
                    "name": "brace-expansion",
                    "versions": {
                        "1.1.11": {
                            "name": "brace-expansion",
                            "version": "1.1.11",
                            "description": "A library for expanding braces",
                            "dependencies": {
                                "balanced-match": "^1.0.2",
                                "concat-map": "0.0.1"
                            },
                        }
                    },
                }
            )
        elif "balanced-match" in url:
            return MockResponse(
                {
                    "name": "balanced-match",
                    "versions": {
                        "1.0.2": {
                            "name": "balanced-match",
                            "version": "1.0.2",
                            "description": "A balanced match library",
                            "dependencies": {},
                        }
                    },
                }
            )
        elif "concat-map" in url:
            return MockResponse(
                {
                    "name": "concat-map",
                    "versions": {
                        "0.0.1": {
                            "name": "concat-map",
                            "version": "0.0.1",
                            "description": "A concat map library",
                            "dependencies": {},
                        }
                    },
                }
            )
        return MockResponse({}, 404)
    mock_get.side_effect = mock_response
    

    client = Client()
    response = client.get("/package/minimatch/3.1.2")
    
    assert response.status_code == 200
    assert response.json() == {
        "dependencies": [
            {
                "dependencies": [
                    {"dependencies": [], "name": "balanced-match", "version": "1.0.2"},
                    {"dependencies": [], "name": "concat-map", "version": "0.0.1"},
                ],
                "name": "brace-expansion",
                "version": "1.1.11",
            }
        ],
        "name": "minimatch",
        "version": "3.1.2",
    }

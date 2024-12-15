from django.test import Client
from unittest.mock import patch
import json


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

@patch("packages.modules.npm.requests.get")
def test_get_package_empty_dependencies(mock_get):
    # Mock the response for the main package (empty-deps)
    def mock_response(url):
        if "empty-deps" in url:
            return MockResponse(
                {
                    "name": "empty-deps",
                    "versions": {
                        "1.0.0": {
                            "name": "empty-deps",
                            "version": "1.0.0",
                            "description": "A package with no dependencies",
                            "dependencies": {},
                        }
                    },
                }
            )
        return MockResponse({}, 404)

    mock_get.side_effect = mock_response

    client = Client()
    response = client.get("/package/empty-deps/1.0.0")

    # Assert that the response is correct for a package with no dependencies
    assert response.status_code == 200
    assert response.json() == {
        "dependencies": [],
        "name": "empty-deps",
        "version": "1.0.0",
    }



@patch("packages.modules.npm.requests.get")
def test_get_package_missing_dependencies_key(mock_get):
    # Mock the response for the main package (missing-deps-key)
    def mock_response(url):
        if "missing-deps-key" in url:
            return MockResponse(
                {
                    "name": "missing-deps-key",
                    "versions": {
                        "1.0.0": {
                            "name": "missing-deps-key",
                            "version": "1.0.0",
                            "description": "A package with no dependencies key",
                            # No "dependencies" key here
                        }
                    },
                }
            )
        return MockResponse({}, 404)

    mock_get.side_effect = mock_response

    client = Client()
    response = client.get("/package/missing-deps-key/1.0.0")

    # Assert that the response is correct for a package without a dependencies key
    assert response.status_code == 200
    assert response.json() == {
        "dependencies": [],
        "name": "missing-deps-key",
        "version": "1.0.0",
    }


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data
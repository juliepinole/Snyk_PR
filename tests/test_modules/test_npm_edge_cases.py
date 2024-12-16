from django.test import Client
from unittest.mock import patch
import json

from tests.test_utils import MockResponse

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


@patch("packages.modules.npm.requests.get")
def test_get_package_circular_dependencies(mock_get):
    # Mock responses for circular dependencies
    def mock_response(url):
        if "package-a" in url:
            return MockResponse(
                {
                    "name": "package-a",
                    "versions": {
                        "1.0.0": {
                            "name": "package-a",
                            "version": "1.0.0",
                            "description": "Package A description",
                            "dependencies": {"package-b": "^1.0.0"},
                        }
                    },
                }
            )
        elif "package-b" in url:
            return MockResponse(
                {
                    "name": "package-b",
                    "versions": {
                        "1.0.0": {
                            "name": "package-b",
                            "version": "1.0.0",
                            "description": "Package B description",
                            "dependencies": {"package-a": "^1.0.0"},
                        }
                    },
                }
            )
        return MockResponse({}, 404)

    mock_get.side_effect = mock_response

    client = Client()
    response = client.get("/package/package-a/1.0.0")

    # Assert the response status code
    assert response.status_code == 200

    # Assert that circular dependencies are handled (no infinite recursion)
    # Adjust the expected result depending on your desired behavior
    assert response.json() == {
        "dependencies": [
            {
                "dependencies": [
                    {
                        "dependencies": [],  # Stop resolving here to prevent recursion
                        "name": "package-a",
                        "version": "1.0.0",
                    }
                ],
                "name": "package-b",
                "version": "1.0.0",
            }
        ],
        "name": "package-a",
        "version": "1.0.0",
    }
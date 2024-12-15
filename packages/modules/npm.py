import requests
import semver
import logging

from packages.models import VersionedPackage

NPM_REGISTRY_URL = "https://registry.npmjs.org"


def get_package(name: str, range: str) -> VersionedPackage:
    url = f"{NPM_REGISTRY_URL}/{name}"

    npm_package = requests.get(url).json()
    versions = list(npm_package["versions"].keys())
    version = semver.min_satisfying(versions, range)

    # Find the matching version
    version = semver.min_satisfying(versions, range)
    if version is None:
        logging.error(f"No matching version found for {name} with range {range} and versions list {versions}, while looking at the mock value of the {npm_package['name']} package")
        return None  # TODO(pinolej): check what to return

    version_record = npm_package["versions"][version]

    package = VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    )
    dependencies = version_record.get("dependencies", {})

    package.dependencies = [
        get_package(name=dep_name, range=dep_range) for dep_name, dep_range in dependencies.items()
    ]

    return package


def request_package(name: str, range: str) -> tuple[VersionedPackage, dict]:
    url = f"{NPM_REGISTRY_URL}/{name}"

    npm_package = requests.get(url).json()

    versions = list(npm_package["versions"].keys())
    version = semver.min_satisfying(versions, range)
    version_record = npm_package["versions"][version]

    return VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    ), version_record.get("dependencies", {})

import requests
import semver
import logging

from packages.models import VersionedPackage

NPM_REGISTRY_URL = "https://registry.npmjs.org"


def get_package(name: str, range: str, visited=None) -> VersionedPackage:
    if visited is None:
        visited = set()

    # Fetch the package data from the registry
    url = f"{NPM_REGISTRY_URL}/{name}"
    npm_package = requests.get(url).json()

    # Resolve the version based on the range
    versions = list(npm_package["versions"].keys())
    version = semver.min_satisfying(versions, range)

    # Check for circular dependencies using (name, version)
    if (name, version) in visited:
        return VersionedPackage(name=name, version=version, description="Circular dependency detected.")

    # Add the package (name, version) to the visited set
    visited.add((name, version))

    # Fetch version details
    version_record = npm_package["versions"][version]
    package = VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    )

    # Resolve dependencies recursively
    dependencies = version_record.get("dependencies", {})
    package.dependencies = [
        get_package(dep_name, dep_range, visited) for dep_name, dep_range in dependencies.items()
    ]

    return package

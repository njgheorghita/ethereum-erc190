import json
from pathlib import Path


class Manifest:
    def __init__(self, manifest_version: int, package_name: str, version: str) -> None:
        self.manifest_version = manifest_version
        self.package_name = package_name
        self.version = version

    def pretty(self) -> str:
        return json.dumps(self.__dict__, indent=4)

    def minified(self) -> str:
        return json.dumps(self.__dict__, separators=(",", ":"), sort_keys=True)


def create_manifest_from_dir(path_to_json, manifest_version, package_name, version):
    solc_output = Path(path_to_json)
    manifest = Manifest(manifest_version, package_name, version)
    with open(solc_output) as f:
        json_data = json.load(f)
    manifest.source = json_data
    return manifest

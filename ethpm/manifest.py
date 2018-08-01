import json


class Manifest:
    def __init__(self, manifest_version: int, package_name: str, version: str) -> None:
        self.manifest_version = manifest_version
        self.package_name = package_name
        self.version = version

    def pretty(self) -> str:
        return json.dumps(self.__dict__, indent=4)

    def minified(self) -> str:
        return json.dumps(self.__dict__, separators=(",", ":"), sort_keys=True)

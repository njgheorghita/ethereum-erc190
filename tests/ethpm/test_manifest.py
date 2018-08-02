from pathlib import Path

from ethpm.manifest import create_manifest_from_dir, Manifest

MANIFEST_VERSION = 2
PACKAGE_NAME = "package"
VERSION = "1.0.0"
PRETTY_MANIFEST = """{
    "manifest_version": 2,
    "package_name": "package",
    "version": "1.0.0"
}"""
MINIFIED_MANIFEST = '{"manifest_version":2,"package_name":"package","version":"1.0.0"}'


def test_manifest():
    manifest = Manifest(MANIFEST_VERSION, PACKAGE_NAME, VERSION)
    assert isinstance(manifest, Manifest)
    assert manifest.minified() == MINIFIED_MANIFEST
    assert manifest.pretty() == PRETTY_MANIFEST

STANDARD_TOKEN_DIR = '/Users/nickgheorghita/ethereum/py-ethpm/tests/ethpm/solc_output.json'

def test_create_simple_manifest_from_dir():
    manifest_version = 2
    package_name = 'standard-token'
    version = '1.0.0'
    manifest = create_manifest_from_dir(STANDARD_TOKEN_DIR, manifest_version, package_name, version)
    assert isinstance(manifest, Manifest)
    assert manifest.manifest_version == manifest_version
    assert manifest.package_name == package_name
    assert manifest.version == version
    assert "contracts" in manifest.source
    # pass in contract dir
    # pass in any relevant options
    # return manifest in json

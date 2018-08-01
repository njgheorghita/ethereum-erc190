from ethpm.manifest import Manifest

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

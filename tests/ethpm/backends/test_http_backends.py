import pytest
from requests.exceptions import HTTPError

from ethpm import Package
from ethpm.backends.http import GithubOverHTTPSBackend
from ethpm.constants import GITHUB_API_AUTHORITY
from ethpm.exceptions import CannotHandleURI, ValidationError

BLOB_URI = "https://api.github.com/repos/ethpm/py-ethpm/git/blobs/a7232a93f1e9e75d606f6c1da18aa16037e03480"


def test_github_over_https_backend_fetch_uri_contents(owned_contract, w3):
    # these tests may occassionally fail CI as a result of their network requests
    backend = GithubOverHTTPSBackend()
    assert backend.base_uri == GITHUB_API_AUTHORITY
    # integration with Package.from_uri
    owned_package = Package.from_uri(BLOB_URI, w3)
    assert owned_package.name == "owned"


def test_github_over_https_backend_raises_error_with_invalid_content_hash(w3):
    invalid_uri = "https://api.github.com/repos/ethpm/py-ethpm/git/blobs/a7232a93f1e9e75d606f6c1da18aa16037e03123"
    with pytest.raises(HTTPError):
        Package.from_uri(invalid_uri, w3)


def test_github_backend_writes_to_disk(tmp_path):
    backend = GithubOverHTTPSBackend()
    contents = backend.fetch_uri_contents(BLOB_URI)
    target_path = tmp_path / "github_uri.txt"
    backend.write_to_disk(BLOB_URI, target_path)
    assert target_path.read_bytes() == contents


def test_github_backend_write_to_disk_raises_exception_if_target_exists(tmp_path):
    target_path = tmp_path / "test.txt"
    target_path.touch()
    with pytest.raises(CannotHandleURI, match="cannot be written to disk."):
        GithubOverHTTPSBackend().write_to_disk(BLOB_URI, target_path)

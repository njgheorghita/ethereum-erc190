import base64
import json
from pathlib import Path
import shutil
import tempfile

from eth_typing import URI
import requests

from ethpm.backends.base import BaseURIBackend
from ethpm.constants import GITHUB_API_AUTHORITY
from ethpm.exceptions import CannotHandleURI
from ethpm.utils.uri import (
    is_valid_content_addressed_github_uri,
    validate_blob_uri_contents,
)


class GithubOverHTTPSBackend(BaseURIBackend):
    """
    Base class for all URIs pointing to a content-addressed Github URI.
    """

    @property
    def base_uri(self) -> str:
        return GITHUB_API_AUTHORITY

    def can_resolve_uri(self, uri: URI) -> bool:
        return is_valid_content_addressed_github_uri(uri)

    def can_translate_uri(self, uri: URI) -> bool:
        """
        GithubOverHTTPSBackend uri's must resolve to a valid manifest,
        and cannot translate to another content-addressed URI.
        """
        return False

    def fetch_uri_contents(self, uri: URI) -> bytes:
        if not self.can_resolve_uri(uri):
            raise CannotHandleURI(f"GithubOverHTTPSBackend cannot resolve {uri}.")

        response = requests.get(uri)
        response.raise_for_status()
        contents = json.loads(response.content)
        if contents["encoding"] != "base64":
            raise CannotHandleURI(
                "Expected contents returned from Github to be base64 encoded, "
                f"instead received {contents['encoding']}."
            )
        decoded_contents = base64.b64decode(contents["content"])
        validate_blob_uri_contents(decoded_contents, uri)
        return decoded_contents

    def write_to_disk(self, uri: URI, target_path: Path) -> None:
        contents = self.fetch_uri_contents(uri)
        if target_path.exists():
            raise CannotHandleURI(
                f"Github blob: {uri} cannot be written to disk since target path ({target_path}) "
                "already exists. Please provide a target_path that does not exist."
            )
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(contents)
            temp.seek(0)
            shutil.copyfile(temp.name, target_path)

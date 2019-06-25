from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from eth_typing import URI


class BaseURIBackend(ABC):
    """
    Generic backend that all URI backends are subclassed from.

    All subclasses must implement:
    can_resolve_uri, can_translate_uri, fetch_uri_contents
    """

    @abstractmethod
    def can_resolve_uri(self, uri: URI) -> bool:
        """
        Return a bool indicating whether this backend class can
        resolve the given URI to it's contents.
        """
        pass

    @abstractmethod
    def can_translate_uri(self, uri: URI) -> bool:
        """
        Return a bool indicating whether this backend class can
        translate the given URI to a corresponding content-addressed URI.
        """
        pass

    @abstractmethod
    def fetch_uri_contents(self, uri: URI) -> Union[bytes, URI]:
        """
        Fetch the contents stored at a URI.
        """
        pass

    @abstractmethod
    def write_to_disk(self, uri: URI, target_path: Path) -> None:
        """
        Writes the contents of target URI to target path.
        Raises exception if target path exists.
        """
        pass

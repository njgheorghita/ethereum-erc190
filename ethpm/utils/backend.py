import logging
from typing import Generator, Type

from eth_typing import URI
from eth_utils import to_tuple
from ipfshttpclient.exceptions import ConnectionError
import trio

from ethpm.backends.base import BaseURIBackend
from ethpm.backends.http import GithubOverHTTPSBackend
from ethpm.backends.ipfs import (
    AsyncIPFS,
    AsyncInfura,
    AsyncLocal,
    DummyIPFSBackend,
    InfuraIPFSBackend,
    IPFSGatewayBackend,
    LocalIPFSBackend,
    get_ipfs_backend_class,
)
from ethpm.backends.registry import RegistryURIBackend
from ethpm.exceptions import CannotHandleURI

URI_BACKENDS = [
    InfuraIPFSBackend,
    IPFSGatewayBackend,
    DummyIPFSBackend,
    LocalIPFSBackend,
    GithubOverHTTPSBackend,
    RegistryURIBackend,
]
ASYNC_URI_BACKENDS = [
    AsyncIPFS,
    AsyncInfura,
    AsyncLocal,
]

logger = logging.getLogger("ethpm.utils.backend")


def resolve_uri_contents(uri: URI, fingerprint: bool = None) -> bytes:
    """
    synchronous fetching single supported c-a uri
    """
    resolvable_backends = get_resolvable_backends_for_uri(uri)
    if resolvable_backends:
        for backend in resolvable_backends:
            try:
                # ignore type b/c resolvable backends only return uri contents
                contents: bytes = backend().fetch_uri_contents(uri)  # type: ignore
            except CannotHandleURI:
                continue
            return contents

    translatable_backends = get_translatable_backends_for_uri(uri)
    if translatable_backends:
        if fingerprint:
            raise CannotHandleURI(
                "Registry URIs must point to a resolvable content-addressed URI."
            )
        package_id = RegistryURIBackend().fetch_uri_contents(uri)
        return resolve_uri_contents(package_id, fingerprint=True)

    raise CannotHandleURI(
        f"URI: {uri} cannot be resolved by any of the available backends."
    )


async def async_resolve_uris(uris):
    """
    takes list of any supported content-addressed uris and returns dict {uri=> contents}
    NO registry uris!
    """
    results = {}
    async with trio.open_nursery() as nursery:
        for uri in uris:
            nursery.start_soon(async_resolve_uri_contents, uri, results)
    return results


async def async_resolve_uri_contents(uri, results):
    async_backends = async_get_resolvable_backends_for_uri(uri)
    send_channel, receive_channel = trio.open_memory_channel(0)
    async def jockey(async_fn):
        try:
            await send_channel.send(await async_fn(uri))
        except CannotHandleURI:
            pass

    async with trio.open_nursery() as nursery:
        for backend in async_backends:
            nursery.start_soon(jockey, backend().fetch_uri_contents)
        # will this hang if no backends can serve uri?
        winner = await receive_channel.receive()
        nursery.cancel_scope.cancel()
        # mutation acceptable here?
        results[uri] = winner


@to_tuple
def get_translatable_backends_for_uri(
    uri: URI
) -> Generator[Type[BaseURIBackend], None, None]:
    # type ignored because of conflict with instantiating BaseURIBackend
    for backend in URI_BACKENDS:
        try:
            if backend().can_translate_uri(uri):  # type: ignore
                yield backend
        except ConnectionError:
            logger.debug("No local IPFS node available on port 5001.", exc_info=True)

@to_tuple
def async_get_resolvable_backends_for_uri(
    uri: URI
) -> Generator[Type[BaseURIBackend], None, None]:
    for backend_class in ASYNC_URI_BACKENDS:
        try:
            if backend_class().can_resolve_uri(uri):  # type: ignore
                yield backend_class
        except ConnectionError:
            logger.debug(
                "No local IPFS node available on port 5001.", exc_info=True
            )

@to_tuple
def get_resolvable_backends_for_uri(
    uri: URI
) -> Generator[Type[BaseURIBackend], None, None]:
    # special case the default IPFS backend to the first slot.
    default_ipfs = get_ipfs_backend_class()
    if default_ipfs in URI_BACKENDS and default_ipfs().can_resolve_uri(uri):
        yield default_ipfs
    else:
        for backend_class in URI_BACKENDS:
            if backend_class is default_ipfs:
                continue
            # type ignored because of conflict with instantiating BaseURIBackend
            else:
                try:
                    if backend_class().can_resolve_uri(uri):  # type: ignore
                        yield backend_class
                except ConnectionError:
                    logger.debug(
                        "No local IPFS node available on port 5001.", exc_info=True
                    )

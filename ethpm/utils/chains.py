import re
from eth_utils import (
    add_0x_prefix,
)


def get_chain_id(web3):
    return web3.eth.getBlock(0)['hash']


BLOCK = "block"

BIP122_URL_REGEX = (
    "^"
    "blockchain://"
    "(?P<chain_id>[a-zA-Z0-9]{64})"
    "/"
    "(?P<resource_type>block|transaction)"
    "/"
    "(?P<resource_hash>[a-zA-Z0-9]{64})"
    "$"
)


def is_BIP122_uri(value):
    return bool(re.match(BIP122_URL_REGEX, value))


def parse_BIP122_uri(blockchain_uri):
    match = re.match(BIP122_URL_REGEX, blockchain_uri)
    if match is None:
        raise ValueError("Invalid URI format: '{0}'".format(blockchain_uri))
    chain_id, resource_type, resource_hash = match.groups()
    return (
        add_0x_prefix(chain_id),
        resource_type,
        add_0x_prefix(resource_hash),
    )


def is_BIP122_block_uri(value):
    if not is_BIP122_uri(value):
        return False
    _, resource_type, _ = parse_BIP122_uri(value)
    return resource_type == BLOCK


def check_if_chain_matches_chain_uri(web3, blockchain_uri):
    chain_id, resource_type, resource_hash = parse_BIP122_uri(blockchain_uri)
    genesis_block = web3.eth.getBlock('earliest')
    if genesis_block['hash'] != chain_id:
        return False

    if resource_type == BLOCK:
        resource = web3.eth.getBlock(resource_hash)
    else:
        raise ValueError("Unsupported resource type: {0}".format(resource_type))

    if resource['hash'] == resource_hash:
        return True
    else:
        return False

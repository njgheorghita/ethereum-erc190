from eth_typing import URI
from eth_utils import encode_hex, remove_0x_prefix
from eth_utils.toolz import curry
from web3 import Web3

from ethpm._utils.chains import BLOCK, create_BIP122_uri, parse_BIP122_uri


def get_genesis_block_hash(web3: Web3) -> str:
    return web3.eth.getBlock(0)["hash"]


@curry
def check_if_chain_matches_chain_uri(web3: Web3, blockchain_uri: URI) -> bool:
    chain_id, resource_type, resource_hash = parse_BIP122_uri(blockchain_uri)
    genesis_block = web3.eth.getBlock("earliest")

    if encode_hex(genesis_block["hash"]) != chain_id:
        return False

    if resource_type == BLOCK:
        resource = web3.eth.getBlock(resource_hash)
    else:
        raise ValueError(f"Unsupported resource type: {resource_type}")

    if encode_hex(resource["hash"]) == resource_hash:
        return True
    else:
        return False


def create_block_uri(chain_id: str, block_identifier: str) -> URI:
    return create_BIP122_uri(chain_id, "block", remove_0x_prefix(block_identifier))

from pathlib import Path
from ethpm.utils.ipfs import generate_links

import pytest

from ethpm.utils.ipfs import extract_ipfs_path_from_uri, generate_file_hash, is_ipfs_uri


@pytest.mark.parametrize(
    "value,expected",
    (
        (
            "ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
        ),
        (
            "ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
        ),
        (
            "ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
        ),
        (
            "ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
        ),
        (
            "ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
        ),
        (
            "ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u",
        ),
        (
            "ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
        ),
        (
            "ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
        ),
        (
            "ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
        ),
        (
            "ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
        ),
        (
            "ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
        ),
        (
            "ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/",
            "QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme",
        ),
    ),
)
def test_extract_ipfs_path_from_uri(value, expected):
    actual = extract_ipfs_path_from_uri(value)
    assert actual == expected


@pytest.mark.parametrize(
    "value,expected",
    (
        ("ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u", True),
        ("ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u", True),
        ("ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u", True),
        ("ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/", True),
        ("ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/", True),
        ("ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/", True),
        ("ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme", True),
        ("ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme", True),
        ("ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme", True),
        ("ipfs:QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/", True),
        ("ipfs:/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/", True),
        ("ipfs://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/", True),
        # malformed
        ("ipfs//QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/", False),
        ("ipfs/QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/", False),
        ("ipfsQmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme/", False),
        # HTTP
        ("http://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme", False),
        ("https://QmTKB75Y73zhNbD3Y73xeXGjYrZHmaXXNxoZqGCagu7r8u/readme", False),
        # No hash
        ("ipfs://", False),
    ),
)
def test_is_ipfs_uri(value, expected):
    actual = is_ipfs_uri(value)
    assert actual is expected


@pytest.mark.parametrize(
    "file_name,file_contents,expected",
    (
        ("test-1.txt", "piper\n", "QmUdxEGxvp71kqYLkA91mtNg9QRRSPBtA3UV6VuYhoP7DB"),
        (
            "test-2.txt",
            "pipermerriam\n",
            "QmXqrQR7EMePe9LCRUVrfkxYg5EHRNpcA1PZnN4AnbM9DW",
        ),
        (
            "test-3.txt",
            "this is a test file for ipfs hash generation\n",
            "QmYknNUKXWSaxfCWVgHd8uVCYHhzPerVCLvCCBedWtqbnv",
        ),
    ),
)
def test_generate_file_hash(tmpdir, file_name, file_contents, expected):
    p = tmpdir.mkdir("sub").join(file_name)
    p.write(file_contents)
    ipfs_multihash = generate_file_hash(Path(p).read_bytes())
    assert ipfs_multihash == expected


def test_generate_file_hash_for_large_files(tmp_path):
    expected_links = (
        (b'QmZ5RgT3jJhRNMEgLSEsez9uz1oDnNeAysLLxRco8jz5Be', 262158),
        (b'QmUZvm5TertyZagJfoaw5E5DRvH6Ssu4Wsdfw69NHaNRTc', 262158),
        (b'QmTA3tDxTZn5DGaDshGTu9XHon3kcRt17dgyoomwbJkxvJ', 262158),
        (b'QmXRkS2AtimY2gujGJDXjSSkpt2Xmgog6FjtmEzt2PwcsA', 262158),
        (b'QmVuqvYLEo76hJVE9c5h9KP2MbQuTxSFyntV22qdz6F1Dr', 262158),
        (b'QmbsEhRqFwKAUoc6ivZyPa1vGUxFKBT4ciH79gVszPcFEG', 262158),
        (b'QmegS44oDgNU2hnD3j8r1WH8xZ2RWfe3Z5eb6aJRHXwJsw', 262158),
        (b'QmbC1ZyGUoxZrmTTjgmiB3KSRRXJFkhpnyKYkiVC6PUMzf', 262158),
        (b'QmZvpEyzP7C8BABesRvpYWPec2HGuzgnTg4VSPiTpQWGpy', 262158),
        (b'QmZhzU2QJF4rUpRSWZxjutWz22CpFELmcNXkGAB1GVb26H', 262158),
        (b'QmZeXvgS1NTxtVv9AeHMpA9oGCRrnVTa9bSCSDgAt52iyT', 262158),
        (b'QmPy1wpe1mACVrXRBtyxriT2T5AffZ1SUkE7xxnAHo4Dvs', 262158),
        (b'QmcHbhgwAVddCyFVigt2DLSg8FGaQ1GLqkyy5M3U5DvTc6', 262158),
        (b'QmNsx32qEiEcHRL1TFcy2bPvwqjHZGp62mbcVa9FUpY9Z5', 262158),
        (b'QmVx2NfXEvHaS8uaRTYaF4ExeLaCSGpTSDhhYBEAembdbk', 69716),
    )
    expected_root_hash = 'QmQgQUbBeMTnH1j3QWwNw9LkXjpWDJrjyGYfZpnPp8x5Lu'
    test = Path(__file__).parent / 'pic.jpg'
    ipfs_multihash = generate_links(test.read_bytes())
    hashes = [(x.Hash, x.Tsize) for x in ipfs_multihash]
    for x in expected_links:
        assert x in hashes
    # test works until here, where it has to calculate the root hash
    root_hash = generate_file_hash(test.read_bytes())
    assert root_hash == expected_root_hash

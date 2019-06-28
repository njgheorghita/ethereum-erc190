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
    pic_expected_links = (
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
    txt_expected_links = (
        (b'QmbYfXF7A7hgXUzEZSifji3D6Nf856kdK8Edu8n7knQSHr', 262158),
        (b'QmZw2JEKQu8n5zisuU7JDAeWSUm2XvqjqV72bizCdDQUDM', 19278),
    )
    pic_expected_root_hash = 'QmQgQUbBeMTnH1j3QWwNw9LkXjpWDJrjyGYfZpnPp8x5Lu'
    txt_exp_hash = 'QmegXsU7EopJ9EVj9ELwgHGE75Xke6FYBP84PaygiAsqB5'
    pic_path = Path(__file__).parent / 'pic.jpg'
    txt_path = Path(__file__).parent / 'txt.txt'
    txt_multihash, txt_blocksizes = generate_links(txt_path.read_bytes())
    pic_multihash, pic_blocksizes = generate_links(pic_path.read_bytes())
    txt_hashes = [(x.Hash, x.Tsize) for x in txt_multihash]
    pic_hashes = [(x.Hash, x.Tsize) for x in pic_multihash]
    for x in txt_expected_links:
        assert x in txt_hashes
    for y in pic_expected_links:
        assert y in pic_hashes
    # test works until here, where it has to calculate the root hash
    txt_root_hash = generate_file_hash(txt_path.read_bytes())
    pic_root_hash = generate_file_hash(pic_path.read_bytes())
    print("txt: actual / expected")
    print(txt_root_hash)
    print(txt_exp_hash)
    print(f'txt blocksizes: count: {len(txt_blocksizes)}, set: {set(txt_blocksizes)}')
    print("pic: actual / expected")
    print(pic_root_hash)
    print(pic_expected_root_hash)
    print(f'pic blocksizes: count: {len(pic_blocksizes)}, set: {set(pic_blocksizes)}')
    assert txt_root_hash == txt_exp_hash	
    assert pic_root_hash == pic_expected_root_hash	

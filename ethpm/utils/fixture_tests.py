import fnmatch
import functools
import hashlib
import json
import os

from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Tuple,
)

from cytoolz import (
    curry,
    identity,
)

from eth_utils import (
  to_tuple
)

from ethpm.typing import MetafuncType


#
# Filesystem fixture loading.
#
@to_tuple
def _recursive_find_files(base_dir: str, pattern: str) -> Generator[str, None, None]:
    for dirpath, _, filenames in os.walk(base_dir):
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                yield os.path.join(dirpath, filename)


def find_fixture_files(fixtures_base_dir: str) -> Generator[str, None, None]:
    all_fixture_paths = _recursive_find_files(fixtures_base_dir, "*.json")
    return all_fixture_paths


@to_tuple
def find_fixtures(fixtures_base_dir: str) -> Generator[Tuple[str, str], None, None]:
    """
    Finds all of the (fixture_path, fixture_key) pairs for a given path under
    the JSON test fixtures directory.
    """
    all_fixture_paths = find_fixture_files(fixtures_base_dir)

    for fixture_path in sorted(all_fixture_paths):
        with open(fixture_path) as fixture_file:
            fixtures = json.load(fixture_file)

        for fixture_key in sorted(fixtures.keys()):
            yield (fixture_path, fixture_key)


# we use an LRU cache on this function so that we can sort the tests such that
# all fixtures from the same file are executed sequentially allowing us to keep
# a small rolling cache of the loaded fixture files.
@functools.lru_cache(maxsize=4)
def load_json_fixture(fixture_path: str) -> Dict[str, Any]:
    """
    Loads a fixture file, caching the most recent files it loaded.
    """
    with open(fixture_path) as fixture_file:
        file_fixtures = json.load(fixture_file)
    return file_fixtures


def load_fixture(fixture_path: str,
                 fixture_key: str,
                 normalize_fn: Callable[[Dict[str, Any]], Dict[str, Any]]=identity
                 ) -> Dict[str, Any]:
    """
    Loads a specific fixture from a fixture file, optionally passing it through
    a normalization function.
    """
    file_fixtures = load_json_fixture(fixture_path)
    fixture = normalize_fn(file_fixtures[fixture_key])
    return fixture


#
# Pytest fixture generation
#
def idfn(fixture_params: List[str]) -> str:
    """
    Function for pytest to produce uniform names for fixtures.
    """
    return ":".join((str(item) for item in fixture_params))


def get_fixtures_file_hash(all_fixture_paths: Generator[str, None, None]) -> str:
    """
    Returns the MD5 hash of the fixture files.  Used for cache busting.
    """
    hasher = hashlib.md5()
    for fixture_path in sorted(all_fixture_paths):
        with open(fixture_path, 'rb') as fixture_file:
            hasher.update(fixture_file.read())
    return hasher.hexdigest()


@curry
def generate_fixture_tests(metafunc: MetafuncType,
                           base_fixture_path: str,
                           filter_fn: Callable[[Any], Any]=identity,
                           preprocess_fn: Callable[[Any], Any]=identity) -> None:
    """
    Helper function for use with `pytest_generate_tests` which will use the
    pytest caching facilities to reduce the load time for fixture tests.
    - `metafunc` is the parameter from `pytest_generate_tests`
    - `base_fixture_path` is the base path that fixture files will be collected from.
    - `filter_fn` handles ignoring or marking the various fixtures.  See `filter_fixtures`.
    - `preprocess_fn` handles any preprocessing that should be done on the raw
       fixtures (such as expanding the statetest fixtures to be multiple tests for
       each fork.
    """
    fixture_namespace = os.path.basename(base_fixture_path)

    if 'fixture_data' in metafunc.fixturenames:
        all_fixture_paths = find_fixture_files(base_fixture_path)
        current_file_hash = get_fixtures_file_hash(all_fixture_paths)

        data_cache_key = 'py-ethpm/fixtures/{0}/data'.format(fixture_namespace)
        file_hash_cache_key = 'py-ethpm/fixtures/{0}/data-hash'.format(fixture_namespace)

        cached_file_hash = metafunc.config.cache.get(file_hash_cache_key, None)
        cached_fixture_data = metafunc.config.cache.get(data_cache_key, None)

        bust_cache = any((
            cached_file_hash is None,
            cached_fixture_data is None,
            cached_file_hash != current_file_hash,
        ))

        if bust_cache:
            all_fixtures = find_fixtures(base_fixture_path)

            metafunc.config.cache.set(data_cache_key, all_fixtures)
            metafunc.config.cache.set(file_hash_cache_key, current_file_hash)
        else:
            all_fixtures = cached_fixture_data

        if not len(all_fixtures):
            raise AssertionError(
                "Suspiciously found zero fixtures: {0}".format(base_fixture_path)
            )

        filtered_fixtures = filter_fn(preprocess_fn(all_fixtures))

        metafunc.parametrize('fixture_data', filtered_fixtures, ids=idfn)


#
# Fixture Normalizers
#
def normalize_ethpmtest_fixture(fixture: Dict[str, Any]) -> Dict[str, Any]:
    normalized_fixture = {
        'in': fixture['in'],
        'out': fixture['out']
    }
    return normalized_fixture

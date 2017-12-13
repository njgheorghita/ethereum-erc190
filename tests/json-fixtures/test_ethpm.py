import pytest

import os

from ethpm.utils.fixture_tests import (
    generate_fixture_tests,
    load_fixture,
    normalize_ethpmtest_fixture,
)

from ethpm.package import (
    Package
)

ROOT_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


BASE_FIXTURE_PATH = os.path.join(ROOT_PROJECT_DIR, 'fixtures', 'EthpmTests')


def pytest_generate_tests(metafunc):
    generate_fixture_tests(
        metafunc=metafunc,
        base_fixture_path=BASE_FIXTURE_PATH,
    )


@pytest.fixture
def fixture(fixture_data):
    print(fixture_data)
    fixture_path, fixture_key = fixture_data
    fixture = load_fixture(
        fixture_path,
        fixture_key,
        normalize_ethpmtest_fixture,
    )
    return fixture


def test_ethpm_fixtures(fixture):
    current_package = Package(fixture['in'])
    expected = fixture['out']
    assert str(current_package.__repr__) == expected['repr']
    assert current_package.package_id == expected['package_identifier']
    assert current_package.name == expected['package_name']
    assert current_package.version == expected['version']
    assert current_package.meta == expected['meta']
    assert current_package.sources == expected['sources']
    assert current_package.build_dependencies == expected['build_dependencies']

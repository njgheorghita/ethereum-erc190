import pytest

from ethpm import Package
from ethpm.exceptions import ValidationError


def test_get_deployments_with_no_match_raises_exception(w3, lockfile_with_no_matching_deployments):
    package = Package(lockfile_with_no_matching_deployments)
    with pytest.raises(ValidationError):
        package.get_deployments(w3)


def test_get_deployments_with_no_deployments_raises_exception(w3, lockfile_with_no_deployments):
    package = Package(lockfile_with_no_deployments)
    with pytest.raises(ValidationError):
        package.get_deployments(w3)


def test_get_deployments_with_a_match_returns_deployments(w3, lockfile_with_matching_deployments):
    package = Package(lockfile_with_matching_deployments)
    deployment = package.get_deployments(w3)
    assert deployment.w3 == w3


def test_get_deployments_with_multiple_matches_raises_exception(w3, lockfile_with_multiple_matches):
    package = Package(lockfile_with_multiple_matches)
    with pytest.raises(ValidationError):
        package.get_deployments(w3)

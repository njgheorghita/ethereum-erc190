import pytest

from ethpm import V2_PACKAGES_DIR
from ethpm.exceptions import ValidationError
from ethpm.utils.manifest_validation import (
    extract_contract_types_from_deployments,
    validate_manifest_against_schema,
    validate_manifest_deployments,
    validate_manifest_exists,
)


def test_validate_manifest_exists_validates():
    assert (
        validate_manifest_exists(str(V2_PACKAGES_DIR / "safe-math-lib" / "1.0.0.json"))
        is None
    )


def test_validate_manifest_exists_invalidates():
    with pytest.raises(ValidationError):
        validate_manifest_exists("DNE")


def test_validate_manifest_against_all_manifest_types(all_manifests):
    assert validate_manifest_against_schema(all_manifests) is None


def test_validate_manifest_invalidates(invalid_manifest):
    with pytest.raises(ValidationError):
        validate_manifest_against_schema(invalid_manifest)


def test_validate_deployed_contracts_present_validates(
    manifest_with_conflicting_deployments
):
    with pytest.raises(ValidationError):
        validate_manifest_deployments(manifest_with_conflicting_deployments)


def test_validate_deployments(manifest_with_matching_deployment, w3):
    validate = validate_manifest_deployments(manifest_with_matching_deployment)
    assert validate is None


def test_validate_deployed_contracts_pr(manifest_with_no_deployments):
    validate = validate_manifest_deployments(manifest_with_no_deployments)
    assert validate is None


@pytest.mark.parametrize(
    "data,expected",
    (
        ({}, set()),
        ([{"some": {"contract_type": "one"}}], set(["one"])),
        (
            [{"some": {"contract_type": "one"}, "other": {"contract_type": "two"}}],
            set(["one", "two"]),
        ),
    ),
)
def test_extract_contract_types_from_deployments(data, expected):
    actual = extract_contract_types_from_deployments(data)
    assert actual == expected

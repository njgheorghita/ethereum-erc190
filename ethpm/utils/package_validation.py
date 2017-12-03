import json
import os

from ethpm import ASSETS_DIR
from ethpm.exceptions import ValidationError

from jsonschema import (
    validate,
    ValidationError as jsonValidationError
)

RELEASE_LOCKFILE_SCHEMA_PATH = os.path.join(ASSETS_DIR, 'release-lockfile.schema.v1.json')


def load_package_data(package_id):
    """
    Load package json located in ASSETS_DIR.
    """
    with open(os.path.join(ASSETS_DIR, package_id)) as package:
        return json.load(package)


def _load_schema_data():
    with open(RELEASE_LOCKFILE_SCHEMA_PATH) as schema:
        return json.load(schema)


def validate_package_against_schema(package_data):
    """
    Load and validate package json against schema
    located at RELEASE_LOCKFILE_SCHEMA_PATH.
    """
    schema_data = _load_schema_data()
    try:
        validate(package_data, schema_data)
    except jsonValidationError:
        raise ValidationError(
            "Package:{0} invalid for schema:{1}".format(0, RELEASE_LOCKFILE_SCHEMA_PATH)
        )


def validate_package_deployments(package_data):
    """
    Validate that a package's deployments contracts reference existing contract_types.
    """
    if set(("contract_types", "deployments")).issubset(package_data):
        all_contract_types = list(package_data["contract_types"].keys())

        deployments = [
            deployment
            for uri, deployment
            in package_data["deployments"].items()
        ]
        deployment_names = [
            name
            for name, value
            in deployments[0].items()
        ]

        if not deployment_names == all_contract_types:
            raise ValidationError(
                "Deployments:{0} do not reference existing contract types.".format(deployment_names)
            )


def validate_package_exists(package_id):
    """
    Validate that package with package_id exists in ASSSETS_DIR
    """
    package_path = os.path.join(ASSETS_DIR, package_id)
    if not os.path.exists(package_path):
        raise ValidationError("Package not found in ASSETS_DIR with id: {0}".format(package_id))

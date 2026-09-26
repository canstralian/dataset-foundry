"""Package-level contract tests for the Dataset Foundry scaffold."""

from importlib.metadata import version

import dataset_foundry


def test_package_is_importable_with_distribution_metadata() -> None:
    """The editable install must expose both the package and distribution metadata."""
    if dataset_foundry.__package__ != "dataset_foundry":
        raise AssertionError("dataset_foundry package identity is not importable as expected")
    if not version("dataset-foundry"):
        raise AssertionError("dataset-foundry distribution metadata is missing a version")

"""Package-level contract tests for the Dataset Foundry scaffold."""

from importlib.metadata import version

import dataset_foundry


def test_package_is_importable_with_distribution_metadata() -> None:
    """Editable install must expose package and distribution metadata."""
    if dataset_foundry.__package__ != "dataset_foundry":
        raise AssertionError("unexpected package identity")
    if not version("dataset-foundry"):
        raise AssertionError("missing distribution version")

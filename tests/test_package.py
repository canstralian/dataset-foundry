"""Package-level contract tests for the Dataset Foundry scaffold."""

from importlib.metadata import version

import dataset_foundry


def test_package_is_importable_with_distribution_metadata() -> None:
    """The editable install must expose both the package and distribution metadata."""
    assert dataset_foundry.__package__ == "dataset_foundry"
    assert version("dataset-foundry")

"""Self-contained unit tests for the algorithms package.

These inspect only this repo's own files and packaging metadata - no schema,
no LinkML, no bilayers pipeline. Schema-compliance and end-to-end generation
are integration concerns and live in the bilayers repo.

  Group 1 - packaging / discoverability (config.yaml ships as package data)
  Group 2 - config.yaml well-formedness
  Group 3 - internal consistency (repo-owned invariants, not schema rules)
"""

from importlib.resources import files

import pytest
import yaml

PKG = "bilayers_algorithms"


def algorithm_names() -> list:
    """Every algorithm subpackage (a directory with an __init__.py)."""
    root = files(PKG)
    return sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_dir()
        and entry.name != "__pycache__"
        and entry.joinpath("__init__.py").is_file()
    )


ALGORITHMS = algorithm_names()


def load_config(name: str) -> dict:
    return yaml.safe_load(files(PKG).joinpath(name).joinpath("config.yaml").read_text())


def test_algorithms_discovered() -> None:
    # Guards against the parametrized tests silently collecting nothing.
    assert ALGORITHMS, "no algorithm subpackages discovered under bilayers_algorithms"


# --- Group 1: packaging / discoverability -------------------------------------


def test_package_imports() -> None:
    import bilayers_algorithms  # noqa: F401


@pytest.mark.parametrize("name", ALGORITHMS)
def test_config_ships_as_package_data(name: str) -> None:
    cfg = files(PKG).joinpath(name).joinpath("config.yaml")
    assert cfg.is_file(), (
        f"{name}/config.yaml is not present as package data - check the "
        "[tool.setuptools.package-data] globs; bilayers reads these via importlib.resources."
    )


# --- Group 2: well-formedness -------------------------------------------------


@pytest.mark.parametrize("name", ALGORITHMS)
def test_config_parses_to_non_empty_mapping(name: str) -> None:
    cfg = load_config(name)
    assert isinstance(cfg, dict) and cfg, f"{name}/config.yaml is not a non-empty YAML mapping"


# --- Group 3: internal consistency --------------------------------------------


@pytest.mark.parametrize("name", ALGORITHMS)
def test_algorithm_folder_name_matches_dir(name: str) -> None:
    cfg = load_config(name)
    declared = cfg.get("algorithm_folder_name")
    assert declared == name, (
        f"{name}/config.yaml: algorithm_folder_name={declared!r} does not match folder {name!r}"
    )


@pytest.mark.parametrize("name", ALGORITHMS)
def test_names_unique_within_each_section(name: str) -> None:
    cfg = load_config(name)
    for section in ("inputs", "outputs", "parameters"):
        items = cfg.get(section) or []
        names = [item.get("name") for item in items if isinstance(item, dict)]
        dupes = sorted({n for n in names if names.count(n) > 1})
        assert not dupes, f"{name}/config.yaml: duplicate {section} names: {dupes}"

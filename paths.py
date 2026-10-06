# =================================================
# Defines all folder paths used for the project
# =================================================

from pathlib import Path


# paths.py is stored in the project root,
# so the directory containing this file is the root.
PROJECT_ROOT = Path(__file__).resolve().parent


def project_root():
    """Return the root directory of the project."""
    return PROJECT_ROOT


def data_path(*parts):
    """Return a path inside the Data folder."""
    return PROJECT_ROOT / "Data" / Path(*parts)


def code_path(*parts):
    """Return a path inside the Code folder."""
    return PROJECT_ROOT / "Code" / Path(*parts)


def out_path(*parts):
    """Return a path inside the out folder."""
    return PROJECT_ROOT / "out" / Path(*parts)
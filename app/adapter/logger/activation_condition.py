"""
Module to determine if a file is in the site-packages directory.
Usage: not initiate the logger if the file is in the site-packages directory.

:author: Alex Traveylan
:date: 2024
"""

from pathlib import Path


def is_on_site_packages(actual_file_path: str | Path) -> bool:
    """
    This function checks if the file is in the site-packages directory.

    Parameters
    ----------
    actual_file_path : str | Path
        Path to the file to check.

    Returns
    -------
    bool
        True if the file is in the site-packages directory, False otherwise.
    """
    absolute_file_path = Path(actual_file_path).resolve()

    is_lib_in_path = "Lib" in str(absolute_file_path)
    is_site_packages_in_path = "site-packages" in str(absolute_file_path)

    return is_lib_in_path and is_site_packages_in_path

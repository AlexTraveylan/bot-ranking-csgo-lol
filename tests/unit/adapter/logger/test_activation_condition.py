"""
Tests for the file adapter/logger/activation_condition.py

:author: Alex Traveylan
:date: 2024
"""

from app.adapter.logger.activation_condition import is_on_site_packages


def test_is_on_site_packages_when_file_in_site_packages():
    """
    Test that is_on_site_packages returns True when the file is in the site-packages directory.
    """

    # When
    file_path = "/path/to/Lib/site-packages/file.py"

    # Then
    result = is_on_site_packages(file_path)

    # Expected
    excepted_result = True

    # Assert
    assert result is excepted_result


def test_is_on_site_packages_when_file_not_in_site_packages():
    """
    Test that is_on_site_packages returns False when the file
    is not in the site-packages directory.
    """

    # When
    file_path = "/path/to/other-directory/file.py"

    # Then
    result = is_on_site_packages(file_path)

    # Expected
    excepted_result = False

    # Assert
    assert result is excepted_result

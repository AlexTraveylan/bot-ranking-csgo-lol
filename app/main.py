"""
Main module for the application
"""

from atexit import register


def main():
    """Entry point for the application."""

    pass


@register
def exit_function():
    """Auto execute when application end"""

    pass


if __name__ == "__main__":
    main()

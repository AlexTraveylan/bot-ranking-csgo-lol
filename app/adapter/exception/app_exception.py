"""
Module for the AppException class

:author: Alex Traveylan
:date: 2024
"""


class AppException(Exception):
    """
    Exception class for the application

    Attributes
    ----------
    message : str
        The message of the exception
    """

    def __init__(self, message: str):
        """
        Constructor for AppException

        Parameters
        ----------
        message : str
            The message of the exception
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

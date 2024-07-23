"""
Test the AppException class

:author: Alex Traveylan
:date: 2024
"""

from app.adapter.exception.bot_exception import BotException


def test_bot_exception():
    """Test the BotException class."""

    message = "Test exception message"
    exception = BotException(message)

    assert str(exception) == message

"""Base exception class

Base exceptions class that takes n args and render default message error
"""


class BaseAudioException(Exception):
    """Exception raised for error manipulating audio

        :param message_args: arguments to render error message
        :param message: explanation of the error
    """
    def __init__(self, default_message, *message_args, message: str = None):
        self.message = message
        self.message_args = message_args
        self.default_message = default_message
        super().__init__()

    def __str__(self):
        if self.message is None and self.default_message is not None:
            return self.default_message % self.message_args
        return self.message

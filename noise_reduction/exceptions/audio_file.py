"""Exceptions related to audio file manipulation"""
from noise_reduction.exceptions.base_exception import BaseAudioException


class SaveTempFileException(BaseAudioException):
    """Exception raised for error trying to save temporary file

    :param tuple `*message_args`: arguments to render error message
    :param str message: explanation of the error
    """
    def __init__(self, *message_args, message: str = None):
        self.message_args = message_args
        self.message = message
        self.default_message = 'Error while saving temporary file %s'
        super().__init__(self.default_message, *message_args, message=message)


class DeleteTempFileException(BaseAudioException):
    """Exception raised for error trying to delete temporary file

        :param tuple message_args: arguments to render error message
        :param str message: explanation of the error
    """

    def __init__(self, *message_args, message: str = None):
        self.message_args = message_args
        self.message = message
        self.default_message = 'Error while deleting temporary file %s'
        super().__init__(self.default_message, *message_args, message=message)

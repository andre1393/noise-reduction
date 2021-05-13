"""Exceptions related to audio processing"""

from noise_reduction.exceptions.base_exception import BaseAudioException


class AudioProcessingException(BaseAudioException):
    """ Exception raised for error processing audio

        :param message_args: arguments to render error message
        :param message: explanation of the error
    """
    def __init__(self, *message_args, message: str = None):
        self.message_args = message_args
        self.message = message
        self.default_message = 'Error processing audio'
        super().__init__(self.default_message, *message_args, message=message)

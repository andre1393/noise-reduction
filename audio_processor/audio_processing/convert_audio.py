"""Module with functions to convert audio"""
import logging
import ffmpeg

logger = logging.getLogger()


def to_one_channel(file: str, rate: int) -> str:
    """Convert audio to one channel

    :param file: audio file
    :param rate: audio rate
    :return: audio converted file name
    """
    try:
        converted_file = f'{file.replace(".wav", "_converted.wav")}'

        ffmpeg \
            .input(file) \
            .output(converted_file, ac=1, ar=rate) \
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        return converted_file
    except ffmpeg.Error as err:
        logger.warning('stdout: %s', err.stdout.decode('utf8'))
        logger.warning('stderr: %s', err.stderr.decode('utf8'))
        raise err

"""Module with functions to extract audio information"""
import logging
import crepe

from noise_reduction.exceptions.audio_processing import AudioProcessingException

logger = logging.getLogger('gunicorn.error.noise')


async def get_metadata(rate, data) -> tuple:
    """Process audio

    process audio using crepe algorithm

    :param rate: audio rate
    :param data: audio data
    :returns:
        - time - [shape=(T,)] The timestamps on which the pitch was estimated
        - frequency - [shape=(T,)] The predicted pitch values in Hz
        - confidence - [shape=(T,)] The confidence of voice activity, between 0 and 1
        - activation - [shape=(T, 360)] The raw activation matrix
    :rtype: tuple
    """
    try:
        logger.info('start crepe algorithm')
        time, frequency, confidence, activation = crepe.predict(
            data, rate, viterbi=True, step_size=10
        )
        logger.info('crepe algorithm finished')
        return time, frequency, confidence, activation
    except Exception as err:
        raise AudioProcessingException() from err

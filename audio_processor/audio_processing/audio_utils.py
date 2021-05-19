"""Audio utils functions"""
import tempfile
from tempfile import SpooledTemporaryFile
import shutil

import librosa

from audio_processor.exceptions.audio_file import SaveTempFileException
from audio_processor.utils import normalized_frequencies, count_value_frequency


def open_audio(file: str):
    """Open audio file

        :param str file: audio file path
        :return: audio rate and audio data
        :rtype: tuple
    """
    data, rate = librosa.load(file)
    return rate, data


def save_file(file: SpooledTemporaryFile, filename: str, delete=False) -> tuple:
    """Save received audio into a temporary file

        :param SpooledTemporaryFile file: audio file received from form
        :param str filename: audio file name
        :param bool delete: delete file after creating
        :return: temp dir and created file name
    """
    try:
        tmp_dir = tempfile.mkdtemp()
        with tempfile.NamedTemporaryFile(
                mode='wb', suffix=f'audio_{filename}', delete=delete, dir=tmp_dir
        ) as buffer:
            shutil.copyfileobj(file, buffer)
            return tmp_dir, buffer.name
    except Exception as err:
        raise SaveTempFileException(filename) from err


def normalize_frequency(freq: float, freq_ref: list) -> float:
    """Normalize note frequency
    Given a frequency, normalize to fit one of the known musical notes

    :param float freq: note frequency
    :param dict freq_ref: list of standard frequencies
    :returns: normalized note
    :rtype: float
    """
    return min(freq_ref, key=lambda list_value: abs(list_value - freq))


def get_modal_note(frequency: list, top: int = 10):
    """Get list of most frequent frequency

    :param list frequency: list of frequencies over time
    :param int top: return n most frequent frequencies
    :return: dict with most frequent frequencies
    """
    return count_value_frequency(
        list(
            map(
                lambda f: normalize_frequency(
                    f,
                    list(normalized_frequencies.values())
                ),
                frequency
            )
        )
    )[:top]

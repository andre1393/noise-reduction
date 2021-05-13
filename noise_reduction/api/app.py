"""API receives and processes audio files"""

import logging
import tempfile
import shutil
from tempfile import SpooledTemporaryFile

from fastapi import FastAPI, File, UploadFile
import crepe
from scipy.io import wavfile

from noise_reduction.utils import normalized_frequencies
from noise_reduction.exceptions.audio_file import SaveTempFileException
from noise_reduction.exceptions.audio_processing import AudioProcessingException

app = FastAPI()

logger = logging.getLogger("gunicorn.error.noise")
logger.setLevel('INFO')


@app.get('/health', status_code=200)
def health_check():
    """API health check
        :return dict: application status OK
    """
    return {'status': 'OK'}


@app.post('/process-audio')
async def process_audio(audio_file: UploadFile = File(...)):
    """Given an audio, process and return the most frequent note
            :param UploadFile audio_file: audio file in WAV format
            :return: dictionary containing the most frequent note
    """
    try:
        audio_temp_file = save_file(audio_file.file)
        time, frequency, _, _ = extract_audio_metadata(audio_temp_file)
        return {
            'status': 'OK',
            'filename': audio_file.filename,
            'tmp': audio_temp_file,
            'audio_length': len(time),
            'frequencies': count_note_frequency(
                list(map(lambda f: normalize_frequency(
                    f,
                    list(normalized_frequencies.values())),
                    frequency
                )))
        }
    except (SaveTempFileException, AudioProcessingException) as err:
        logger.exception(err)
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}
    except Exception as err:
        logger.exception('unknown error:')
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}


def save_file(file: SpooledTemporaryFile, delete=False) -> str:
    """Save received audio into a temporary file

        :param SpooledTemporaryFile file: audio file received from form
        :param bool delete: delete file after creating
        :return: created file name
        :rtype: str
    """
    try:
        with tempfile.NamedTemporaryFile(
                mode='wb', suffix=f'audio_{file.name}', delete=delete
        ) as buffer:
            shutil.copyfileobj(file, buffer)
            return buffer.name
    except Exception as err:
        raise SaveTempFileException(file.name) from err


def extract_audio_metadata(audio_file_path: str) -> tuple:
    """Process audio

    Open wav file and process using crepe algorithm

    :param str audio_file_path: audio file path
    :returns:
        - time - [shape=(T,)] The timestamps on which the pitch was estimated
        - frequency - [shape=(T,)] The predicted pitch values in Hz
        - confidence - [shape=(T,)] The confidence of voice activity, between 0 and 1
        - activation - [shape=(T, 360)] The raw activation matrix
    :rtype: tuple
    """
    try:
        rate, data = wavfile.read(audio_file_path)
        return crepe.predict(
            data, rate, viterbi=True, step_size=10
        )
    except Exception as err:
        raise AudioProcessingException() from err


def count_note_frequency(arr: list) -> dict:
    """
    Given an array of floats, creates a dictionary
    where the keys are the unique values and the values are frequencies
        :param list arr: list array of floats
        :returns: dictionary with values frequencies
        :rtype: dict
    """
    frequency_dict = {}
    for item in arr:
        if item in frequency_dict:
            frequency_dict[item] += 1
        else:
            frequency_dict[item] = 1
    return dict(sorted(frequency_dict.items(), key=lambda i: i[1], reverse=True))


def normalize_frequency(freq: float, freq_ref: list) -> float:
    """Normalize note frequency
    Given a note frequency normalize to fit one of the known musical notes

    :param float freq: note frequency
    :param dict freq_ref: list of standard frequencies
    :returns: normalized note
    :rtype: float
    """
    return min(freq_ref, key=lambda list_value: abs(list_value - freq))

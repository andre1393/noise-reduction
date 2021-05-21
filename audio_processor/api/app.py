"""API receives and processes audio files"""

import os
import logging

from fastapi import FastAPI, File, UploadFile

from audio_processor.exceptions.audio_file import SaveTempFileException
from audio_processor.exceptions.audio_processing import AudioProcessingException
from audio_processor.audio_processing.enhance_audio import denoise
from audio_processor.audio_processing.audio_utils import save_file, open_audio, get_modal_note
from audio_processor.audio_processing.extract_audio_info import get_metadata

app = FastAPI()

logger = logging.getLogger("gunicorn.error.noise")
logger.setLevel('INFO')


@app.get('/health', status_code=200)
def health_check():
    """API health check
        :return dict: application status OK
    """
    return {'status': 'OK'}


@app.post('/process')
async def process_audio(audio_file: UploadFile = File(...), convert_audio: bool = File(...)):
    """Given an audio, process and return the most frequent note
            :param UploadFile audio_file: audio file in WAV format
            :param bool convert_audio: whether it should convert audio to one channel
            :return: dictionary containing the most frequent note
    """
    try:
        tmp_dir, audio_temp_file_name = save_file(audio_file.file, audio_file.filename)

        audio_temp_file = os.path.join(tmp_dir, audio_temp_file_name)

        rate, data = open_audio(audio_temp_file)

        await denoise(tmp_dir, audio_temp_file_name, rate, convert_audio=convert_audio)

        time, frequency, _, _ = await get_metadata(rate, data)

        return {
            'status': 'OK',
            'filename': audio_file.filename,
            'tmp': audio_temp_file,
            'audio_length': len(time),
            'frequencies': get_modal_note(frequency)
        }
    except (SaveTempFileException, AudioProcessingException) as err:
        logger.exception(err)
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}
    except Exception as err:
        logger.exception('unknown error:')
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}

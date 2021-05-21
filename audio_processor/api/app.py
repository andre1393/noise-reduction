"""API receives and processes audio files"""
import logging

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from audio_processor.exceptions.audio_file import SaveTempFileException
from audio_processor.exceptions.audio_processing import AudioProcessingException
from audio_processor.audio_processing.enhance_audio import denoise
from audio_processor.audio_processing.audio_utils import get_modal_note
from audio_processor.audio_processing.extract_audio_info import get_metadata
from audio_processor.audio_processing.audio_utils import prepare_audio

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
        tmp_dir, audio_temp_file_name, _, rate, data = prepare_audio(audio_file.file, audio_file.filename)
        enhanced_audio = await denoise(tmp_dir, audio_temp_file_name, rate, convert_audio=convert_audio)
        time, frequency, _, _ = await get_metadata(rate, data)
        return FileResponse(enhanced_audio,
                            media_type='audio/wav',
                            headers={'frequencies': str(get_modal_note(frequency))}
                            )
    except (SaveTempFileException, AudioProcessingException) as err:
        logger.exception(err)
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}
    except Exception as err:
        logger.exception('unknown error:')
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}


@app.post('/denoise')
async def denoise_audio(audio_file: UploadFile = File(...), convert_audio: bool = File(...)):
    """Given an audio, process and return the most frequent note
            :param UploadFile audio_file: audio file in WAV format
            :param bool convert_audio: whether it should convert audio to one channel
            :return: dictionary containing the most frequent note
    """
    try:
        tmp_dir, audio_temp_file_name, _, rate, data = prepare_audio(audio_file.file, audio_file.filename)
        enhanced_audio = await denoise(tmp_dir, audio_temp_file_name, rate, convert_audio=convert_audio)
        return FileResponse(enhanced_audio, media_type='audio/wav')
    except (SaveTempFileException, AudioProcessingException) as err:
        logger.exception(err)
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}
    except Exception as err:
        logger.exception('unknown error:')
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}


@app.post('/modal-frequencies')
async def process_audio(audio_file: UploadFile = File(...)):
    """Given an audio, process and return the most frequent note
            :param UploadFile audio_file: audio file in WAV format
            :return: dictionary containing the most frequent note
    """
    try:
        _, _, _, rate, data = prepare_audio(audio_file.file, audio_file.filename)
        time, frequency, _, _ = await get_metadata(rate, data)
        return {'frequencies': get_modal_note(frequency)}
    except (SaveTempFileException, AudioProcessingException) as err:
        logger.exception(err)
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}
    except Exception as err:
        logger.exception('unknown error:')
        return {'status': 'ERROR', 'filename': audio_file.filename, 'error': str(err)}

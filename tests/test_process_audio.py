import pytest

from noise_reduction.api.app import process_audio
from fastapi import UploadFile


@pytest.mark.asyncio
async def test_process_audio(crepe_predict_mock, wavfile_read_mock, save_file_mock):
    file = UploadFile('test_file.wav')
    result = await process_audio(file)

    crepe_predict_mock.assert_called_once_with(None, None, viterbi=True, step_size=10)
    wavfile_read_mock.assert_called_once_with('/tmp/test_file.wav')
    save_file_mock.assert_called_once_with(file.file)

    assert result['status'] == 'OK'
    assert result['filename'] == 'test_file.wav'
    assert result['tmp'] == '/tmp/test_file.wav'
    assert result['audio_length'] == 3
    assert result['frequencies'] == {18.354046: 2, 19.445435: 1}

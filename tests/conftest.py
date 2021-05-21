import pytest
from types import SimpleNamespace
import audio_processor


@pytest.fixture
def crepe_predict_mock(mocker):
    return mocker.patch('crepe.predict', return_value=([0.1, 0.2, 0.3], [18., 20., 18.], None, None))


@pytest.fixture
def wavfile_read_mock(mocker):
    return mocker.patch('librosa.load', return_value=(None, None))


@pytest.fixture
def ffmpeg_run_mock(mocker):
    return mocker.patch('ffmpeg.run')


@pytest.fixture
def enhance_mock(mocker):
    return mocker.patch('denoiser.enhance.enhance')


@pytest.fixture
def save_file_mock(mocker):
    from audio_processor.audio_processing.audio_utils import save_file
    mock = mocker.patch('audio_processor.audio_processing.audio_utils.save_file', return_value=('/tmp', '/tmp/test.wav'))
    import pdb; pdb.set_trace()
    return mock
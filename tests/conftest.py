import pytest


@pytest.fixture
def crepe_predict_mock(mocker):
    return mocker.patch('crepe.predict', return_value=([0.1, 0.2, 0.3], [18., 20., 18.], None, None))


@pytest.fixture
def wavfile_read_mock(mocker):
    return mocker.patch('scipy.io.wavfile.read', return_value=(None, None))


@pytest.fixture
def save_file_mock(mocker):
    return mocker.patch('noise_reduction.api.app.save_file', return_value='/tmp/test_file.wav')

import os
from tempfile import SpooledTemporaryFile

from audio_processor.audio_processing.audio_utils import save_file


def test_save_file():
    file = SpooledTemporaryFile()
    _, saved_file = save_file(file, file.name)
    assert os.path.exists(saved_file)

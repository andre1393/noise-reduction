import os
from tempfile import SpooledTemporaryFile

from noise_reduction.api.app import save_file


def test_save_file():
    file = SpooledTemporaryFile()
    saved_file = save_file(file)
    assert os.path.exists(saved_file)

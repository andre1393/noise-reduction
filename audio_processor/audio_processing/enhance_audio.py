"""Module with functions to enhance audio"""
from types import SimpleNamespace
import os
import logging

from denoiser import enhance
from audio_processor.audio_processing.convert_audio import to_one_channel

logger = logging.getLogger('gunicorn.error.noise')


async def denoise(tmp_dir: str, file: str, rate: int, convert_audio: bool) -> str:
    """remove audio noisy

    :param tmp_dir: temporary directory containing audio file
    :param file: audio file
    :param rate: audio rate
    :param convert_audio: should convert audio before denoising
    :return: enhanced audio file name
    """
    logger.info('starting denoise')
    if convert_audio:
        file = to_one_channel(file, rate)

    noisy_json = os.path.join(tmp_dir, 'noisy.json')
    with open(noisy_json, 'w+') as buffer:
        buffer.write(f'[["{file}", {os.path.getsize(file)}]]')

    args = get_enhance_args(tmp_dir, noisy_json, rate)
    enhance.enhance(args)
    logger.info('denoise complete')
    return file.replace('.wav', '_enhanced.wav')


def get_enhance_args(tmp_dir: str, noisy_json: str, sample_rate: int) -> SimpleNamespace:
    """get arguments to use in denoiser algorithm

    :param tmp_dir: temporary directory containing audio file
    :param noisy_json: noisy_json file name
    :param sample_rate: audio rate
    :return: arguments of denoiser algorithm
    """
    return SimpleNamespace(
        noisy_dir=None,
        batch_size=2,
        device='cpu',
        dns48=False,
        dns64=False,
        dry=0,
        master64=False,
        model_path=None,
        noisy_json=noisy_json,
        num_workers=1,
        out_dir=tmp_dir,
        sample_rate=sample_rate,
        streaming=False,
        verbose=20
    )

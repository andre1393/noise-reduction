from audio_processor.api.app import normalize_frequency


def test_normalize_frequency():
    normalized_frequency = normalize_frequency(10.0, [8.0, 11., 12.])
    assert normalized_frequency == 11.

from audio_processor.audio_processing.audio_utils import count_value_frequency


def test_count_note_frequency():
    note_counts = count_value_frequency([10., 11., 10.])
    assert note_counts == {10.: 2, 11.: 1}

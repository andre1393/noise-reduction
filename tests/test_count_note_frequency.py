from audio_processor.api.app import count_note_frequency


def test_count_note_frequency():
    note_counts = count_note_frequency([10., 11., 10.])
    assert note_counts == {10.: 2, 11.: 1}

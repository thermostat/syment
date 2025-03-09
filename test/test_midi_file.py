
import syment.midi_file

import os

def test_midi_file():
    mf = syment.midi_file.MidiFile('test_data/HALLS.MID')
    mf.load()

    assert mf.track_count() == 2

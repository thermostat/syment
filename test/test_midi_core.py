
import syment.midi_core


def test_pitch():
    n = syment.midi_core.Pitch.value_to_name(60)
    assert n == "C4"
    v = syment.midi_core.Pitch.name_to_value("C4")
    assert v == 60

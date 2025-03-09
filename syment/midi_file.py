#!/bin/env python3

"""
midi_file - General Midi File object model
"""

from syment import midi_core
from syment.midi_core import Pitch, Note
import mido

class MidiFile:
    def __init__(self, filename):
        self._filename = filename
        self._mido_file = mido.MidiFile(filename)
        self._tracks : list[MidiTrack] = []
        self._midi_file_type = self._mido_file.type

    def load(self):
        for t in self._mido_file.tracks:
            mt = MidiTrack(t)
            self._tracks.append(mt)

    def tracks(self):
        return iter(self._tracks)

    def track_count(self):
        return len(self._tracks)

class MidiTrack:
    def __init__(self, mido_track):
        self._mido_track = mido_track
        self._meta = []
        self._notes = []
        self._cc = []
        self.name = self._mido_track.name
        self._parse()

    def _parse(self):
        concurrent_notes = {}
        max_polyphony = 0
        abstime = 0
        # NB, this assumes one channel per track
        for message in self._mido_track:
            # first update abs time
            abstime += message.time
            if message.is_meta or message.is_cc():
                self._meta.append(message)
            elif message.type == 'note_on':
                concurrent_notes[message.note] = (message, abstime)
                if len(concurrent_notes) > max_polyphony:
                    max_polyphony=len(concurrent_notes)
            elif message.type == 'note_off':
                start,stime = concurrent_notes[message.note]
                note = midi_core.Note(Pitch(value=message.note),
                                      stime, abstime,
                                      vel=start.velocity,
                                      channel=start.channel)
                self._notes.append(note)
                del concurrent_notes[message.note]
            elif message.type == 'program_change':
                self._meta.append(message)
            else:
                # Warn
                print(f"Warning, unknown message, {message.type}")
        self._max_polyphony = max_polyphony

class MidiTime:
    def __init__(self, ticks, timesigdict=None):
        self._ticks = ticks
        self._timesigdict = timesigdict
        self._clocks_per_click = self._timesigdict['clocks_per_click']

    def measure(self):
        return self._ticks // (self._cocks_per_click *
                               self._timesigdict['numerator'])

    def quarter(self):
        return self._ticks // (self._cocks_per_click)

    def sixteenth(self):
        return self._ticks // (self._cocks_per_click//2)

    def __str__(self):
        return self._ticks


###########################################################################
# Debug
###########################################################################

def debug_typestrn(lst):
    typeset = set()
    for x in lst:
        typeset.add(x.dict()['type'])
        if x.dict()['type'] == "program_change":
            print (str(x.dict())+":"+x.hex())
    return "{"+','.join([str(t) for t in typeset])+"}"


def debug_print_file_details(fname):
    mf = mido.MidiFile(fname)
    print(f"File {fname}")
    print(f"  {len(mf.tracks)} tracks")
    print(f"  General Midi file type {mf.type}")
    print(f"  Division {mf.ticks_per_beat}")
    print("Tracks:")
    for i,t in enumerate(mf.tracks):
        s = debug_typestrn(t)
        print(f" [{i}] : {t.name} {len(t)} messages, {s}")
    return mf

def debug_print_track_details(mf, tracknbr):
    for m in mf.tracks[tracknbr]:
        print(m.dict())
    


#!/bin/env python3

"""
midi_file - General Midi File object model
"""

from syment import midi_core
import mido

class MidiFile:
    def __init__(self, filename):
        self._filename = filename
        self._mido_file = mido.MidiFile(filename)


class MidiTrack:
    def __init__(self, mido_track):
        self._mido_track = mido_track
        self.name = None 

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
    


#!/bin/env python

"""
syment.midi_core - Core midi functionality
"""

import mido

from typing import Optional

PITCH_OFFSETS = {
    "C"  : 0,
    "C#" : 1,
    "Db" : 1,
    "D"  : 2,
    "D#" : 3,
    "Eb" : 3,
    "E"  : 4,
    "F"  : 5,
    "F#" : 6,
    "Gb" : 6,
    "G"  : 7,
    "G#" : 8,
    "Ab" : 8,
    "A"  : 9,
    "A#" :10,
    "Bb" :10,
    "B"  :11
    }

VALUE_NAMES = [
    "C",  "C#", "D", "Eb", "E", "F",
    "F#", "G", "Ab", "A", "Bb", "B"
    ]

class Pitch:
    """ 
   Pitch value in notation and MIDI value format

    C4 = 60 
    """
    @staticmethod
    def name_to_value(name: str) -> int:
        scale = int(name[-1])+1
        pitch = PITCH_OFFSETS[name[:-1]]
        return (scale*12)+pitch

    @staticmethod
    def value_to_name(value: int) -> str:
        if value < 12 or value > 110:
            raise ValueError
        scale = (value // 12)-1
        pitch = VALUE_NAMES[value%12]
        return f"{pitch}{scale}"
    
    def __init__(self,
                 name:Optional[str]=None,
                 value:Optional[int]=None):
        self._name = name
        self._value = value
        if self._name != None and self._value == None:
            self._value = Pitch.name_to_value(self._name)
        elif self._name == None and self._value != None:
            self._name = Pitch.value_to_name(self._value)

    def __str__(self):
        return self._name

    def __int__(self):
        return self._value

    def note_value(self):
        return self._value
    
    def hex(self):
        return hex(self.value)


class Note:
    """
    A note consists of a pitch with a start, end, velocity and 
    channel.
    """
    def __init__(self,
                 pitch: Pitch,
                 starttime: int,
                 endtime: int,
                 vel:int=127,
                 channel:int=0):
        self._pitch = pitch
        self._starttime = starttime
        self._endtime = endtime
        self._velocity = vel
        self._channel = channel


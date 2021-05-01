import sys
import os
import glob
import numbers

def check_or_create_folder(name):
    if os.path.isdir(name):
        return
    os.makedirs(name + "/")

def transpose_to_octave(pitch_or_pitches, octave):
    if isinstance(pitch_or_pitches, numbers.Number):
        return (octave)*12 + pitch_or_pitches
    elif isinstance(pitch_or_pitches, list):
        return [(octave)*12 + p for p in pitch_or_pitches]
    
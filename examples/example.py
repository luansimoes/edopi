from edopi import TonalSystem, Scale, transpose_to_octave
from scamp import Session
import random as rd

z = TonalSystem(20)
z.set_generator(11)
diatonic = z.diatonic_scale()
midi_classes = diatonic.get_elements() #[0, 2, 4, 6, 8, 9, 11, 13, 15, 17, 19]

midi_pitches = diatonic.midi_pitch_classes #[0, 0.6, 1.2, 1.8, 2.4, 3.0, ..., 11.4]

central_note = 100

microtonal_melody_1 = [rd.choice(midi_classes) for _ in range(24)]
microtonal_melody_2 = [rd.choice(midi_pitches) for _ in range(24)]
microtonal_melody_3 = [diatonic.next(central_note, rd.randint(-5, 5)) for _ in range(24)]

print([z.midi_pitch(e) for e in microtonal_melody_3])

#SCAMP
s = Session()
p = s.new_part('piano')
s.start_transcribing()
for pc in microtonal_melody_1:
    p.play_note(z.midi_pitch(pc, 4), 0.8, 1/3)

for pc in microtonal_melody_2:
    p.play_note(transpose_to_octave(pc, 2), 0.8, 1/3)

for pitch in microtonal_melody_3:
    p.play_note(z.midi_pitch(pitch), 0.8, 1/3)
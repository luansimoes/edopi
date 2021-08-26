from edopi import TonalSystem
from scamp import Session

z = TonalSystem(20, 11)
diatonic = z.diatonic_scale()

central_note = 100
smooth_melody_1 = diatonic.smooth_line(central_note, (80, 120), 24)
smooth_melody_2 = diatonic.smooth_line(central_note, (80, 120), 24)
composite_melody = diatonic.composite_line([smooth_melody_1, smooth_melody_2], 24)

print([e for e in smooth_melody_1])
print([e for e in smooth_melody_2])
print([e for e in composite_melody])

#SCAMP
s = Session()
p = s.new_part('piano')
s.start_transcribing()
for pitch in smooth_melody_1:
    p.play_note(z.midi_pitch(pitch), 0.8, 1/3)

s.wait(1)

for pitch in smooth_melody_2:
    p.play_note(z.midi_pitch(pitch), 0.8, 1/3)

s.wait(1)

for pitch in composite_melody:
    p.play_note(z.midi_pitch(pitch), 0.8, 1/3)
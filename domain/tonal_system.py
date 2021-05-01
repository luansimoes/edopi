from .gcycle import GCycle
from .tonal_system_element import TonalSystemElement
from .scale import Scale
from .balzano_diagram import BalzanoDiagram
from typing import Union
import math

class TonalSystem:
    def __init__(self, n: int, g=1):
        assert n>1, "Tonal System must have more than one element"
        self.cardinality = n
        self.generator = TonalSystemElement(g, n)
        self.cycle = GCycle(self.generator)


    def scale(self, elements=[], struct=[], name='Generic Scale'):
        assert (len(elements)==0) ^ (len(struct)==0), "argument must be either elements or struct"
        if len(elements)!=0:
            elements.sort()
            if all(isinstance(e, TonalSystemElement) for e in elements):
                circle_elements = elements + [elements[0]]
            elif all(isinstance(e, int) for e in elements):
                circle_elements = [TonalSystemElement(e, self.cardinality) for e in elements] + [TonalSystemElement(elements[0], self.cardinality)]

            struct = tuple((circle_elements[i]-circle_elements[i-1]).pitch_class for i in range(1, len(circle_elements)))

        return Scale(self.cardinality, struct, name=name)

    def diatonic_scale(self):
        return self.cycle.diatonic_scale(0)

    def get_generators(self):
        n = self.cardinality
        return [x for x in range(n) if math.gcd(x, n)==1]

    def set_generator(self, g: Union[TonalSystemElement, int]):
        if isinstance(g, int):
            assert math.gcd(g, self.cardinality)==1, "Element must be a generator"
            self.generator = TonalSystemElement(g, self.cardinality)
        elif isinstance(g, TonalSystemElement):
            assert g.is_generator(), "Element must be a generator"
            self.generator = g
        self.cycle = GCycle(self.generator)

    def get_midi_pitch_classes(self):
        n = self.cardinality
        return [TonalSystemElement(i, n).midi for i in range(n)]

    def midi_pitch(self, pitch_class: int, oct=0):
        oct+=2
        if oct==2:
            oct += int(pitch_class//self.cardinality) - 2
        return TonalSystemElement(pitch_class, self.cardinality).midi + (12*oct)

    def balzano_diagram(self, minor: int, major: int):
        n = self.cardinality
        assert TonalSystemElement(minor+major, n)==self.generator, "thirds must sum up to generator"
        return BalzanoDiagram(n, TonalSystemElement(minor, n), TonalSystemElement(major, n))

    def show_gCycle(self):
        self.cycle.show()
    
    def show(self):
        GCycle(TonalSystemElement(1, self.cardinality)).show()

    def __str__(self):
        return f'{self.cardinality}-Fold Tonal System with generator {self.generator}'

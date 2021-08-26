from .gcycle import GCycle
from .chroma import Chroma
from .scale import Scale
from .balzano_diagram import BalzanoDiagram
from typing import Union
import math

class TonalSystem:
    """
    Instantiate a Tonal System.
    A Tonal System is a group of n elements and it has a generator chosen as a generalized fifth. 
    All the other structures are defined within a Tonal System.
    
    :param n: The number of elements.
    :type n: int

    :param g: The generalized fifth of the System.
    :type g: int
    """

    def __init__(self, n: int, g=1):
        assert n>1, "Tonal System must have more than one element"
        self.cardinality = n
        self._generator = Chroma(g, n)
        self.cycle = GCycle(self._generator)
        self.scale = self.diatonic_scale()

    @property
    def generators(self):
        n = self.cardinality
        return [x for x in range(n) if math.gcd(x, n)==1]

    @property
    def generator(self):
        return self._generator.pitch_class
    
    @generator.setter
    def generator(self, value):
        self.set_generator(value)

    def set_generator(self, g: Union[Chroma, int]):
        if isinstance(g, int):
            assert math.gcd(g, self.cardinality)==1, "Element must be a generator"
            self._generator = Chroma(g, self.cardinality)
        elif isinstance(g, Chroma):
            assert g.is_generator, "Element must be a generator"
            self._generator = g
        self.cycle = GCycle(self._generator)
        self.scale = self.diatonic_scale()

    def scale(self, elements=[], struct=[], name='Generic Scale'):
        assert (len(elements)==0) ^ (len(struct)==0), "argument must be either elements or struct"
        if len(elements)!=0:
            elements.sort()
            if all(isinstance(e, Chroma) for e in elements):
                circle_elements = elements + [elements[0]]
            elif all(isinstance(e, int) for e in elements):
                circle_elements = [Chroma(e, self.cardinality) for e in elements] + [Chroma(elements[0], self.cardinality)]

            struct = tuple((circle_elements[i]-circle_elements[i-1]).pitch_class for i in range(1, len(circle_elements)))

        return Scale(self.cardinality, struct, name=name)

    def diatonic_scale(self):
        return self.cycle.diatonic_scale(0)
    
    def chromatic_scale(self):
        struct = tuple([1 for _ in range(self.cardinality)])
        return Scale(self.cardinality, struct, name=f'{self.cardinality}EDO Chromatic Scale')

    # TODO: Figure out another way to do this
    def midi_pitch(self, pitch_class: int, oct=0):
        oct+=2
        if oct==2:
            oct += int(pitch_class//self.cardinality) - 2
        return Chroma(pitch_class, self.cardinality).midi + (12*oct)

    def balzano_diagram(self, minor: int, major: int):
        n = self.cardinality
        assert Chroma(minor+major, n)==self._generator, "thirds must sum up to generator"
        return BalzanoDiagram(n, Chroma(minor, n), Chroma(major, n))
    
    #---------------------COMPOSITION METHODS------------------------

    def show_gCycle(self):
        self.cycle.show()
    
    def show(self):
        GCycle(Chroma(1, self.cardinality)).show()

    def __str__(self):
        return f'{self.cardinality}-Fold Tonal System with generator {self._generator}'

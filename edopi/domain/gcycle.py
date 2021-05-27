from .tonal_system_element import TonalSystemElement
from .scale import DiatonicScale
from typing import Union
import copy
import numpy as np
import matplotlib.pyplot as plt

class GCycle:
    """
    Instantiate a G-Cycle of the Tonal System.
    A G-Cycle is a generalized Cycle of Fifths - which is isomorph to the Group.
    In most cases, there's no need to interact directly with this class.
    
    :param generator: The generator of the Cycle.
    :type g: TonalSystemElement
    """

    def __init__(self, generator: TonalSystemElement):
        assert generator.is_generator(), 'GCycle must be initialized with a element that is a generator of the given system'
        self.generator = generator
        self.system_size = self.generator.module
        self.elements = self.generate_cycle()
        #self.scale_sizes = sorted([self.generator.inverse().pitch_class, self.generator.inverse().symmetrical().pitch_class])

    def generate_cycle(self):
        elements = [TonalSystemElement(0, self.system_size)]
        for _ in range(self.system_size - 1):
            elements.append(elements[-1] + self.generator)
        return elements

    #TODO: Gerar escala diatônica e pentatônica, dependendo das características
    #TODO: Gerar no modo dórico generalizado
    def diatonic_scale(self, tonic: int):
        length = self.generator.inverse().pitch_class

        start_element = TonalSystemElement(-self.generator.pitch_class, self.system_size)
        
        sc_elements = [start_element]
        for _ in range(length-1):
            sc_elements.append(sc_elements[-1]+self.generator)
        sc_elements.sort()
        sc_elements.append(sc_elements[0])

        struct = tuple((sc_elements[i]-sc_elements[i-1]).pitch_class for i in range(1, len(sc_elements)))

        return DiatonicScale(self.system_size, struct, self.generator, tonic=tonic, name="Diatonic Scale")

    # TODO: return integer if elem is an integer
    def next(self, elem: Union[TonalSystemElement, int], steps: int):
        real_elem = TonalSystemElement(elem, self.system_size) if isinstance(elem, int) else elem
        next_index = (self.elements.index(real_elem) + steps) % len(self.elements)
        return copy.deepcopy(self.elements[next_index])

    def show(self):
        r = 10
        angle = 2 * np.pi / self.system_size
        x = [self.elements[0].pitch_class]
        y = [r]

        figure, axes = plt.subplots()
        cycle = plt.Circle((0, 0), r, fill=False)
        axes.add_artist(cycle)

        for i in range(1, self.system_size + 1):
            x.append(r * np.sin(i * angle))
            y.append(r * np.cos(i * angle))

        #plt.plot(x, y, markersize=20)
        plt.plot(x, y, 'wo', markersize=20)
        for i in range(self.system_size):
            plt.text(x[i], y[i],self.elements[i], ha='center', va='center')
        plt.axis('equal')
        plt.axis('off')
        plt.show()

    def __str__(self):
        resp_str = f'\n*************Cycle:***************\n'
        resp_str += f'Elements: {[str(e) for e in self.elements]}\n'
        #resp_str += f'Scale Sizes: {self.scale_sizes[0]} {self.scale_sizes[1]}'
        return resp_str
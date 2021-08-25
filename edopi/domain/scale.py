from numpy.lib import math
from .chroma import Chroma
from .utils import check_or_create_folder
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Scale:
    """
    Instantiate a Scale.
    A Scale is an ordered collection of elements, starting and ending at the same element, called tonic. 
    It is defined by an interval struct within a Tonal System.
    
    :param system_size: The number of elements of the system.
    :type system_size: int

    :param interval_struct: The pattern of intervals that generates the scale.
    :type interval_struct: tuple

    :param tonic: the first element of the scale.
    :type tonic: int

    :param name: The name of the scale.
    :type name: str
    """
    def __init__(self, system_size: int, interval_struct: tuple, tonic=0, name="Generic Scale"):
        self.system_size = system_size
        self.interval_struct = interval_struct
        self.tonic = tonic
        self._elements = self.build_elements(tonic)
        self.name = name
        self._interval_vector = None

    @property
    def midi_pitch_classes(self):
        return [e.midi for e in self._elements]

    @property
    def elements(self):
        return [e.pitch_class for e in self._elements]
    
    @property
    def is_chromatic(self):
        return len(self)==self.system_size
    
    @property
    def interval_vector(self):
        if self._interval_vector==None:
            self._interval_vector = self.vector()

        return self._interval_vector
    
    def build_elements(self, tonic: int):
        elements = []
        actual = tonic
        for i in self.interval_struct:
            elements.append(Chroma(actual, self.system_size))
            actual += i
        return elements

    def set_tonic(self, tonic: int):
        self.tonic = tonic
        self._elements = self.build_elements(tonic)

    # if element doesnt belong to scale it finds the last one that belongs
    def next(self, elem: int, steps: int):
        if isinstance(elem, int):
            real_elem = Chroma(elem, self.system_size)
            octave = int(elem // self.system_size)
        else:
            real_elem = elem
            octave = 0

        while real_elem not in self._elements:
            real_elem -= 1
        
        next_index = (self._elements.index(real_elem) + steps) % len(self._elements)
        if steps > 0 and self._elements[next_index].pitch_class < real_elem.pitch_class:
            octave += 1
        elif steps < 0 and self._elements[next_index].pitch_class > real_elem.pitch_class:
            octave -= 1
        return self._elements[next_index].pitch_class + (octave * self.system_size)

    # TODO: usar algoritmo de Manacher para otimizar
    def find_symmetric_rotation(self):
        struct = list(self.interval_struct)
        for i in range(0, len(struct)):
            rotated = struct[i:] + struct[:i]
            if rotated == rotated[::-1]:
                return i
        return -1

    # TODO: garantir que file_name tenha .scl e que o kbm substitua.
    def export_scala_files(self, file_name: str, kbm_pattern=None):
        chroma_cents = 1200 / self.system_size
        check_or_create_folder('scala_files')
        f = open(f'scala_files/{file_name}', 'w')

        # Headers
        f.write(f'! {file_name}\n!\n {self.name}\n {len(self)}\n!')

        sum_interval = 0
        for interval in self.interval_struct:
            sum_interval += interval
            format_value = "{:.5f}".format(sum_interval * chroma_cents)
            f.write(f'\n {format_value}')
        f.close()

        kbm_name = file_name[:-3] + 'kbm'
        kbm = open(f'scala_files/{kbm_name}', 'w')

        if kbm_pattern == None:
            kbm_pattern = [i for i in range(len(self))]

        if len(kbm_pattern) <= 12:
            length = 12
            kbm.write(
                f'! {kbm_name}\n{length}\n{0}\n{127}\n{60 + self._elements[0].pitch_class}\n{69}\n440.00000\n{len(self._elements)}\n')
            kbm.write('! Mapping.')
            for e in (kbm_pattern + ['x' for _ in range(12 - len(kbm_pattern))]):
                kbm.write(f'\n{e}')

        else:
            length = len(kbm_pattern)
            kbm.write(
                f'! {kbm_name}\n{length}\n{0}\n{127}\n{60 + self._elements[0].pitch_class}\n{69}\n440.00000\n{len(self)}\n')
            kbm.write('! Mapping.')
            for e in kbm_pattern:
                kbm.write(f'\n{e}')

        kbm.close()

    def show(self, generator=1, write_all=False, as_subgroup=False):
        g = Chroma(generator, self.system_size)
        assert g.is_generator, 'Element must be a generator of the Group'

        #size of the cycle
        size = len(self) if as_subgroup else self.system_size

        r = 5
        angle = 2 * np.pi / size
        x = [0]
        y = [r]

        for i in range(1, size + 1):
            x.append(r * np.sin(i * angle))
            y.append(r * np.cos(i * angle))

        figure, axes = plt.subplots()
        circle = plt.Circle((0, 0), r, fill=False)
        axes.add_artist(circle)

        # plotting sequential lines and white circles behind text 
        x_line = []
        y_line = []
        x_circles = []
        y_circles = []

        # set the universe of elements (system elements or scale elements)
        use_all = write_all and not as_subgroup
        system_elements = [Chroma(i, self.system_size) for i in range(self.system_size)]
        elements = self._elements if not use_all else system_elements

        # ordering elements to get equivalent subgroup position 
        ordered = sorted(elements, key=lambda x:x/g)

        for e in elements:
            pos = (e/g).pitch_class if not as_subgroup else ordered.index(e)

            # all elements have white circles and text
            x_circles.append(x[pos])
            y_circles.append(y[pos])
            plt.text(x[pos], y[pos], e.pitch_class, ha='center', va='center')

            if e in self._elements:
                # only scale elements are linked by lines
                x_line.append(x[pos])
                y_line.append(y[pos])
                

        # plotting
        x_line.append(x[0])
        y_line.append(y[0])
        plt.plot(x_line, y_line, markersize=20)
        plt.plot(x_circles, y_circles, 'wo', markersize=20)
        plt.axis('equal')
        plt.axis('off')

        plt.show()

    def vector(self):
        v = [0 for _ in range(int(self.system_size / 2))]
        scale = self._elements
        for i, pivot in enumerate(scale):
            for el in scale[i + 1:]:
                dist = min((el - pivot).pitch_class % self.system_size, (pivot - el).pitch_class % self.system_size)
                v[dist - 1] += 1
        return v


    #----------------------COMPOSITION METHODS--------------------------
    def smooth_line(self, base_pitch, line_range, size, max_step=1):
        low, high = line_range
        range_size = high-low
        assert base_pitch>=low and base_pitch<=high, 'base_pitch must be in line_range'

        line = [self.next(base_pitch, 0)]
        cur_pitch = base_pitch
        for _ in range(size-1):
            p = [(cur_pitch-low)/range_size, (high-cur_pitch)/range_size]
            dir = np.random.choice([-1, 1], p=p)
            step = np.random.randint(max_step) + 1
            cur_pitch = self.next(cur_pitch, dir*step)
            line.append(cur_pitch)

        return line

    def __eq__(self, o):
        if not isinstance(o, Scale):
            return False
        return (self.interval_struct == o.interval_struct) and (self.system_size == o.system_size)

    def __len__(self):
        return len(self._elements)

    def __str__(self):
        output_str = self.name
        output_str += f'\nElements: {[e.pitch_class for e in self._elements]}'
        output_str += f'\nInterval Vector: {self.interval_vector}'
        output_str += f'\nInterval Struct: {self.interval_struct}\n'
        return output_str


class DiatonicScale(Scale):
    """
    Instantiate a diatonic Scale.
    The main difference of this class and the generic scale is that this class contains a generator, 
    used for visualization inside the cycle.
    
    :param system_size: The number of elements of the system.
    :type system_size: int

    :param interval_struct: The pattern of intervals that generates the scale.
    :type interval_struct: tuple

    :param generator: The generator of the GCycle from which the scale was built.
    :type generator: Chroma

    :param tonic: the first element of the scale.
    :type tonic: int

    :param name: The name of the scale.
    :type name: str
    """
    def __init__(self, system_size: int, interval_struct: tuple, generator : Chroma, tonic=0, name="Diatonic Scale"):
        self.generator = generator
        super().__init__(system_size, interval_struct, tonic, name)
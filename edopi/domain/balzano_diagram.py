from .tonal_system_element import Chroma
from .gcycle import GCycle
import matplotlib.pyplot as plt
import numpy as np

class BalzanoDiagram:
    """
    Instantiate a Balzano Diagram for visualization.
    A Balzano Diagram is a 2D representation of a Tonal System.
    It is generated from two elements x and y, such as x+y is equal to the generator of the System. 
    
    :param system_size: The number of elements of the system.
    :type system_size: int

    :param x: The smaller generator.
    :type x: Chroma

    :param y: The bigger generator.
    :type y: Chroma.
    """
    def __init__(self, system_size: int, x: Chroma, y: Chroma):
        self.system_size = system_size
        self.generator = x+y
        self.thirds = (x, y)
        self.scale = GCycle(self.generator).diatonic_scale(0)
        self.matrix = self.build_matrix(system_size, x, y)
        self.compact_matrix = self.build_compact_matrix(system_size, x, y)
        self.dims = (len(self.matrix), len(self.matrix[0]))

    def build_compact_matrix(self, system_size: int, x: Chroma, y: Chroma):
        matrix = []
        gen = x+y
        #TODO: classe subgrupo??
        dims = [int((gen.inverse().pitch_class+1)/2) +1, int((gen.inverse().pitch_class-1)/2)+1]


        rotation = self.scale.find_symmetric_rotation()
        initial = self.scale._elements[rotation] if rotation!=-1 else self.scale._elements[0]
        init_pos = (initial*gen.inverse()).pitch_class
        coords = (init_pos%x.subgroup(), init_pos%y.subgroup())
        for i in range(coords[0], coords[0]+dims[0]):
            row = []
            for j in range(coords[1], coords[1]+dims[1]):
                row.append(Chroma(i*x.pitch_class + j*y.pitch_class, system_size))
            matrix.append(row)
        return matrix

    def build_matrix(self, system_size: int, x: Chroma, y: Chroma):
        matrix = []
        gen = x+y
        #TODO: classe subgrupo??
        dims = [x.subgroup()+1, y.subgroup()+1]

        rotation = self.scale.find_symmetric_rotation()
        initial = self.scale._elements[rotation] if rotation!=-1 else self.scale._elements[0]
        init_pos = (initial*gen.inverse()).pitch_class
        coords = (init_pos%x.subgroup(), init_pos%y.subgroup())

        for i in range(coords[0], coords[0]+dims[0]):
            row = []
            for j in range(coords[1], coords[1]+dims[1]):
                row.append(Chroma(i*x.pitch_class + j*y.pitch_class, system_size))
            matrix.append(row)
        return matrix

    def contains_scale(self):
        pos = [0,0]
        matrix = self.matrix
        actual = matrix[pos[0]][pos[1]]
        region = []
        step = 0
        while len(region)!=len(self.scale.elements)+1:
            region.append(actual)
            pos[step]+=1
            step = (step+1)%2
            actual = matrix[pos[0]%(len(matrix)-1)][pos[1]%(len(matrix[0])-1)]

        if region[-1]!=region[0]: return False
        region = sorted(region[:-1])
        region.append(region[0])

        r_struct = list((region[i]-region[i-1]).pitch_class for i in range(1, len(region)))
        s_struct = list(self.scale.interval_struct)
        for i in range(len(s_struct)):
            if (r_struct[i:]+r_struct[:i]) == s_struct: return True

        return False
    
    def show(self, compact=True):
        fig, ax = plt.subplots()

        matrix = self.matrix if not compact else self.compact_matrix
        dims = [len(matrix), len(matrix[0])]

        if self.contains_scale():

            #Paddings
            pad_x = 0.02*(dims[1]+1)
            pad_y = 0.021*(dims[0]+1)
            p = (pad_x+pad_y)/2

            #i and j handle matrix; x and y handle the coordinates
            i, j = 0, 0
            x, y = 0.5, 0.5

            #First step is vertical TODO: checar qual é o primeiro passo com base no tipo da escala
            h = False

            #Draw matrix lines till it reaches the start element again
            while (matrix[i][j]!=matrix[0][0] or (i,j)==(0,0)):
                #If step is horizontal, increments column; else increments row
                dest = (i,(j+1)%dims[1]) if h else ((i+1)%dims[0], j)
                pos_dest = (0.5+dest[1], 0.5+dest[0])

                #Compute paddings and color
                px = pad_x if h else 0
                py = 0 if h else pad_y
                color = 'r' if h else 'b'

                #Draw line and diagonal if needed
                if (dest[0]<dims[0] and dest[1]<dims[1]) and (dest[0]>=i and dest[1]>=j):
                    plt.plot([x+px, pos_dest[0]-px], [y+py, pos_dest[1]-py], color=color)
                    if (i+1 < dims[0]) and (j+1 < dims[1]) and (matrix[dest[0]][dest[1]]!=matrix[0][0]):
                        plt.plot([x+p, x+1-p], [y+p, y+1-p], color='g')
                    h = not h


                if dest[0]<i:
                    plt.plot([x-1+pad_x, x-pad_x], [0.5, 0.5], color='r')
                    plt.plot([x-1+p, x-p], [0.5+p, 1.5-p], color='g')
                elif dest[1]<j:
                    plt.plot([0.5, 0.5], [y-pad_y, y-1+pad_y], color='b')
                    plt.plot([0.5+p, 1.5-p], [y-1+p, y-p], color='g')

                i, j = dest
                x, y = pos_dest


        for i in range(dims[0]):
            for j in range(dims[1]):
                el = matrix[i][j]
                ax.text(j+0.5, i+0.5, str(el), va='center', ha='center')

        ax.set_xlim(0, dims[1])
        ax.set_ylim(0, dims[0])
        ax.set_xticks(np.arange(dims[1]))
        ax.set_yticks(np.arange(dims[0]))

        plt.axis('off')

        ax.grid()
        plt.show()

    def __str__(self):
        return str([[str(x) for x in row] for row in self.matrix])

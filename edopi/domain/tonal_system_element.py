import math

class TonalSystemElement:
    """
    Instantiate a Tonal System Element.
    Elements must have a chroma defined in a System. 
    The System's cardinality acts as a module when operating microtonal chromas.
    
    :param pitch: A value that will be transformed into a chroma.
    :type pitch: int

    :param module: The cardinality of the System.
    :type module: int
    """

    def __init__(self, pitch: int, module: int):
        self.pitch_class = pitch % module
        self.module = module

        self.cents = self.pitch_class * (1200/self.module)
        self.midi = (self.cents/100)
    
    def is_generator(self):
        return math.gcd(self.pitch_class, self.module)==1

    def __add__(self, o):
        assert isinstance(o, TonalSystemElement), f"Cannot add TonalSystemElement to {type(o)}"
        assert self.module == o.module, "Cannot add elements of different modules"
        return TonalSystemElement(self.pitch_class + o.pitch_class, self.module)

    def __sub__(self, o):
        assert isinstance(o, TonalSystemElement), f"Cannot subtract TonalSystemElement to {type(o)}"
        assert self.module == o.module, "Cannot subtract elements of different modules"
        return TonalSystemElement(self.pitch_class - o.pitch_class, self.module)

    def __mul__(self, o):
        assert isinstance(o, TonalSystemElement), f"Cannot multiply TonalSystemElement to {type(o)}"
        assert self.module == o.module, "Cannot multiply elements of different modules"
        return TonalSystemElement(self.pitch_class * o.pitch_class, self.module)

    def __eq__(self, o):
        return isinstance(o, TonalSystemElement) and self.pitch_class == o.pitch_class and self.module == o.module

    def __gt__(self, o):
        return isinstance(o, TonalSystemElement) and (self.pitch_class > o.pitch_class) and self.module == o.module

    def __lt__(self, o):
        return isinstance(o, TonalSystemElement) and self.pitch_class < o.pitch_class and self.module == o.module

    def __le__(self, o):
        return isinstance(o, TonalSystemElement) and self.pitch_class <= o.pitch_class and self.module == o.module

    def __ge__(self, o):
        return isinstance(o, TonalSystemElement) and self.pitch_class >= o.pitch_class and self.module == o.module

    def inverse(self):
        if math.gcd(self.pitch_class, self.module) != 1:
            return None
        else:
            for i in range(self.module):
                if (i * self.pitch_class) % self.module == 1:
                    return TonalSystemElement(i, self.module)

    def symmetrical(self):
        return TonalSystemElement(-self.pitch_class, self.module)

    def subgroup(self):
        i = 1
        pitch_class = self.pitch_class
        while pitch_class!=0:
            i+=1
            pitch_class = (pitch_class+self.pitch_class)%self.module
        return i
    
    def __str__(self):
        return str(self.pitch_class)

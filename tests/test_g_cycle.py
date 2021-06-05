import  unittest

from edopi import GCycle, Chroma, Scale


class TestGCycle(unittest.TestCase):

    def setUp(self):
        diatonic = (2, 2, 1, 2, 2, 2, 1)
        self.c1 = GCycle(Chroma(7, 12))
        self.s1 = Scale(12, diatonic)

    def test_diatonic_scale(self):
        self.assertEqual(self.s1, self.c1.diatonic_scale(0))
    
    def test_next(self):
        do = Chroma(0, 12)
        self.assertEqual(do, self.c1.next(5, 1))
  
if __name__ == '__main__':  
    unittest.main()  
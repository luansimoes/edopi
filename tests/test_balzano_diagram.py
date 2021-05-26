import  unittest
from edopi import TonalSystemElement, BalzanoDiagram, Scale

class TestBalzanoDiagram(unittest.TestCase):
   
    def setUp(self):
        self.b1 = BalzanoDiagram(12, TonalSystemElement(3,12), TonalSystemElement(4, 12))
        self.b2 = BalzanoDiagram(12, TonalSystemElement(2,12), TonalSystemElement(5,12))
        self.b3 = BalzanoDiagram(20, TonalSystemElement(5, 20), TonalSystemElement(6,20))
    
    def test_build_matrix(self):
        m = [[2, 6, 10, 2],
                [5, 9, 1, 5],
                [8, 0, 4, 8],
                [11, 3, 7, 11],
                [2, 6, 10, 2]]
        
        el_matrix = [[TonalSystemElement(e, 12) for e in row] for row in m]
        self.assertEqual(el_matrix, self.b1.matrix)
    
    def test_build_compact_matrix(self):
        m = [[2, 6, 10, 2],
                [5, 9, 1, 5],
                [8, 0, 4, 8],
                [11, 3, 7, 11],
                [2, 6, 10, 2]]

        el_matrix = [[TonalSystemElement(e, 12) for e in row] for row in m]
        self.assertEqual(el_matrix, self.b1.compact_matrix)
    
    def test_contains_scale(self):
        self.assertTrue(self.b1.contains_scale())
        self.assertFalse(self.b2.contains_scale())
        self.assertTrue(self.b3.contains_scale())
  
if __name__ == '__main__':  
    unittest.main()  
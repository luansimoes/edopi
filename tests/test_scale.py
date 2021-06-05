import unittest

from edopi import Chroma, Scale, TonalSystem


class TestScale(unittest.TestCase):

    def setUp(self):
        diatonic = (2, 2, 1, 2, 2, 2, 1)
        self.s1 = Scale(12, diatonic, name="12-Pitch Diatonic Major Scale")
    
    def test_build_elements(self):
        diatonic = [0, 2, 4, 5, 7, 9, 11]
        elements = [Chroma(e, 12) for e in diatonic]
        self.assertEqual(elements, self.s1.build_elements(0))

    def test_set_tonic(self):
        exp = [0, 2, 4, 5, 7, 9, 11]
        self.assertEqual(exp, self.s1.elements)
        exp = [3, 5, 7, 8, 10, 0, 2]
        self.s1.set_tonic(3)
        self.assertEqual(exp, self.s1.elements)

    def test_next(self):
        re = Chroma(2, 12)
        self.assertEqual(re.pitch_class, self.s1.next(0, 1))

    def test_export_scala_files(self):
        f = open('tests/test_files/z12_7_test.scl', 'r')
        f2 = open('tests/test_files/z12_7_test.kbm', 'r')
        content = f.read()
        content2 = f2.read()

        self.s1.export_scala_files('z12_7.scl')
        f_result = open('scala_files/z12_7.scl', 'r')
        f2_result = open('scala_files/z12_7.kbm', 'r')
        result = f_result.read()
        result2 = f2_result.read()

        self.assertEqual(content, result)
        self.assertEqual(content2, result2)

        f_result.close()
        f2_result.close()
        f.close()
        f2.close()

    def test_get_elements(self):
        diatonic = [0, 2, 4, 5, 7, 9, 11]
        self.assertEqual(diatonic, self.s1.elements)

    def test_vector(self):
        exp = [2, 5, 4, 3, 6, 1]
        self.assertEqual(exp, self.s1.interval_vector)

    def test_find_symmetric_rotation(self):
        self.assertEqual(1, self.s1.find_symmetric_rotation())
    
    def test_is_chromatic(self):
        s = Scale(12, tuple([1] * 12))
        self.assertTrue(s.is_chromatic)
    
    # TODO: test
    def test_diatonic(self):
        pass


if __name__ == '__main__':
    unittest.main()

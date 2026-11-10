import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from red_social import Agente, RedSocial
from calculos import extremismo, esfuerzo, es_aplicable

RS1 = RedSocial((Agente(100, .5, 1), Agente(100, .1, 1), Agente(-10, .1, 1)), 55)
RS2 = RedSocial((Agente(-30, .9, 1), Agente(20, .1, 2), Agente(50, .5, 1)), 35)


class Enunciado(unittest.TestCase):
    def test_ejemplo1(self):
        self.assertEqual(esfuerzo(RS1, [0, 0, 1]), 9)
        self.assertAlmostEqual(extremismo(RS1, [0, 0, 1]), 47.14, 2)
        self.assertEqual(esfuerzo(RS1, [1, 0, 0]), 50)
        self.assertAlmostEqual(extremismo(RS1, [1, 0, 0]), 33.5, 1)

    def test_ejemplo2(self):
        self.assertEqual(esfuerzo(RS2, [0, 1, 0]), 36)
        self.assertFalse(es_aplicable(RS2, [0, 1, 0]))
        self.assertEqual(esfuerzo(RS2, [1, 0, 1]), 28)
        self.assertAlmostEqual(extremismo(RS2, [1, 0, 1]), 9.43, 2)

    def test_techo_con_float(self):  # 100*(1-0.7)*1.6 = 48 exacto, en float da 48.0000000001
        self.assertEqual(esfuerzo(RedSocial((Agente(-100, .7, 1.6),), 99), [1]), 48)


if __name__ == "__main__":
    unittest.main()
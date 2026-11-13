import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.gui import _listar_pruebas


class ListarPruebasTests(unittest.TestCase):
    def test_incluye_todas_las_pruebas_en_orden_numerico(self):
        with tempfile.TemporaryDirectory() as carpeta:
            for nombre in (
                "Prueba2.txt",
                "Prueba36.txt",
                "Prueba4.txt",
                "Prueba_extra.txt",
                "Prueba1.csv",
            ):
                open(os.path.join(carpeta, nombre), "w", encoding="utf-8").close()

            pruebas = _listar_pruebas(carpeta)

        self.assertEqual(
            [nombre for _, nombre, _ in pruebas],
            ["Prueba2.txt", "Prueba4.txt", "Prueba36.txt"],
        )


if __name__ == "__main__":
    unittest.main()

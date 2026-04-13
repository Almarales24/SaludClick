import unittest
from utilidades.seguridad import hashear_contrasena, verificar_contrasena


class TestSeguridadContrasena(unittest.TestCase):

    def test_hash_no_es_texto_plano(self):
        hash_result = hashear_contrasena("MiClave123")
        self.assertNotEqual(hash_result, "MiClave123")

    def test_hash_es_string(self):
        hash_result = hashear_contrasena("MiClave123")
        self.assertIsInstance(hash_result, str)

    def test_hash_no_vacio(self):
        hash_result = hashear_contrasena("MiClave123")
        self.assertTrue(len(hash_result) > 0)

    def test_verificar_contrasena_correcta(self):
        contrasena = "MiClave123"
        hash_result = hashear_contrasena(contrasena)
        self.assertTrue(verificar_contrasena(contrasena, hash_result))

    def test_verificar_contrasena_incorrecta(self):
        hash_result = hashear_contrasena("MiClave123")
        self.assertFalse(verificar_contrasena("OtraClave456", hash_result))

    def test_verificar_contrasena_vacia_contra_hash(self):
        hash_result = hashear_contrasena("MiClave123")
        self.assertFalse(verificar_contrasena("", hash_result))

    def test_dos_hashes_de_misma_contrasena_son_distintos(self):
        # werkzeug usa sal aleatoria, así que deben ser distintos
        h1 = hashear_contrasena("MiClave123")
        h2 = hashear_contrasena("MiClave123")
        self.assertNotEqual(h1, h2)

    def test_ambos_verifican_correctamente(self):
        # Aunque los hashes sean distintos, ambos verifican la misma clave
        contrasena = "MiClave123"
        h1 = hashear_contrasena(contrasena)
        h2 = hashear_contrasena(contrasena)
        self.assertTrue(verificar_contrasena(contrasena, h1))
        self.assertTrue(verificar_contrasena(contrasena, h2))


if __name__ == "__main__":
    unittest.main()

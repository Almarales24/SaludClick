import unittest
from utilidades.validaciones import validar_email, validar_telefono, validar_contrasena, campo_vacio


class TestValidarEmail(unittest.TestCase):

    def test_email_valido(self):
        self.assertTrue(validar_email("usuario@ejemplo.com"))

    def test_email_con_punto_en_nombre(self):
        self.assertTrue(validar_email("nombre.apellido@dominio.org"))

    def test_email_sin_arroba(self):
        self.assertFalse(validar_email("usuarioejemplo.com"))

    def test_email_sin_dominio(self):
        self.assertFalse(validar_email("usuario@"))

    def test_email_sin_extension(self):
        self.assertFalse(validar_email("usuario@dominio"))

    def test_email_vacio(self):
        self.assertFalse(validar_email(""))


class TestValidarTelefono(unittest.TestCase):

    def test_telefono_valido_10_digitos(self):
        self.assertTrue(validar_telefono("1234567890"))

    def test_telefono_valido_7_digitos(self):
        self.assertTrue(validar_telefono("1234567"))

    def test_telefono_valido_15_digitos(self):
        self.assertTrue(validar_telefono("123456789012345"))

    def test_telefono_con_letras(self):
        self.assertFalse(validar_telefono("12345abc90"))

    def test_telefono_muy_corto(self):
        self.assertFalse(validar_telefono("123456"))

    def test_telefono_muy_largo(self):
        self.assertFalse(validar_telefono("1234567890123456"))

    def test_telefono_vacio(self):
        self.assertFalse(validar_telefono(""))


class TestValidarContrasena(unittest.TestCase):

    def test_contrasena_valida(self):
        self.assertTrue(validar_contrasena("Segura123"))

    def test_contrasena_sin_mayuscula(self):
        self.assertFalse(validar_contrasena("segura123"))

    def test_contrasena_sin_numero(self):
        self.assertFalse(validar_contrasena("Segurapass"))

    def test_contrasena_muy_corta(self):
        self.assertFalse(validar_contrasena("Se1"))

    def test_contrasena_exactamente_8_caracteres(self):
        self.assertTrue(validar_contrasena("Abcdef1!"))

    def test_contrasena_vacia(self):
        self.assertFalse(validar_contrasena(""))


class TestCampoVacio(unittest.TestCase):

    def test_campo_con_texto(self):
        self.assertFalse(campo_vacio("algo"))

    def test_campo_solo_espacios(self):
        self.assertTrue(campo_vacio("   "))

    def test_campo_vacio_string(self):
        self.assertTrue(campo_vacio(""))

    def test_campo_none(self):
        self.assertTrue(campo_vacio(None))

    def test_campo_con_espacios_y_texto(self):
        self.assertFalse(campo_vacio("  texto  "))


if __name__ == "__main__":
    unittest.main()

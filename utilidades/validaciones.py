import re

def validar_email(email: str) -> bool:
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return bool(re.match(patron, email))

def validar_telefono(telefono: str) -> bool:
    patron = r"^\d{7,15}$"
    return bool(re.match(patron, telefono))

def validar_contrasena(contrasena: str) -> bool:
    return bool(re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", contrasena))

def campo_vacio(texto: str) -> bool:
    return not texto or texto.strip() == ""
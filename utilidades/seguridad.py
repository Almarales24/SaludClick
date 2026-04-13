from werkzeug.security import generate_password_hash, check_password_hash

def hashear_contrasena(contrasena: str) -> str:
    return generate_password_hash(contrasena)

def verificar_contrasena(contrasena: str, hash: str) -> bool:
    return check_password_hash(hash, contrasena)
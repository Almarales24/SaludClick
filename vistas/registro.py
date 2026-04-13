import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Usuario
from utilidades.seguridad import hashear_contrasena
from utilidades.validaciones import validar_email, validar_telefono, validar_contrasena, campo_vacio

def vista_registro(page: ft.Page):
    page.controls.clear()

    nombre = ft.TextField(label="Nombre", width=320)
    apellido = ft.TextField(label="Apellido", width=320)
    documento = ft.TextField(label="Número de documento", width=320)
    direccion = ft.TextField(label="Dirección", width=320)
    email = ft.TextField(label="Correo electrónico", width=320)
    telefono = ft.TextField(label="Teléfono", width=320)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=320)
    confirmar = ft.TextField(label="Confirmar contraseña", password=True, can_reveal_password=True, width=320)
    error = ft.Text(color="red400", size=13)

    def registrar(e):
        error.value = ""

        campos = [nombre, apellido, documento, direccion, email, telefono, contrasena, confirmar]
        if any(campo_vacio(f.value) for f in campos):
            error.value = "Completa todos los campos."
            page.update()
            return

        if not validar_email(email.value):
            error.value = "Correo no válido."
            page.update()
            return

        if not validar_telefono(telefono.value):
            error.value = "Teléfono no válido (solo números, 7-15 dígitos)."
            page.update()
            return

        if not validar_contrasena(contrasena.value):
            error.value = "Mínimo 8 caracteres, una mayúscula y un número."
            page.update()
            return

        if contrasena.value != confirmar.value:
            error.value = "Las contraseñas no coinciden."
            page.update()
            return

        with Session() as db:
            if db.query(Usuario).filter_by(email=email.value.strip()).first():
                error.value = "Este correo ya está registrado."
                page.update()
                return

            if db.query(Usuario).filter_by(documento=documento.value.strip()).first():
                error.value = "Este documento ya está registrado."
                page.update()
                return

            nuevo = Usuario(
                nombre=nombre.value.strip(),
                apellido=apellido.value.strip(),
                documento=documento.value.strip(),
                direccion=direccion.value.strip(),
                email=email.value.strip(),
                telefono=telefono.value.strip(),
                contrasena_hash=hashear_contrasena(contrasena.value),
            )
            db.add(nuevo)
            db.commit()

        from vistas.login import vista_login
        vista_login(page)

    def ir_login(e):
        from vistas.login import vista_login
        vista_login(page)

    page.add(
        ft.Column(
            controls=[
                ft.Text("Crear cuenta", size=28, weight="bold"),
                ft.Divider(height=10, color="transparent"),
                nombre, apellido, documento, direccion,
                email, telefono, contrasena, confirmar,
                error,
                ft.ElevatedButton("Registrarse", width=320, on_click=registrar),
                ft.TextButton("¿Ya tienes cuenta? Inicia sesión", on_click=ir_login),
            ],
            horizontal_alignment="center",
            alignment="center",
            expand=True,
            scroll="auto",
        )
    )
    page.update()
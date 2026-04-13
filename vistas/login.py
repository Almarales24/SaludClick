import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Usuario
from utilidades.seguridad import verificar_contrasena
from utilidades.validaciones import campo_vacio
from utilidades.sesion import sesion

def vista_login(page: ft.Page):
    page.controls.clear()

    email = ft.TextField(label="Correo electrónico", width=320)
    contrasena = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=320)
    error = ft.Text(color="red400", size=13)

    def iniciar_sesion(e):
        error.value = ""
        if campo_vacio(email.value) or campo_vacio(contrasena.value):
            error.value = "Completa todos los campos."
            page.update()
            return

        with Session() as db:
            usuario = db.query(Usuario).filter_by(email=email.value.strip()).first()

        if not usuario or not verificar_contrasena(contrasena.value, usuario.contrasena_hash):
            error.value = "Correo o contraseña incorrectos."
            page.update()
            return

        sesion["usuario_id"] = usuario.id
        sesion["usuario_rol"] = usuario.rol
        sesion["usuario_nombre"] = usuario.nombre

        if usuario.rol == "recepcionista":
            from vistas.vista_recepcionista import vista_recepcionista
            vista_recepcionista(page)
        elif usuario.rol == "doctor":
            from vistas.vista_doctor import vista_doctor
            vista_doctor(page)
        else:
            from vistas.dashboard_paciente import vista_dashboard_paciente
            vista_dashboard_paciente(page)

    def ir_registro(e):
        from vistas.registro import vista_registro
        vista_registro(page)

    page.add(
        ft.Column(
            controls=[
                ft.Text("SaludClick", size=32, weight="bold"),
                ft.Text("Inicia sesión para continuar", size=14, color="grey400"),
                ft.Divider(height=20, color="transparent"),
                email,
                contrasena,
                error,
                ft.ElevatedButton("Iniciar sesión", width=320, on_click=iniciar_sesion),
                ft.TextButton("¿No tienes cuenta? Regístrate", on_click=ir_registro),
            ],
            horizontal_alignment="center",
            alignment="center",
            expand=True,
        )
    )
    page.update()
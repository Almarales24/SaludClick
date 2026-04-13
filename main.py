import flet as ft
from dotenv import load_dotenv
from base_datos.conexion import iniciar_base_datos
from vistas.login import vista_login

load_dotenv()

def main(page: ft.Page):
    page.title = "SaludClick"
    page.theme_mode = "dark"
    page.padding = 0

    iniciar_base_datos()
    from base_datos.conexion import seed_especialistas
    seed_especialistas()
    from base_datos.conexion import seed_usuarios
    seed_usuarios()
    vista_login(page)

ft.run(main)
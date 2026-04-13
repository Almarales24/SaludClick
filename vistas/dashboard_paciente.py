import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Cita
from utilidades.sesion import sesion

def vista_dashboard_paciente(page: ft.Page):
    page.controls.clear()

    nombre = sesion.get("usuario_nombre")
    usuario_id = sesion.get("usuario_id")

    with Session() as db:
        citas = db.query(Cita).filter_by(paciente_id=usuario_id).all()
        lista_citas = [
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"Dr. {c.especialista.nombre} — {c.especialista.especialidad}", weight="bold"),
                        ft.Text(f"Fecha: {c.fecha_hora.strftime('%d/%m/%Y %H:%M')}"),
                        ft.Text(f"Estado: {c.estado.capitalize()}", color="cyan300"),
                    ]),
                    padding=12,
                )
            )
            for c in citas
        ]

    def agendar(e):
        from vistas.agendar_cita import vista_agendar_cita
        vista_agendar_cita(page)

    def cerrar_sesion(e):
        sesion.clear()
        from vistas.login import vista_login
        vista_login(page)

    controles = [
        ft.Row([
            ft.Text(f"Hola, {nombre}", size=22, weight="bold"),
            ft.IconButton(ft.Icons.LOGOUT, tooltip="Cerrar sesión", on_click=cerrar_sesion),
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Text("Mis citas", size=17, weight="w600"),
    ]

    if lista_citas:
        controles.extend(lista_citas)
    else:
        controles.append(ft.Text("No tienes citas agendadas.", color="grey400"))

    controles.append(ft.ElevatedButton("Nueva cita", icon=ft.Icons.ADD, on_click=agendar))

    page.add(
        ft.Column(
            controls=controles,
            expand=True,
            scroll="auto",
        )
    )
    page.update()
import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Cita
from utilidades.sesion import sesion

def vista_confirmacion(page: ft.Page):
    page.controls.clear()

    cita_id = sesion.get("ultima_cita_id")

    with Session() as db:
        cita = db.query(Cita).filter_by(id=cita_id).first()
        nombre_paciente = cita.paciente.nombre
        nombre_especialista = cita.especialista.nombre
        especialidad = cita.especialista.especialidad
        fecha_hora = cita.fecha_hora.strftime("%d/%m/%Y %H:%M")

    def ir_dashboard(e):
        from vistas.dashboard_paciente import vista_dashboard_paciente
        vista_dashboard_paciente(page)

    page.add(
        ft.Column(
            controls=[
                ft.Icon(ft.Icons.CHECK_CIRCLE, color="green400", size=72),
                ft.Text("¡Cita agendada!", size=28, weight="bold"),
                ft.Divider(height=10, color="transparent"),
                ft.Text(f"Paciente: {nombre_paciente}", size=15),
                ft.Text(f"Especialista: {nombre_especialista}", size=15),
                ft.Text(f"Especialidad: {especialidad}", size=15),
                ft.Text(f"Fecha y hora: {fecha_hora}", size=15),
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton("Ir al inicio", on_click=ir_dashboard),
            ],
            horizontal_alignment="center",
            alignment="center",
            expand=True,
        )
    )
    page.update()
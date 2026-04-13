import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Cita, Especialista
from utilidades.sesion import sesion

def vista_doctor(page: ft.Page):
    page.controls.clear()

    usuario_id = sesion.get("usuario_id")
    nombre_doctor = sesion.get("usuario_nombre")

    def finalizar_cita(cita_id, e):
        with Session() as db:
            cita = db.query(Cita).filter_by(id=cita_id).first()
            if cita:
                cita.estado = "finalizada"
                db.commit()
        vista_doctor(page)

    def cerrar_sesion(e):
        sesion.clear()
        from vistas.login import vista_login
        vista_login(page)

    with Session() as db:
        perfil = db.query(Especialista).filter_by(usuario_id=usuario_id).first()
        
        if not perfil:
            page.add(ft.Text("Error: No se encontró perfil médico."))
            return

        citas = db.query(Cita).filter_by(especialista_id=perfil.id).all()
        
        tarjetas = []
        for c in citas:
            boton_finalizar = ft.ElevatedButton(
                "Finalizar Consulta", 
                on_click=lambda e, cid=c.id: finalizar_cita(cid, e),
                bgcolor="green700",
                color="white",
                visible=(c.estado != "finalizada" and c.estado != "cancelada")
            )

            # Usamos Container en lugar de Padding para evitar errores de versión
            tarjetas.append(
                ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(10),
                        content=ft.Column([
                            ft.Text(f"Paciente: {c.paciente.nombre} {c.paciente.apellido}", weight="bold"),
                            ft.Text(f"Fecha: {c.fecha_hora.strftime('%d/%m/%Y %H:%M')}"),
                            ft.Text(f"Estado: {c.estado.upper()}", color="blue700", size=12),
                            ft.Text(f"Síntomas: {c.sintomas if c.sintomas else 'N/A'}", italic=True),
                            ft.Divider(height=10, color="transparent"),
                            boton_finalizar
                        ])
                    )
                )
            )

    # Layout limpio
    page.add(
        ft.Column(
            controls=[
                ft.Row([
                    ft.Text(f"Dr. {nombre_doctor}", size=22, weight="bold"),
                    ft.IconButton(ft.Icons.LOGOUT, on_click=cerrar_sesion),
                ], alignment="spaceBetween"),
                ft.Text(f"Especialidad: {perfil.especialidad}", italic=True),
                ft.Divider(),
                ft.Column(tarjetas, scroll="auto", expand=True) # Scroll habilitado
            ],
            expand=True,
            scroll="auto"
        )
    )
    page.update()

import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Cita, Especialista
from utilidades.ia_gemini import analizar_sintomas
from utilidades.validaciones import campo_vacio
from utilidades.sesion import sesion
from datetime import datetime
import asyncio

def vista_agendar_cita(page: ft.Page):
    page.controls.clear()

    # --- Elementos Básicos Estables ---
    titulo = ft.Text("Solicitud de Cita Médica", size=26, weight="bold", color="blue700")
    
    sintomas = ft.TextField(
        label="Descripción de síntomas",
        multiline=True,
        min_lines=3,
        width=400,
        hint_text="Describa cómo se siente...",
    )

    resultado_ia = ft.Text("", color="blue700", size=13, weight="w500", italic=True)

    especialistas_dropdown = ft.Dropdown(
        label="Seleccionar Especialista",
        width=400,
    )

    fecha_input = ft.TextField(
        label="Fecha (YYYY-MM-DD)",
        hint_text="Ej: 2026-05-20",
        width=190,
    )

    hora_input = ft.TextField(
        label="Hora (HH:MM)",
        hint_text="Ej: 14:30",
        width=190,
    )

    error_text = ft.Text(color="red400", size=12)

    # --- Carga de Especialistas ---
    with Session() as db:
        especialistas = db.query(Especialista).all()
        # Si no hay registrados, mostramos un mensaje en el dropdown
        if not especialistas:
            especialistas_dropdown.options = [ft.dropdown.Option("Sin especialistas disponibles")]
        else:
            especialistas_dropdown.options = [
                ft.dropdown.Option(key=str(e.id), text=f"{e.nombre} - {e.especialidad}")
                for e in especialistas
            ]

    async def analizar(e):
        if campo_vacio(sintomas.value):
            error_text.value = "Describa sus síntomas primero."
            page.update()
            return

        resultado_ia.value = "Consultando con IA..."
        page.update()
        
        resultado = await asyncio.to_thread(analizar_sintomas, sintomas.value)
        resultado_ia.value = f"Sugerencia IA: {resultado}"
        page.update()

    def agendar(e):
        error_text.value = ""
        if not fecha_input.value or not hora_input.value or not especialistas_dropdown.value:
            error_text.value = "Complete todos los campos obligatorios."
            page.update()
            return

        try:
            fecha_hora = datetime.strptime(f"{fecha_input.value} {hora_input.value}", "%Y-%m-%d %H:%M")
        except ValueError:
            error_text.value = "Formato de fecha u hora inválido."
            page.update()
            return

        with Session() as db:
            cita = Cita(
                paciente_id=sesion.get("usuario_id"),
                especialista_id=int(especialistas_dropdown.value),
                fecha_hora=fecha_hora,
                sintomas=sintomas.value.strip(),
            )
            db.add(cita)
            db.commit()
            db.refresh(cita)
            sesion["ultima_cita_id"] = cita.id

        from vistas.confirmacion import vista_confirmacion
        vista_confirmacion(page)

    def volver(e):
        from vistas.dashboard_paciente import vista_dashboard_paciente
        vista_dashboard_paciente(page)

    # --- Layout Seguro ---
    page.add(
        ft.Column(
            controls=[
                titulo,
                ft.Divider(height=10, color="transparent"),
                sintomas,
                ft.ElevatedButton(
                    "Consultar Triaje IA",
                    on_click=lambda e: page.run_task(analizar, e)
                ),
                resultado_ia,
                ft.Divider(height=10),
                especialistas_dropdown,
                ft.Row(
                    [fecha_input, hora_input],
                    alignment="center",
                ),
                error_text,
                ft.ElevatedButton(
                    "Confirmar Cita",
                    width=400,
                    on_click=agendar,
                    bgcolor="blue700",
                    color="white"
                ),
                ft.TextButton("Volver al Inicio", on_click=volver),
            ],
            horizontal_alignment="center",
            alignment="center",
            expand=True,
            scroll="auto",
        )
    )
    page.update()
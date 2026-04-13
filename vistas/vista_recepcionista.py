import flet as ft
from base_datos.conexion import Session
from base_datos.modelos import Cita, Especialista, Usuario
from utilidades.sesion import sesion
from werkzeug.security import generate_password_hash

def vista_recepcionista(page: ft.Page):
    page.controls.clear()

    nombre_admin = sesion.get("usuario_nombre")

    def cerrar_sesion(e):
        sesion.clear()
        from vistas.login import vista_login
        vista_login(page)

    def cambiar_estado_cita(cita_id, nuevo_estado, e):
        with Session() as db:
            cita = db.query(Cita).filter_by(id=cita_id).first()
            if cita:
                cita.estado = nuevo_estado
                db.commit()
        vista_recepcionista(page)

    def agregar_doctor(e):
        if not nuevo_nombre.value or not nueva_especialidad.value or not nuevo_email.value:
            page.snack_bar = ft.SnackBar(ft.Text("Complete todos los campos del doctor."))
            page.snack_bar.open = True
            page.update()
            return

        with Session() as db:
            user = Usuario(
                nombre=nuevo_nombre.value,
                apellido="Dr.",
                documento=f"ID-{nuevo_email.value}",
                direccion="Sede Central",
                email=nuevo_email.value,
                telefono="0000000",
                contrasena_hash=generate_password_hash("doctor123"),
                rol="doctor"
            )
            db.add(user)
            db.flush()
            
            perfil = Especialista(
                usuario_id=user.id,
                nombre=f"Dr. {nuevo_nombre.value}",
                especialidad=nueva_especialidad.value
            )
            db.add(perfil)
            db.commit()
        
        vista_recepcionista(page)

    def eliminar_especialista(esp_id, e):
        with Session() as db:
            esp = db.query(Especialista).filter_by(id=esp_id).first()
            if esp:
                db.delete(esp)
                db.commit()
        vista_recepcionista(page)

    def mostrar_citas(e):
        panel_citas.visible = True
        panel_medicos.visible = False
        btn_ver_citas.bgcolor = "blue700"
        btn_ver_medicos.bgcolor = "blue200"
        page.update()

    def mostrar_medicos(e):
        panel_citas.visible = False
        panel_medicos.visible = True
        btn_ver_citas.bgcolor = "blue200"
        btn_ver_medicos.bgcolor = "blue700"
        page.update()

    # --- Panel de Citas ---
    with Session() as db:
        citas = db.query(Cita).all()
        lista_citas = []
        for c in citas:
            lista_citas.append(
                ft.Card(
                    content=ft.Container(
                        padding=ft.padding.all(10),
                        content=ft.Row([
                            ft.Column([
                                ft.Text(f"Paciente: {c.paciente.nombre}", weight="bold"),
                                ft.Text(f"Dr: {c.especialista.nombre} ({c.especialista.especialidad})"),
                                ft.Text(f"Fecha: {c.fecha_hora.strftime('%d/%m %H:%M')} | {c.estado}", size=12),
                            ], expand=True),
                            ft.IconButton(ft.Icons.CHECK, icon_color="green", on_click=lambda e, cid=c.id: cambiar_estado_cita(cid, "confirmada", e)),
                            ft.IconButton(ft.Icons.CANCEL, icon_color="red", on_click=lambda e, cid=c.id: cambiar_estado_cita(cid, "cancelada", e)),
                        ])
                    )
                )
            )
    
    panel_citas = ft.Column(lista_citas, visible=True, scroll="auto", expand=True)

    # --- Panel de Médicos ---
    nuevo_nombre = ft.TextField(label="Nombre Dr.", width=350)
    nuevo_email = ft.TextField(label="Email", width=350)
    nueva_especialidad = ft.TextField(label="Especialidad", width=350)
    
    with Session() as db:
        especialistas = db.query(Especialista).all()
        lista_medicos = []
        for esp in especialistas:
            lista_medicos.append(
                ft.ListTile(
                    title=ft.Text(esp.nombre),
                    subtitle=ft.Text(esp.especialidad),
                    trailing=ft.IconButton(ft.Icons.DELETE, icon_color="red", on_click=lambda e, eid=esp.id: eliminar_especialista(eid, e))
                )
            )
    
    panel_medicos = ft.Column([
        ft.Text("Registrar Nuevo Médico", size=18, weight="bold"),
        nuevo_nombre, nuevo_email, nueva_especialidad,
        ft.ElevatedButton("Dar de Alta", on_click=agregar_doctor, bgcolor="green", color="white"),
        ft.Divider(),
        ft.Text("Doctores Activos", size=18, weight="bold"),
        ft.Column(lista_medicos) # Esta es la lista que queremos ver
    ], visible=False, scroll="auto", expand=True)

    # Botones de navegación
    btn_ver_citas = ft.ElevatedButton("Administrar Citas", on_click=mostrar_citas, bgcolor="blue700", color="white")
    btn_ver_medicos = ft.ElevatedButton("Directorio de Doctores", on_click=mostrar_medicos, bgcolor="blue200", color="white")

    # --- Salida Final ---
    # Usamos Column con scroll="auto" y expand=True para garantizar el scroll
    page.add(
        ft.Row([
            ft.Text(f"Administrador: {nombre_admin}", size=20, weight="bold"),
            ft.IconButton(ft.Icons.LOGOUT, on_click=cerrar_sesion, tooltip="Cerrar sesión"),
        ], alignment="spaceBetween"),
        ft.Divider(),
        ft.Row([btn_ver_citas, btn_ver_medicos], alignment="center"),
        ft.Column([panel_citas, panel_medicos], expand=True, scroll="auto")
    )
    page.update()
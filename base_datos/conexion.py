from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_datos.modelos import Base, Usuario, Especialista
from werkzeug.security import generate_password_hash

ENGINE = create_engine("sqlite:///saludclick.db", echo=False)
Session = sessionmaker(bind=ENGINE)

def iniciar_base_datos():
    Base.metadata.create_all(ENGINE)

def seed_usuarios_y_doctores():
    with Session() as db:
        # 1. Admin / Recepcionista
        admin_email = "admin@saludclick.com"
        if not db.query(Usuario).filter_by(email=admin_email).first():
            admin = Usuario(
                nombre="Admin",
                apellido="SaludClick",
                documento="000000",
                direccion="Sede Central",
                email=admin_email,
                telefono="0000000000",
                contrasena_hash=generate_password_hash("recepcion123"),
                rol="recepcionista"
            )
            db.add(admin)

        # 2. Doctores (Usuarios + Especialistas)
        doctores_data = [
            ("Alejandro", "Ruiz", "ruiz@saludclick.com", "Cardiología"),
            ("Elena", "Martínez", "martinez@saludclick.com", "Pediatría"),
            ("Ricardo", "Silva", "silva@saludclick.com", "Neurología"),
            ("Lucía", "Torres", "torres@saludclick.com", "Dermatología"),
            ("Jorge", "Vargas", "vargas@saludclick.com", "Medicina General"),
        ]

        for nom, ape, mail, esp in doctores_data:
            if not db.query(Usuario).filter_by(email=mail).first():
                user = Usuario(
                    nombre=nom,
                    apellido=ape,
                    documento=f"DOC-{mail}",
                    direccion="Clínica SaludClick",
                    email=mail,
                    telefono="0000000000",
                    contrasena_hash=generate_password_hash("doctor123"),
                    rol="doctor"
                )
                db.add(user)
                db.flush() # Para obtener el ID

                perfil = Especialista(
                    usuario_id=user.id,
                    nombre=f"Dr. {nom} {ape}",
                    especialidad=esp
                )
                db.add(perfil)
        
        db.commit()

# Alias para compatibilidad si se llamaban por separado
def seed_especialistas():
    seed_usuarios_y_doctores()

def seed_usuarios():
    seed_usuarios_y_doctores()
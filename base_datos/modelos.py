from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    documento = Column(String, unique=True, nullable=False)
    direccion = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=False)
    contrasena_hash = Column(String, nullable=False)
    rol = Column(String, default="paciente")
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    citas = relationship("Cita", back_populates="paciente")
    perfil_especialista = relationship("Especialista", back_populates="usuario", uselist=False, cascade="all, delete-orphan")


class Especialista(Base):
    __tablename__ = "especialistas"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id")) # Vínculo para login
    nombre = Column(String, nullable=False)
    especialidad = Column(String, nullable=False)

    usuario = relationship("Usuario", back_populates="perfil_especialista")
    citas = relationship("Cita", back_populates="especialista")


class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    especialista_id = Column(Integer, ForeignKey("especialistas.id"), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    sintomas = Column(String)
    estado = Column(String, default="pendiente")
    creado_en = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    paciente = relationship("Usuario", back_populates="citas")
    especialista = relationship("Especialista", back_populates="citas")
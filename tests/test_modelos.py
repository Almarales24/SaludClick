import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from base_datos.modelos import Base, Usuario, Especialista, Cita
from utilidades.seguridad import hashear_contrasena


def crear_engine_memoria():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    return engine


class TestModeloUsuario(unittest.TestCase):

    def setUp(self):
        self.engine = crear_engine_memoria()
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def _crear_usuario(self, db, email="test@ejemplo.com", documento="12345678", rol="paciente"):
        usuario = Usuario(
            nombre="Juan",
            apellido="Pérez",
            documento=documento,
            direccion="Calle 123",
            email=email,
            telefono="1234567890",
            contrasena_hash=hashear_contrasena("Clave123"),
            rol=rol
        )
        db.add(usuario)
        db.commit()
        return usuario

    def test_crear_usuario_paciente(self):
        with self.Session() as db:
            usuario = self._crear_usuario(db)
            recuperado = db.query(Usuario).filter_by(email="test@ejemplo.com").first()
            self.assertIsNotNone(recuperado)
            self.assertEqual(recuperado.nombre, "Juan")
            self.assertEqual(recuperado.rol, "paciente")

    def test_documento_unico(self):
        with self.Session() as db:
            self._crear_usuario(db, email="a@a.com", documento="99999")
            with self.assertRaises(Exception):
                self._crear_usuario(db, email="b@b.com", documento="99999")

    def test_email_unico(self):
        with self.Session() as db:
            self._crear_usuario(db, email="dup@a.com", documento="11111")
            with self.assertRaises(Exception):
                self._crear_usuario(db, email="dup@a.com", documento="22222")

    def test_rol_default_es_paciente(self):
        with self.Session() as db:
            usuario = Usuario(
                nombre="Ana",
                apellido="Gómez",
                documento="55555",
                direccion="Av. 456",
                email="ana@ejemplo.com",
                telefono="9876543210",
                contrasena_hash=hashear_contrasena("Clave123")
            )
            db.add(usuario)
            db.commit()
            recuperado = db.query(Usuario).filter_by(email="ana@ejemplo.com").first()
            self.assertEqual(recuperado.rol, "paciente")

    def test_creado_en_se_asigna_automaticamente(self):
        with self.Session() as db:
            usuario = self._crear_usuario(db)
            self.assertIsNotNone(usuario.creado_en)
            self.assertIsInstance(usuario.creado_en, datetime)


class TestModeloEspecialista(unittest.TestCase):

    def setUp(self):
        self.engine = crear_engine_memoria()
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_crear_especialista_vinculado_a_usuario(self):
        with self.Session() as db:
            usuario = Usuario(
                nombre="Dr. Luis",
                apellido="Hernández",
                documento="DOC-001",
                direccion="Clinica",
                email="luis@clinica.com",
                telefono="1111111111",
                contrasena_hash=hashear_contrasena("Doctor123"),
                rol="doctor"
            )
            db.add(usuario)
            db.flush()

            especialista = Especialista(
                usuario_id=usuario.id,
                nombre="Dr. Luis Hernández",
                especialidad="Cardiología"
            )
            db.add(especialista)
            db.commit()

            resultado = db.query(Especialista).filter_by(especialidad="Cardiología").first()
            self.assertIsNotNone(resultado)
            self.assertEqual(resultado.nombre, "Dr. Luis Hernández")
            self.assertEqual(resultado.usuario_id, usuario.id)

    def test_relacion_usuario_especialista(self):
        with self.Session() as db:
            usuario = Usuario(
                nombre="Dra. María",
                apellido="López",
                documento="DOC-002",
                direccion="Clinica",
                email="maria@clinica.com",
                telefono="2222222222",
                contrasena_hash=hashear_contrasena("Doctor123"),
                rol="doctor"
            )
            db.add(usuario)
            db.flush()

            especialista = Especialista(
                usuario_id=usuario.id,
                nombre="Dra. María López",
                especialidad="Pediatría"
            )
            db.add(especialista)
            db.commit()

            db.refresh(usuario)
            self.assertIsNotNone(usuario.perfil_especialista)
            self.assertEqual(usuario.perfil_especialista.especialidad, "Pediatría")


class TestModeloCita(unittest.TestCase):

    def setUp(self):
        self.engine = crear_engine_memoria()
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def _setup_datos(self, db):
        paciente = Usuario(
            nombre="Carlos",
            apellido="Ramírez",
            documento="PAC-001",
            direccion="Casa",
            email="carlos@paciente.com",
            telefono="3333333333",
            contrasena_hash=hashear_contrasena("Paciente1"),
            rol="paciente"
        )
        db.add(paciente)

        doctor_user = Usuario(
            nombre="Dr. Pedro",
            apellido="Soto",
            documento="DOC-003",
            direccion="Clinica",
            email="pedro@clinica.com",
            telefono="4444444444",
            contrasena_hash=hashear_contrasena("Doctor123"),
            rol="doctor"
        )
        db.add(doctor_user)
        db.flush()

        especialista = Especialista(
            usuario_id=doctor_user.id,
            nombre="Dr. Pedro Soto",
            especialidad="Neurología"
        )
        db.add(especialista)
        db.flush()

        return paciente, especialista

    def test_crear_cita(self):
        with self.Session() as db:
            paciente, especialista = self._setup_datos(db)
            cita = Cita(
                paciente_id=paciente.id,
                especialista_id=especialista.id,
                fecha_hora=datetime(2026, 5, 15, 10, 0),
                sintomas="Dolor de cabeza",
                estado="pendiente"
            )
            db.add(cita)
            db.commit()

            resultado = db.query(Cita).first()
            self.assertIsNotNone(resultado)
            self.assertEqual(resultado.sintomas, "Dolor de cabeza")
            self.assertEqual(resultado.estado, "pendiente")

    def test_estado_default_cita(self):
        with self.Session() as db:
            paciente, especialista = self._setup_datos(db)
            cita = Cita(
                paciente_id=paciente.id,
                especialista_id=especialista.id,
                fecha_hora=datetime(2026, 5, 20, 9, 0)
            )
            db.add(cita)
            db.commit()

            resultado = db.query(Cita).first()
            self.assertEqual(resultado.estado, "pendiente")

    def test_relacion_cita_paciente(self):
        with self.Session() as db:
            paciente, especialista = self._setup_datos(db)
            cita = Cita(
                paciente_id=paciente.id,
                especialista_id=especialista.id,
                fecha_hora=datetime(2026, 6, 1, 11, 0)
            )
            db.add(cita)
            db.commit()

            db.refresh(cita)
            self.assertEqual(cita.paciente.nombre, "Carlos")

    def test_relacion_cita_especialista(self):
        with self.Session() as db:
            paciente, especialista = self._setup_datos(db)
            cita = Cita(
                paciente_id=paciente.id,
                especialista_id=especialista.id,
                fecha_hora=datetime(2026, 6, 1, 11, 0)
            )
            db.add(cita)
            db.commit()

            db.refresh(cita)
            self.assertEqual(cita.especialista.especialidad, "Neurología")


if __name__ == "__main__":
    unittest.main()

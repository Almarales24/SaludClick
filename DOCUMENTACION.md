# 🩺 Documentación SaludClick

SaludClick es un sistema integral de agendamiento y gestión de citas médicas desarrollado con **Python**, **Flet** y **SQLite**, integrando Inteligencia Artificial (**Gemini**) para el triaje inicial de pacientes.

---

## 🚀 Cómo Ejecutar el Proyecto

1. Asegúrate de tener instalado Python 3.13.
2. Instala las dependencias: `pip install -r requirements.txt`
3. Configura tu API Key de Gemini en el archivo `.env`:
   ```
   GOOGLE_API_KEY=tu_api_key_aqui
   ```
4. Ejecuta la aplicación: `python main.py`

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una estructura modular para facilitar su mantenimiento:

```
SaludClick - Prueba/
│
├── main.py                     # Punto de entrada de la aplicación
├── requirements.txt            # Dependencias del proyecto
├── saludclick.db               # Base de datos SQLite (generada automáticamente)
├── .env                        # Variables de entorno (API Key Gemini)
├── DOCUMENTACION.md            # Este archivo
│
├── base_datos/
│   ├── modelos.py              # Modelos ORM: Usuario, Especialista, Cita
│   └── conexion.py             # Motor SQLAlchemy, inicialización y seed de datos
│
├── utilidades/
│   ├── seguridad.py            # Hashing y verificación de contraseñas (Werkzeug)
│   ├── validaciones.py         # Validaciones de email, teléfono, contraseña y campos
│   ├── sesion.py               # Diccionario global de sesión activa
│   └── ia_gemini.py            # Integración con la API de Gemini (google-genai)
│
├── vistas/
│   ├── login.py                # Vista de inicio de sesión
│   ├── registro.py             # Vista de registro de nuevos pacientes
│   ├── dashboard_paciente.py   # Panel principal del paciente
│   ├── agendar_cita.py         # Flujo de agendamiento de cita con triaje IA
│   ├── confirmacion.py         # Confirmación de cita agendada
│   ├── vista_doctor.py         # Panel del médico (agenda y consultas)
│   └── vista_recepcionista.py  # Panel del administrador/recepción
│
└── tests/
    ├── test_validaciones.py    # Pruebas unitarias de validaciones (18 casos)
    ├── test_seguridad.py       # Pruebas unitarias de seguridad (8 casos)
    └── test_modelos.py         # Pruebas unitarias de modelos ORM (9 casos)
```

---

## 👥 Roles de Usuario y Credenciales de Prueba

### 👨‍💼 Administrador (Recepción)
Tiene control total sobre las citas y el personal médico.
- **Correo**: `admin@saludclick.com`
- **Contraseña**: `recepcion123`
- **Funciones**: Confirmar/Cancelar citas, añadir o eliminar doctores del sistema.

### 🩺 Médicos (Doctores)
Cada doctor tiene su propio acceso para ver su agenda personalizada.
- **Doctores disponibles**:

| Correo | Especialidad |
|---|---|
| `ruiz@saludclick.com` | Cardiología |
| `martinez@saludclick.com` | Pediatría |
| `silva@saludclick.com` | Neurología |
| `torres@saludclick.com` | Dermatología |
| `vargas@saludclick.com` | Medicina General |

- **Contraseña**: `doctor123` (para todos por defecto)
- **Funciones**: Ver citas asignadas, consultar síntomas analizados por la IA, finalizar consultas.

### 👤 Pacientes
Usuarios que se registran públicamente a través de la aplicación.
- **Funciones**: Agendar citas, describir síntomas para análisis por IA, ver historial de citas.

---

## 🤖 Integración con IA (Gemini)

El sistema utiliza el modelo `gemini-2.0-flash` para analizar los síntomas descritos por el paciente.

- **Flujo**: Al descripción de síntomas en "Agendar Cita", la IA sugiere la especialidad médica más adecuada antes de que el paciente elija al doctor.
- **Requisito**: Tener una API Key válida de Google AI Studio configurada en `.env` como `GOOGLE_API_KEY`.

---

## 🗄️ Modelo de Datos

### `Usuario`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer PK | ID único |
| `nombre` / `apellido` | String | Nombre completo |
| `documento` | String UNIQUE | Número de documento de identidad |
| `email` | String UNIQUE | Correo electrónico |
| `telefono` | String | Número de teléfono |
| `contrasena_hash` | String | Contraseña hasheada con Werkzeug |
| `rol` | String | `paciente`, `doctor` o `recepcionista` |
| `creado_en` | DateTime | Fecha de creación (UTC) |

### `Especialista`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer PK | ID único |
| `usuario_id` | FK → Usuario | Vínculo para login |
| `nombre` | String | Nombre completo con prefijo Dr./Dra. |
| `especialidad` | String | Especialidad médica |

### `Cita`
| Campo | Tipo | Descripción |
|---|---|---|
| `id` | Integer PK | ID único |
| `paciente_id` | FK → Usuario | Paciente que agenda |
| `especialista_id` | FK → Especialista | Doctor asignado |
| `fecha_hora` | DateTime | Fecha y hora de la cita |
| `sintomas` | String | Síntomas descritos por el paciente |
| `estado` | String | `pendiente`, `confirmada` o `finalizada` |
| `creado_en` | DateTime | Fecha de creación (UTC) |

---

## 🧪 Pruebas Unitarias

Las pruebas se ubican en la carpeta `tests/` y se ejecutan con `pytest`.

```bash
python -m pytest tests/ -v
```

**Resultado esperado**: 43 pruebas pasadas, 0 fallidas.

| Archivo | Módulo cubierto | Casos |
|---|---|---|
| `test_validaciones.py` | `utilidades/validaciones.py` | 18 |
| `test_seguridad.py` | `utilidades/seguridad.py` | 8 |
| `test_modelos.py` | `base_datos/modelos.py` | 9 |

Los modelos se prueban con una base de datos SQLite **en memoria** para no modificar `saludclick.db`.

---

## 🛠️ Tecnologías Utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.13 | Lenguaje principal |
| Flet (Flutter) | Interfaz gráfica |
| SQLite + SQLAlchemy | Base de datos y ORM |
| Werkzeug | Hashing seguro de contraseñas |
| google-genai | SDK de Gemini (IA) |
| python-dotenv | Manejo de variables de entorno |
| pytest | Pruebas unitarias |

---

*Desarrollado para el Proyecto de Ingeniería de Software 1.*

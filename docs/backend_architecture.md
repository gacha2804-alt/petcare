# backend_architecture.md

## 1. Objetivo
Arquitectura FastAPI + PostgreSQL (SQLAlchemy/Alembic), integración Google Gemini (google-genai) con guardrails + Function Calling/Tool Use, y servicio Cloudinary.

## 2. Stack Backend
- FastAPI, Uvicorn/Gunicorn
- SQLAlchemy 2.0, Alembic
- PostgreSQL
- Pydantic v2
- python-jose/passlib/bcrypt
- google-genai
- cloudinary
- httpx, python-multipart
- psycopg

## 3. Estructura
```
backend/
├── alembic/
├── app/
│   ├── api/v1/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── cloudinary_service.py
│   │   └── agenda_service.py
│   ├── tools/
│   │   ├── agenda_tools.py
│   │   └── cita_tools.py
│   └── main.py
└── requirements.txt
```

## 4. Modelo de Datos (SQLAlchemy)
### Usuarios/Roles
- `usuarios(id, nombre, apellido, correo_electronico, telefono, password_hash, fecha_registro, activo)`
- `roles(id, nombre_rol)` (propietario, veterinario, personal_clinica, administrador)
- `usuario_roles(id_usuario, id_rol, fecha_asignacion)`

### Mascotas
- `mascotas(id, id_propietario FK, nombre, especie, sexo, fecha_nacimiento, datos_identificatorios, imagen_url, fecha_registro)`  
  **imagen_url debe apuntar a Cloudinary (secure_url)**

### Historial/Consultas
- `historial_clinico(id, id_mascota FK, id_propietario FK, fecha_creacion, observaciones_generales)`
- `consultas_veterinarias(id, ..., motivo_consulta, diagnostico_registrado, observaciones, ...)`
- `vacunas(id, id_mascota FK, nombre_vacuna, fecha_aplicacion, fecha_proxima_recomendada, ...)`
- `desparasitaciones(id, id_mascota FK, tipo_tratamiento, producto, fecha_tratamiento, fecha_proxima_recomendada, ...)`
- `permisos_historial_clinico(id, id_mascota FK, id_veterinario FK, fecha_autorizacion, fecha_revocacion, activo)`

### Sedes/Agenda/Citas
- `sedes(id, nombre, direccion, telefono, activa, es_una_de_dos_sedes)` → Sede 1 y Sede 2
- `agenda(id, id_sede FK, id_veterinario FK, fecha, activa)`
- `disponibilidad(id, id_agenda FK, fecha, hora_inicio, hora_fin, disponible, ocupado)`
- `citas(id, id_mascota FK, id_propietario FK, id_sede FK, id_veterinario FK, id_agenda FK, id_disponibilidad FK, fecha_cita, hora_cita, motivo_consulta, estado, fecha_solicitud, fecha_confirmacion)`

### Chat IA
- `chat_conversaciones(id, id_usuario FK, id_mascota FK, id_cita FK, fecha_inicio, fecha_ultima_actividad, estado, urgencia_detectada, clasificacion_urgencia, derivacion_requerida)`
- `chat_mensajes(id, id_conversacion FK, remitente, contenido, fecha_envio, contiene_informacion_clinica, es_orientacion_inicial)`

### Auditoría
- `auditoria(id, id_usuario FK, tipo_operacion, entidad_afectada, id_registro_afectado, fecha_hora, detalles)`

## 5. Google Gemini - System Prompt + Tools
### System Prompt
Incluir reglas inquebrantables:
- Emergencias primero (sangrado/asfixia/convulsiones/letargo severo) → alerta inmediata, NO condicionar agendamiento
- NUNCA diagnóstico definitivo
- NUNCA medicamentos humanos / inducir vómito
- Requiere `id_mascota` obligatoria
- Si requiere valoración → justificar + ofrecer agendar con Sede 1/Sede 2 usando disponibilidad REAL
- No garantizar seguridad si no hay alarmas
- Transparente sobre limitaciones

### Function Calling / Tool Use
- `consultar_disponibilidad(sede_id, fecha)` → slots libres desde BD
- `reservar_cita(datos_cita)` → transacción atómica con `SELECT ... FOR UPDATE`, marcar `disponibilidad.ocupado=true`, crear cita, evitar duplicados
- `obtener_mascota_contexto(id_mascota)` → contexto mínimo

### Guardrails
- Bloquear sin mascota válida
- Post-proceso respuestas peligrosas
- Enviar mínimo al LLM
- Auditoría si info clínica

## 6. Cloudinary
- Servicio con `upload_image` → retorna `secure_url`, `public_id`
- Endpoint `POST /cloudinary/upload` (auth, validar tipo/tamaño)
- **TODAS** las imágenes a Cloudinary

## 7. Endpoints principales
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/auth/login` | JWT |
| GET/POST | `/mascotas` | CRUD + imagen Cloudinary |
| GET | `/historial/{mascota_id}` | Historial autorizado |
| GET | `/agenda/disponibilidad` | Disponibilidad 2 sedes |
| POST | `/citas` | Crear cita con validación |
| POST/GET | `/chat/conversaciones` | Crear/listar conversación |
| POST/GET | `/chat/conversaciones/{id}/mensajes` | Mensajes + IA |
| POST | `/cloudinary/upload` | Subir imagen |

## 8. Reglas Backend
- Chat requiere `id_mascota` válido
- Emergencia → no agendar en ese flujo
- Transacción + lock al reservar
- Validar solapamientos
- RBAC 4 roles
- Auditoría operaciones críticas

## 9. .env
```env
DATABASE_URL=postgresql+psycopg://...
SECRET_KEY=...
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.5-flash
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...
CORS_ORIGINS=http://localhost:3000
``` 

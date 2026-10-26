# PLAN DE DESARROLLO TÉCNICO — PETCARE

## Resumen del Cronograma y Fases
```
[Fase 1] Base de Datos & Backend Core (Semanas 1-2)
 └── [Fase 2] Frontend Base, Autenticación & Cloudinary (Semanas 3-4)
      └── [Fase 3] Módulo Clínico & Agendamiento Tradicional (Semanas 5-6)
           └── [Fase 4] Asistente Gemini API + Guardrails (Semanas 7-8)
                └── [Fase 5] Agendamiento Integrado en Chat (Semanas 9-10)
                     └── [Fase 6] Testing, Auditoría & Despliegue (Semanas 11-12)
```

---

## FASE 1: Infraestructura Backend, PostgreSQL y Auth Core
> **Objetivo:** Tener la base de datos migrada, autenticación JWT con RBAC y modelos de SQLAlchemy listos.

### Tasks Backend
1. **Configuración de Proyecto FastAPI:**
   - Estructurar directorio `/app` con `main.py`, `/core`, `/db`, `/models`, `/schemas`, `/api`.
   - Configurar variables de entorno (`.env`) e inicializar Alembic.
2. **Esquema Relacional PostgreSQL (SQLAlchemy):**
   - Crear modelos: `Usuario`, `Rol`, `UsuarioRol`, `Mascota`, `HistorialClinico`, `ConsultaVeterinaria`, `Vacuna`, `Desparasitacion`, `PermisoHistorialClinico`.
   - Crear modelos para sedes y agenda: `Sede` (Sede 1 y Sede 2), `Agenda`, `Disponibilidad`, `Cita`.
   - Crear modelos de chat: `ChatConversacion`, `ChatMensaje`, `Auditoria`.
   - Generar y ejecutar migración inicial con Alembic.
3. **Autenticación y Seguridad (RBAC):**
   - Endpoint `POST /api/v1/auth/login` (JWT token).
   - Middleware de RBAC para validar los 4 roles: `propietario`, `veterinario`, `personal_clinica`, `administrador` (RNF-10).

### Entregable Fase 1
Base de datos relacional desplegada localmente con datos semilla (Sede 1, Sede 2 y Roles) + API funcional de registro/login.

---

## FASE 2: Frontend Base, Autenticación y Cloudinary
> **Objetivo:** Construir la interfaz base con la paleta de colores oficial, layout responsive y carga centralizada de imágenes en Cloudinary.

### Tasks Frontend
1. **Setup Next.js & Tailwind CSS:**
   - Configurar CSS variables en `globals.css` y la paleta de colores obligatoria (`#16A34A`, `#166534`, `#1E3A8A`, `#F8FAFC`, `#FFFFFF`, `#0F172A`, `#E2E8F0`) en `tailwind.config.ts`.
   - Crear Layout principal con `Header` y `Sidebar` adaptables (Desktop/Tablet/Mobile - RNF-05).
2. **Módulo de Autenticación & Layouts:**
   - Vistas `/login` y `/register`.
   - Zustand store para manejo de sesión del tutor/usuario.
3. **Integración con Cloudinary (Servicio Centralizado):**
   - **Backend:** Endpoint `POST /api/v1/cloudinary/upload` con librería oficial `cloudinary`.
   - **Frontend:** Componente reutilizable `ImageUpload.tsx` que maneja preview y obtiene `secure_url`.
   - **Regla:** Ninguna imagen se guarda en el servidor local; todas apuntan a Cloudinary (RF-01).

### Tasks Módulo Mascotas (RF-01)
1. Endpoint `POST /api/v1/mascotas` y `GET /api/v1/mascotas`.
2. Componente `PetForm.tsx` e interfaz `/dashboard/mascotas` con carga de foto obligatoria a Cloudinary.

### Entregable Fase 2
Dashboard navegable, flujo de login/registro activo, CRUD funcional de mascotas con fotos alojadas en Cloudinary.

---

## FASE 3: Módulo Clínico, Permisos y Agendamiento Tradicional
> **Objetivo:** Implementar la gestión de historial médico, vacunas, desparasitaciones y motor de citas sin colisiones.

### Tasks Módulo Clínico (RF-02 a RF-08)
1. **Historial y Consultas:**
   - Endpoints para consultar historial (`GET /historial/{mascota_id}`) y registrar consulta (`POST /consultas`).
   - Vista `/dashboard/historial` con componentes vacíos claros si no hay registros (HU-02).
2. **Permisos y Seguridad (RF-03, RNF-01):**
   - Endpoints para autorizar y revocar acceso de veterinarios (`permisos_historial_clinico`).
   - Validaciones en backend: solo el propietario o veterinario autorizado puede leer la historia clínica.
3. **Vacunas, Desparasitaciones y Recordatorios:**
   - Endpoints y tablas de consulta (`RF-06`, `RF-07`).
   - Cron Job / Servicio backend para identificar vencimientos próximos y generar alertas (`RF-08`).

### Tasks Agendamiento Físico de Citas (RF-05, RF-14, RNF-14)
1. API `GET /api/v1/agenda/disponibilidad?sede_id={id}&fecha={yyyy-mm-dd}`.
2. Lógica de Reserva Atómica (`POST /api/v1/citas`):
   - Uso de `SELECT ... FOR UPDATE` en PostgreSQL para bloquear el slot de disponibilidad y evitar reservas duplicadas simultáneas.
3. Interfaz `/dashboard/citas` con componentes `SedeSelector.tsx` (Sede 1 vs Sede 2) y `SlotPicker.tsx`.

### Entregable Fase 3
Historial clínico con permisos funcionales y módulo de agendamiento directo desde la web sin solapamientos.

---

## FASE 4: Asistente Gemini API y Guardrails de Seguridad
> **Objetivo:** Integrar la SDK `google-genai`, configurar el System Prompt con barreras clínicas y estructurar las herramientas de Function Calling.

### Tasks Backend (Gemini Service)
1. **Instalación y Setup SDK:**
   - Integrar `google-genai` usando el modelo `gemini-2.5-flash`.
2. **Implementación de System Prompt & Guardrails (RF-11, RF-12, RNF-11 a RNF-13):**
   - Inyección de reglas inquebrantables:
     - Detección prioritaria de emergencias (sangrado, asfixia, convulsiones).
     - Prohibición de diagnósticos definitivos, recetas humanas e inducción de vómito.
     - Obligatoriedad de vincular la conversación a un `id_mascota` activo.
3. **Function Calling / Tool Use (`agenda_tools.py`):**
   - Definir schema de tools para Gemini:
     - `consultar_disponibilidad(sede_id: int, fecha: str)`
     - `reservar_cita(id_mascota: int, sede_id: int, fecha_hora: str, motivo: str)`
4. **Endpoints de Chat:**
   - `POST /api/v1/chat/conversaciones` (crea sesión asociada a mascota).
   - `POST /api/v1/chat/conversaciones/{id}/mensajes` (procesa texto, consulta Gemini, ejecuta tools y retorna respuesta).

### Entregable Fase 4
API de Chat capaz de procesar lenguaje natural, aplicar guardrails de seguridad veterinaria e invocar funciones de disponibilidad de base de datos.

---

## FASE 5: Agendamiento Integrado en Chat (Frontend & Flujo Completo)
> **Objetivo:** Conectar el frontend con el asistente de IA para permitir el triaje y la reserva de citas sin salir de la conversación.

### Tasks Frontend (`/dashboard/chat/[mascotaId]`)
1. **Selector de Mascota Obligatorio (RF-09):**
   - Interfaz en `/dashboard/chat` que exige seleccionar una mascota antes de abrir la ventana de conversación.
2. **Componente de Chat (`ChatWindow.tsx` & `MessageBubble.tsx`):**
   - Renderizado de mensajes del usuario y respuestas empáticas del asistente.
3. **Manejo de Alertas de Emergencia (RF-12):**
   - Si la IA detecta urgencia (`urgencia_detectada = True`), renderizar un banner destacado (`EmergencyAlert.tsx`) priorizando atención veterinaria presencial e inhabilitando el agendamiento estándar.
4. **Widget de Agendamiento Interactivo (`AppointmentCard.tsx` - RF-13 a RF-17):**
   - Si Gemini recomienda valoración presencial, el mensaje renderiza un widget dinámico dentro del chat.
   - El tutor selecciona entre Sede 1 y Sede 2, consulta slots en tiempo real, confirma los datos obligatorios (motivo, mascota) y realiza la reserva atómica en PostgreSQL.

```
[Usuario escribe síntoma]
       │
       ▼
[Gemini procesa con Guardrails]
       │
       ├──► ¿Es Emergencia? ──► [SÍ] ──► Muestra Alerta Urgente (Sin agendamiento)
       │
       └──► ¿Requiere Cita? ──► [SÍ] ──► Despliega AppointmentCard (Sede 1/2 + Slots)
                                                  │
                                                  ▼
                                      [Reserva Atómica en PostgreSQL]
```

### Entregable Fase 5
Flujo de chat 100% interactivo capaz de responder consultas de orientación, alertar emergencias y concretar citas reales desde el hilo de conversación.

---

## FASE 6: Testing, Auditoría, Hardening y Despliegue
> **Objetivo:** Garantizar la seguridad de la información, el cumplimiento de RNF y la estabilidad del sistema.

### Tasks
1. **Auditoría y Trazabilidad (RNF-03, RNF-07):**
   - Validar que cada cambio en citas, permisos e historial escriba un registro en la tabla `auditoria` con usuario, timestamp y detalle.
2. **Pruebas de Estrés y Concurrencia (RNF-14):**
   - Testear reservas simultáneas en el mismo horario para verificar que las transacciones con lock (`FOR UPDATE`) eviten citas duplicadas.
3. **Pruebas de Inyección de Prompts en IA (RNF-13):**
   - Validar que Gemini no rompa los guardrails ante intentos de manipular su comportamiento (e.g., pedir recetas de medicamentos humanos).
4. **Validación de Accesibilidad y Responsive (RNF-05, RNF-06):**
   - Verificación de contraste de color con la paleta `#16A34A`, `#1E3A8A`, etc., y correcto funcionamiento en navegadores móviles.

### Entregable Fase 6
Sistema PetCare probado, auditado y listo para producción con la documentación técnica y manuales correspondientes.
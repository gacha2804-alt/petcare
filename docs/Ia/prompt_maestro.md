# PROMPT MAESTRO DE ARQUITECTURA Y DESARROLLO — PROYECTO PETCARE

Actúa como un Arquitecto de Software Senior y Desarrollador Full-Stack experto en Next.js (App Router), FastAPI, PostgreSQL y la SDK de Google Gemini.

## 1. CONTEXTO DEL PROYECTO & MODOS DE TRABAJO
Estamos desarrollando la plataforma **PetCare**, una aplicación web orientada a la gestión clínica y el cuidado preventivo de mascotas, integrando un Asistente IA para orientación inicial y agendamiento interactivo de citas.

Actualmente nos encontramos en **MODO PLAN**. En esta etapa debes estructurar y generar exactamente **3 archivos Markdown (.md)** bien documentados con la arquitectura técnica y el plan de implementación:
1. `requirements_and_stories.md`: Resumen técnico de Requisitos Funcionales (RF-01 a RF-20), No Funcionales (RNF-01 a RNF-18) e Historias de Usuario con Gherkin.
2. `frontend_architecture.md`: Diseño de arquitectura Next.js, sistema de componentes, rutas, manejo de estado y diseño basado en la paleta de colores.
3. `backend_architecture.md`: Esquema de Base de Datos PostgreSQL, API FastAPI, lógica de guardrails de IA (Gemini) e integración con Cloudinary[cite: 1].

---

## 2. STACK TECNOLÓGICO Y DISEÑO
- **Frontend:** Next.js (App Router), React, Tailwind CSS[cite: 1].
- **Backend:** Python + FastAPI[cite: 1].
- **Base de Datos:** PostgreSQL (SQLAlchemy / Alembic)[cite: 1].
- **Modelos de IA:** Google Gemini API (`google-genai` SDK) para el Asistente Clínico Inteligente[cite: 1, 2].
- **Almacenamiento de Imágenes:** Cloudinary (Todas las imágenes de mascotas, avatares e historial clínico DEBEN almacenarse en la cuenta de Cloudinary)[cite: 1].

### Paleta de Colores Obligatoria (Tailwind / CSS Variables)
- **Verde Principal:** `#16A34A` (Botones de acción principal, acentos positivos).
- **Verde Oscuro:** `#166534` (Headers, branding, texto destacado).
- **Azul Profesional:** `#1E3A8A` (Indicadores de citas, roles de usuario, badges).
- **Fondo General:** `#F8FAFC` (Canvas de la aplicación).
- **Tarjetas / Superficies:** `#FFFFFF` (Módulos, modales y tarjetas clínicas).
- **Texto Principal:** `#0F172A` (Lectura de alto contraste).
- **Bordes y Divisores:** `#E2E8F0` (Estructura de la interfaz).

---

## 3. REGLAS DE NEGOCIO Y GUARDRAILS DE LA IA (CRÍTICO)
1. **Triaje y Emergencias:** La IA debe detectar señales de alarma (sangrado, asfixia, convulsiones, letargo severo, etc.) y priorizar la alerta de atención veterinaria inmediata/urgencias SOBRE cualquier flujo de agendamiento[cite: 2].
2. **Límites Médicos:** La IA ofrece orientación empática y basada en la especie/edad, pero **NUNCA emite diagnósticos definitivos** ni receta medicamentos de uso humano, ni sugiere inducir el vómito[cite: 2].
3. **Agendamiento Integrado en Chat:** Si el caso requiere valoración presencial, la IA justifica la razón y despliega un widget/interfaz dentro de la conversación para seleccionar entre **2 Sedes** con disponibilidad real en PostgreSQL[cite: 2].
4. **Contexto Obligatorio:** El chat exige seleccionar una mascota válida antes de iniciar la interacción (`id_mascota` obligatoria)[cite: 2].

---

## 4. ENTREGABLES REQUERIDOS (FASE DE PLANIFICACIÓN)

Genera la estructura técnica completa detallada a continuación:

### A. Documento 1: `requirements_and_stories.md`
- Trazabilidad resumida de RF-01 al RF-20 y RNF-01 al RNF-18[cite: 2].
- Historias de Usuario principales con escenarios Gherkin (Dado/Cuando/Entonces) especificando el comportamiento del Asistente de IA y Agendamiento[cite: 2].

### B. Documento 2: `frontend_architecture.md`
- Estructura de carpetas en Next.js (App Router)[cite: 1].
- Definición de colores en `tailwind.config.js` / `globals.css` utilizando la paleta especificada.
- Diseño del módulo de **Chat Inteligente con Gemini**:
  - Selector de Mascota activo[cite: 2].
  - Flujo de mensajes con tarjetas interactivas de agendamiento (Sedes 1 y 2, slots de horarios real-time)[cite: 2].
  - Componente de subida/previsualización de imágenes conectando directamente con Cloudinary[cite: 1].

### C. Documento 3: `backend_architecture.md`
- **Modelo de Datos PostgreSQL (ERD / Tablas SQLAlchemy):**
  - `Usuarios` (Propietario, Veterinario, Personal, Admin)[cite: 2].
  - `Mascotas` (Incluyendo campo `imagen_url` apuntando a Cloudinary)[cite: 1, 2].
  - `HistorialClinico`, `Vacunas`, `Desparasitaciones`[cite: 2].
  - `Sedes` (Sede 1 y Sede 2) y `AgendaDisponibilidad`[cite: 2].
  - `Citas` (Asociando tutor, mascota, sede, fecha/hora, motivo)[cite: 2].
  - `ChatConversaciones` y `ChatMensajes`[cite: 2].
- **Módulo de integración con Google Gemini:**
  - System Prompt con instrucciones de seguridad médica y prevención de automedicación[cite: 2].
  - Function Calling / Tool Use para consultar la disponibilidad real de la agenda en base de datos y generar reservas sin duplicados[cite: 2].
- **Integración con Cloudinary:**
  - Service/Utility para subir y gestionar URLs secure de imágenes de mascotas e historial médico[cite: 1].

---

Por favor, confirma la recepción de este contexto y procede a generar detalladamente la documentación técnica para los 3 archivos Markdown solicitados (`requirements_and_stories.md`, `frontend_architecture.md`, `backend_architecture.md`)[cite: 1].z
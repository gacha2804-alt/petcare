# requirements_and_stories.md

## 1. Objetivo
Documentar requisitos funcionales/no funcionales, reglas de negocio y guardrails para PetCare (orientación IA + agendamiento desde chat). Basado en `docs/Ia/requisitos.md`, historias existentes y requerimientos del prompt.

## 2. Requisitos Funcionales (RF-01 a RF-20)
| ID | Nombre | Descripción | Actor | Prioridad |
|---|---|---|---|---|
| RF-01 | Registro de mascota | Registrar nombre, especie, sexo, fecha nacimiento, datos identificatorios. | Tutor | Must |
| RF-02 | Consulta historial clínico | Consultar historial autorizado de mascota. | Tutor | Must |
| RF-03 | Autorización acceso veterinario | Autorizar/consultar/revocar acceso al historial por mascota. | Tutor | Must |
| RF-04 | Registro consulta veterinaria | Registrar consulta (motivo/diagnóstico/observaciones). | Veterinario autorizado | Must |
| RF-05 | Solicitud y confirmación de citas | Solicitar cita seleccionando sede/veterinario/horario disponible. | Tutor | Must |
| RF-06 | Consulta vacunas | Ver vacunas con fechas y próxima recomendada. | Tutor | Must |
| RF-07 | Consulta desparasitaciones | Ver desparasitaciones con fechas. | Tutor | Should |
| RF-08 | Recordatorios preventivos | Generar alertas para vacunas/desparasitaciones próximas. | Sistema/Personal | Should |
| RF-09 | Selección mascota en chat | Seleccionar mascota válida antes de iniciar chat IA. | Tutor | Must |
| RF-10 | Registro motivo consulta | Capturar motivo en lenguaje natural con preguntas mínimas. | Tutor/IA | Must |
| RF-11 | Orientación inicial IA | Orientación empática basada en especie/edad/antecedentes, sin diagnóstico. | IA | Must |
| RF-12 | Detección alarmas/urgencias | Detectar señales, priorizar urgencia sobre agendamiento. | IA | Must |
| RF-13 | Recomendación valoración presencial | Justificar y ofrecer "Agendar cita" sin presión. | IA/Tutor | Must |
| RF-14 | Sedes y disponibilidad real | Mostrar 2 sedes con disponibilidad real desde PostgreSQL. | Sistema/Tutor | Must |
| RF-15 | Agendamiento integrado en chat | Completar reserva desde conversación sin salir. | Tutor/Sistema | Must |
| RF-16 | Confirmación con datos obligatorios | Validar motivo/mascota/datos antes de confirmar. | Sistema/Tutor | Must |
| RF-17 | Asociación cita | Asociar a tutor/mascota/sede/agenda. | Sistema | Must |
| RF-18 | Consulta cita en módulos | Visible para tutor y personal autorizado. | Tutor/Personal | Must |
| RF-19 | Errores/cancelación/disponibilidad | Gestionar sin duplicados/inconsistencias. | Sistema/Tutor | Must |
| RF-20 | Derivación/escalamiento | Escalar a humano si supera orientación; documentar si no implementado. | Sistema/Personal | Should |

## 3. Requisitos No Funcionales (RNF-01 a RNF-18)
| ID | Requisito | Criterio |
|---|---|---|
| RNF-01 | Acceso restringido historial | Solo propietario/veterinarios autorizados |
| RNF-02 | Protección credenciales/datos | Auth + almacenamiento seguro, mínimo en IA/logs |
| RNF-03 | Integridad/auditoría | Cambios trazados con usuario/fecha |
| RNF-04 | Rendimiento | Respuesta fluida chat/reserva (razonable) |
| RNF-05 | Multiplataforma | Web responsive (desktop/tablet/móvil) |
| RNF-06 | Usabilidad | Feedback/errores/confirmaciones |
| RNF-07 | Trazabilidad | Asociar a usuario/timestamp/entidad |
| RNF-08 | Respaldo/recuperación | Críticos recuperables |
| RNF-09 | Privacidad IA | Mínimos datos, políticas de uso |
| RNF-10 | RBAC (4 roles) | Validación por rol; definir admin |
| RNF-11 | Sin diagnóstico definitivo | Nota de limitación visible |
| RNF-12 | Prevención peligros | No automedicación/vómito/medicamentos humanos |
| RNF-13 | Protección IA | Guardrails contra inyecciones |
| RNF-14 | Agenda sin duplicados | Validar solapamientos |
| RNF-15 | Agendamiento ágil desde chat | Pocos pasos, validación clara |
| RNF-16 | Robustez ante fallos | Mensajes/error/reintentos/sin inconsistencias |
| RNF-17 | Transparencia limitaciones | Distinguir general/profesional/urgencia |
| RNF-18 | Accesible no-técnico | Lenguaje claro/empático/corto |

## 4. Guardrails IA (Críticos)
1. **Emergencias primero**: sangrado, asfixia, convulsiones, letargo severo → alerta inmediata, NO condicionar a agendamiento.
2. **Sin diagnóstico/medicación humana/inducir vómito**: explícitamente prohibido.
3. **Chat requiere mascota**: `id_mascota` obligatoria.
4. **Agendamiento integrado**: si requiere valoración → explicar + widget con 2 sedes + disponibilidad real.
5. **Privacidad**: mínimo de datos al llamar Gemini; filtrar info sensible.
6. **Sin garantía de seguridad**: si no hay alarmas, NO afirmar "seguro", siempre distinguir niveles.

## 5. Historias Usuario con Gherkin
Ver [docs/Ia/historias_usuario_criterios_aceptacion.md](Ia/historias_usuario_criterios_aceptacion.md) completo. Destacan HU-09 (selección mascota), HU-12 (urgencias), HU-13-HU-17 (agendamiento desde chat).

## 6. Trazabilidad RF-HU-Módulo
| RF | HU | Módulo |
|---|---|---|
| RF-09-12 | HU-09-12 | Asistente IA/Chat |
| RF-13-17 | HU-13-17 | Agendamiento/Citas |
| RF-01-08 | HU-01-08 | Gestión Mascotas/Historial/Recordatorios |

## 7. Notas
- MVP visual no funcional. Esta documentación es diseño objetivo.
- Citas desde chat usan disponibilidad real PostgreSQL.
- Imágenes SIEMPRE en Cloudinary.

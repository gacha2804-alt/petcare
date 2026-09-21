# Requisitos — PetCare
Plataforma híbrida (app móvil + web) de cuidado preventivo de mascotas mediante IA, que conecta propietarios,
veterinarios, personal de clínica y administradores.

Fuente: entrevista simulada con cliente veterinario (ver [`docs/ia/entrevista.md`](./ia/entrevista.md)) + contexto del [README del proyecto].

## 1. Requerimientos Funcionales

| ID | Requerimiento |
|---|---|
| RF-01 | El sistema debe permitir registrar la aplicación de una vacuna/desparasitación con: producto, fabricante, lote, fecha, dosis, vía, peso, edad, veterinario y novedades. |
| RF-02 | El sistema debe permitir configurar protocolos de refuerzo por tipo de producto y especie/edad (ej. cachorro vs. adulto). |
| RF-03 | El sistema debe calcular automáticamente la fecha del próximo refuerzo según el protocolo configurado. |
| RF-04 | El sistema debe generar una alerta semanal al personal de clínica con las mascotas próximas a vencer, antes de notificar al propietario. |
| RF-05 | El sistema debe enviar un recordatorio automático al propietario (push/WhatsApp) con opción de agendar directamente. |
| RF-06 | El sistema debe reenviar un segundo recordatorio si el propietario no responde en un plazo definido. |
| RF-07 | El sistema debe permitir al propietario confirmar o cancelar una cita desde la app. |
| RF-08 | El sistema debe permitir al propietario reprogramar una cita seleccionando un horario disponible. |
| RF-09 | El sistema debe liberar automáticamente el cupo si el cliente cancela o no confirma dentro del plazo definido (ej. 12 h antes). |
| RF-10 | El sistema debe permitir inscribirse en lista de espera y notificar automáticamente al primero cuando se libere un cupo. |
| RF-11 | El sistema debe mostrar al personal de clínica un tablero con el estado de las citas del día (confirmadas/pendientes/canceladas). |
| RF-12 | El sistema debe centralizar el historial clínico del paciente y hacerlo visible sin importar la sede donde fue atendido. |
| RF-13 | El sistema debe permitir al propietario consultar historial, vacunas y resultados de exámenes de su mascota. |
| RF-14 | El sistema debe generar reportes gerenciales de cumplimiento de vacunación/desparasitación (al día, pendientes, sin atender). |

## 2. Requerimientos No Funcionales

| ID | Requerimiento |
|---|---|
| RNF-01 | **Usabilidad**: los flujos de confirmación/reprogramación de citas deben completarse en máximo 3 pasos, considerando usuarios con baja habilidad tecnológica. |
| RNF-02 | **Disponibilidad**: la plataforma debe estar disponible ≥99% del tiempo en horario de atención de las clínicas. |
| RNF-03 | **Sincronización**: los cambios en el historial clínico deben reflejarse en todas las sedes en menos de 1 minuto. |
| RNF-04 | **Seguridad y privacidad**: los datos de salud de las mascotas y de contacto de los propietarios deben estar cifrados en tránsito y en reposo, con acceso basado en roles. |
| RNF-05 | **Escalabilidad**: el sistema debe soportar el crecimiento a nuevas sedes sin rediseño de arquitectura. |
| RNF-06 | **Integración de notificaciones**: el envío de recordatorios debe soportar al menos WhatsApp y notificaciones push, con posibilidad de agregar canales. |
| RNF-07 | **Rendimiento**: el cálculo semanal de vencimientos debe ejecutarse sobre la base completa de pacientes en menos de 5 minutos. |
| RNF-08 | **Auditabilidad**: toda aplicación de producto (vacuna/antiparasitario) debe quedar trazable a un veterinario y un lote, sin posibilidad de edición retroactiva silenciosa. |

## 3. Historias de Usuario (Borrador inicial — MoSCoW)

| # | Prioridad | Historia | Criterios de aceptación |
|---|---|---|---|
| HU-01 | **Must** | Como **propietario**, quiero recibir recordatorios automáticos de vacunas/desparasitación de mi mascota, para no olvidar las fechas de refuerzo. | - Dado que a mi mascota le falta ≤7 días para un refuerzo, cuando se cumpla la condición, entonces recibo una notificación con el nombre de la mascota, el producto y la fecha sugerida.<br>- Dado que no respondo en 3 días, cuando se cumpla el plazo, entonces recibo un segundo recordatorio. |
| HU-02 | **Must** | Como **personal de clínica**, quiero ver semanalmente la lista de mascotas con vencimientos próximos, para validar antes de notificar al propietario. | - Dado que es lunes, cuando se genere el reporte semanal, entonces veo la lista de pacientes con vencimiento en los próximos 7 días.<br>- Puedo aprobar o posponer el envío de cada recordatorio individualmente. |
| HU-03 | **Must** | Como **veterinario**, quiero registrar la vacuna/desparasitación aplicada con sus datos completos, para que el sistema calcule automáticamente la próxima fecha. | - Al guardar el registro con producto, lote, dosis, peso y fecha, el sistema muestra la próxima fecha calculada según el protocolo configurado.<br>- Si el producto no tiene protocolo configurado, el sistema me alerta antes de guardar. |
| HU-04 | **Must** | Como **propietario**, quiero confirmar o cancelar mi cita desde la app, para que la clínica sepa si asistiré. | - Recibo un recordatorio 24-48h antes con botones "Confirmar" / "Cancelar".<br>- Al confirmar, el estado de la cita cambia a "confirmada" en el tablero de la clínica. |
| HU-05 | **Must** | Como **propietario**, quiero reprogramar mi cita a otro horario disponible sin llamar a la clínica. | - Al elegir "Reprogramar", veo horarios disponibles de los próximos 7 días.<br>- Al seleccionar uno, la cita anterior se cancela y la nueva queda confirmada automáticamente. |
| HU-06 | **Should** | Como **personal de clínica**, quiero que el cupo se libere automáticamente si el cliente cancela o no confirma a tiempo, para ofrecerlo a otro paciente. | - Si no hay confirmación 12h antes de la cita, el horario pasa a "disponible" en el calendario.<br>- El horario liberado es visible de inmediato para nuevas citas. |
| HU-07 | **Should** | Como **propietario**, quiero anotarme en lista de espera cuando no hay cupos, para que me avisen si se libera un horario. | - Puedo unirme a la lista de espera de un horario lleno.<br>- Si se libera un cupo, el primero de la lista recibe una notificación con opción de tomarlo en los siguientes 15 minutos. |
| HU-08 | **Must** | Como **veterinario**, quiero acceder al historial clínico completo de la mascota sin importar la sede donde fue atendida, para tomar decisiones informadas en consultas urgentes. | - Al buscar un paciente, veo el historial consolidado de ambas sedes, con fecha y sede de cada evento.<br>- La información se actualiza en menos de 1 minuto tras un registro en cualquier sede. |
| HU-09 | **Should** | Como **propietario**, quiero ver el historial médico, vacunas y resultados de exámenes de mi mascota desde la app, para tener todo organizado en un solo lugar. | - Puedo ver, por mascota, línea de tiempo de vacunas, consultas y exámenes.<br>- Puedo descargar o compartir un examen en PDF. |
| HU-10 | **Could** | Como **propietario**, quiero generar un perfil de emergencia con código QR de mi mascota, para que cualquier veterinario acceda rápido a su información básica en caso de urgencia. | - El QR muestra especie, raza, alergias conocidas, vacunas vigentes y contacto del propietario.<br>- El QR es accesible sin necesidad de iniciar sesión en la app. |
| HU-11 | **Could** | Como **propietario**, quiero recibir alertas basadas en IA sobre posibles cambios relevantes en mi mascota (peso, actividad reportada), para saber si necesito llevarla a consulta. | - El sistema compara los últimos 3 registros de peso/actividad contra el rango esperado por raza/edad.<br>- Si hay una desviación >15%, se genera una alerta explicando el motivo. |
| HU-12 | **Won't (esta iteración)** | Como **administrador**, quiero que PetCare integre facturación e inventario, para centralizar todo en una sola plataforma. | Fuera de alcance del MVP: el sistema actual de facturación/inventario ya funciona bien según el cliente; se evaluará en una fase posterior. |

## 4. Checklist INVEST — Problemas detectados y correcciones

Se aplicó el checklist **INVEST** (Independent, Negotiable, Valuable, Estimable, Small, Testable) sobre el borrador anterior. Se identificaron y corrigieron los siguientes problemas:

| Problema | Corrección | Justificación |
|---|---|---|
| **HU-08 original** mezclaba dos responsabilidades: sincronizar datos entre sedes (infraestructura) y consultarlos (interfaz para el veterinario). Violaba **Small** y **Testable** (no hay un criterio único y verificable). | Se dividió en dos historias: **HU-08a** "Como sistema, los registros clínicos deben sincronizarse entre sedes en <1 min" (respaldada por RNF-03) y **HU-08** (mantenida arriba) enfocada solo en la consulta del historial consolidado por el veterinario. | Separar la infraestructura de la experiencia de usuario permite estimar, desarrollar y probar cada parte de forma independiente (cumple I y S de INVEST). |
| **HU-11 original** decía "detectar cambios en el comportamiento de la mascota" sin definir qué datos se analizan ni qué umbral dispara una alerta. Violaba **Testable**. | Se reescribió especificando las variables (peso, actividad reportada), la ventana de comparación (últimos 3 registros) y el umbral (desviación >15%). | Sin un criterio medible no es posible diseñar una prueba que determine si la historia está "hecha"; el umbral explícito la hace verificable. |
| **HU-04 y HU-05 originales** (confirmar cita / reprogramar) estaban redactadas como si una dependiera secuencialmente de la otra, y compartían casi los mismos criterios de aceptación, generando duplicidad y afectando **Independent**. | Se separaron con criterios de aceptación distintos y no secuenciales: HU-04 cubre solo confirmar/cancelar; HU-05 cubre solo la reprogramación, pudiendo desarrollarse y priorizarse en sprints distintos. | Historias independientes se pueden priorizar, estimar y entregar por separado sin bloquear el backlog si una se retrasa. |
| **HU-02 original** no indicaba una acción concreta y verificable del personal de clínica (solo decía "revisar la lista"), lo que la hacía difícil de estimar y no claramente **Valuable** por sí sola sin HU-01. | Se agregó la acción explícita "aprobar o posponer el envío de cada recordatorio individualmente" como criterio de aceptación. | Convierte una tarea pasiva ("ver una lista") en una acción con valor de negocio propio (control humano antes del envío automático), y la hace estimable/testeable. |

## 5. Próximos pasos

- Revisar y priorizar el backlog con el equipo (Sprint 0).
- Definir wireframes para los flujos Must (HU-01 a HU-05, HU-08).
- Validar con el cliente el umbral de alerta de IA (HU-11) antes de construir el modelo.

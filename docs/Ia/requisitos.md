# Requisitos — PetCare

PetCare — Estado actual del proyecto y propósito de los requisitos

Estado actual:
PetCare no tiene una página web funcional ni un backend implementado. El proyecto parte de un MVP visual elaborado con Google Stitch IA, que sirve como referencia de diseño pero no contiene funcionalidades operativas. Este documento especifica el sistema que se quiere construir, sin presentar como implementadas las funcionalidades que solo están diseñadas o documentadas.

Propósito de los requisitos:
Este documento define los requisitos funcionales y no funcionales del sistema PetCare futuro, con un enfoque en dos nuevas capacidades mediante asistente de IA:
1. Orientación inicial segura para el tutor, incluyendo reconocimiento de señales de alarma.
2. Agendamiento de citas veterinarias integrado en la conversación de chat, desde la recomendación de valoración presencial hasta la reserva confirmada.

Diferencia entre el MVP visual existente y el sistema futuro:
El MVP actual es una propuesta de diseño estático sin lógica, bases de datos ni flujos operativos. El sistema futuro debe proporcionar autenticación, asociación de mascotas, consulta de historial clínico, generación de recordatorios, gestión de citas con disponibilidad real de dos sedes, y un asistente de IA que ofrezca orientación empática y basada en criterios veterinarios sin sustituir la atención profesional. Los requisitos aquí especificados son objetivos de construcción, no descripciones de lo que ya funciona.

---

PetCare es una plataforma web orientada a la gestión y el cuidado preventivo de mascotas, que permite centralizar información clínica, gestionar citas veterinarias y facilitar el seguimiento de vacunas y desparasitaciones, conectando a propietarios con profesionales y personal de clínicas veterinarias.

Fuente: entrevista simulada con cliente veterinario (ver [docs/Ia/entrevista.md](./entrevista.md)) y contexto del [README.md](../../README.md). Este documento conserva los requisitos existentes que siguen siendo válidos y actualiza únicamente los aspectos que cambian con la nueva funcionalidad de asistente de IA para orientación inicial y agendamiento de citas desde el chat.

## 1. Requisitos funcionales actualizados

### 1.1 Requisitos funcionales base conservados

| ID | Nombre | Descripción | Actor responsable | Precondiciones | Flujo principal | Flujos alternativos y excepciones | Postcondiciones | Criterios de aceptación verificables | Prioridad |
|---|---|---|---|---|---|---|---|---|---|
| RF-01 | Registro de mascota | El tutor (propietario) registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos identificatorios. | Tutor (propietario) | El tutor está autenticado y no ha bloqueado la gestión de mascotas. | El tutor completa los datos obligatorios y confirma la operación. | Si faltan datos obligatorios, el sistema no registra la mascota y solicita la información faltante. | La mascota queda asociada al propietario y disponible para su consulta y gestión. | Se valida que el registro exige datos mínimos obligatorios; el sistema informa errores de validación y no persiste registros incompletos. | Must |
| RF-02 | Consulta del historial clínico | El tutor consulta el historial clínico de una mascota registrada. | Tutor | Existe al menos una mascota asociada al tutor. | El sistema muestra histórico clínico, fechas, motivo y registros asociables. | Si no existe historial, se presenta un estado vacío con información clara. | El propietario visualiza la información autorizada y la historia queda trazada. | Se verifica que la vista incluye registros médicos y no expone información no autorizada. | Must |
| RF-03 | Autorización de acceso veterinario | El tutor autoriza, consulta y revoca el acceso de veterinarios al historial clínico de cada mascota. | Tutor | La mascota existe y el veterinario está registrado en la plataforma. | El tutor gestiona permisos por mascota y veterinario. | Si un veterinario es revocado, pierde acceso inmediato a la información. | El permiso queda actualizado en el registro de seguridad. | Se valida que cada cambio de acceso queda asociado a la mascota y al usuario. | Must |
| RF-04 | Registro de consulta veterinaria | El veterinario autorizado registra una consulta asociada a una mascota. | Veterinario | Hay autorización vigente y la mascota existe. | El veterinario registra motivo, diagnóstico y observaciones. | Si faltan datos obligatorios, se rechaza el registro. | La consulta queda vinculada a la mascota y a la sede correspondiente. | Se valida que la consulta requiere datos mínimos y se asocia a la mascota y al veterinario. | Must |
| RF-05 | Solicitud y confirmación de citas | El tutor solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica. | Tutor | Existe disponibilidad real. | El tutor selecciona clínica, veterinario y horario. | Si el horario ya no está disponible, el sistema ofrece otras opciones o rechaza la elección. | La cita queda registrada en el sistema y visible para el personal correspondiente. | Se valida que la disponibilidad usada para la confirmación corresponde a un horario real y no duplicado. | Must |
| RF-06 | Consulta de vacunas | El tutor consulta el registro de vacunas de una mascota. | Tutor | La mascota está registrada y sus vacunas se registran en el historial. | El sistema muestra fecha de aplicación y próxima fecha recomendada. | Si faltan datos, la vista informa que no hay información suficiente. | La información de vacunación queda visible y trazada. | Se verifica que cada vacuna está asociada a la mascota y a la fecha de aplicación. | Must |
| RF-07 | Consulta de desparasitaciones | El tutor consulta el registro de desparasitaciones de una mascota. | Tutor | La mascota está registrada y el registro existe. | El sistema muestra fecha del tratamiento y próxima fecha recomendada. | Si no existe registro, se presenta vacío o con mensaje de ausencia de información. | La información queda disponible para seguimiento. | Se valida que se muestran fechas y no se infieren tratamientos inexistentes. | Should |
| RF-08 | Recordatorios preventivos | El sistema genera recordatorios para vacunas y desparasitaciones próximas a vencer. | Personal de clínica / sistema | Existe información de vacunación o desparasitación y configuración de recordatorios. | El sistema identifica vencimientos próximos y genera alertas. | Si se requiere confirmación o postergación, el personal debe poder gestionarlo. | El propietario recibe recordatorio y se registra el estado del mismo. | Se valida que el recordatorio se genera a partir de fechas reales y que se pueden registrar acciones sobre él. | Should |

### 1.2 Nuevos requisitos para el asistente veterinario inteligente y agendamiento desde el chat

| ID | Nombre | Descripción | Actor responsable | Precondiciones | Flujo principal | Flujos alternativos y excepciones | Postcondiciones | Criterios de aceptación verificables | Prioridad |
|---|---|---|---|---|---|---|---|---|---|
| RF-09 | Selección de mascota en el chat | El tutor debe poder seleccionar una mascota y abrir un chat con contexto de la mascota elegida antes de describir la situación. | Tutor (propietario) | El tutor está autenticado y tiene al menos una mascota registrada. | El tutor elige una mascota y el sistema asocia el hilo de conversación con esa mascota. | Si la mascota no existe o no está asociada, el sistema no permitirá continuar con el chat clínico. | El chat queda vinculado a la mascota seleccionada y su historial relevante puede consultarse si corresponde. | Se valida que el hilo de chat sólo puede iniciar con una mascota válida y que la selección queda visible en la conversación. | Must |
| RF-10 | Registro y comprensión del motivo de consulta | El asistente debe captar el motivo de la consulta del tutor mediante un mensaje libre o una conversación guiada, sin forzar un formulario médico largo. | Tutor / asistente IA | La mascota está seleccionada. | El tutor describe el percance, síntoma o comportamiento inusual; el sistema guarda una síntesis del motivo y realiza preguntas breves. | Si la información es insuficiente, la IA solicita datos específicos de gravedad o evolución. | El motivo de consulta queda registrado en el hilo para continuar la orientación y, si aplica, el agendamiento. | Se valida que la conversación conserva el motivo principal, que la IA solicita solo preguntas necesarias y que no exigirá más datos que los relevantes. | Must |
| RF-11 | Orientación inicial basada en criterios veterinarios | El asistente ofrece orientación inicial empática, clara y comprensible, en lenguaje no técnico, tomando en cuenta la especie, edad y antecedentes de la mascota cuando exista y sea pertinente. | Asistente IA | La mascota y el motivo de consulta han sido identificados. | La IA hace preguntas breves, reconoce el contexto clínico disponible y responde con recomendaciones generales y señales a vigilar. | Si no hay información suficiente, la IA señala la limitación y solicita solo los datos mínimos necesarios. | El tutor recibe recomendaciones iniciales de bajo riesgo y una explicación de cuándo buscar atención profesional. | Se valida que la respuesta: (a) usa lenguaje claro, (b) no ofrece diagnóstico definitivo, (c) contempla información disponible de la mascota, y (d) recomienda atención profesional cuando procede. | Must |
| RF-12 | Identificación de señales de alarma y recomendaciones de urgencia | El asistente debe detectar indicios de emergencia y alertar de manera clara sin generar miedo artificial ni demora innecesaria. | Asistente IA | Hay síntomas, comportamientos o indicadores que pueden sugerir urgencia. | La IA clasifica la situación según severidad y recomienda atención veterinaria inmediata cuando corresponda. | Si el tutor menciona síntomas graves, el sistema debe priorizar la urgencia sobre cualquier proceso de agendamiento. | El tutor queda informado de que debe buscar atención de urgencias si la situación lo requiere. | Se valida que la IA no condiciona la urgencia a completar el proceso de agendamiento y que el mensaje es explícito sobre la necesidad de atención inmediata. | Must |
| RF-13 | Recomendación justificada de valoración presencial | Cuando la situación requiere valoración profesional, la IA debe explicar por qué es conveniente acudir a una sede de PetCare y ofrece la opción de agendar una cita. | Asistente IA / tutor | Se ha reunido suficiente información para decidir que la situación requiere valoración presencial. | La IA explica la recomendación y propone la opción “Agendar cita”. | Si el tutor no desea agendar, puede continuar conversando o cerrar el chat sin presión. | Queda registrada la recomendación de valoración presencial y la opción de cita queda disponible. | Se valida que la recomendación incluye una explicación clara de por qué la valoración presencial es útil y que no reemplaza la decisión del veterinario. | Must |
| RF-14 | Presentación de las dos sedes y disponibilidad real | El sistema debe presentar las dos sedes de PetCare y consultar disponibilidad real según la agenda existente. | Sistema / tutor | Hay dos sedes activas con disponibilidad definida. | El tutor elige una de las sedes y el sistema consulta horarios vigentes. | Si no hay disponibilidad en una sede, se ofrece la otra sede u otros horarios. | El tutor solo ve horarios reales y no ficticios. | Se valida que la disponibilidad mostrada proviene de la agenda actual y que no se superponen reservas. | Must |
| RF-15 | Agendamiento integrado en el chat | El tutor debe poder iniciar y completar el proceso de agendamiento desde la misma conversación, sin salir del chat para buscar citas manualmente. | Tutor / sistema | Existe recomendación de valoración presencial y la mascota y la sede están seleccionadas. | El tutor activa “Agendar cita”, selecciona fecha/hora y confirma la reserva. | Si la reserva no es válida, el sistema muestra errores y ofrece alternativas; si hay conflicto de horario, pide reintento. | La cita queda registrada como reserva efectiva y disponible en el módulo de citas. | Se valida que el flujo completo puede realizarse dentro del chat y que la cita no se registra si no se cumplen las reglas de negocio. | Must |
| RF-16 | Confirmación de la reserva y datos obligatorios | El sistema solicita o confirma el motivo de consulta, la mascota y los datos necesarios antes de la reserva definitiva. | Sistema / tutor | El horario ha sido elegido y la mascota ya fue identificada. | El tutor confirma el motivo, revisa los detalles y finaliza la reserva. | Si faltan datos obligatorios, el sistema no confirma la cita y exige completarlos. | La cita queda disponible solo cuando la reserva es realmente efectiva. | Se valida que la cita no se registra sin motivo de consulta ni datos mínimos requeridos y que la confirmación incluye los datos correctos. | Must |
| RF-17 | Asociación de la cita con mascota, tutor y sede | El sistema debe asociar cada cita con el tutor, la mascota atendida, la sede elegida y el profesional o agenda correspondiente si aplica. | Sistema | La reserva se ha validado. | El sistema genera la cita con una relación explícita a la mascota y al tutor. | Si el horario corresponde a otra sede o veterinario, se rechaza la reserva y se informa el motivo. | La cita queda trazada en el historial, en agenda y en los módulos autorizados. | Se valida que cada cita tiene al menos los identificadores de tutor, mascota y sede y que se visualiza en el módulo correspondiente. | Must |
| RF-18 | Consulta y manejo de la cita desde módulos de personal | La cita agendada desde el chat debe estar disponible en el módulo de citas del tutor y en los módulos del personal autorizado. | Personal autorizado / tutor | La cita ya fue registrada. | El tutor y el personal autorizado consultan el estado, la fecha/hora y la metadata asociada. | Si la cita es cancelada o reprogramada, los módulos deben reflejar el nuevo estado. | La cita queda visible con trazabilidad y cambios auditable. | Se valida que la cita aparece en los módulos correspondientes y que las modificaciones quedan registradas. | Must |
| RF-19 | Manejo de errores, cancelación y falta de disponibilidad | El sistema debe gestionar errores de validación, cancelaciones, horarios no disponibles y ausencia de alternativas sin bloquear la experiencia del tutor. | Sistema / tutor | Existe un flujo de agendamiento en curso. | El sistema presenta mensajes claros y ofrece soluciones válidas. | Si no hay disponibilidad, propone otras sedes o horarios; si el tutor cancela, la operación se retira sin generar reserva. | La conversación continúa con estado consistente y sin reservas duplicadas. | Se valida que no se generan reservas con datos incompletos, no se duplican citas ni se queda la reserva en estado inconsistente. | Must |
| RF-20 | Transferencia o escalamiento a personal veterinario | Cuando el caso lo requiere y la arquitectura lo permite, la sesión puede derivarse o escalarse a personal veterinario o personal autorizado para apoyo adicional. | Personal veterinario / sistema | La situación supera la capacidad de orientación inicial o requiere evaluación humana. | El sistema identifica la necesidad de intervención humana y presenta la derivación o escalamiento. | Si no está implementado el escalamiento, debe dejarse explícito como funcionalidad futura o dependiente de la arquitectura. | Se registra la derivación o, en su defecto, se ofrece la información de contacto o la ruta definida por la clínica. | Se valida que la derivación no sustituye la atención veterinaria ni la urgencia y que, si no se implementa, la limitación queda documentada. | Should |

## 2. Requisitos no funcionales actualizados

| ID | Requisito | Criterio medible / validación |
|---|---|---|
| RNF-01 | El sistema debe restringir el acceso al historial clínico de cada mascota únicamente al propietario y a los veterinarios que este haya autorizado. | La plataforma debe verificar permisos por usuario, mascota y rol antes de mostrar o editar información clínica. |
| RNF-02 | El sistema debe proteger las credenciales y los datos personales del tutor y la mascota mediante mecanismos de autenticación y almacenamiento seguro. | Se requiere autenticación y controles mínimos de seguridad; los datos sensibles no deben exponerse en mensajes de chat ni logs sin filtrado. |
| RNF-03 | El sistema debe garantizar la integridad de la información clínica, evitando modificaciones realizadas por usuarios no autorizados. | Cualquier cambio en citas, historial o permisos debe quedar registrado con usuario, fecha y motivo si aplica. |
| RNF-04 | Las operaciones habituales de consulta, orientación de IA y agendamiento deben responder en un tiempo adecuado para permitir una interacción fluida. **[SUPUESTO]** | Tiempo objetivo de respuesta: el chat debe devolver mensajes en un intervalo razonable para la experiencia del usuario y la reserva no debe tardar más de la ventana esperada por el negocio. |
| RNF-05 | La plataforma debe ser accesible desde navegadores web modernos y adaptarse a equipos de escritorio, tabletas y dispositivos móviles. | La interfaz del chat y la gestión de citas debe ser usable con lectura y navegación sin conocimientos técnicos especializados. |
| RNF-06 | La interfaz debe permitir que propietarios, veterinarios y personal de clínica realicen sus tareas principales de forma clara y comprensible. | Las pantallas y flujos principales deben incluir retroalimentación, mensajes de error y confirmación de acciones. |
| RNF-07 | El sistema debe mantener trazabilidad de la información clínica, de las citas y de los cambios asociados. | Cada operación relevante debe quedar asociada a un usuario, un timestamp y, si aplica, a la mascota, la sede o la cita involucrada. |
| RNF-08 | El sistema debe contar con mecanismos de respaldo y recuperación ante fallos. | La información crítica de mascotas, permisos y citas debe poder recuperarse con procedimientos definidos por la infraestructura. |
| RNF-09 | La información enviada al servicio de IA debe proteger la privacidad del tutor y de la mascota y no debe utilizarse para fines distintos de la atención y la orientación. | Los datos enviados al servicio de IA deben limitarse a lo mínimo necesario, y deben existir políticas de tratamiento y control de acceso. |
| RNF-10 | Debe existir control de acceso según los cuatro roles existentes: propietario, veterinario, personal de clínica y administrador. | Cada acción debe validarse por rol; las funciones de agenda, historial y IA no deben quedar accesibles a todos los perfiles. **Pendiente**: se requieren definiciones específicas de funciones y permisos del rol administrador. |
| RNF-11 | La IA debe ofrecer orientación inicial sin asumir diagnósticos definitivos ni reemplazar la valoración veterinaria profesional. | El sistema debe incluir una nota visible de limitación y la conversación no debe presentar resultados clínicos como certeza. |
| RNF-12 | La IA debe prevenir recomendaciones veterinarias peligrosas, incluidos medicamentos humanos, provocación del vómito sin indicación profesional y automedicación. | Las respuestas de la IA deben desincentivar estas acciones y priorizar la consulta profesional o la atención de urgencias. |
| RNF-13 | El sistema debe proteger al asistente contra instrucciones maliciosas o intentos de manipular su comportamiento. | El modelo debe responder con guardrails y no debe revelar información privilegiada ni ejecutar acciones fuera de su alcance. |
| RNF-14 | La disponibilidad y consistencia de la agenda deben garantizar que no haya reservas duplicadas ni horarios ocupados. | El sistema debe validar solapamientos antes de confirmar la cita. |
| RNF-15 | El proceso de agendamiento desde el chat debe ser usable en condiciones normales de navegación y no debe exigir más pasos de los necesarios. | La experiencia debe permitir completar la reserva en un flujo breve, comprensible y con validación clara de errores. |
| RNF-16 | El sistema debe manejar errores y recuperarse de fallos durante la orientación o la reserva de citas. | Si falla una operación, el sistema debe indicar el error, permitir reintentar y evitar reservas inconsistentes. |
| RNF-17 | La IA debe ser transparente sobre sus limitaciones y no debe sugerir que una situación es segura solo porque no se hayan identificado señales de alarma. | Cada respuesta de orientación debe distinguir entre recomendación general, consulta profesional y urgencia. |
| RNF-18 | La experiencia del chat debe ser accesible y comprensible para personas sin conocimientos veterinarios. | Debe evitarse terminología técnica innecesaria y los mensajes deben ser claros, cortos y empáticos. |

## 3. Reglas de negocio y seguridad veterinaria

1. La IA ofrece orientación inicial, pero no reemplaza la consulta veterinaria ni la atención profesional.
2. Las emergencias no deben quedar condicionadas al proceso de agendamiento ni a la disponibilidad de una cita en PetCare.
3. La IA no debe sugerir administrar medicamentos humanos, provocar el vómito, ni recomendar tratamientos sin indicación veterinaria.
4. Cuando exista un riesgo potencial, la IA debe recomendar valoración profesional o atención de urgencias de forma clara y sin demora innecesaria.
5. La recomendación de una cita presencial debe basarse en indicadores de seguridad y riesgo, no solo en la ausencia de alarmas.
6. La reserva de citas debe validar la disponibilidad real de la agenda, la sede, la mascota, el motivo de consulta y los datos obligatorios.
7. La cita agendada desde el chat debe quedar asociada al tutor, a la mascota seleccionada, a la sede elegida y al módulo de agenda correspondiente.
8. Si no hay disponibilidad, el sistema debe ofrecer alternativas válidas, incluyendo otra sede u otros horarios cuando corresponda.
9. La cancelación o reprogramación de una cita debe reflejarse en los módulos de tutor y personal autorizado, manteniendo trazabilidad.
10. La IA no debe emitir diagnósticos definitivos ni garantizar resultados sobre la condición de la mascota.
11. Si la arquitectura lo permite, la sesión puede escalarse a personal veterinario o clínico para asistencia adicional, pero la urgencia no debe demorarse por el agendamiento.

## 4. Supuestos y decisiones pendientes de confirmación

- El sistema debe confirmar si el agendamiento desde el chat se realiza directamente sobre la agenda de la clínica o requiere aprobación de personal de clínica antes de confirmar la reserva.
- Debe definirse quién revisa la disponibilidad real de cada sede: la agenda de la clínica, un calendario compartido o un servicio de disponibilidad centralizado.
- Debe confirmarse si el asistente guarda un historial mínimo de la conversación o si solo usa el contexto de la sesión actual.
- Se requiere definir si el escalamiento a personal veterinario se hace por notificación interna, por derivación a un canal de atención o por un caso específico del flujo de urgencias.
- Debe validarse si el servicio de IA usado para el asistente puede procesar información sensible de mascotas y si requiere políticas de consentimiento, almacenamiento o anonimización.

## 5. Criterio de prioridad y alcance

- Must: selección de mascota, motivos clínicos, triage inicial, señales de urgencia, recomendación de valoración presencial, disponibilidad real de sedes, agendamiento integrado en el chat, confirmación segura, almacenamiento y trazabilidad de la cita.
- Should: escalamiento a personal veterinario, refinamiento del contexto de la mascota y mejoras de experiencia del asistente.
- Los requisitos de IA deben tratarse como apoyo de orientación y no como sustituto de la atención profesional.

## 9. Matriz de trazabilidad requisitos - roles - historias de usuario - módulos

| Requisito | Rol principal | Historia de usuario | Módulo del sistema |
|---|---|---|---|
| RF-01 | Tutor (propietario) | Registrar nueva mascota en el sistema | Gestión de mascotas |
| RF-02 | Tutor (propietario) | Consultar historial clínico de la mascota | Historial clínico |
| RF-03 | Tutor (propietario) | Gestionar permisos de acceso veterinario | Seguridad y permisos |
| RF-04 | Veterinario | Registrar consulta veterinaria | Consulta y registro clínico |
| RF-05 | Tutor | Solicitar cita veterinaria | Agendamiento de citas |
| RF-06 | Tutor | Consultar registro de vacunas | Historial clínico / Vacunas |
| RF-07 | Tutor | Consultar registro de desparasitaciones | Historial clínico / Desparasitación |
| RF-08 | Personal de clínica | Recibir recordatorios de vencimientos | Recordatorios / Sistema |
| RF-09 | Tutor | Seleccionar mascota y iniciar chat con contexto | Asistente IA / Chat |
| RF-10 | Tutor / asistente IA | Expresar motivo de consulta en chat | Asistente IA |
| RF-11 | Tutor | Recibir orientación inicial de la IA | Asistente IA |
| RF-12 | Tutor | Recibir alerta de señales de alarma | Asistente IA |
| RF-13 | Tutor | Recibir recomendación de valoración presencial y agendar cita | Agendamiento de citas |
| RF-14 | Tutor | Ver disponibilidad de dos sedes | Sedes |
| RF-15 | Tutor | Agendar cita desde el chat sin salir | Agendamiento de citas |
| RF-16 | Tutor | Confirmar reserva con datos obligatorios | Agendamiento de citas |
| RF-17 | Sistema | Asociar cita a tutor, mascota y sede | Agendamiento de citas / Historial |
| RF-18 | Tutor / personal autorizado | Consultar estado de cita agendada | Agendamiento de citas |
| RF-19 | Sistema / tutor | Manejo de errores, cancelaciones y disponibilidad | Agendamiento de citas |
| RF-20 | Personal veterinario / sistema | Derivación o escalamiento a humano | Asistencia humana / Flujo de urgencias |
| RNF-01 | Propietario, veterinario | Acceso restringido al historial clínico | Seguridad / Permisos |
| RNF-02 | Tutor, mascota | Protección de credenciales y datos personales | Seguridad / Autenticación |
| RNF-03 | Todo usuario | Integridad de información clínica con trazabilidad | Seguridad / Auditoria |
| RNF-04 | Tutor | Tiempos de respuesta adecuados para interacción fluida | Rendimiento |
| RNF-05 | Todo usuario | Accesibilidad en navegadores y dispositivos | Interfaz / UI |
| RNF-06 | Todos los roles | Interfaces claras con retroalimentación y confirmación | Usabilidad |
| RNF-07 | Todo usuario | Trazabilidad de información, citas y cambios | Seguridad / Auditoria |
| RNF-08 | Todo usuario | Mecanismos de respaldo y recuperación ante fallos | Infraestructura |
| RNF-09 | Tutor, mascota | Privacidad en información enviada al servicio de IA | IA / Privacidad |
| RNF-10 | Los cuatro roles | Control de acceso por rol | Seguridad / Permisos |
| RNF-11 | Tutor | IA sin diagnósticos definitivos ni reemplazo profesional | Asistente IA |
| RNF-12 | Tutor | IA que previene recomendaciones peligrosas | Asistente IA / Seguridad |
| RNF-13 | Sistema | IA protegida contra instrucciones maliciosas | IA / Seguridad |
| RNF-14 | Sistema | Agenda sin reservas duplicadas ni horarios ocupados | Agendamiento |
| RNF-15 | Tutor | Agendamiento usable desde el chat en pocos pasos | Usabilidad / Chat |
| RNF-16 | Sistema | Manejo de errores y recuperación en orientación y reserva | Robustez |
| RNF-17 | Tutor | IA transparente sobre limitaciones | Asistente IA |
| RNF-18 | Tutor sin conocimientos veterinarios | Chat accesible y comprensible sin terminología técnica | Usabilidad / Chat |

## 6. Notas de implementación y validación

La funcionalidad propuesta amplía el alcance de PetCare sin alterar la base del proyecto: conserva la gestión de mascotas, historial clínico, permisos, citas y sedes, y agrega un flujo asistido para orientación inicial y agendamiento directo desde el chat. Cualquier integración real con IA, agenda veterinaria o derivación humana debe validarse con la operación real de la clínica antes de considerarla un requisito completamente implementado.
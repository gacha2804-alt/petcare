# Historias de Usuario y Criterios de Aceptación (Gherkin) - PetCare

## 1. Objetivo
Definir las historias de usuario con criterios de aceptación en formato Gherkin, basadas en los requisitos RF-01 a RF-20 y RNF-01 a RNF-18, manteniendo trazabilidad con la matriz de requisitos y el modelo propuesto.

## 2. Historias de Usuario y Criterios de Aceptación

### HU-01 - Registrar mascota
**RF Relacionado:** RF-01  
**Prioridad:** Must  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero registrar una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos identificatorios, para mantener centralizada su información.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Registrar mascota correctamente
  Given que el propietario ha iniciado sesión y está autenticado
  When registra una mascota con nombre, especie, sexo, fecha de nacimiento y datos identificatorios
  Then el sistema debe guardar la mascota asociada al propietario
  And la mascota debe quedar disponible para consulta y gestión

Scenario: No registrar mascota con datos obligatorios faltantes
  Given que el propietario ha iniciado sesión
  When intenta registrar una mascota sin completar datos obligatorios
  Then el sistema no debe persistir el registro
  And debe mostrar mensaje de validación solicitando los datos faltantes
```

### HU-02 - Consultar historial clínico
**RF Relacionado:** RF-02  
**Prioridad:** Must  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero consultar el historial clínico de una mascota registrada, para conocer su historial médico autorizado.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Consultar historial clínico con información existente
  Given que el propietario está autenticado y tiene una mascota registrada
  And existe historial clínico asociado a la mascota
  When consulta el historial clínico de la mascota
  Then el sistema debe mostrar los registros médicos autorizados con fechas y motivos

Scenario: Consultar historial cuando no existe información
  Given que el propietario está autenticado y tiene una mascota registrada
  And no existe historial clínico previo
  When consulta el historial clínico de la mascota
  Then el sistema debe mostrar un estado vacío con mensaje claro
  And no debe exponer información no autorizada
```

### HU-03 - Gestionar permisos de acceso veterinario
**RF Relacionado:** RF-03  
**Prioridad:** Must  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada mascota, para controlar quién puede acceder a la información clínica.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Autorizar acceso veterinario a una mascota
  Given que el propietario está autenticado
  And existe un veterinario registrado en la plataforma
  And existe una mascota asociada al propietario
  When autoriza el acceso del veterinario a esa mascota
  Then el permiso debe quedar registrado con fecha de autorización
  And el veterinario debe poder consultar el historial autorizado

Scenario: Revocar acceso veterinario
  Given que existe un permiso de acceso activo para un veterinario y una mascota
  When el propietario revoca dicho acceso
  Then el permiso debe quedar inactivo con fecha de revocación
  And el veterinario debe perder acceso inmediato al historial de esa mascota

Scenario: Consultar permisos por mascota
  Given que el propietario está autenticado y tiene mascotas registradas
  When consulta los permisos de acceso de una mascota
  Then el sistema debe mostrar veterinarios autorizados, fecha de autorización y estado
```

### HU-04 - Registrar consulta veterinaria
**RF Relacionado:** RF-04  
**Prioridad:** Must  
**Rol:** Veterinario (autorizado)  
**Historia:** Como veterinario autorizado, quiero registrar una consulta veterinaria asociada a una mascota, para documentar motivo, diagnóstico y observaciones.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Registrar consulta con datos obligatorios
  Given que el veterinario está autenticado y tiene autorización vigente
  And existe una mascota asociada con permiso activo
  When registra una consulta con motivo, diagnóstico y observaciones
  Then la consulta debe quedar vinculada a la mascota, veterinario y sede correspondiente
  And debe quedar registrada con fecha y hora

Scenario: Rechazar registro sin autorización
  Given que el veterinario no tiene autorización vigente para la mascota
  When intenta registrar una consulta
  Then el sistema debe rechazar la operación
  And debe mostrar mensaje de acceso no autorizado
```

### HU-05 - Solicitar cita veterinaria
**RF Relacionado:** RF-05  
**Prioridad:** Must  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero solicitar una cita seleccionando una clínica/sede, veterinario y horario disponible ofrecido por la clínica, para agendar una valoración.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Solicitar cita con disponibilidad real
  Given que el propietario está autenticado y tiene una mascota registrada
  And existe disponibilidad real en alguna de las dos sedes
  When selecciona sede, veterinario y horario disponible
  Then el sistema debe mostrar los datos para confirmación
  And la disponibilidad debe corresponder a un horario real

Scenario: Rechazar cita con horario no disponible
  Given que un horario seleccionado ya fue ocupado
  When el propietario intenta confirmar la cita
  Then el sistema debe rechazar la reserva
  And debe ofrecer otras opciones de horarios o sedes
```

### HU-06 - Consultar registro de vacunas
**RF Relacionado:** RF-06  
**Prioridad:** Must  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero consultar el registro de vacunas de una mascota, para conocer fechas de aplicación y próxima fecha recomendada.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Consultar vacunas con registros existentes
  Given que el propietario está autenticado y tiene una mascota registrada
  And existen registros de vacunas
  When consulta el registro de vacunas
  Then el sistema debe mostrar fecha de aplicación, nombre de vacuna y próxima fecha recomendada

Scenario: Consultar vacunas sin registros
  Given que no existen registros de vacunas
  When consulta el registro de vacunas
  Then el sistema debe mostrar mensaje informativo sin inventar fechas
```

### HU-07 - Consultar registro de desparasitaciones
**RF Relacionado:** RF-07  
**Prioridad:** Should  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero consultar el registro de desparasitaciones de una mascota, para conocer fechas de tratamiento y próxima fecha recomendada.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Consultar desparasitaciones con registros existentes
  Given que existen registros de desparasitaciones
  When consulta el registro
  Then el sistema debe mostrar fecha de tratamiento y próxima fecha recomendada

Scenario: Consultar sin registros
  Given que no hay registros
  When consulta
  Then el sistema debe mostrar estado vacío sin inferir tratamientos
```

### HU-08 - Recordatorios preventivos
**RF Relacionado:** RF-08  
**Prioridad:** Should  
**Rol:** Personal de clínica / Sistema  
**Historia:** Como sistema/personal de clínica, quiero generar recordatorios para vacunas y desparasitaciones próximas a vencer, para facilitar el seguimiento preventivo.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Generar recordatorios para próximas fechas
  Given que existen vacunas o desparasitaciones con fecha próxima recomendada
  When el sistema evalúa vencimientos
  Then debe generar recordatorios asociados a la mascota
  And debe registrar fecha de generación y estado

Scenario: Gestionar recordatorio
  Given que existe un recordatorio generado
  When el personal gestiona el recordatorio
  Then el sistema debe registrar la acción y actualizar el estado
```

### HU-09 - Seleccionar mascota e iniciar chat con IA
**RF Relacionado:** RF-09  
**Prioridad:** Must  
**Rol:** Tutor (Propietario)  
**Historia:** Como propietario, quiero seleccionar una mascota y abrir un chat con contexto de la mascota, para recibir orientación inicial desde el asistente de IA.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Iniciar chat con mascota válida
  Given que el propietario está autenticado y tiene al menos una mascota registrada
  When selecciona una mascota para iniciar chat con IA
  Then el sistema debe vincular el hilo de conversación a esa mascota
  And debe mostrar el contexto de la mascota en la conversación

Scenario: No iniciar chat sin mascota válida
  Given que la mascota no existe o no está asociada al propietario
  When intenta iniciar chat
  Then el sistema debe impedir continuar
  And debe mostrar mensaje de error
```

### HU-10 - Registrar motivo de consulta en chat
**RF Relacionado:** RF-10  
**Prioridad:** Must  
**Rol:** Tutor / Asistente IA  
**Historia:** Como propietario, quiero describir mi motivo de consulta en lenguaje natural, para que la IA entienda el caso sin llenar un formulario largo.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Capturar motivo de consulta
  Given que hay una conversación iniciada con mascota seleccionada
  When el propietario describe el síntoma o percance
  Then el sistema debe guardar una síntesis del motivo
  And la IA debe solicitar solo preguntas necesarias si la información es insuficiente
```

### HU-11 - Orientación inicial con IA
**RF Relacionado:** RF-11  
**Prioridad:** Must  
**Rol:** Tutor  
**Historia:** Como propietario, quiero recibir orientación inicial empática y comprensible, para entender cuándo debo buscar atención profesional.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Recibir orientación inicial segura
  Given que se identificó mascota y motivo de consulta
  When la IA responde
  Then la respuesta debe usar lenguaje claro, no técnico
  And no debe ofrecer diagnóstico definitivo
  And debe considerar especie/edad/antecedentes si están disponibles
  And debe recomendar atención profesional cuando proceda
```

### HU-12 - Identificación de señales de alarma
**RF Relacionado:** RF-12  
**Prioridad:** Must  
**Rol:** Tutor / Asistente IA  
**Historia:** Como propietario, quiero que la IA detecte señales de alarma y me alerte claramente, para buscar atención inmediata si es una emergencia.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Detectar emergencia y priorizar
  Given que el propietario describe síntomas graves
  When la IA evalúa la situación
  Then debe clasificar como urgencia/emergencia
  And debe alertar explícitamente sobre necesidad de atención inmediata
  And no debe condicionar la urgencia al agendamiento
  And debe priorizar la urgencia sobre el proceso de agendamiento
```

### HU-13 - Recomendación de valoración presencial y agendamiento
**RF Relacionado:** RF-13  
**Prioridad:** Must  
**Rol:** Tutor  
**Historia:** Como propietario, quiero recibir una recomendación justificada de valoración presencial con opción de agendar cita desde el chat, sin presión.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Recomendar valoración presencial con opción de agendar
  Given que la situación requiere valoración profesional
  When la IA hace la recomendación
  Then debe explicar por qué es conveniente acudir
  And debe ofrecer la opción "Agendar cita"
  And el tutor puede rechazar sin presión
```

### HU-14 - Ver disponibilidad de dos sedes
**RF Relacionado:** RF-14  
**Prioridad:** Must  
**Rol:** Tutor  
**Historia:** Como propietario, quiero ver las dos sedes de PetCare y su disponibilidad real, para elegir dónde agendar.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Mostrar disponibilidad real de ambas sedes
  Given que hay dos sedes activas
  When el tutor consulta disponibilidad para agendar
  Then el sistema debe mostrar horarios reales de la agenda
  And no debe mostrar horarios ficticios
  And si no hay disponibilidad en una sede debe ofrecer alternativas
```

### HU-15 - Agendar cita desde el chat
**RF Relacionado:** RF-15  
**Prioridad:** Must  
**Rol:** Tutor  
**Historia:** Como propietario, quiero agendar una cita desde la misma conversación sin salir del chat, para completar el proceso rápidamente.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Agendar cita completa desde el chat
  Given que hay recomendación de valoración presencial
  And hay disponibilidad real
  When el tutor selecciona sede, fecha, hora y confirma
  Then la reserva debe completarse dentro del flujo del chat
  And la cita debe quedar registrada correctamente
```

### HU-16 - Confirmación con datos obligatorios
**RF Relacionado:** RF-16  
**Prioridad:** Must  
**Rol:** Tutor / Sistema  
**Historia:** Como propietario, quiero confirmar la reserva con los datos obligatorios, para asegurar que la cita se registre correctamente.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Confirmar solo con datos completos
  Given que se seleccionó horario
  When el tutor confirma la reserva
  Then el sistema debe validar motivo, mascota y datos obligatorios
  And solo debe confirmar si todos son válidos
  And debe mostrar resumen de la cita antes de confirmar
```

### HU-17 - Asociación de cita a tutor, mascota y sede
**RF Relacionado:** RF-17  
**Prioridad:** Must  
**Rol:** Sistema  
**Historia:** Como sistema, quiero asociar cada cita al tutor, mascota seleccionada, sede elegida y agenda correspondiente, para garantizar trazabilidad.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Asociar cita correctamente
  Given que la reserva fue validada
  When se confirma la cita
  Then debe quedar asociada a id_propietario, id_mascota, id_sede e id_agenda
  And debe quedar trazable en los módulos correspondientes
```

### HU-18 - Consulta de cita desde módulos autorizados
**RF Relacionado:** RF-18  
**Prioridad:** Must  
**Rol:** Tutor / Personal autorizado  
**Historia:** Como tutor o personal autorizado, quiero consultar el estado de la cita agendada, para dar seguimiento.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Consultar cita agendada
  Given que existe una cita registrada
  When el tutor o personal autorizado consulta
  Then debe ver fecha, hora, sede, estado y datos asociados
  And los cambios de estado deben reflejarse correctamente
```

### HU-19 - Manejo de errores, cancelación y disponibilidad
**RF Relacionado:** RF-19  
**Prioridad:** Must  
**Rol:** Sistema / Tutor  
**Historia:** Como sistema, quiero gestionar errores, cancelaciones y falta de disponibilidad sin generar reservas duplicadas o inconsistentes.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: No duplicar citas
  Given que un horario acaba de ser ocupado
  When otro usuario intenta reservarlo
  Then el sistema debe rechazar la reserva
  And debe ofrecer alternativas

Scenario: Cancelar sin generar reserva
  Given que el tutor cancela durante el proceso
  When cancela
  Then no debe crearse ninguna cita
  And el flujo debe continuar o cerrarse sin reservas inconsistentes
```

### HU-20 - Derivación o escalamiento a personal veterinario
**RF Relacionado:** RF-20  
**Prioridad:** Should  
**Rol:** Personal veterinario / Sistema  
**Historia:** Como sistema, quiero identificar casos que requieran escalamiento a personal veterinario, dejando explícito si no está implementado.

#### Criterios de Aceptación (Gherkin)

```gherkin
Scenario: Identificar necesidad de escalamiento
  Given que el caso supera la capacidad de orientación inicial
  When el sistema lo detecta
  Then debe presentar opción de derivación o escalamiento
  And si no está implementado debe documentar la limitación claramente
  And nunca debe demorar la urgencia por agendamiento
```

## 3. Trazabilidad RF → HU → Gherkin

| RF | HU | Escenarios clave | Prioridad |
|---|---|---|---|
| RF-01 | HU-01 | Registro exitoso / datos faltantes | Must |
| RF-02 | HU-02 | Consulta con historial / vacío | Must |
| RF-03 | HU-03 | Autorizar / revocar / consultar | Must |
| RF-04 | HU-04 | Registrar con autorización / sin autorización | Must |
| RF-05 | HU-05 | Solicitar con disponibilidad / horario ocupado | Must |
| RF-06 | HU-06 | Consultar con registros / sin registros | Must |
| RF-07 | HU-07 | Consultar / sin registros | Should |
| RF-08 | HU-08 | Generar recordatorios / gestionar | Should |
| RF-09 | HU-09 | Iniciar con mascota válida / inválida | Must |
| RF-10 | HU-10 | Capturar motivo / insuficiente información | Must |
| RF-11 | HU-11 | Orientación segura sin diagnóstico | Must |
| RF-12 | HU-12 | Emergencia prioritaria sobre agendamiento | Must |
| RF-13 | HU-13 | Recomendación + opción agendar sin presión | Must |
| RF-14 | HU-14 | Dos sedes disponibilidad real / alternativas | Must |
| RF-15 | HU-15 | Agendar desde chat completo | Must |
| RF-16 | HU-16 | Confirmar con datos obligatorios | Must |
| RF-17 | HU-17 | Asociación tutor/mascota/sede/agenda | Must |
| RF-18 | HU-18 | Consulta en módulos autorizados | Must |
| RF-19 | HU-19 | Sin duplicados / cancelación sin reserva | Must |
| RF-20 | HU-20 | Escalamiento / limitación si no implementado | Should |

## 4. Notas
- Basado en `docs/Ia/requisitos.md`, `docs/Ia/entrevista.md` y `docs/Ia/prompts.md`
- MVP visual no funcional; historias corresponden a arquitectura propuesta
- Se priorizan emergencias sobre agendamiento
- IA no diagnostica, no recomienda medicamentos peligrosos
- BD/proveedor LLM/calendario externo no asumidos

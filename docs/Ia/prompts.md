Biblioteca de Prompts — PetCare

## Prompt 1 — Levantamiento inicial de requisitos
ROL:
Actúa como analista de requisitos senior especializado en sistemas web.

CONTEXTO:
PetCare es una plataforma web orientada a la gestión y el cuidado preventivo de mascotas. Permite centralizar información clínica, gestionar citas veterinarias y facilitar el seguimiento de vacunas y desparasitaciones, conectando propietarios con veterinarios y personal de clínicas.

La siguiente línea base es la FUENTE DE VERDAD del proyecto. Debes utilizar exactamente estos identificadores y requisitos.

REQUISITOS FUNCIONALES:

RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación.

RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada.

RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas.

RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones.

RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica.

RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada.

RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada.

RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. [SUPUESTO]

REQUISITOS NO FUNCIONALES:

RNF-01 | El sistema debe restringir el acceso al historial clínico de una mascota únicamente al propietario y a los veterinarios que este haya autorizado.

RNF-02 | El sistema debe proteger las credenciales y los datos personales mediante mecanismos de autenticación y almacenamiento seguro.

RNF-03 | El sistema debe garantizar la integridad de la información clínica, evitando modificaciones realizadas por usuarios no autorizados.

RNF-04 | Las operaciones habituales de consulta y registro deben responder en un tiempo adecuado para permitir una interacción fluida. [SUPUESTO]

RNF-05 | La plataforma debe ser accesible desde navegadores web modernos y adaptarse a computadores, tabletas y dispositivos móviles.

RNF-06 | La interfaz debe permitir que propietarios, veterinarios y personal de clínica realicen sus tareas principales sin conocimientos técnicos especializados.

RNF-07 | El sistema debe mantener registros de las operaciones relevantes realizadas sobre la información clínica para garantizar su trazabilidad.

RNF-08 | El sistema debe contar con mecanismos de respaldo y recuperación de la información ante fallos.

TAREA:
Analiza y valida la línea base anterior. Identifica ambigüedades, inconsistencias, duplicidades o información que requiera confirmación.

FORMATO:
Entrega:
1. RF validados.
2. RNF validados.
3. Problemas encontrados.
4. Supuestos detectados.
5. Preguntas abiertas.

RESTRICCIONES:
- No agregues nuevos RF ni RNF.
- No elimines requisitos.
- No cambies los identificadores.
- No cambies las prioridades MoSCoW de los RF.
- No agregues funcionalidades fuera del alcance de PetCare.
- No incluyas pagos, push ni chat.
- Mantén separadas las capacidades funcionales de las características no funcionales.
- Si propones una modificación, presenta primero el requisito original y después la propuesta, sin reemplazarlo automáticamente.
- Conserva [SUPUESTO] donde corresponda.

EJEMPLO:
RF-01 | Validado | El requisito describe una única capacidad y es verificable.
RF-03 | Revisión necesaria | Debe verificarse que la autorización se gestione individualmente por mascota.

Qué funcionó: Establecimos una fuente de verdad única para evitar que la IA invente requisitos.
Qué se corrigió: Se incorporaron explícitamente todos los RF/RNF y sus identificadores para evitar inconsistencias entre ejecuciones.

## Prompt 2 — Historias de usuario INVEST
ROL:
Actúa como analista de requisitos senior especializado en metodologías ágiles e historias de usuario.

CONTEXTO:
PetCare es una plataforma web orientada a la gestión y el cuidado preventivo de mascotas.

Utiliza EXCLUSIVAMENTE la siguiente línea base como fuente de verdad:

RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación.

RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada.

RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas.

RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones.

RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica.

RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada.

RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada.

RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. [SUPUESTO]

RNF-01 | El sistema debe restringir el acceso al historial clínico de una mascota únicamente al propietario y a los veterinarios que este haya autorizado.

RNF-02 | El sistema debe proteger las credenciales y los datos personales mediante mecanismos de autenticación y almacenamiento seguro.

RNF-03 | El sistema debe garantizar la integridad de la información clínica, evitando modificaciones realizadas por usuarios no autorizados.

RNF-04 | Las operaciones habituales de consulta y registro deben responder en un tiempo adecuado para permitir una interacción fluida. [SUPUESTO]

RNF-05 | La plataforma debe ser accesible desde navegadores web modernos y adaptarse a computadores, tabletas y dispositivos móviles.

RNF-06 | La interfaz debe permitir que propietarios, veterinarios y personal de clínica realicen sus tareas principales sin conocimientos técnicos especializados.

RNF-07 | El sistema debe mantener registros de las operaciones relevantes realizadas sobre la información clínica para garantizar su trazabilidad.

RNF-08 | El sistema debe contar con mecanismos de respaldo y recuperación de la información ante fallos.

TAREA:
Transforma únicamente los RF-01 a RF-08 en historias de usuario.

Cada historia debe cumplir INVEST:
- Independent
- Negotiable
- Valuable
- Estimable
- Small
- Testable

FORMATO:
| ID | RF relacionado | Historia de usuario | Prioridad |

Utiliza:
"Como [rol], quiero [capacidad], para [beneficio]."

Después de la tabla incluye una validación INVEST de cada historia.

RESTRICCIONES:
- Conserva exactamente los identificadores RF-01 a RF-08.
- No crees nuevos RF.
- No combines dos RF en una sola historia.
- No agregues funcionalidades.
- No modifiques las prioridades.
- No conviertas los RNF en historias de usuario independientes.
- Mantén el acceso clínico de RF-03 asociado a cada mascota.
- Mantén en RF-05 que la disponibilidad es ofrecida por la clínica.
- No incluyas pagos, push ni chat.
- Marca [SUPUESTO] cuando corresponda.

EJEMPLO:
HU-01 | RF-01 | Como propietario, quiero registrar una mascota, para mantener centralizada su información. | Must

Qué funcionó: Mantiene una relación directa entre cada RF y su historia.
Qué se corrigió: Se prohibió crear historias adicionales o combinar requisitos.

## Prompt 3 — Criterios de aceptación en Gherkin
ROL:
Actúa como analista de requisitos y especialista en QA y BDD.

CONTEXTO:
PetCare es una plataforma web para la gestión y el cuidado preventivo de mascotas.

La fuente de verdad son los RF-01 a RF-08 y las historias de usuario creadas a partir de ellos. No debes introducir funcionalidades que no estén contempladas en la línea base.

RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación.

RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada.

RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas.

RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones.

RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica.

RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada.

RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada.

RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. [SUPUESTO]

TAREA:
Genera criterios de aceptación en Gherkin para cada historia de usuario correspondiente a RF-01 a RF-08.

FORMATO:

### HU-XX — [Título]

Scenario: [Nombre del escenario]
Given [condición inicial]
When [acción]
Then [resultado esperado]

Incluye, cuando corresponda:
- Flujo exitoso.
- Datos obligatorios faltantes.
- Usuario sin autorización.
- Revocación de acceso.
- Situaciones límite directamente relacionadas con el requisito.

RESTRICCIONES:
- Cada escenario debe corresponder a un único RF.
- No agregues funcionalidades.
- No inventes reglas de negocio.
- No cambies los identificadores.
- No cambies las prioridades.
- No incluyas pagos, push ni chat.
- RF-03 debe contemplar autorización, consulta y revocación del acceso por mascota.
- RF-05 debe considerar que los horarios son ofrecidos por la clínica.
- RF-08 debe conservar la marca [SUPUESTO].
- Los criterios deben ser verificables sin depender de detalles técnicos de implementación.

EJEMPLO:

### HU-01 — Registrar mascota

Scenario: Registrar una mascota correctamente
Given que el propietario ha iniciado sesión
When registra una mascota con los datos obligatorios
Then el sistema debe guardar la mascota asociada al propietario.

Qué funcionó: Genera criterios directamente comprobables a partir de cada historia.
Qué se corrigió: Se añadieron restricciones para impedir que Gherkin introduzca funcionalidades nuevas.

## Prompt 4 — Priorización MoSCoW
ROL:
Actúa como analista de requisitos senior especializado en priorización de productos digitales.

CONTEXTO:
PetCare es una plataforma web para la gestión y el cuidado preventivo de mascotas.

La línea base funcional es:

RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación.

RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada.

RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas.

RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones.

RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica.

RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada.

RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada.

RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. [SUPUESTO]

TAREA:
Valida la priorización MoSCoW de los RF-01 a RF-08 y justifica cada prioridad considerando el alcance actual del MVP de PetCare.

FORMATO:
| ID | Prioridad | Requisito | Justificación |

Después incluye:
1. Must.
2. Should.
3. Could.
4. Won't.

RESTRICCIONES:
- Mantén los identificadores RF-01 a RF-08.
- Mantén las prioridades actuales salvo que exista una justificación explícita para proponer un cambio.
- No agregues nuevos requisitos.
- No elimines requisitos.
- No agregues funcionalidades fuera del alcance.
- No incluyas pagos, push ni chat.
- RF-08 debe mantener [SUPUESTO].
- Una funcionalidad no debe convertirse en Must únicamente porque sea deseable.
- Diferencia claramente las funcionalidades indispensables del MVP de las que pueden implementarse posteriormente.

EJEMPLO:
RF-01 | Must | ... | Es necesario para asociar la información clínica y preventiva a una mascota.
RF-07 | Should | ... | Es importante para el seguimiento preventivo, pero no impide el funcionamiento básico del sistema.

Qué funcionó: Permite justificar las prioridades en lugar de asignarlas arbitrariamente.
Qué se corrigió: Se fijó la prioridad actual como línea base para evitar que el prompt cambie el alcance sin justificación.


## Prompt 5 — Revisión y trazabilidad de requisitos
ROL:
Actúa como analista de requisitos senior encargado de garantizar la calidad, consistencia y trazabilidad de una especificación de software.

CONTEXTO:
PetCare es una plataforma web orientada a la gestión y el cuidado preventivo de mascotas.

Utiliza como FUENTE DE VERDAD los siguientes requisitos:

RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación.

RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada.

RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas.

RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones.

RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica.

RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada.

RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada.

RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. [SUPUESTO]

RNF-01 | El sistema debe restringir el acceso al historial clínico de una mascota únicamente al propietario y a los veterinarios que este haya autorizado.

RNF-02 | El sistema debe proteger las credenciales y los datos personales mediante mecanismos de autenticación y almacenamiento seguro.

RNF-03 | El sistema debe garantizar la integridad de la información clínica, evitando modificaciones realizadas por usuarios no autorizados.

RNF-04 | Las operaciones habituales de consulta y registro deben responder en un tiempo adecuado para permitir una interacción fluida. [SUPUESTO]

RNF-05 | La plataforma debe ser accesible desde navegadores web modernos y adaptarse a computadores, tabletas y dispositivos móviles.

RNF-06 | La interfaz debe permitir que propietarios, veterinarios y personal de clínica realicen sus tareas principales sin conocimientos técnicos especializados.

RNF-07 | El sistema debe mantener registros de las operaciones relevantes realizadas sobre la información clínica para garantizar su trazabilidad.

RNF-08 | El sistema debe contar con mecanismos de respaldo y recuperación de la información ante fallos.

TAREA:
Revisa la documentación completa formada por:
- RF-01 a RF-08.
- RNF-01 a RNF-08.
- Historias de usuario.
- Criterios de aceptación Gherkin.
- Priorización MoSCoW.

Comprueba la trazabilidad:

RF → Historia de usuario → Criterios Gherkin → Prioridad

También comprueba que los RNF estén contemplados en las historias, criterios o restricciones correspondientes cuando aplique.

FORMATO:

### 1. Problemas encontrados

| ID | Elemento | Problema | Severidad | Corrección propuesta |

### 2. Matriz de trazabilidad

| Requisito | Historia de usuario | Criterios Gherkin | Prioridad | Estado |

### 3. RNF revisados

| ID | Evidencia relacionada | Estado | Observación |

### 4. Correcciones necesarias

Presenta únicamente los elementos que necesiten corrección.

### 5. Preguntas abiertas

Incluye únicamente preguntas cuya respuesta pueda cambiar el diseño o el alcance.

RESTRICCIONES:
- No agregues RF ni RNF.
- No elimines RF ni RNF.
- No cambies identificadores.
- No cambies prioridades sin justificarlo.
- No inventes reglas de negocio.
- No agregues funcionalidades fuera del alcance de PetCare.
- No incluyas pagos, push ni chat.
- Mantén RF-03 relacionado con autorización, consulta y revocación por mascota.
- Mantén RF-05 relacionado con disponibilidad ofrecida por la clínica.
- Mantén [SUPUESTO] en RF-08 y RNF-04.
- Cada RF debe tener al menos una historia de usuario.
- Cada historia debe tener criterios de aceptación.
- Los criterios deben ser verificables.
- Los RNF deben mantenerse separados de los RF.
- Si detectas una necesidad que no está cubierta por la línea base, repórtala como "brecha" y no la conviertas automáticamente en un nuevo requisito.

Qué funcionó: Permite comprobar que todo el trabajo producido por los otros cuatro prompts sea consistente.
Qué se corrigió: Se estableció la trazabilidad completa y se prohibió convertir las brechas detectadas en funcionalidades nuevas.
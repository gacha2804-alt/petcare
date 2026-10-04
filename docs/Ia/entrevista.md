# Entrevista simulada — Cliente veterinario
**Rol simulado:** Dr. Andrés Molina, veterinario y propietario de una clínica veterinaria con dos sedes.

**Objetivo:** Levantamiento de requisitos para el desarrollo de una plataforma web para la gestión y seguimiento de pacientes veterinarios.

**Herramienta:** IA (Claude) actuando como cliente mediante un prompt de rol con contexto del negocio.
---
## 1. Presentación y contexto del negocio

**Entrevistador:** Doctor, para comenzar, ¿podría contarnos un poco sobre su clínica y cómo trabajan actualmente?

**Dr. Andrés Molina:** Claro. Tenemos una clínica veterinaria con dos sedes y llevamos aproximadamente 12 años trabajando. Atendemos principalmente perros y gatos, aunque ocasionalmente también recibimos otros animales. En cada sede tenemos veterinarios y personal administrativo.

**Entrevistador:** ¿Cuántos pacientes atienden aproximadamente?

**Dr. Andrés Molina:** Dependiendo del día podemos atender entre 15 y 30 pacientes por sede. Tenemos bastantes pacientes frecuentes, especialmente para controles, vacunas, desparasitación y tratamientos.

**Entrevistador:** ¿Actualmente utilizan algún sistema para manejar la información de los pacientes?

**Dr. Andrés Molina:** Sí. Tenemos un software instalado en los computadores de la clínica desde hace unos seis años. Allí registramos las historias clínicas, pero es un sistema de escritorio y no está conectado con otros procesos que manejamos.

**Entrevistador:** ¿Qué otros sistemas utilizan?

**Dr. Andrés Molina:** Para las citas usamos principalmente Google Calendar y la secretaria es quien organiza la agenda. Los recordatorios a los propietarios normalmente se hacen por WhatsApp, pero manualmente.

**Entrevistador:** Entonces, ¿los sistemas están conectados entre sí?

**Dr. Andrés Molina:** No. Ese es precisamente uno de los problemas. La historia clínica está en un sistema, las citas en otro y los recordatorios dependen mucho de la secretaria.
---

# 2. Problemas actuales

**Entrevistador:** ¿Cuál considera que es actualmente el proceso que más problemas genera en la clínica?

**Dr. Andrés Molina:** Diría que el seguimiento de los pacientes. Tenemos que estar pendientes de cuándo les corresponde una vacuna, una desparasitación o un control. Muchas veces esa información queda registrada, pero nadie recibe una alerta automática.

**Entrevistador:** ¿Cómo hacen actualmente para recordar esas fechas?

**Dr. Andrés Molina:** La secretaria revisa las historias y trata de identificar los pacientes que ya deberían volver. Después comienza a escribirles por WhatsApp uno por uno.

**Entrevistador:** ¿Cuánto tiempo puede tomar ese proceso?

**Dr. Andrés Molina:** Fácilmente unas dos o tres horas a la semana, dependiendo de la cantidad de pacientes pendientes.

**Entrevistador:** ¿Han tenido casos en los que se les olvide contactar a algún propietario?

**Dr. Andrés Molina:** Sí. No es que pase todos los días, pero sucede. Cuando tenemos mucho trabajo, algunos pacientes pueden quedar sin seguimiento.

---

# 3. Manejo de las historias clínicas

**Entrevistador:** ¿Cómo se registra actualmente la información durante una consulta?

**Dr. Andrés Molina:** El veterinario revisa la historia del paciente y después registra la consulta en el sistema. El problema es que muchas veces estamos atendiendo un paciente tras otro y terminamos completando algunos datos después.

**Entrevistador:** ¿Eso puede generar información incompleta?

**Dr. Andrés Molina:** Sí. Puede ocurrir que algún detalle de la consulta quede sin registrar o que el veterinario tenga que volver a revisar notas para completar la información.

**Entrevistador:** ¿Qué información considera indispensable dentro de la historia clínica?

**Dr. Andrés Molina:** Datos del propietario y del paciente, especie, raza, edad, peso, antecedentes, vacunas, desparasitaciones, consultas anteriores, diagnósticos, medicamentos formulados, exámenes y observaciones del veterinario.

**Entrevistador:** ¿También sería importante guardar documentos o resultados de exámenes?

**Dr. Andrés Molina:** Sí. Sería bastante útil poder adjuntar resultados de laboratorio, imágenes, fórmulas o documentos relacionados con el paciente.

---

# 4. Problema entre las dos sedes

**Entrevistador:** Mencionó que tienen dos sedes. ¿Cómo manejan la información cuando un paciente es atendido en una sede diferente?

**Dr. Andrés Molina:** Ese es otro problema importante. La información no siempre está actualizada de la misma manera en las dos sedes.

**Entrevistador:** ¿Qué hacen cuando necesitan consultar información que está en la otra sede?

**Dr. Andrés Molina:** Normalmente llamamos a la otra sede o pedimos que nos envíen fotografías o capturas de la información por WhatsApp.

**Entrevistador:** ¿Qué inconvenientes genera esto?

**Dr. Andrés Molina:** Se pierde tiempo y también puede haber errores. Por ejemplo, si un paciente fue vacunado en una sede y en la otra no tienen la información actualizada, podrían pensar que la vacuna todavía está pendiente.

**Entrevistador:** Entonces, ¿consideraría importante tener una única plataforma web para las dos sedes?

**Dr. Andrés Molina:** Sí. Me gustaría que, sin importar en cuál sede se atienda el paciente, el veterinario autorizado pueda consultar la información actualizada.

---

# 5. Gestión de citas

**Entrevistador:** Hablemos ahora de las citas. ¿Cómo se solicitan actualmente?

**Dr. Andrés Molina:** Normalmente el propietario escribe por WhatsApp o llama a la clínica. La secretaria revisa el calendario y busca un horario disponible.

**Entrevistador:** ¿Qué sucede después de agendar una cita?

**Dr. Andrés Molina:** La cita queda registrada en el calendario, pero la confirmación depende de que la secretaria se acuerde de escribirle al propietario.

**Entrevistador:** ¿Han tenido problemas con personas que no asisten a sus citas?

**Dr. Andrés Molina:** Sí, tenemos algunos casos de personas que reservan una cita y simplemente no aparecen.

**Entrevistador:** ¿Qué le gustaría que hiciera el sistema en esos casos?

**Dr. Andrés Molina:** Sería bueno que el sistema enviara automáticamente un recordatorio y permitiera confirmar la asistencia. Algo sencillo como "Confirmar cita" o "Cancelar cita".

**Entrevistador:** ¿Y si el propietario no puede asistir?

**Dr. Andrés Molina:** Debería poder cancelar o solicitar otro horario sin tener que llamar necesariamente a la clínica.

---

# 6. Agenda de la clínica

**Entrevistador:** ¿Qué información debería poder visualizar la secretaria en la agenda?

**Dr. Andrés Molina:** Me gustaría que pudiera ver las citas del día, el nombre del propietario, el paciente, el motivo de la consulta, el veterinario asignado y el estado de la cita.

**Entrevistador:** ¿Qué estados considera necesarios?

**Dr. Andrés Molina:** Por ejemplo: pendiente, confirmada, cancelada, atendida y no asistió.

**Entrevistador:** ¿Debería poder filtrar las citas?

**Dr. Andrés Molina:** Sí. Sería útil filtrar por fecha, sede y veterinario.

**Entrevistador:** ¿Y los veterinarios deberían tener acceso a toda la agenda?

**Dr. Andrés Molina:** No necesariamente. Sería mejor que cada veterinario pueda consultar las citas que tiene asignadas, mientras que la secretaria y el administrador tengan una vista más completa.

---

# 7. Usuarios y permisos

**Entrevistador:** ¿Quiénes utilizarían la plataforma web?

**Dr. Andrés Molina:** Principalmente los veterinarios, las secretarias y el administrador de la clínica.

**Entrevistador:** ¿Todos deberían tener los mismos permisos?

**Dr. Andrés Molina:** No. Creo que debería existir una diferencia.

**Entrevistador:** ¿Cómo los dividiría?

**Dr. Andrés Molina:** El administrador debería poder gestionar usuarios, sedes y configuraciones. La secretaria debería gestionar citas y consultar información básica de los pacientes. El veterinario debería poder consultar y actualizar historias clínicas.

**Entrevistador:** ¿Considera importante que cada usuario tenga su propia cuenta?

**Dr. Andrés Molina:** Sí. No me parece conveniente que todos entren con el mismo usuario porque después no sabríamos quién modificó una historia.

**Entrevistador:** Entonces, ¿sería importante registrar quién realizó cada modificación?

**Dr. Andrés Molina:** Definitivamente. Sobre todo en información clínica.

---

# 8. Vacunas y desparasitaciones

**Entrevistador:** ¿Qué información registran cuando aplican una vacuna?

**Dr. Andrés Molina:** Registramos el nombre de la vacuna, fabricante, lote, fecha de aplicación, dosis, vía de aplicación, peso del paciente, edad y veterinario que la aplicó.

**Entrevistador:** ¿Actualmente el sistema calcula automáticamente cuándo debe aplicarse la siguiente dosis?

**Dr. Andrés Molina:** No. Ese cálculo depende mucho del veterinario o de la secretaria.

**Entrevistador:** ¿Cómo le gustaría que funcionara?

**Dr. Andrés Molina:** Me gustaría poder configurar los protocolos y que el sistema calcule automáticamente la próxima fecha.

**Entrevistador:** ¿El protocolo debería ser igual para todos los animales?

**Dr. Andrés Molina:** No. Puede depender de la especie, edad y producto utilizado.

**Entrevistador:** ¿Qué debería hacer el sistema cuando se acerque la fecha?

**Dr. Andrés Molina:** Debería generar una alerta para el personal de la clínica. Por ejemplo, una semana antes.

---

# 9. Seguimiento de pacientes

**Entrevistador:** Además de vacunas y desparasitación, ¿qué otros seguimientos considera importantes?

**Dr. Andrés Molina:** Los controles posteriores a una cirugía, tratamientos prolongados, enfermedades crónicas y pacientes que necesitan exámenes de control.

**Entrevistador:** ¿Sería útil que el sistema permitiera crear tareas o alertas de seguimiento?

**Dr. Andrés Molina:** Sí. Por ejemplo, si atendemos un paciente y queremos volver a revisarlo en 15 días, sería bueno registrar esa fecha y que el sistema nos avise.

**Entrevistador:** ¿Quién debería recibir esas alertas?

**Dr. Andrés Molina:** Principalmente el veterinario responsable y, dependiendo del caso, la secretaria.

---

# 10. Panel principal de la plataforma

**Entrevistador:** Si usted ingresara a la plataforma cada mañana, ¿qué información le gustaría encontrar en la pantalla principal?

**Dr. Andrés Molina:** Me gustaría ver las citas del día, pacientes pendientes de seguimiento, vacunas próximas a vencer y alertas importantes.

**Entrevistador:** ¿También le gustaría tener indicadores generales?

**Dr. Andrés Molina:** Sí. Sería interesante saber cuántas consultas se atendieron, cuántas citas fueron canceladas y cuántos pacientes tienen seguimientos pendientes.

**Entrevistador:** ¿Considera necesario que esa información pueda filtrarse por sede?

**Dr. Andrés Molina:** Sí. Como tenemos dos sedes, sería muy útil poder consultar cada una por separado o ver la información general de las dos.

---

# 11. Búsqueda de pacientes

**Entrevistador:** Cuando necesita encontrar un paciente, ¿cómo lo busca actualmente?

**Dr. Andrés Molina:** Normalmente por nombre del paciente o del propietario.

**Entrevistador:** ¿Qué otros filtros serían útiles?

**Dr. Andrés Molina:** Número de identificación del propietario, especie, raza o incluso número de historia clínica.

**Entrevistador:** ¿Le gustaría que desde los resultados de búsqueda pudiera acceder directamente a la historia?

**Dr. Andrés Molina:** Sí. La idea sería no tener que buscar en varios lugares.

---

# 12. Acceso a información de los propietarios

**Entrevistador:** ¿Actualmente los propietarios pueden consultar la información de sus mascotas?

**Dr. Andrés Molina:** No directamente. Si necesitan una fórmula, un resultado o información de una consulta, normalmente la solicitamos por WhatsApp o se les entrega físicamente.

**Entrevistador:** ¿Consideraría útil que la plataforma permitiera generar documentos para entregar al propietario?

**Dr. Andrés Molina:** Sí. Por ejemplo, una fórmula médica o un resumen de la consulta.

**Entrevistador:** ¿Le gustaría que esos documentos quedaran asociados a la historia del paciente?

**Dr. Andrés Molina:** Sí, sería mucho mejor para tener todo organizado.
---

# 13. Seguridad de la información

**Entrevistador:** Al manejar información clínica, ¿qué aspectos de seguridad considera importantes?

**Dr. Andrés Molina:** Primero, que cada usuario tenga su propia cuenta y contraseña. También que no cualquier empleado pueda modificar información clínica.

**Entrevistador:** ¿Le gustaría saber quién modificó una historia clínica?

**Dr. Andrés Molina:** Sí. Debería quedar registrado el usuario y la fecha de modificación.

**Entrevistador:** ¿Qué pasaría si un empleado deja de trabajar en la clínica?

**Dr. Andrés Molina:** Su acceso debería poder desactivarse inmediatamente.

---

# 14. Facilidad de uso

**Entrevistador:** ¿Qué tan importante es para usted que la plataforma sea sencilla?

**Dr. Andrés Molina:** Bastante. No quiero un sistema complicado que haga que los empleados terminen volviendo a WhatsApp, Excel o papel.

**Entrevistador:** ¿Qué espera de la interfaz?

**Dr. Andrés Molina:** Que sea clara, rápida y que las funciones principales estén fáciles de encontrar. Por ejemplo, buscar paciente, registrar consulta y revisar citas no debería requerir muchos pasos.

---

# 15. Problemas que espera solucionar

**Entrevistador:** Si tuviéramos que resumir los principales problemas que espera solucionar con la plataforma, ¿cuáles serían?

**Dr. Andrés Molina:** Principalmente:

1. Tener la información de los pacientes centralizada.
2. Evitar que la información se pierda entre las dos sedes.
3. Reducir el trabajo manual de la secretaria.
4. Automatizar los recordatorios de vacunas y seguimientos.
5. Mejorar la gestión de citas.
6. Reducir las inasistencias.
7. Facilitar el registro y consulta de historias clínicas.
8. Tener mayor control sobre los usuarios que modifican información.
9. Poder consultar información y estadísticas de la clínica.
10. Tener una plataforma que sea fácil de utilizar.

---

# 16. Cierre de la entrevista

**Entrevistador:** Para terminar, si pudiera pedir tres funciones indispensables para la primera versión de la plataforma, ¿cuáles serían?

**Dr. Andrés Molina:** Primero, una buena gestión de historias clínicas. Segundo, una agenda de citas que permita controlar las confirmaciones. Y tercero, un sistema de alertas para vacunas, desparasitaciones y seguimientos.

**Entrevistador:** ¿Hay alguna función que no considere prioritaria para una primera versión?

**Dr. Andrés Molina:** La facturación y el inventario de medicamentos ya los manejamos con otro sistema y actualmente funcionan bien. No sería necesario incluirlos en esta primera versión.

**Entrevistador:** ¿Qué esperaría finalmente de esta plataforma?

**Dr. Andrés Molina:** Que nos ayude a organizar la información y a reducir tareas manuales. No quiero que reemplace el trabajo del veterinario, sino que nos permita tener la información organizada y recibir alertas para poder hacer un mejor seguimiento de los pacientes.

---

## Principales necesidades identificadas

A partir de la entrevista se identifican las siguientes necesidades:

| Necesidad                        | Situación actual                              | Solución esperada                              |
| -------------------------------- | --------------------------------------------- | ---------------------------------------------- |
| Historias clínicas centralizadas | Información separada entre sedes              | Historia clínica web centralizada              |
| Gestión de citas                 | Google Calendar y gestión manual              | Agenda web con estados y disponibilidad        |
| Confirmación de citas            | WhatsApp manual                               | Confirmación y cancelación desde la plataforma |
| Seguimiento de vacunas           | Revisión manual                               | Alertas y cálculo de próximas fechas           |
| Seguimiento de pacientes         | Depende de recordatorios manuales             | Alertas configurables                          |
| Información entre sedes          | Llamadas y envío de fotos                     | Acceso centralizado según permisos             |
| Registro de consultas            | Se completa posteriormente                    | Registro directo desde la plataforma           |
| Control de usuarios              | Acceso limitado y poco seguimiento            | Roles y permisos                               |
| Auditoría                        | No siempre se identifica quién modificó datos | Registro de usuario y fecha                    |
| Reportes                         | Información dispersa                          | Dashboard con indicadores                      |
| Documentos clínicos              | WhatsApp o documentos físicos                 | Archivos asociados a cada paciente             |
| Facturación e inventario         | Ya existe otro sistema                        | Fuera del alcance inicial                      |

## Alcance inicial de la plataforma

**Incluido:**

* Gestión de usuarios y roles.
* Gestión de pacientes y propietarios.
* Historias clínicas.
* Registro de consultas.
* Gestión de vacunas y desparasitaciones.
* Alertas y seguimientos.
* Agenda y gestión de citas.
* Gestión de las dos sedes.
* Búsqueda y filtros.
* Dashboard administrativo.
* Gestión de documentos clínicos.
* Registro de actividades y modificaciones.

**Fuera del alcance inicial:**

* Facturación.
* Inventario de medicamentos.
* Procesos contables.
* Integración con sistemas externos que actualmente utiliza la clínica.


Biblioteca de Prompts — PetCare

1. Definición de la arquitectura del sistema

Objetivo

Utilizar Inteligencia Artificial para proponer una arquitectura inicial para PetCare, 
teniendo en cuenta que el proyecto está compuesto por una aplicación móvil para propietarios 
y una plataforma web para veterinarios, personal de clínica y administradores.

Prompt utilizado

Actúa como arquitecto de software y analiza el siguiente proyecto llamado PetCare. 
Es una plataforma híbrida Web + Aplicación móvil enfocada en el cuidado preventivo
de mascotas mediante Inteligencia Artificial.
Los roles del sistema son: Propietario, Veterinario, Personal de clínica y Administrador.
El MVP incluye autenticación, gestión de mascotas, historial de salud, síntomas y observaciones, 
vacunas, medicamentos, seguimiento de evolución, citas, notificaciones, roles y permisos, 
evaluación preventiva mediante IA, detección de cambios, resumen de historial mediante IA, 
panel web para veterinarios, panel administrativo, QR de emergencia y localización de veterinarias.
Propón una arquitectura tecnológica organizada por frontend, backend, base de datos, inteligencia artificial 
y servicios externos. Explica la función de cada componente y cómo se comunicarían entre sí.

 Resultado

La IA permitió obtener una propuesta inicial de arquitectura separando claramente el frontend móvil, 
frontend web, backend, base de datos y servicios relacionados con IA.

 ¿Qué funcionó?
 
-Ayudó a identificar los componentes principales del sistema.
-Permitió separar las responsabilidades de cada parte.
-Facilitó la comprensión de la comunicación entre frontend, backend y base de datos.
-Ayudó a identificar servicios adicionales necesarios para notificaciones, QR y localización.

¿Qué no funcionó?

La primera propuesta incluía tecnologías y servicios que no necesariamente eran necesarios para el MVP
y aumentaban la complejidad del proyecto.

¿Qué se corrigió?

Se simplificó la arquitectura y se priorizaron únicamente los componentes necesarios para el MVP. 
También se mantuvo la IA como herramienta de apoyo preventivo y no como sustituto del diagnóstico veterinario.

2. Diseño de la base de datos

Objetivo

Utilizar IA para identificar las entidades principales necesarias para almacenar la información de propietarios, 
mascotas, historial médico, vacunas, medicamentos y citas.

Prompt utilizado

Analiza el proyecto PetCare y diseña un modelo de base de datos relacional para su MVP.
Debe permitir almacenar información de usuarios con diferentes roles: Propietario, Veterinario, Personal de clínica y Administrador.
Cada propietario puede registrar una o varias mascotas. Para cada mascota se debe almacenar información básica, historial de salud,
síntomas y observaciones, vacunas, medicamentos, peso y evolución, citas veterinarias, documentos y datos necesarios para un perfil
de emergencia mediante QR.
Propón las tablas principales, sus campos, claves primarias y relaciones entre ellas.
Evita crear tablas innecesarias y explica brevemente la finalidad de cada tabla.

Resultado

La IA propuso entidades como usuarios, mascotas, historial de salud, vacunas, medicamentos, citas y registros de evolución.

 ¿Qué funcionó?

-Permitió identificar rápidamente las entidades principales.
-Ayudó a detectar relaciones entre usuarios y mascotas.
-Facilitó la organización de la información del historial de cada mascota.
-Sirvió como punto de partida para construir el modelo entidad-relación.

¿Qué no funcionó?

La primera propuesta separaba demasiados datos en tablas independientes y algunas estructuras podían generar complejidad innecesaria.

¿Qué se corrigió?

Se revisaron las entidades y se eliminaron estructuras que no eran necesarias para el MVP.
También se verificó que cada relación tuviera sentido con los roles y funcionalidades definidas para PetCare.

 3. Definición de roles y permisos

 Objetivo

Validar la matriz de permisos de PetCare y determinar qué funcionalidades puede utilizar cada tipo de usuario.

Prompt utilizado

Revisa la siguiente matriz de permisos para una plataforma llamada PetCare:
- Propietario: puede gestionar sus mascotas, consultar y registrar información de salud, gestionar citas, utilizar las funciones de IA y consultar emergencias.
- Veterinario: puede consultar mascotas, gestionar información de salud, gestionar citas, utilizar IA y consultar información de emergencia.
- Personal de clínica: puede consultar información de mascotas, consultar información de salud, gestionar citas y consultar información de emergencia.
- Administrador: tiene acceso a las funciones administrativas y puede consultar la información necesaria para administrar la plataforma.
- Analiza si los permisos son coherentes con las responsabilidades de cada rol. Identifica posibles riesgos de seguridad y propone ajustes sin modificar el objetivo general del proyecto.

 Resultado

La IA permitió detectar que no todos los usuarios deben tener el mismo nivel de acceso a la información.

 ¿Qué funcionó?

* Ayudó a diferenciar claramente las responsabilidades.
* Permitió identificar información que debe estar protegida.
* Sirvió para justificar el uso de roles y permisos.
* Ayudó a plantear el principio de mínimo privilegio.

 ¿Qué no funcionó?

La primera propuesta otorgaba al personal de clínica acceso a información que podría no ser necesaria para realizar sus funciones.

 ¿Qué se corrigió?

Se ajustaron los permisos para que cada rol tenga únicamente el acceso necesario.
También se estableció que el administrador tiene funciones de gestión del sistema y que la información clínica debe manejarse
de acuerdo con los permisos establecidos.

4. Diseño del módulo de Inteligencia Artificial

Objetivo

Definir cómo podría utilizarse la Inteligencia Artificial dentro de PetCare sin convertirla en un sistema de diagnóstico veterinario.

 Prompt utilizado

- Diseña el módulo de Inteligencia Artificial para PetCare, una plataforma de cuidado preventivo de mascotas.
- La IA debe utilizar información proporcionada por el propietario y registrada en el historial de la mascota, como síntomas,
observaciones, peso, evolución, medicamentos y antecedentes.
- La IA debe generar orientación preventiva, identificar posibles cambios relevantes y generar resúmenes del historial para
facilitar la comunicación entre propietario y veterinario.
- No debe realizar diagnósticos definitivos ni reemplazar la valoración de un profesional veterinario.
- Propón las funciones del módulo, los datos de entrada, los resultados esperados y las principales medidas de seguridad que deberían implementarse.

Resultado

Se definieron tres funciones principales para el uso de IA:

1. Evaluación preventiva.
2. Detección de cambios o patrones.
3. Generación de resúmenes del historial.

 ¿Qué funcionó?

- Permitió establecer claramente el propósito de la IA.
- Ayudó a diferenciar orientación preventiva de diagnóstico.
- Permitió identificar qué información puede utilizarse como entrada.
- Ayudó a definir mensajes de advertencia para los usuarios.

¿Qué no funcionó?

Una primera propuesta utilizaba términos como "diagnosticar", "determinar enfermedad" o "indicar tratamiento", 
lo cual no correspondía con el objetivo de PetCare.

 ¿Qué se corrigió?

Se reemplazaron esas funciones por evaluación preventiva, identificación de posibles cambios, generación de alertas y resumen de información.
Se estableció que la IA es una herramienta de apoyo y que las decisiones clínicas corresponden al veterinario.

 5. Generación de historias de usuario

 Objetivo

Utilizar IA para transformar las funcionalidades del MVP en historias de usuario que puedan utilizarse posteriormente para organizar el desarrollo.

 Prompt utilizado

-Actúa como analista de requisitos y crea historias de usuario para el proyecto PetCare.
- Los roles son:
* Propietario
* Veterinario
* Personal de clínica
* Administrador

- El MVP incluye autenticación, gestión de mascotas, historial de salud, síntomas y observaciones, vacunas, medicamentos,
seguimiento de evolución, citas, notificaciones, roles y permisos, evaluación preventiva mediante IA, detección de cambios,
resumen de historial mediante IA, panel web para veterinarios, panel administrativo, QR de emergencia y localización de veterinarias.

- Escribe las historias utilizando el formato:

- "Como [rol], quiero [acción], para [beneficio]."

- Evita historias demasiado grandes y divídelas cuando sea necesario.

 Resultado

La IA generó historias de usuario agrupadas por rol y funcionalidad.

 ¿Qué funcionó?

- Permitió convertir rápidamente las funcionalidades generales en requisitos más concretos.
- Ayudó a identificar necesidades específicas de cada rol.
- Facilitó la organización inicial del backlog.
-Permitió detectar funcionalidades que necesitaban dividirse.

¿Qué no funcionó?

Algunas historias generadas inicialmente eran demasiado amplias y agrupaban varias funcionalidades diferentes en una sola historia.

 ¿Qué se corrigió?

Las historias grandes se dividieron en historias más pequeñas y específicas. Se mantuvo el formato "Como..., quiero..., para..." 
para facilitar posteriormente la definición de criterios de aceptación.


En PetCare, la IA se plantea como una herramienta de apoyo para organizar información, detectar posibles cambios y facilitar el seguimiento preventivo, pero no como sustituto del criterio profesional veterinario.

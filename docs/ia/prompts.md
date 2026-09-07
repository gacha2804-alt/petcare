Biblioteca de Prompts — PetCare

 1. Análisis general del proyecto

 Actúa como analista de sistemas y analiza el proyecto PetCare. PetCare es una plataforma híbrida Web + Aplicación móvil enfocada en el cuidado preventivo de mascotas mediante Inteligencia Artificial. Los roles son Propietario, Veterinario, Personal de clínica y Administrador. El sistema debe incluir autenticación, gestión de mascotas, historial de salud, síntomas, observaciones, vacunas, medicamentos, seguimiento de evolución, citas, notificaciones, roles y permisos, evaluación preventiva mediante IA, detección de cambios, resumen de historial mediante IA, panel veterinario, panel administrativo, QR de emergencia y localización de veterinarias. Analiza el proyecto y divídelo en módulos funcionales. Para cada módulo indica objetivo, usuarios, funcionalidades, datos necesarios y dependencias con otros módulos. No agregues funcionalidades innecesarias para el MVP.

 2. Definición de requisitos

 Actúa como ingeniero de requisitos. A partir de la descripción del proyecto PetCare, genera los requisitos funcionales y no funcionales del sistema. Organiza los requisitos por módulos: autenticación, mascotas, salud, citas, IA, emergencias, veterinarias, notificaciones y administración. Para cada requisito utiliza un identificador único como RF-001, RF-002, etc. No inventes funcionalidades que no estén relacionadas con el proyecto.

 3. Arquitectura general del sistema

Actúa como arquitecto de software. Diseña la arquitectura tecnológica para PetCare, una plataforma híbrida compuesta por una aplicación web y una aplicación móvil. La arquitectura debe contemplar frontend web, aplicación móvil, backend/API REST, base de datos, servicio de autenticación, servicio de Inteligencia Artificial, notificaciones, mapas/localización y generación y lectura de códigos QR. Explica cómo se comunican los componentes. Propón una arquitectura sencilla, escalable y adecuada para un proyecto universitario. No agregues microservicios innecesarios.

 4. Selección de tecnologías

Recomienda un stack tecnológico para desarrollar PetCare como plataforma híbrida Web + Aplicación móvil. Compara opciones para frontend web, aplicación móvil, backend, base de datos, autenticación, Inteligencia Artificial, notificaciones, mapas y código QR. El proyecto debe ser adecuado para estudiantes y permitir desarrollo local. Prioriza tecnologías gratuitas o con planes gratuitos. Explica ventajas y desventajas de cada alternativa y termina proponiendo un stack recomendado.

 5. Estructura de carpetas

 iseña una estructura profesional de carpetas para PetCare. El proyecto tendrá frontend web, aplicación móvil, backend, base de datos, documentación y módulo de IA. Propón una estructura organizada y escalable. Incluye los archivos principales que debería tener cada carpeta y explica la responsabilidad de cada una. La estructura debe ser adecuada para trabajar colaborativamente con Git y GitHub.

 6. Diseño de base de datos

Diseña una base de datos relacional para PetCare. Debe manejar usuarios, roles, mascotas, historial de salud, síntomas, observaciones, vacunas, medicamentos, peso, evolución, alimentación, documentos, citas, notificaciones, evaluaciones de IA, alertas, clínicas y veterinarias. Cada propietario puede tener varias mascotas. Los veterinarios pueden consultar la información autorizada de las mascotas. El personal de clínica tendrá permisos limitados y el administrador podrá gestionar el sistema. Define tablas, campos, tipos de datos, claves primarias, claves foráneas y relaciones. Normaliza el modelo y evita almacenar información duplicada. Finalmente genera el script SQL de creación de la base de datos.

 7. Backend y API REST

Actúa como desarrollador backend. Construye el backend de PetCare utilizando una arquitectura organizada. El backend debe proporcionar una API REST para que la aplicación web y móvil puedan comunicarse con la misma plataforma. Debe incluir autenticación, usuarios, roles, mascotas, historial de salud, vacunas, medicamentos, peso y evolución, citas, notificaciones, emergencias, veterinarias y funciones de Inteligencia Artificial. Utiliza controladores, rutas, servicios y middleware. Implementa manejo de errores y validación de datos. Explica dónde debe colocarse cada archivo. No mezcles la lógica de negocio directamente con las rutas.

 8. Diseño de API

Diseña todos los endpoints REST necesarios para PetCare. Organízalos por módulos: autenticación, usuarios, mascotas, salud, vacunas, medicamentos, evolución, citas, notificaciones, IA, emergencias, veterinarias y administración. Para cada endpoint indica método HTTP, URL, propósito, parámetros, datos enviados, respuesta esperada y rol autorizado. Utiliza nombres consistentes y una estructura adecuada para que tanto la aplicación web como la móvil puedan consumir la misma API.

 9. Autenticación

Implementa el módulo de autenticación de PetCare. Debe permitir registro, inicio de sesión, cierre de sesión, recuperación de contraseña, protección de rutas y manejo de roles. Los roles son Propietario, Veterinario, Personal de clínica y Administrador. Utiliza autenticación segura basada en tokens. Las contraseñas deben almacenarse utilizando hash seguro. Nunca almacenes contraseñas en texto plano. Explica cómo el frontend web y la aplicación móvil utilizarán la autenticación.

 10. Gestión de mascotas

Diseña e implementa el módulo de gestión de mascotas de PetCare. El propietario debe poder registrar, editar, consultar y eliminar sus mascotas. Los datos deben incluir nombre, especie, raza, sexo, fecha de nacimiento, peso, foto y características relevantes. El veterinario debe poder consultar la información de las mascotas que tenga autorizadas. Implementa frontend, backend, endpoints y modelo de base de datos. Agrega validaciones para impedir que un propietario acceda a mascotas de otros usuarios.

 11. Historial de salud

Implementa el módulo de historial de salud de PetCare. Cada mascota debe tener un historial organizado cronológicamente. Debe permitir registrar consultas, síntomas, observaciones, diagnósticos registrados por profesionales, tratamientos, medicamentos, vacunas y documentos. Diferencia claramente la información introducida por el propietario de la información registrada por un veterinario. Implementa frontend, backend y base de datos respetando los permisos de cada rol.

 12. Vacunas

Implementa el módulo de vacunas de PetCare. Debe permitir registrar nombre de la vacuna, fecha de aplicación, próxima fecha, veterinario responsable y observaciones. Los propietarios pueden consultar la información permitida y los veterinarios pueden gestionar la información clínica. El sistema debe generar recordatorios para próximas vacunas. Diseña frontend, backend, endpoints y estructura de base de datos.

 13. Medicamentos

Implementa el módulo de medicamentos de PetCare. Debe permitir registrar nombre del medicamento, dosis cuando corresponda, frecuencia, fecha de inicio, fecha de finalización, veterinario responsable y observaciones. Los propietarios pueden consultar la información y recibir recordatorios. Los veterinarios pueden registrar y modificar información clínica según sus permisos. No permitas que la Inteligencia Artificial prescriba medicamentos.

 14. Seguimiento de peso y evolución

Crea el módulo de seguimiento de evolución de mascotas. El usuario debe poder registrar el peso de la mascota periódicamente. El sistema debe guardar fecha, peso y observación. Debe mostrar una gráfica de evolución. También debe permitir al módulo de IA analizar cambios significativos en la evolución. No realices diagnósticos médicos. Implementa frontend, backend y base de datos.

 15. Gestión de citas

Implementa el módulo de citas veterinarias de PetCare. El propietario debe poder solicitar y consultar citas. El veterinario debe poder ver, aceptar, reprogramar y cancelar citas. El personal de clínica debe poder gestionar las citas según sus permisos. La cita debe incluir mascota, propietario, veterinario, fecha, hora, motivo, estado y observaciones. Implementa validaciones para evitar conflictos de horarios.

16. Notificaciones y recordatorios

Diseña el sistema de notificaciones de PetCare. Debe generar recordatorios relacionados con vacunas, medicamentos, citas, seguimiento de peso y alertas preventivas generadas por IA. Diferencia notificaciones informativas de alertas importantes. Diseña el modelo de datos, backend y frontend. Evita generar notificaciones excesivas y permite controlar las preferencias del usuario.

 17. Inteligencia Artificial — Evaluación preventiva

Diseña la función de evaluación preventiva mediante Inteligencia Artificial de PetCare. La IA recibirá información proporcionada por el usuario como especie, edad, peso, síntomas, observaciones, cambios de comportamiento e historial relevante. La IA debe generar orientación preventiva, nivel de atención sugerido, posibles factores que deberían observarse y recomendación de consultar a un veterinario cuando corresponda. La IA NO debe realizar diagnósticos definitivos, prescribir medicamentos ni sustituir al veterinario. Diseña el flujo completo desde el frontend hasta el servicio de IA y el almacenamiento del resultado.

 18. Inteligencia Artificial — Detección de cambios

Diseña una función de Inteligencia Artificial para detectar cambios relevantes en los registros de una mascota. Utiliza información histórica como peso, síntomas, alimentación, observaciones, medicamentos y actividad registrada. La IA debe comparar información actual con información histórica y señalar cambios que podrían requerir atención. No debe realizar diagnósticos. Explica datos de entrada, proceso, resultado, alertas y limitaciones. Genera ejemplos de respuestas seguras para el propietario.

 19. Inteligencia Artificial — Resumen del historial

Crea una función de Inteligencia Artificial que genere un resumen del historial de una mascota para facilitar una consulta veterinaria. El resumen debe incluir datos básicos, antecedentes relevantes, vacunas, medicamentos, síntomas recientes, cambios de peso, consultas anteriores y observaciones importantes. El resumen debe ser claro, breve y organizado cronológicamente. No inventes información que no esté presente en los registros. Indica explícitamente cuando un dato no esté disponible.

 20. Inteligencia Artificial — Diseño de prompts

Diseña un sistema de prompts para el módulo de Inteligencia Artificial de PetCare. Crea prompts separados para evaluación preventiva, detección de cambios y resumen del historial. Cada prompt debe incluir contexto, datos de entrada, instrucciones, restricciones y formato de salida. La IA debe evitar diagnósticos definitivos, prescripción de medicamentos y afirmaciones que puedan sustituir al veterinario. Diseña respuestas claras y seguras para propietarios y profesionales veterinarios.

 21. QR de emergencia

Diseña e implementa el módulo de perfil de emergencia mediante código QR para PetCare. Cada mascota debe tener un código QR único. Al escanearlo, una persona autorizada debe poder consultar información básica de emergencia como nombre de la mascota, especie, información relevante, contacto del propietario e información veterinaria que el propietario haya autorizado. No debe mostrar información privada innecesaria. Diseña backend, generación del QR, pantalla móvil y página web de consulta.

 22. Localización de veterinarias

Diseña el módulo de localización de veterinarias cercanas para PetCare. La aplicación debe permitir al usuario encontrar veterinarias cercanas utilizando su ubicación. Debe mostrar nombre, dirección, distancia aproximada, información de contacto cuando esté disponible y ubicación en mapa. Explica cómo integrar un servicio de mapas y cómo solicitar permisos de ubicación en la aplicación móvil. Incluye consideraciones de privacidad.

23. Aplicación móvil para propietarios

Diseña la aplicación móvil de PetCare enfocada principalmente en propietarios. Debe incluir inicio de sesión, registro, inicio/dashboard, mis mascotas, perfil de mascota, historial de salud, vacunas, medicamentos, peso y evolución, citas, notificaciones, evaluación preventiva mediante IA, resumen mediante IA, QR de emergencia, veterinarias cercanas y perfil del usuario. Diseña una navegación sencilla para dispositivos móviles. Prioriza accesibilidad, claridad y facilidad de uso. No agregues funcionalidades fuera del MVP.

 24. Navegación de la aplicación móvil

Diseña la navegación completa de la aplicación móvil PetCare. Define las pantallas principales, navegación inferior, menús, rutas y flujo entre pantallas para el rol Propietario. Incluye inicio, mascotas, salud, citas, IA, emergencias, veterinarias, notificaciones y perfil. Explica qué acciones puede realizar el usuario desde cada pantalla. La navegación debe ser intuitiva y adecuada para dispositivos móviles.

 25. Aplicación web para veterinarios

Diseña el frontend web de PetCare orientado a veterinarios y personal de clínica. El panel debe permitir inicio/dashboard, buscar mascotas autorizadas, consultar historial, revisar síntomas, revisar vacunas, revisar medicamentos, gestionar citas, consultar evolución, consultar resúmenes generados por IA y registrar información clínica según permisos. Diseña una interfaz profesional, clara y responsive. Utiliza componentes reutilizables. El acceso debe depender del rol del usuario.

 26. Panel administrativo

Diseña el panel administrativo web de PetCare. El administrador debe poder gestionar usuarios, roles, veterinarios, personal de clínica, clínicas, estado de cuentas y configuraciones generales. El administrador no debe modificar información clínica sin una justificación y permiso específico. Incluye dashboard, tablas, búsqueda, filtros, crear, editar, desactivar y consultar. Diseña una interfaz profesional y segura.

 27. Control de permisos

Implementa autorización basada en roles para PetCare. Los roles son Propietario, Veterinario, Personal de clínica y Administrador. Crea una matriz de permisos para cada módulo. Después implementa middleware en el backend y protección de rutas en frontend. Un usuario nunca debe poder acceder a información que no corresponda a su rol. También valida en backend los permisos aunque el frontend oculte los botones.

 28. Diseño de interfaz

Diseña la identidad visual y experiencia de usuario de PetCare. La plataforma debe transmitir confianza, cuidado, tecnología, cercanía y profesionalismo veterinario. Define colores, tipografías, botones, tarjetas, formularios, navegación, iconografía y estados de alerta. La interfaz debe ser responsive para web y adaptable a dispositivos móviles. Prioriza accesibilidad y facilidad de uso.

 29. Diseño responsive

Revisa la interfaz de PetCare y conviértela en un diseño responsive. Debe funcionar correctamente en computadores, tablets y teléfonos móviles. Revisa menús, tablas, formularios, tarjetas, gráficas, botones y modales. No reduzcas simplemente el tamaño de los elementos. Adapta la distribución y navegación según el dispositivo.

 30. Pruebas del sistema

Actúa como ingeniero QA y crea un plan de pruebas para PetCare. Incluye pruebas para registro, login, roles, mascotas, historial, vacunas, medicamentos, citas, notificaciones, IA, QR, veterinarias, panel veterinario y panel administrativo. Para cada prueba indica ID, funcionalidad, precondiciones, pasos, resultado esperado, resultado obtenido y estado. Incluye pruebas positivas y negativas.

 31. Corrección de errores

 Analiza el siguiente error de PetCare:

[Uncaught ReferenceError: Mascotas is not defined at App.jsx:25]

Indica:

1. Qué significa.
2. Cuál podría ser la causa.
3. Qué archivo debería revisarse.
4. Cómo corregirlo.
5. Cómo comprobar que la solución funciona.

No cambies código que no esté relacionado con el error. Si necesitas información adicional, indica exactamente qué archivo o código necesitas revisar.

 32. Revisión de código

Actúa como desarrollador senior y revisa el siguiente código de PetCare:

[import React, { useEffect, useState } from "react";
import axios from "axios";

function Mascotas() {
  const [mascotas, setMascotas] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:3000/api/mascotas")
      .then((response) => {
        setMascotas(response.data);
      });
  }, []);

  return (
    <div>
      <h2>Mis Mascotas</h2>

      {mascotas.map((mascota) => (
        <div key={mascota.id}>
          <h3>{mascota.nombre}</h3>
          <p>{mascota.especie}</p>
          <p>{mascota.raza}</p>
        </div>
      ))}
    </div>
  );
}

export default Mascotas;]

Analiza errores, seguridad, organización, código duplicado, manejo de errores, validaciones, rendimiento y legibilidad. No reescribas todo el archivo. Primero identifica los problemas y después propone las modificaciones necesarias. Mantén la arquitectura y funcionalidades existentes.

 33. Seguridad, documentación y GitHub

Realiza una revisión completa de seguridad y documentación del proyecto PetCare. Revisa autenticación, contraseñas, tokens, roles, permisos, API, base de datos, variables de entorno, información de mascotas, información clínica, QR de emergencia y datos de ubicación. Indica también qué debe incluir el README y qué archivos deben estar en .gitignore. Asegúrate de que contraseñas, tokens, claves privadas, archivos .env y node_modules no se suban al repositorio.

 34. Prompt maestro para continuar el desarrollo

Actúa como desarrollador senior del proyecto PetCare.

Antes de modificar cualquier archivo, analiza el contexto del proyecto y respeta:

* La arquitectura existente.
* Los roles existentes.
* Los endpoints existentes.
* La estructura de base de datos.
* Los componentes existentes.
* Las funcionalidades del MVP.

No reemplaces código funcional sin justificarlo.
No cambies tecnologías sin autorización.

No inventes archivos que no existan.

Cuando necesites modificar un archivo:

1. Explica qué se va a modificar.
2. Indica por qué.
3. Proporciona el código completo si es necesario.
4. Indica exactamente dónde debe colocarse.
5. Explica cómo probarlo.

Si existe un error, corrige primero la causa y evita realizar cambios innecesarios.

Mantén siempre la separación entre:

* Aplicación web.
* Aplicación móvil.
* Backend.
* Base de datos.
* Inteligencia Artificial.

El objetivo es mantener PetCare funcional, seguro, organizado y escalable.

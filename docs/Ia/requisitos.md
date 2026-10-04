# Requisitos — PetCare
- PetCare es una plataforma web orientada a la gestión y el cuidado preventivo de mascotas, que permite centralizar información clínica, gestionar citas veterinarias y facilitar el seguimiento de vacunas y desparasitaciones, conectando a propietarios con profesionales y personal de clínicas veterinarias.

Fuente: entrevista simulada con cliente veterinario (ver [`docs/ia/entrevista.md`](./ia/entrevista.md)) + contexto del [README del proyecto].

## 1. Requerimientos Funcionales

## 1. RF — Requisitos funcionales
| ID | Prioridad | Requisito |
|---|---|---|
| RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación. |
| RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada. |
| RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas. |
| RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones. |
| RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica. |
| RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada. |
| RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada. |
| RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. **[SUPUESTO]** |

## 2. RNF — Requisitos no funcionales
| ID | Requisito |
|---|---|
| RNF-01 | El sistema debe restringir el acceso al historial clínico de una mascota únicamente al propietario y a los veterinarios que este haya autorizado. |
| RNF-02 | El sistema debe proteger las credenciales y los datos personales mediante mecanismos de autenticación y almacenamiento seguro. |
| RNF-03 | El sistema debe garantizar la integridad de la información clínica, evitando modificaciones realizadas por usuarios no autorizados. |
| RNF-04 | Las operaciones habituales de consulta y registro deben responder en un tiempo adecuado para permitir una interacción fluida. **[SUPUESTO]** |
| RNF-05 | La plataforma debe ser accesible desde navegadores web modernos y adaptarse a computadores, tabletas y dispositivos móviles. |
| RNF-06 | La interfaz debe permitir que propietarios, veterinarios y personal de clínica realicen sus tareas principales sin conocimientos técnicos especializados. |
| RNF-07 | El sistema debe mantener registros de las operaciones relevantes realizadas sobre la información clínica para garantizar su trazabilidad. |
| RNF-08 | El sistema debe contar con mecanismos de respaldo y recuperación de la información ante fallos. |                          |

## Análisis de requerimientos

| ID | Prioridad | Requisito |
|---|---|---|
| RF-01 | Must | El propietario registra una mascota proporcionando nombre, especie, sexo, fecha de nacimiento y datos de identificación. |
| RF-02 | Must | El propietario consulta el historial clínico de una mascota registrada. |
| RF-03 | Must | El propietario puede autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de sus mascotas. |
| RF-04 | Must | El veterinario autorizado registra una consulta asociada a una mascota, incluyendo fecha, motivo, diagnóstico y observaciones. |
| RF-05 | Must | El propietario solicita una cita seleccionando una clínica, un veterinario y un horario disponible ofrecido por la clínica. |
| RF-06 | Must | El propietario consulta el registro de vacunas de una mascota, incluyendo fecha de aplicación y próxima fecha recomendada. |
| RF-07 | Should | El propietario consulta el registro de desparasitaciones de una mascota, incluyendo fecha del tratamiento y próxima fecha recomendada. |
| RF-08 | Should | El sistema genera recordatorios para vacunas y desparasitaciones cuya próxima fecha recomendada esté próxima. **[SUPUESTO]** |

Criterio de priorización: los Must cubren el núcleo del MVP: mascotas, información clínica, control de acceso, atención veterinaria, citas y vacunación. Los Should aportan al seguimiento preventivo, pero pueden incorporarse después sin impedir el funcionamiento básico de PetCare.

## ## Historias de usuario priorizadas con MoSCoW

| ID | Prioridad | Historia de usuario |
|---|---|---|
| **HU-01** | **Must** | Como propietario, quiero registrar una mascota proporcionando su nombre, especie, sexo, fecha de nacimiento y datos de identificación, para gestionar su información en PetCare y contar con un identificador único generado automáticamente por el sistema. |
| **HU-02** | **Must** | Como propietario, quiero consultar el historial clínico de una mascota registrada, para conocer y dar seguimiento a su información veterinaria. |
| **HU-03** | **Must** | Como propietario, quiero autorizar, consultar y revocar el acceso de veterinarios al historial clínico de cada una de mis mascotas, para controlar qué veterinarios pueden consultar su información clínica. |
| **HU-04** | **Must** | Como veterinario autorizado, quiero registrar una consulta asociada a una mascota, incluyendo la fecha, el motivo, el diagnóstico y las observaciones, para mantener actualizado su historial clínico. |
| **HU-05** | **Must** | Como propietario, quiero seleccionar una clínica, un veterinario y un horario disponible ofrecido por la clínica, para confirmar automáticamente una cita veterinaria. |
| **HU-06** | **Must** | Como propietario, quiero consultar el registro de vacunas de una mascota, incluyendo la fecha de aplicación y la próxima fecha recomendada, para realizar el seguimiento de su vacunación. |
| **HU-07** | **Should** | Como propietario, quiero consultar el registro de desparasitaciones de una mascota, incluyendo la fecha del tratamiento y la próxima fecha recomendada, para realizar el seguimiento de su cuidado preventivo. |
| **HU-08** | **Should** | Como propietario, quiero consultar dentro de PetCare recordatorios sobre próximas vacunas y desparasitaciones, para realizar oportunamente el seguimiento preventivo de mi mascota. |

## Criterios Gherkin — HU-01

### Escenario 1: Registro exitoso de una mascota

```gherkin
Scenario: Registrar una mascota correctamente
  Given que el propietario ha iniciado sesión
  And proporciona el nombre, especie, sexo, fecha de nacimiento y datos de identificación de la mascota
  When confirma el registro
  Then el sistema registra la mascota
  And genera automáticamente un identificador único
  And muestra la mascota registrada al propietario
```

### Escenario 2: Registro con datos incompletos

```gherkin
Scenario: Intentar registrar una mascota con datos obligatorios incompletos
  Given que el propietario está registrando una mascota
  And falta uno o más datos obligatorios
  When confirma el registro
  Then el sistema no registra la mascota
  And informa los datos que deben completarse
```

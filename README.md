# 🐾 PetCare — Plataforma Web para el Cuidado Preventivo de Mascotas

> **PetCare** es una plataforma web orientada a la gestión y el cuidado preventivo de mascotas, que permite centralizar información clínica, gestionar citas veterinarias y facilitar el seguimiento de vacunas y desparasitaciones, conectando a propietarios con profesionales y personal de clínicas veterinarias.

---

## 📑 Índice

1. [Visión del Proyecto](#-visión-del-proyecto)
2. [Problema que Resolvemos](#-problema-que-resolvemos)
3. [Solución](#-solución)
4. [Roles y Matriz de Permisos](#-roles-y-matriz-de-permisos)
5. [Alcance del MVP](#-alcance-del-mvp)
6. [Módulos del Sistema](#-módulos-del-sistema)
7. [Arquitectura y Tecnologías](#-arquitectura-y-tecnologías)
8. [Instalación y Configuración](#-instalación-y-configuración)
9. [Contribución](#-contribución)
10. [Licencia y Contacto](#-licencia-y-contacto)

---

## 🎯 Visión del Proyecto

PetCare busca facilitar el cuidado preventivo de las mascotas mediante una plataforma web que centraliza su información médica, facilita la gestión de citas y permite realizar seguimiento a vacunas y desparasitaciones.

La plataforma busca mejorar la comunicación entre propietarios, veterinarios y personal de clínica, proporcionando información organizada y recordatorios oportunos para contribuir al seguimiento de la salud de las mascotas.

PetCare funciona como una herramienta de apoyo para la gestión y seguimiento de la información veterinaria. Las decisiones relacionadas con diagnósticos, tratamientos y procedimientos médicos corresponden a los profesionales veterinarios.

---

## 🐾 Problema que Resolvemos

Los propietarios y las clínicas veterinarias pueden enfrentar diferentes dificultades en el seguimiento de la salud de las mascotas:

* **Olvido de vacunas y desparasitaciones:** Los propietarios pueden olvidar las fechas de los próximos refuerzos o tratamientos preventivos.
* **Información médica dispersa:** El historial de una mascota puede encontrarse distribuido entre diferentes registros y documentos.
* **Dificultad para gestionar citas:** Los propietarios pueden necesitar comunicarse directamente con la clínica para confirmar o reprogramar una cita.
* **Falta de información centralizada:** Los veterinarios pueden necesitar consultar información registrada en diferentes momentos o sedes para conocer el historial completo de una mascota.
* **Poca visibilidad sobre próximos vencimientos:** El personal de la clínica necesita identificar qué mascotas tienen vacunas o desparasitaciones próximas a vencer para realizar el seguimiento correspondiente.
* **Pérdida de oportunidades de atención:** Las cancelaciones o citas no confirmadas pueden dejar horarios disponibles que podrían ser utilizados por otros pacientes.

---

## 💡 Solución

PetCare proporciona una plataforma web que centraliza la información relacionada con las mascotas y facilita la comunicación y gestión entre propietarios y clínicas veterinarias.

### Características principales

* **Recordatorios preventivos:** Notificaciones automáticas sobre próximas vacunas y desparasitaciones.
* **Gestión de vacunas y desparasitaciones:** Registro de productos, lotes, dosis, peso y fechas de aplicación.
* **Cálculo de próximos refuerzos:** El sistema calcula la próxima fecha de acuerdo con el protocolo configurado para el producto.
* **Gestión de citas:** Los propietarios pueden confirmar, cancelar o reprogramar sus citas.
* **Disponibilidad de horarios:** Los propietarios pueden consultar horarios disponibles para reprogramar una cita.
* **Gestión de vencimientos:** El personal de la clínica puede consultar semanalmente las mascotas con próximos vencimientos y decidir cuándo enviar los recordatorios.
* **Historial clínico centralizado:** Los veterinarios pueden consultar el historial completo de una mascota, incluyendo los registros realizados en diferentes sedes.
* **Consulta del historial por parte del propietario:** El propietario puede consultar vacunas, consultas y resultados de exámenes desde la plataforma.
* **Lista de espera:** Permite registrar propietarios interesados en horarios que actualmente no tienen disponibilidad.
* **Perfil de emergencia:** Como funcionalidad de expansión, se contempla la generación de un perfil de emergencia mediante código QR.
* **Alertas preventivas basadas en IA:** Como funcionalidad de expansión, se contempla el análisis de registros de peso y actividad para identificar posibles cambios relevantes.

---

## 👥 Roles y Matriz de Permisos

### Roles definidos

* **Propietario:** Gestiona la información de sus mascotas, consulta su historial, recibe recordatorios y administra sus citas.
* **Veterinario:** Registra vacunas y desparasitaciones, consulta el historial clínico de las mascotas y utiliza la información disponible para la atención veterinaria.
* **Personal de Clínica:** Gestiona el calendario, consulta los próximos vencimientos y administra el envío de recordatorios y disponibilidad de citas.
* **Administrador:** Gestiona la configuración general de la plataforma y los usuarios del sistema.

### Matriz de módulos

| Módulo                          | Propietario | Veterinario | Personal de Clínica | Administrador |
| :------------------------------ | :---------: | :---------: | :-----------------: | :-----------: |
| **Autenticación**               |      Sí     |      Sí     |          Sí         |       Sí      |
| **Gestión de Mascotas**         |      Sí     |     Ver     |         Ver         |       Sí      |
| **Vacunas y Desparasitaciones** |     Ver     |      Sí     |         Ver         |       Sí      |
| **Historial Clínico**           |      Sí     |      Sí     |         Ver         |       Sí      |
| **Citas**                       |      Sí     |      Sí     |          Sí         |       Sí      |
| **Recordatorios**               |    Recibe   |      No     |       Gestiona      |       Sí      |
| **Lista de Espera**             |      Sí     |     Ver     |       Gestiona      |       Sí      |
| **Perfil de Emergencia / QR**   |      Sí     |     Ver     |         Ver         |       Sí      |
| **Alertas con IA**              |      Sí     |      Sí     |          No         |       No      |
| **Administración**              |      No     |      No     |          No         |       Sí      |

---

## 🚀 Alcance del MVP

El Producto Mínimo Viable (MVP) se enfoca en las funcionalidades prioritarias **Must** definidas para PetCare:

### Gestión preventiva

* [x] Registro de vacunas y desparasitaciones.
* [x] Registro de producto, lote, dosis, peso y fecha de aplicación.
* [x] Cálculo automático de la próxima fecha de refuerzo según el protocolo configurado.
* [x] Validación de productos sin protocolo configurado.

### Recordatorios

* [x] Generación de recordatorios para vacunas y desparasitaciones próximas.
* [x] Segundo recordatorio cuando el propietario no responde dentro del plazo establecido.
* [x] Reporte semanal de mascotas con vencimientos próximos.
* [x] Aprobación o postergación individual de recordatorios por parte del personal de clínica.

### Gestión de citas

* [x] Confirmación de citas por parte del propietario.
* [x] Cancelación de citas.
* [x] Reprogramación de citas.
* [x] Consulta de horarios disponibles durante los próximos días.
* [x] Actualización del estado de la cita en el sistema de la clínica.

### Historial clínico

* [x] Consulta del historial clínico de la mascota.
* [x] Consolidación de información registrada en diferentes sedes.
* [x] Identificación de la fecha y sede correspondiente a cada registro.
* [x] Actualización de la información clínica después de nuevos registros.

---

## 🔮 Funcionalidades de Expansión

Además del MVP, PetCare contempla funcionalidades clasificadas como **Should** y **Could** dentro de las historias de usuario.

### Prioridad Should

* Liberación automática de horarios cuando una cita no es confirmada.
* Lista de espera para horarios sin disponibilidad.
* Notificación al siguiente propietario cuando se libera un cupo.
* Consulta del historial médico, vacunas y resultados de exámenes por parte del propietario.
* Descarga y compartición de resultados de exámenes en PDF.

### Prioridad Could

* Perfil de emergencia mediante código QR.
* Acceso rápido a información básica de la mascota mediante el QR.
* Alertas preventivas mediante Inteligencia Artificial.
* Análisis de cambios en peso y actividad según los registros disponibles.

---

## 🧩 Módulos del Sistema

```text
                    ┌──────────────────────┐
                    │    Autenticación     │
                    │   y gestión de roles │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       Gestión de         Gestión de      Vacunas y
        Mascotas            Citas       Desparasitaciones
              │                │                │
              │                │                ▼
              │                │         Recordatorios
              │                │                │
              ▼                ▼                │
       Historial Clínico ◄─────┘                │
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                    Seguimiento Preventivo
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼                         ▼
          Lista de Espera           Funcionalidades
                                    de expansión
                                    (QR / IA)
```

### Módulos principales

**1. Autenticación y Roles**
Control de acceso según el tipo de usuario: propietario, veterinario, personal de clínica y administrador.

**2. Gestión de Mascotas**
Administración de la información básica de cada mascota y asociación con su propietario.

**3. Vacunas y Desparasitaciones**
Registro de aplicaciones y cálculo de próximas fechas de acuerdo con los protocolos configurados.

**4. Recordatorios Preventivos**
Gestión de alertas relacionadas con vacunas y desparasitaciones próximas a vencer.

**5. Gestión de Citas**
Creación, confirmación, cancelación y reprogramación de citas.

**6. Historial Clínico**
Consulta centralizada de los registros médicos de cada mascota, incluyendo información de diferentes sedes.

**7. Lista de Espera**
Gestión de propietarios interesados en horarios que actualmente no cuentan con disponibilidad.

**8. Funcionalidades de Expansión**
Incluye el perfil de emergencia mediante QR y las alertas preventivas apoyadas por Inteligencia Artificial.

---

## 🏗️ Arquitectura y Tecnologías

PetCare está diseñado como una plataforma web con una arquitectura orientada a mantener una separación clara entre la interfaz, la lógica de negocio y la gestión de datos.

### Capas principales

```text
┌─────────────────────────────────────┐
│          Interfaz Web               │
│     Propietario / Clínica           │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Lógica de Aplicación       │
│ Citas · Recordatorios · Historial   │
│ Vacunas · Usuarios · Mascotas       │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│          Persistencia de Datos      │
│     Usuarios · Mascotas · Citas     │
│     Historial · Vacunas · etc.      │
└─────────────────────────────────────┘
```

### Tecnologías

> Las tecnologías específicas utilizadas por el proyecto pueden definirse y actualizarse conforme avance el desarrollo.

* **Frontend:** Aplicación web.
* **Backend:** Servicios para gestionar la lógica de negocio y las operaciones del sistema.
* **Base de datos:** Almacenamiento estructurado de usuarios, mascotas, citas e información clínica.
* **Control de versiones:** Git y GitHub.
* **IA:** Funcionalidad de expansión para análisis preventivo.
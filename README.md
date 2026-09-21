# 🐾 PetCare — Plataforma de Cuidado Preventivo de Mascotas con IA

> **PetCare** es una plataforma híbrida (Aplicación Móvil + Web) orientada al seguimiento y cuidado preventivo de mascotas mediante Inteligencia Artificial, conectando a propietarios y profesionales veterinarios para una atención más oportuna.

---

## 📌 Índice
1. [Visión del Proyecto](#-visión-del-proyecto)
2. [Problema que Resolvemos](#-problema-que-resolvemos)
3. [Solución](#-solución)
4. [Roles y Matriz de Permisos (RBAC)](#-roles-y-matriz-de-permisos-rbac)
5. [Alcance del MVP](#-alcance-del-mvp)
6. [Módulos del Sistema](#-módulos-del-sistema)
7. [Arquitectura y Tecnologías](#-arquitectura-y-tecnologías)
8. [Instalación y Configuración](#-instalación-y-configuración)
9. [Contribución](#-contribución)
10. [Licencia y Contacto](#-licencia-y-contacto)

---

## 🎯 Visión del Proyecto

Centralizar la información médica y comportamental de las mascotas en un solo lugar y utilizar **Inteligencia Artificial** como una herramienta de apoyo preventivo. 

> **Nota:** PetCare **no reemplaza la consulta profesional**, sino que analiza síntomas, patrones e historial para generar alertas, orientaciones y resúmenes estructurados que faciliten la labor del veterinario.

---

## ❓ Problema que Resolvemos

- **Información Dispersa:** Los datos clínicos, esquemas de vacunación y recordatorios suelen gestionarse en libretas, notas, chats y fotografías fragmentadas.
- **Dificultad en Detección Temprana:** A los propietarios les cuesta identificar cuándo un cambio sutil de conducta o síntoma requiere atención médica.
- **Información No Confiable en la Web:** Ante cualquier anomalía, los dueños suelen acudir a búsquedas genéricas en Internet que generan desinformación o alarma injustificada.
- **Historial Incompleto para el Veterinario:** Al momento de la consulta, los veterinarios carecen de un registro continuo de lo sucedido previo al síntoma.

---

## 💡 Solución

Una plataforma integral que conecta a **Propietarios** (vía App Móvil) con **Veterinarios y Personal de Clínica** (vía Panel Web).

### Características Clave
- **Gestión Centralizada:** Historial clínico, vacunas, medicamentos, peso, síntomas y documentos.
- **Análisis Preventivo con IA:** Detección de patrones anómalos, evaluación de síntomas e informes resumidos para el veterinario.
- **Perfil de Emergencia con QR:** Acceso rápido a datos críticos del paciente en situaciones de pérdida o emergencia.
- **Geolocalización:** Búsqueda rápida de clínicas y servicios veterinarios cercanos.

---

## 👥 Roles y Matriz de Permisos (RBAC)

### Roles Definidos
- 🐶 **Propietario:** Gestiona sus mascotas, registra síntomas, consulta la IA y agenda citas.
- 🩺 **Veterinario:** Consulta historiales, lee resúmenes de IA y atiende consultas/citas.
- 🏥 **Personal de Clínica:** Gestiona la agenda de citas y recepción de pacientes.
- ⚙️ **Administrador:** Administra usuarios, clínicas, métricas e infraestructura de la plataforma.

### Matriz de Módulos

| Módulo | Propietario | Veterinario | Personal de Clínica | Administrador |
| :--- | :---: | :---: | :---: | :---: |
| **Autenticación** | Sí | Sí | Sí | Sí |
| **Gestión de Mascotas** | Sí | Ver | Ver | Ver |
| **Salud** | Sí | Sí | Ver | Ver |
| **Citas** | Sí | Sí | Sí | Ver |
| **Inteligencia Artificial** | Sí | Sí | No | No |
| **Emergencias (QR)** | Sí | Ver | Ver | Ver |
| **Administración** | No | No | No | Sí |

---

## 🚀 Alcance del MVP

El Producto Mínimo Viable (MVP) incluye:

- [x] Autenticación y gestión de usuarios por roles.
- [x] Registro y gestión de mascotas (alimentación, peso, síntomas).
- [x] Historial de salud, vacunas, medicamentos y documentos.
- [x] Agendamiento y gestión de citas médicas.
- [x] Motor de evaluación y alertas preventivas impulsado por IA.
- [x] Generación de resúmenes clínicos con IA para el veterinario.
- [x] Generador de Perfil y Código QR de emergencia.
- [x] Localización geográfica de veterinarias cercanas.
- [x] Panel Web de gestión para veterinarios y administradores.

---

## 🧩 Módulos del Sistema

```text
Autenticación
     ↓
Gestión de Mascotas ──→ QR de Emergencia
     ↓
Módulo de Salud ──────→ Geolocalización de Clínicas
     ↓
Gestión de Citas
     ↓
Evaluación Preventiva e Insights con IA
     ↓
Panel Administrativo / Clínica

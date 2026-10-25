# Historias de Usuario - PetCare (HU-01 a HU-20)

## 1. Objetivo
Documentar las historias de usuario con trazabilidad desde requisitos RF-01 a RF-20, basadas en `docs/Ia/requisitos.md`, `docs/Ia/entrevista.md` y `docs/Ia/prompts.md`. Arquitectura propuesta (MVP visual no funcional).

## 2. Tracabilidad y criterios clave
Ver archivo con criterios Gherkin completo en `historias_usuario_criterios_aceptacion.md`. Este diagrama muestra mapeo RF → HU.

## 3. Prioridades
Must: HU-01 a HU-06, HU-09 a HU-19  
Should: HU-07, HU-08, HU-20

## 4. Principios aplicados
- Control de acceso por rol y autorización por mascota
- Emergencias prioritarias sobre agendamiento
- IA sin diagnóstico definitivo, sin medicamentos peligrosos
- Agendamiento desde chat con disponibilidad real
- Prevención de duplicados, trazabilidad y auditoría
- Sin imponer BD/proveedor LLM/calendario externo

## 5. Diagrama Mermaid
```mermaid
graph LR
  subgraph BaseRequisitos["Base: requisitos.md / entrevista.md / prompts.md"]
    RF["RF-01 a RF-20"]
    RNF["RNF-01 a RNF-18"]
  end
  
  subgraph Historias["Historias de Usuario (HU)"]
    HU01["HU-01 RF-01 Registrar mascota"]
    HU02["HU-02 RF-02 Consultar historial"]
    HU03["HU-03 RF-03 Permisos veterinario"]
    HU04["HU-04 RF-04 Registrar consulta"]
    HU05["HU-05 RF-05 Solicitar cita"]
    HU06["HU-06 RF-06 Consultar vacunas"]
    HU07["HU-07 RF-07 Consultar desparasitaciones"]
    HU08["HU-08 RF-08 Recordatorios"]
    HU09["HU-09 RF-09 Seleccionar mascota + chat"]
    HU10["HU-10 RF-10 Motivo consulta chat"]
    HU11["HU-11 RF-11 Orientación inicial IA"]
    HU12["HU-12 RF-12 Señales alarma"]
    HU13["HU-13 RF-13 Recomendación + agendar"]
    HU14["HU-14 RF-14 Dos sedes disponibilidad"]
    HU15["HU-15 RF-15 Agendar desde chat"]
    HU16["HU-16 RF-16 Confirmación datos obligatorios"]
    HU17["HU-17 RF-17 Asociación cita"]
    HU18["HU-18 RF-18 Consulta cita"]
    HU19["HU-19 RF-19 Errores/cancelación"]
    HU20["HU-20 RF-20 Escalamiento"]
  end
  
  RF --> HU01
  RF --> HU02
  RF --> HU03
  RF --> HU04
  RF --> HU05
  RF --> HU06
  RF --> HU07
  RF --> HU08
  RF --> HU09
  RF --> HU10
  RF --> HU11
  RF --> HU12
  RF --> HU13
  RF --> HU14
  RF --> HU15
  RF --> HU16
  RF --> HU17
  RF --> HU18
  RF --> HU19
  RF --> HU20
```

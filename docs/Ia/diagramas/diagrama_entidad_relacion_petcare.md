# Diagrama Entidad-Relación - PetCare (Propuesto)

## 1. Objetivo del modelo de datos
Representar la estructura de datos propuesta para PetCare (futura implementación), cubriendo usuarios/roles/permisos, mascotas, historial clínico/consultas, vacunas/desparasitaciones/recordatorios, sedes/agenda/disponibilidad/citas, conversaciones IA, y auditoría. Diferencia entre MVP visual (no funcional) y diseño propuesto.

## 2. Entidades y atributos principales
Ver archivo .mmd con entidades: USUARIO, ROL, USUARIO_ROL, PROPIETARIO, VETERINARIO, PERSONAL_CLINICA, ADMINISTRADOR, SEDE, MASCOTA, PERMISO_HISTORIAL_CLINICO, HISTORIAL_CLINICO, CONSULTA_VETERINARIA, VACUNA, DESPARASITACION, RECORDATORIO, AGENDA, DISPONIBILIDAD, CITA, CONVERSACION_IA, MENSAJE_IA, AUDITORIA.

## 3. Claves primarias y foráneas
- PK: uuid como identificador principal en entidades
- FK: relaciones entre entidades (usuario-rol, mascota-propietario, consulta-mascota/veterinario/sede, cita-disponibilidad/agenda, etc.)

## 4. Relaciones y cardinalidades
- Usuario 1:N UsuarioRol N:1 Rol
- Usuario 1:0..1 especializaciones (Propietario/Veterinario/Personal/Administrador)
- Propietario 1:N Mascota
- Mascota 1:1 HistorialClinico, 1:N Consultas/Vacunas/Desparasitaciones/Recordatorios/Citas
- Veterinario autorizado via PERMISO_HISTORIAL_CLINICO (por mascota)
- Sede 1:N Agenda/Personal/Citas
- Agenda 1:N Disponibilidad
- Disponibilidad 1:1 Cita (evita doble asignación)
- ConversacionIA 1:N MensajeIA, 0..1 -> 1 Cita
- Auditoria N:1 Usuario

## 5. Citas, sedes y disponibilidad
- SEDE representa las dos sedes (flag es_una_de_dos_sedes)
- AGENDA por sede/veterinario/fecha
- DISPONIBILIDAD con hora_inicio/fin, disponible/ocupado
- CITA vincula mascota, propietario, sede, veterinario, agenda, disponibilidad con estado/fechas
- Validación para evitar solapados/duplicados (reglas de negocio)

## 6. Conversaciones con IA
- CONVERSACION_IA asociada a usuario y mascota válida; opcionalmente a CITA
- MENSAJE_IA almacena intercambio
- Campos urgencia_detectada/clasificacion_urgencia/derivacion_requerida
- persistencia_pendiente: política de almacenamiento no definida (no forzar almacenamiento permanente)

## 7. Restricciones de integridad y seguridad
- Permisos por mascota (PERMISO_HISTORIAL_CLINICO) con fecha_autorizacion/revocacion/activo
- Solo veterinarios autorizados acceden a historial
- Auditoría centralizada (AUDITORIA) registra operaciones críticas
- No almacenar diagnósticos definitivos de IA como registros veterinarios
- Datos clínicos protegidos según RNF-01 a RNF-03

## 8. Decisiones pendientes sobre persistencia y tecnología
- Motor BD: no definido (Postgres/MySQL/otro) - representar abstracciones
- Persistencia conversaciones IA: pendiente (sesión vs histórico)
- Origen disponibilidad real: agenda clínica/calendario compartido/centralizado - pendiente
- Aprobación citas desde chat: directa o con aprobación - pendiente
- Integración calendario externo: no documentada - no incluir
- Políticas de datos sensibles para IA: pendiente

## Código Mermaid
```mermaid
erDiagram
    USUARIO { uuid id_usuario PK string nombre string apellido string correo_electronico string telefono date fecha_registro boolean activo }
    ROL { uuid id_rol PK string nombre_rol string descripcion boolean pendiente_definir }
    USUARIO_ROL { uuid id_usuario_rol PK uuid id_usuario FK uuid id_rol FK date fecha_asignacion }
    PROPIETARIO { uuid id_propietario PK uuid id_usuario FK }
    VETERINARIO { uuid id_veterinario PK uuid id_usuario FK string especialidad uuid id_sede_principal FK boolean autorizado }
    PERSONAL_CLINICA { uuid id_personal PK uuid id_usuario FK string cargo uuid id_sede FK }
    ADMINISTRADOR { uuid id_administrador PK uuid id_usuario FK text funciones_pendientes }
    SEDE { uuid id_sede PK string nombre string direccion string telefono boolean activa boolean es_una_de_dos_sedes }
    MASCOTA { uuid id_mascota PK uuid id_propietario FK string nombre string especie string sexo date fecha_nacimiento string datos_identificatorios date fecha_registro }
    PERMISO_HISTORIAL_CLINICO { uuid id_permiso PK uuid id_mascota FK uuid id_veterinario FK uuid id_propietario_autoriza FK date fecha_autorizacion date fecha_revocacion boolean activo text motivo }
    HISTORIAL_CLINICO { uuid id_historial PK uuid id_mascota FK uuid id_propietario FK date fecha_creacion text observaciones_generales }
    CONSULTA_VETERINARIA { uuid id_consulta PK uuid id_historial FK uuid id_mascota FK uuid id_veterinario FK uuid id_sede FK date fecha_consulta time hora_consulta text motivo_consulta text diagnostico_registrado text observaciones uuid id_usuario_registro FK timestamp fecha_registro }
    VACUNA { uuid id_vacuna PK uuid id_mascota FK string nombre_vacuna string fabricante string lote date fecha_aplicacion date fecha_proxima_recomendada uuid id_veterinario_aplico FK uuid id_sede FK }
    DESPARASITACION { uuid id_desparasitacion PK uuid id_mascota FK string tipo_tratamiento string producto date fecha_tratamiento date fecha_proxima_recomendada uuid id_veterinario_aplico FK uuid id_sede FK }
    RECORDATORIO { uuid id_recordatorio PK uuid id_mascota FK string tipo date fecha_objetivo string estado uuid id_usuario_asignado FK timestamp fecha_generacion timestamp fecha_accion text accion_realizada }
    AGENDA { uuid id_agenda PK uuid id_sede FK uuid id_veterinario FK date fecha boolean activa }
    DISPONIBILIDAD { uuid id_disponibilidad PK uuid id_agenda FK date fecha time hora_inicio time hora_fin boolean disponible boolean ocupado }
    CITA { uuid id_cita PK uuid id_mascota FK uuid id_propietario FK uuid id_sede FK uuid id_veterinario FK uuid id_agenda FK uuid id_disponibilidad FK date fecha_cita time hora_cita text motivo_consulta string estado timestamp fecha_solicitud timestamp fecha_confirmacion uuid id_usuario_confirma FK text motivo_cancelacion timestamp fecha_cancelacion }
    CONVERSACION_IA { uuid id_conversacion PK uuid id_usuario FK uuid id_mascota FK uuid id_cita FK timestamp fecha_inicio timestamp fecha_ultima_actividad string estado boolean urgencia_detectada string clasificacion_urgencia boolean derivacion_requerida boolean persistencia_pendiente }
    MENSAJE_IA { uuid id_mensaje PK uuid id_conversacion FK string remitente text contenido timestamp fecha_envio boolean contiene_informacion_clinica boolean es_orientacion_inicial }
    AUDITORIA { uuid id_auditoria PK uuid id_usuario FK string tipo_operacion string entidad_afectada uuid id_registro_afectado timestamp fecha_hora string direccion_ip text detalles text datos_sensibles_filtrados }
    USUARIO ||--o{ USUARIO_ROL : tiene
    ROL ||--o{ USUARIO_ROL : asignado_a
    USUARIO ||--o| PROPIETARIO : es
    USUARIO ||--o| VETERINARIO : es
    USUARIO ||--o| PERSONAL_CLINICA : es
    USUARIO ||--o| ADMINISTRADOR : es
    SEDE ||--o{ VETERINARIO : sede_principal
    SEDE ||--o{ PERSONAL_CLINICA : trabaja_en
    PROPIETARIO ||--o{ MASCOTA : posee
    MASCOTA ||--o| HISTORIAL_CLINICO : tiene
    MASCOTA ||--o{ PERMISO_HISTORIAL_CLINICO : permisos
    VETERINARIO ||--o{ PERMISO_HISTORIAL_CLINICO : autorizado
    HISTORIAL_CLINICO ||--o{ CONSULTA_VETERINARIA : contiene
    MASCOTA ||--o{ CONSULTA_VETERINARIA : registra
    VETERINARIO ||--o{ CONSULTA_VETERINARIA : atiende
    SEDE ||--o{ CONSULTA_VETERINARIA : realizada_en
    MASCOTA ||--o{ VACUNA : tiene
    VETERINARIO ||--o{ VACUNA : aplica
    MASCOTA ||--o{ DESPARASITACION : tiene
    VETERINARIO ||--o{ DESPARASITACION : aplica
    MASCOTA ||--o{ RECORDATORIO : genera
    SEDE ||--o{ AGENDA : tiene
    VETERINARIO ||--o{ AGENDA : atiende
    AGENDA ||--o{ DISPONIBILIDAD : contiene
    MASCOTA ||--o{ CITA : solicitada_para
    PROPIETARIO ||--o{ CITA : solicita
    SEDE ||--o{ CITA : en_sede
    VETERINARIO ||--o{ CITA : asignado
    AGENDA ||--o{ CITA : usa
    DISPONIBILIDAD ||--o{ CITA : reserva_horario
    USUARIO ||--o{ CONVERSACION_IA : inicia
    MASCOTA ||--o{ CONVERSACION_IA : contexto
    CITA ||--o| CONVERSACION_IA : conduce_a
    CONVERSACION_IA ||--o{ MENSAJE_IA : contiene
    USUARIO ||--o{ AUDITORIA : realiza
```

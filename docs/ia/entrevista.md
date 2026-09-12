# Entrevista simulada — Cliente veterinario 

**Rol simulado:** Dr. Andrés Molina, veterinario, dueño de clínica veterinaria con dos sedes.
**Objetivo:** Levantamiento de requisitos para la plataforma híbrida PetCare (app móvil + web).
**Herramienta:** IA (Claude) actuando como cliente, prompt de rol con contexto del negocio (README del proyecto).

## 1. Situación actual — manejo de la información

- Historias clínicas: software de escritorio instalado hace ~6 años.
- Agenda de citas: Google Calendar, gestionada manualmente por la secretaria.
- Recordatorios a propietarios: WhatsApp manual, uno por uno.
- Estos tres sistemas **no están integrados entre sí**.
- Facturación e inventario de medicamentos: funcionan bien con un sistema aparte (**fuera de alcance** del proyecto).
- Problema de sincronización: el historial no se actualiza igual entre las dos sedes.

## 2. Procesos que más generan dificultad

1. **Recordatorios de vacunas/desparasitación** — proceso 100% manual, toma 2-3 horas semanales, se escapan casos.
2. **Confirmación de citas** — no hay confirmación automática, alto índice de inasistencias ("no-shows").
3. **Historial disperso entre sedes** — si el paciente viene de la otra sede, hay que llamar o esperar fotos por WhatsApp.
4. **Registro de la consulta** — el veterinario digita las notas después de atender, entre pacientes, y a veces omite detalles.
5. **Acceso del cliente a su información** — no hay forma de que el propietario vea historial, exámenes o fórmulas organizados.

## 3. Profundización — Recordatorios de vacunas/desparasitación

Flujo deseado por el cliente:

1. El sistema calcula automáticamente la próxima fecha según el **protocolo definido por tipo de producto y especie** (ej. cachorros vs. adultos).
2. La alerta llega **primero al personal de la clínica** (una semana antes) para validar antes de notificar al propietario.
3. El propietario recibe un recordatorio automático (WhatsApp o notificación de app) con opción de **agendar cita directamente**.
4. Si no hay respuesta, el sistema **reenvía un segundo recordatorio**.
5. Se genera un **reporte gerencial**: pendientes, al día, sin atender.

### Datos que se registran al aplicar una vacuna/desparasitación

| Dato | Uso |
|---|---|
| Nombre comercial y tipo de producto | Determina el protocolo de refuerzo |
| Fabricante y número de lote | Trazabilidad / alertas sanitarias |
| Fecha de aplicación | Base del cálculo de la próxima dosis |
| Dosis y vía de aplicación | Registro clínico |
| Peso del paciente | Cálculo de dosis y evolución |
| Edad del paciente | Define el esquema (cachorro vs. adulto) |
| Veterinario que aplicó | Responsabilidad profesional |
| Reacciones/novedades | Alertas para futuras aplicaciones |

Requisito clave del cliente: poder **configurar protocolos por producto y especie** (ej. "vacuna X en perros: refuerzo cada 12 meses; en cachorros <4 meses, cada 21 días").

## 4. Profundización — Citas y no-shows

El cliente no quiere solo un recordatorio informativo, sino un flujo completo:

1. **Confirmación activa** (botón "Sí, voy" / "No puedo asistir"), no solo aviso.
2. **Reprogramación self-service** desde la misma app, mostrando horarios disponibles.
3. **Liberación automática del cupo** si el cliente cancela o no confirma dentro de un plazo (ej. 12 h antes).
4. **Lista de espera**: si un horario está lleno, el cliente se anota y se notifica automáticamente al primero de la lista cuando se libera un cupo.
5. **Tablero administrativo** para que la secretaria vea de un vistazo citas confirmadas/pendientes/canceladas del día.
6. Requisito transversal: la experiencia debe ser **muy simple**, porque muchos propietarios tienen poca habilidad tecnológica.

Nota: la entrevista continúa cubriendo registro de consultas y acceso del propietario a la información; los puntos 1 y 2 fueron los priorizados por el cliente para esta primera iteración del levantamiento.

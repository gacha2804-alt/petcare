-- =============================================================================
-- PetCare Database Schema (DDL)
-- Plataforma Híbrida de Cuidado Preventivo de Mascotas con IA
-- Compatible con PostgreSQL y SQLite
-- =============================================================================

-- 1. Roles del Sistema
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rol_id INT NOT NULL,
    nombre_completo VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    telefono VARCHAR(30),
    activo BOOLEAN DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuario_rol FOREIGN KEY (rol_id) REFERENCES roles(id) ON DELETE RESTRICT
);

-- 3. Clínicas Veterinarias
CREATE TABLE IF NOT EXISTS clinicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    email VARCHAR(150),
    latitud DECIMAL(10, 8) NOT NULL,
    longitud DECIMAL(11, 8) NOT NULL,
    horario_atencion VARCHAR(100),
    tiene_urgencias_24h BOOLEAN DEFAULT 0,
    activa BOOLEAN DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Asignación de Personal a Clínicas (Veterinarios y Recepción)
CREATE TABLE IF NOT EXISTS personal_clinica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INT UNIQUE NOT NULL,
    clinica_id INT NOT NULL,
    tarjeta_profesional VARCHAR(100),
    especialidad VARCHAR(100),
    CONSTRAINT fk_personal_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_personal_clinica FOREIGN KEY (clinica_id) REFERENCES clinicas(id) ON DELETE CASCADE
);

-- 5. Mascotas
CREATE TABLE IF NOT EXISTS mascotas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    propietario_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100),
    sexo VARCHAR(10) NOT NULL,
    fecha_nacimiento DATE,
    esterilizado BOOLEAN DEFAULT 0,
    peso_actual DECIMAL(5, 2),
    foto_url TEXT,
    codigo_qr_token VARCHAR(100) UNIQUE NOT NULL,
    contacto_emergencia_tel VARCHAR(30),
    condiciones_criticas TEXT,
    activa BOOLEAN DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mascota_propietario FOREIGN KEY (propietario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 6. Esquema de Vacunación / Desparasitación (RF-01)
CREATE TABLE IF NOT EXISTS vacunas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    veterinario_id INT,
    nombre_vacuna VARCHAR(100) NOT NULL,          -- producto
    tipo_aplicacion VARCHAR(30) DEFAULT 'vacuna', -- vacuna | desparasitacion
    fabricante VARCHAR(150),
    lote VARCHAR(50),
    dosis VARCHAR(100),
    via_aplicacion VARCHAR(50),                   -- SC, IM, IV, oral...
    peso_kg DECIMAL(5, 2),
    edad_aplicacion VARCHAR(30),                  -- meses o categoría (cachorro/adulto/senior)
    protocolo_id INT,
    fecha_aplicacion DATE NOT NULL,
    fecha_proxima_dosis DATE,                     -- calculada por el protocolo (RF-03)
    novedades TEXT,
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_vacuna_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    CONSTRAINT fk_vacuna_veterinario FOREIGN KEY (veterinario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    CONSTRAINT fk_vacuna_protocolo FOREIGN KEY (protocolo_id) REFERENCES protocolos_refuerzo(id) ON DELETE SET NULL
);

-- 7. Medicamentos y Prescripciones
CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    veterinario_id INT,
    nombre VARCHAR(150) NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    frecuencia_horas INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    indicaciones TEXT,
    activo BOOLEAN DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_medicamento_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    CONSTRAINT fk_medicamento_veterinario FOREIGN KEY (veterinario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- 8. Registro y Seguimiento de Peso
CREATE TABLE IF NOT EXISTS registros_peso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    peso_kg DECIMAL(5, 2) NOT NULL,
    fecha_registro DATE NOT NULL,
    notas VARCHAR(255),
    CONSTRAINT fk_peso_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- 9. Alimentación y Nutrición
CREATE TABLE IF NOT EXISTS registros_alimentacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    tipo_alimento VARCHAR(100) NOT NULL,
    marca VARCHAR(100),
    cantidad_gramos_dia INT,
    frecuencia_veces_dia INT,
    observaciones TEXT,
    fecha_registro DATE NOT NULL,
    CONSTRAINT fk_alimentacion_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- 10. Síntomas y Observaciones de Evolución
CREATE TABLE IF NOT EXISTS sintomas_observaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    usuario_id INT NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    descripcion TEXT NOT NULL,
    severidad VARCHAR(20) DEFAULT 'leve',
    fecha_inicio TIMESTAMP NOT NULL,
    resuelto BOOLEAN DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sintoma_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    CONSTRAINT fk_sintoma_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 11. Consultas Médicas y Diagnósticos Profesionales (Exclusivo Veterinario)
CREATE TABLE IF NOT EXISTS consultas_medicas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    veterinario_id INT NOT NULL,
    fecha_consulta TIMESTAMP NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    anamnesis TEXT,
    constantes_vitales TEXT, -- JSON o texto: temperatura, frec. cardíaca, etc.
    diagnostico_profesional TEXT NOT NULL,
    plan_tratamiento TEXT NOT NULL,
    notas_adicionales TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_consulta_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    CONSTRAINT fk_consulta_veterinario FOREIGN KEY (veterinario_id) REFERENCES usuarios(id) ON DELETE RESTRICT
);

-- 12. Documentos Médicos (exámenes, radiografías)
CREATE TABLE IF NOT EXISTS documentos_salud (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    tipo_documento VARCHAR(50),
    archivo_url TEXT NOT NULL,
    fecha_documento DATE NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_documento_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- 12. Citas Médicas
CREATE TABLE IF NOT EXISTS citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    propietario_id INT NOT NULL,
    veterinario_id INT,
    clinica_id INT NOT NULL,
    fecha_hora TIMESTAMP NOT NULL,
    motivo TEXT NOT NULL,
    estado VARCHAR(30) DEFAULT 'pendiente',
    diagnostico_consulta TEXT,
    indicaciones_consulta TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cita_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    CONSTRAINT fk_cita_propietario FOREIGN KEY (propietario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_cita_veterinario FOREIGN KEY (veterinario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    CONSTRAINT fk_cita_clinica FOREIGN KEY (clinica_id) REFERENCES clinicas(id) ON DELETE CASCADE
);

-- 13. Evaluaciones y Consultas de IA
CREATE TABLE IF NOT EXISTS consultas_ia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    usuario_id INT NOT NULL,
    prompt_usuario TEXT NOT NULL,
    contexto_clinico_snapshot TEXT,
    respuesta_ia TEXT NOT NULL,
    nivel_urgencia_sugerido VARCHAR(20),
    recomendaciones TEXT,
    disclaimer_aceptado BOOLEAN DEFAULT 1,
    fecha_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ia_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE,
    CONSTRAINT fk_ia_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 14. Alertas de Evolución Detectadas por IA
CREATE TABLE IF NOT EXISTS alertas_evolucion_ia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mascota_id INT NOT NULL,
    tipo_alerta VARCHAR(50) NOT NULL,
    mensaje TEXT NOT NULL,
    nivel_riesgo VARCHAR(20) NOT NULL,
    revisada BOOLEAN DEFAULT 0,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_alerta_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- 15. Notificaciones del Sistema
CREATE TABLE IF NOT EXISTS notificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    mensaje TEXT NOT NULL,
    leida BOOLEAN DEFAULT 0,
    referencia_id INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notificacion_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 16. Protocolos de Refuerzo (RF-02 / RF-03)
CREATE TABLE IF NOT EXISTS protocolos_refuerzo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_producto VARCHAR(150) NOT NULL,
    fabricante VARCHAR(150),
    tipo_aplicacion VARCHAR(30) NOT NULL DEFAULT 'vacuna', -- vacuna | desparasitacion
    especie VARCHAR(50) NOT NULL,                          -- perro, gato...
    categoria_edad VARCHAR(30) NOT NULL,                   -- cachorro | adulto | senior
    edad_min_meses INTEGER,                                -- rango de aplicación opcional
    edad_max_meses INTEGER,
    intervalo_refuerzo_dias INTEGER NOT NULL,              -- días hasta la próxima dosis (RF-03)
    esquema_refuerzos TEXT,                                -- JSON: dosis iniciales y refuerzos adicionales en días
    requiere_alerta_previa_dias INTEGER DEFAULT 7,         -- ventana de alerta semanal (RF-04, HU-01)
    descripcion TEXT,
    activo BOOLEAN DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_protocolo UNIQUE (tipo_aplicacion, nombre_producto, especie, categoria_edad)
);

-- 17. Agenda / Slots de Atención Disponibles (RF-08, RF-09)
CREATE TABLE IF NOT EXISTS horarios_atencion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinica_id INT NOT NULL,
    veterinario_id INT,                          -- NULL = recepción / sin profesional asignado
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    tipo_atencion VARCHAR(30) DEFAULT 'consulta', -- consulta | vacunacion | urgencia
    estado VARCHAR(20) DEFAULT 'disponible',     -- disponible | reservado | bloqueado | liberado
    cita_id INT,                                 -- reserva vinculada al slot
    notas TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_slot_clinica FOREIGN KEY (clinica_id) REFERENCES clinicas(id) ON DELETE CASCADE,
    CONSTRAINT fk_slot_veterinario FOREIGN KEY (veterinario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    CONSTRAINT fk_slot_cita FOREIGN KEY (cita_id) REFERENCES citas(id) ON DELETE SET NULL
);

-- 18. Lista de Espera (RF-10 / HU-07)
CREATE TABLE IF NOT EXISTS lista_espera (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clinica_id INT NOT NULL,
    slot_id INT,                                 -- horario al que se aspira (NULL = lista general de la clínica)
    usuario_id INT NOT NULL,
    mascota_id INT,
    motivo VARCHAR(255),
    estado VARCHAR(20) DEFAULT 'en_espera',      -- en_espera | notificado | tomado | expirado | cancelado
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_notificacion TIMESTAMP,                -- inicio de la ventana de 15 min para aceptar (HU-07)
    fecha_expiracion TIMESTAMP,                  -- fecha_notificacion + 15 min
    CONSTRAINT fk_espera_clinica FOREIGN KEY (clinica_id) REFERENCES clinicas(id) ON DELETE CASCADE,
    CONSTRAINT fk_espera_slot FOREIGN KEY (slot_id) REFERENCES horarios_atencion(id) ON DELETE SET NULL,
    CONSTRAINT fk_espera_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_espera_mascota FOREIGN KEY (mascota_id) REFERENCES mascotas(id) ON DELETE CASCADE
);

-- Índices para Optimización de Consultas
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_mascotas_propietario ON mascotas(propietario_id);
CREATE INDEX IF NOT EXISTS idx_mascotas_qr_token ON mascotas(codigo_qr_token);
CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_citas_veterinario ON citas(veterinario_id);
CREATE INDEX IF NOT EXISTS idx_vacunas_mascota ON vacunas(mascota_id);
CREATE INDEX IF NOT EXISTS idx_sintomas_mascota ON sintomas_observaciones(mascota_id);
CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario ON notificaciones(usuario_id, leida);

-- Índices para vencimientos, agenda y lista de espera (RNF-07, RF-08, RF-10)
CREATE INDEX IF NOT EXISTS idx_vacunas_proxima_dosis ON vacunas(fecha_proxima_dosis);
CREATE INDEX IF NOT EXISTS idx_vacunas_protocolo ON vacunas(protocolo_id);
CREATE INDEX IF NOT EXISTS idx_protocolos_tipo_especie ON protocolos_refuerzo(tipo_aplicacion, especie, categoria_edad);
CREATE INDEX IF NOT EXISTS idx_slots_fecha_estado ON horarios_atencion(fecha, clinica_id, estado);
CREATE INDEX IF NOT EXISTS idx_espera_estado ON lista_espera(slot_id, estado);
